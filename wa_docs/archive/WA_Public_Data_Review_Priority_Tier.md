# [ARCHIVED — NOT FOR OPERATIONAL USE] Proposed Public-Data Review-Priority Tier Framework

*Evidence Base Extraction: Section H*

---

**ARCHIVED DOCUMENT. DO NOT USE THIS RUBRIC TO SCORE, RANK, OR FLAG ANY REAL FACILITY OR OPERATOR.**

This memo is retained only for provenance, to document an early, exploratory idea from the project's evidence-base phase. It has been superseded and is not part of the project's canonical framing.

- **It is not a validated instrument.** The point weights below (20, 10, etc.) were never statistically calibrated, tested for false-positive rates, or reviewed against ground truth. They are illustrative placeholders, not measured coefficients.
- **It is not a fraud score.** No numeric total produced by this rubric indicates that fraud, abuse, or any wrongdoing has occurred or is likely.
- **It is not used anywhere in the manuscript, the anonymized dataset, or the pipeline scripts.** The publication-facing version of this idea is the qualitative PDRT description in the manuscript's Appendix B, which deliberately avoids assigning a single composite numeric score to any facility, precisely because a single number invites exactly the misreading this archived draft risked.
- **Do not extract, screenshot, or cite the scoring table below out of this context.** Out of context, a "60-point" or "30-point" example below could be misread as an actual risk score assigned to a real facility. It is not; the examples are hypothetical illustrations of how the point categories would combine, not a real facility's computed score.

If you are looking for the current, canonical framing of review-priority indicators, see:
- The manuscript's Appendix B (qualitative PDRT framing), posted on [SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7070198)
- `GUARDRAILS.md` (repository root)
- `wa_docs/README.md` (this folder's canonical-vs-superseded index)

---

## Original memo (superseded, preserved for provenance only)

Because billing data (claims) is not public, a public-data review-priority approach must rely on licensing, concentration, and complaint signals rather than claims analytics. Based on the Minnesota review-priority indicators (RF-01 to RF-20), an early draft of this project proposed a **Public-Data Review-Priority Tier system, derived from a 0-100 point rubric,** for WA AFHs, computable entirely from the datasets generated in this pilot. This rubric was never adopted; it is shown below only to document how the idea was originally framed before being replaced with the qualitative approach in the manuscript's Appendix B.

### Scoring Components (100 Points Total) — illustrative only, never adopted

**1. Network & Concentration Signal (40 Points)**
*Proxy for RF-08 (Related-Party Networks) and RF-03 (Concentration)*
- **Shared Phone Cluster (20 pts):** Facility shares a public phone number with ≥2 other licenses.
- **Rapid Network Expansion (20 pts):** Operator cluster added ≥2 new licenses within a 12-month period.

**2. Enforcement & Complaint History (40 Points)**
*Proxy for RF-14 (Documentation) and RF-18 (Oversight Signals)*
- **Stop-Placement Order (20 pts):** Active or recent DSHS stop-placement (severe life/safety or compliance failure).
- **Repeat Enforcement (10 pts):** ≥2 enforcement letters in the 2023-2026 window.
- **High Complaint Load (10 pts):** ≥3 complaint investigations in the 2023-2026 window.

**3. Geographic Density Signal (20 Points)**
*Proxy for RF-01 (Rapid Growth)*
- **High-Density County (10 pts):** Facility located in a county exceeding 7.0 AFHs per 1,000 seniors (e.g., Snohomish, Pierce).
- **Out-of-State Operator (10 pts):** Licensee mailing address or SOS CCFS governor address is outside Washington (requires CCFS sampling).

### Hypothetical illustration only — no real facility was scored

- **Hypothetical "high review priority" combination (60+ pts):** a facility in a 4-home phone cluster (20) in a high-density county (10), with a stop-placement (20) and high complaints (10), would sum to 60 points under this never-adopted rubric.
- **Hypothetical "moderate review priority" combination (30-50 pts):** a facility in a 2-home cluster (20) with repeat enforcement (10) would sum to 30 points.
- **Hypothetical "baseline" combination (0-20 pts):** a single-home operator with a clean inspection record would sum to 0 points.

*This point rubric was never applied to any real facility in the pilot dataset. It does not allege fraud, and it is not recommended for operational use under any circumstances without claims-data validation, statistical calibration, human review, and due-process protections that were never built for it.*
