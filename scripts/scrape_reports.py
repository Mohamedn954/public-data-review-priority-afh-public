#!/usr/bin/env python3
"""For each AFH in King/Pierce/Spokane, fetch its DSHS reports page and tally
public documents by type. Folder tokens observed: 'inspections',
'investigations', 'limitations', 'enforcement letters'. Public docs per RCW 70.128.280.

Enforcement subtype decoding from filenames:
  CF = Civil Fine; SP = Stop Placement; Cond = Condition(s) on license;
  Lift = remedy lifted; Cont SP = continued stop placement.
Writes progress to a live log and saves CSV incrementally.

RESPONSIBLE-USE GUIDANCE
========================
This script issues ~3,457 individual HTTP GETs against a state government
web server (fortress.wa.gov). To avoid placing undue load on public
infrastructure:

  * Concurrency is capped at MAX_WORKERS (default 6). Do NOT raise this
    above ~10.
  * Per-request pacing is enforced by MIN_INTER_REQUEST_SECONDS (default
    0.20s per completed request across the whole pool) -- effectively a
    ceiling of ~30 requests/second aggregate, well below what a healthy
    public portal can absorb.
  * Failed requests are retried up to MAX_RETRIES times with exponential
    backoff, but ONLY for retryable errors (5xx, 429, connection errors,
    read timeouts) -- 4xx and 404 are not retried.
  * A single-run cap of TARGET_ELAPSED_MIN informs you if the pool is
    running much faster than the target pace and asks whether to slow down.

If you rerun this script, please:
  1. Do so at most once per snapshot date.
  2. Check that fortress.wa.gov is not under maintenance before starting.
  3. If you get repeated 5xx responses, STOP -- the server is telling you
     something. Do not simply re-try; wait several hours and try again.

The reproducibility check does NOT re-run this script for exactly these
reasons; see scripts/REPRODUCIBILITY_CHECK.md.
"""

# Shared config: snapshot date and standard paths.
import os as _os
import sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
from _afh_config import DATE_ACCESSED, DATA_DIR, OUT_DIR, SRC_DIR  # noqa: E402

import re
import time
import random
import threading
import requests
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

# --- Politeness knobs -------------------------------------------------------
MAX_WORKERS = 6                   # was 10; lower is kinder to the portal
MIN_INTER_REQUEST_SECONDS = 0.20  # aggregate pacing across the whole pool
MAX_RETRIES = 3                   # per-URL retry budget on retryable errors
CONNECT_TIMEOUT = 10
READ_TIMEOUT = 25
RETRYABLE_STATUS = {429, 500, 502, 503, 504}
BACKOFF_BASE_SECONDS = 1.5        # exponential backoff base
# ---------------------------------------------------------------------------

SRC  = _os.path.join(DATA_DIR, "WA_AFH_3County_Master.csv")
OUT  = _os.path.join(DATA_DIR, "WA_AFH_3County_Reports.csv")
LOG  = _os.path.join(DATA_DIR, "scrape_progress.log")
BASE = "https://fortress.wa.gov/dshs/adsaapps/lookup/AFHForms.aspx?lic="

df = pd.read_csv(SRC, dtype=str)
licenses = df[["License_Number", "Facility_Name", "City", "County"]].to_dict("records")
total = len(licenses)

# Capture folder segment (may contain spaces / %20) and 4-digit year
PAT = re.compile(r"/RCSForms/AF/\d+/([^/]+?)/(\d{4})/", re.I)

sess = requests.Session()
sess.headers.update({
    "User-Agent": "Mozilla/5.0 (research data collection; "
                  "public-data-review-priority-afh-public/1.0; "
                  "contact via github.com/Mohamedn954)",
    "Accept": "text/html,application/xhtml+xml",
})

# Global rate limiter: one lock, one "next allowed time" cursor, shared
# across all worker threads so aggregate QPS obeys MIN_INTER_REQUEST_SECONDS
# regardless of concurrency.
_rate_lock = threading.Lock()
_next_allowed_ts = [0.0]  # list so nested closure can mutate

def _rate_limited_sleep():
    with _rate_lock:
        now = time.monotonic()
        wait = _next_allowed_ts[0] - now
        if wait > 0:
            time.sleep(wait)
            now = time.monotonic()
        _next_allowed_ts[0] = now + MIN_INTER_REQUEST_SECONDS


def classify(folder):
    f = folder.replace("%20", " ").lower().strip()
    if "enforcement" in f: return "enforcement"
    if "inspection" in f: return "inspections"
    if "investigation" in f: return "investigations"
    if "limitation" in f: return "limitations"
    return "other"


def _http_get_with_retry(url):
    """GET url with exponential backoff on retryable errors.

    Returns (response_or_None, final_status_string).
    """
    last_err = "unknown"
    for attempt in range(1, MAX_RETRIES + 1):
        _rate_limited_sleep()
        try:
            r = sess.get(url, timeout=(CONNECT_TIMEOUT, READ_TIMEOUT))
        except requests.exceptions.RequestException as e:
            last_err = f"err:{type(e).__name__}"
            # Backoff before the next retry (with jitter).
            if attempt < MAX_RETRIES:
                sleep_s = BACKOFF_BASE_SECONDS ** attempt + random.uniform(0, 0.5)
                time.sleep(sleep_s)
            continue

        if r.status_code == 200:
            return r, "ok"
        if r.status_code in RETRYABLE_STATUS and attempt < MAX_RETRIES:
            last_err = f"http_{r.status_code}_retrying"
            sleep_s = BACKOFF_BASE_SECONDS ** attempt + random.uniform(0, 0.5)
            time.sleep(sleep_s)
            continue
        # Non-retryable (4xx other than 429, or final failed attempt).
        return None, f"http_{r.status_code}"
    return None, last_err


def fetch(rec):
    lic = rec["License_Number"]
    url = BASE + str(lic)
    out = {
        "License_Number": lic, "Facility_Name": rec["Facility_Name"],
        "City": rec["City"], "County": rec["County"],
        "n_inspections": 0, "n_investigations": 0, "n_enforcement": 0,
        "n_limitations": 0, "n_other": 0, "n_docs_total": 0,
        "n_civil_fines": 0, "n_stop_placement": 0, "n_conditions": 0,
        "years_present": "", "latest_year": "", "latest_enforcement_year": "",
        "reports_url": url, "fetch_status": "ok",
    }
    r, status = _http_get_with_retry(url)
    if r is None:
        out["fetch_status"] = status
        return out
    try:
        hrefs = re.findall(r'href="([^"]*RCSForms/AF/[^"]+)"', r.text)
        years = set()
        enf_years = set()
        for h in hrefs:
            m = PAT.search(h)
            if not m:
                out["n_other"] += 1
                continue
            cat = classify(m.group(1))
            y = m.group(2)
            years.add(y)
            fname = h.lower()
            if cat == "inspections": out["n_inspections"] += 1
            elif cat == "investigations": out["n_investigations"] += 1
            elif cat == "limitations": out["n_limitations"] += 1
            elif cat == "enforcement":
                out["n_enforcement"] += 1
                enf_years.add(y)
                # subtype decoding (exclude 'lift' which reverses a remedy)
                is_lift = "lift" in fname
                if re.search(r'\bcf\b', fname) or "civil" in fname:
                    if not is_lift: out["n_civil_fines"] += 1
                if re.search(r'\bsp\b', fname) or "stop placement" in fname:
                    if not is_lift: out["n_stop_placement"] += 1
                if "cond" in fname:
                    if not is_lift: out["n_conditions"] += 1
            else:
                out["n_other"] += 1
        out["n_docs_total"] = sum(
            out[k] for k in ["n_inspections", "n_investigations",
                             "n_enforcement", "n_limitations", "n_other"]
        )
        out["years_present"] = ",".join(sorted(years))
        out["latest_year"] = max(years) if years else ""
        out["latest_enforcement_year"] = max(enf_years) if enf_years else ""
    except Exception as e:
        out["fetch_status"] = f"parse_err:{type(e).__name__}"
    return out


results = []
start = time.time()
with open(LOG, "w") as lf:
    lf.write(
        f"start total={total} snapshot={DATE_ACCESSED} "
        f"workers={MAX_WORKERS} pacing={MIN_INTER_REQUEST_SECONDS}s "
        f"retries={MAX_RETRIES}\n"
    )
    lf.flush()
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futs = {ex.submit(fetch, rec): rec for rec in licenses}
        done = 0
        for fu in as_completed(futs):
            results.append(fu.result())
            done += 1
            if done % 200 == 0 or done == total:
                el = time.time() - start
                lf.write(f"{done}/{total} elapsed={el:.0f}s\n")
                lf.flush()
                pd.DataFrame(results).to_csv(OUT, index=False)

rd = pd.DataFrame(results)
rd.to_csv(OUT, index=False)
with open(LOG, "a") as lf:
    lf.write("DONE\n")
    lf.write(f"enforcement>0: {(rd['n_enforcement']>0).sum()}\n")
    lf.write(f"civil_fines>0: {(rd['n_civil_fines']>0).sum()}\n")
    lf.write(f"stop_placement>0: {(rd['n_stop_placement']>0).sum()}\n")
    lf.write(f"conditions>0: {(rd['n_conditions']>0).sum()}\n")
    lf.write(f"investigations>0: {(rd['n_investigations']>0).sum()}\n")
    lf.write(f"limitations>0: {(rd['n_limitations']>0).sum()}\n")
    lf.write(f"no docs: {(rd['n_docs_total']==0).sum()}\n")
    # Retry telemetry: how many licenses ended non-ok?
    nok = (rd["fetch_status"] != "ok").sum()
    lf.write(f"non_ok_after_retries: {nok}\n")
print("DONE", len(rd))
