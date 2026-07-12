# Reproducibility Check

**Performed:** 2026-07-03
**Method:** Fresh `git clone` of both repositories into a clean directory, a new
Python virtual environment (no packages pre-installed), and `pip install -r
scripts/requirements.txt` (private repo: `portable_scripts/requirements.txt`)
before running anything. No files were copied in from an existing working
directory.

## Environment

- Python 3.9.6 (also expected to work on any Python ≥3.9)
- Dependencies installed from `requirements.txt` with no version conflicts:
  `pandas==2.3.3`, `numpy==2.0.2`, `matplotlib==3.9.4`, `requests==2.32.5`,
  `openpyxl==3.1.5`

## What was tested

### Private repository (`public-data-review-priority-afh`)

Scripts were run in the documented order (`README_SCRIPTS.md`, steps 4–10)
against the intermediate CSVs already checked into
`data_package_with_everything/wa_data/`, using
`AFH_DATA_DIR` / `AFH_OUT_DIR` environment variables to point at a clean
output folder outside the clone.

| Script | Result |
|---|---|
| `build_charts.py` | Ran to completion; regenerated the spending and county charts |
| `build_clusters.py` | Ran to completion; regenerated the 72-cluster operator table |
| `build_normalized.py` | Ran to completion; regenerated the Census-normalized density table |
| `make_figures.py` | Ran to completion; regenerated Figures 4 and 5 |
| `build_growth.py` | Ran to completion; regenerated the 14-row growth series |
| `build_growth_chart.py` | Ran to completion; regenerated the growth chart |
| `build_rf_coding.py` | Ran to completion; regenerated the review-priority indicator coding and testability matrix |
| `build_anonymized.py` | Ran to completion; regenerated the anonymized package with a built-in self-check |

`build_anonymized.py`'s own self-check output on this clean run:

```
=== ANONYMIZED PACKAGE BUILT ===
  Facilities: 3457 (expect 3457)
  Beds: 20157 (expect 20157)
  In clusters: 164 (expect 164)
  >=1 enforcement: 165 (expect 165)
  Clusters: 72 (expect 72)
  County split: {'King': 1795, 'Pierce': 1052, 'Spokane': 610}
  'City' column present: False (expect False)
```

Every headline number reported in the manuscript reproduced exactly from a
clean clone with no manual intervention.

### Steps not re-executed: `build_afh_master.py`, `build_3county.py`, `scrape_reports.py`

These three scripts pull live data directly from DSHS's public ArcGIS feature
service and the DSHS RCS document portal (one HTTP request per facility,
rate-limited). They were **not** re-run for this check, for two reasons:

1. Re-running them would not reproduce the original snapshot — DSHS's public
   roster changes continuously, so a fresh pull today returns today's data,
   not the 2026-06-26 snapshot the manuscript analyzes.
2. `scrape_reports.py` makes on the order of 3,457 individual requests to a
   state government server. Re-running it purely to test reproducibility
   would place unnecessary load on public infrastructure with no benefit,
   since it cannot reproduce the original historical snapshot anyway.

These scripts were exercised during the original data-collection process (the
resulting intermediate CSVs are the ones checked into `wa_data/` and used
above); this check does not re-verify that step, only that everything
downstream of it is genuinely reproducible.

### Public repository (`public-data-review-priority-afh-public`)

The public package ships the **final, anonymized** output of the pipeline
(`anonymized_data/*.csv`), not the intermediate, pre-anonymization files the
scripts expect as input. Running the scripts directly against
`anonymized_data/` fails — for example, `build_charts.py` expects
`WA_Operator_PhoneClusters.csv` (the private-repo intermediate filename), and
the public package correctly does not include that file under that name.

**What is genuinely verifiable from the public repo alone:** that the
provided anonymized CSVs support every number reported in the manuscript, and
that the analysis code is available for inspection. Full pipeline
re-execution (steps 1–10 in order, from raw roster to anonymized package) is
only possible with the private repository's intermediate files, which is the
intended design — the public repo is the transparent, de-identified
evidence layer, not a re-runnable copy of the raw pipeline.

## Bottom line

- **Fully reproducible, verified by clean-room execution:** the entire
  analysis pipeline from intermediate roster/enforcement data through the
  final anonymized package and all figures (private repo).
- **Not reproducible from the public repo alone by design:** the raw-data
  acquisition steps, because the public package intentionally ships only
  de-identified final outputs.
- **Not re-testable to identical results:** the initial live-data pull,
  because DSHS's public data changes over time; the manuscript documents
  this as a limitation (Section 9) already.
