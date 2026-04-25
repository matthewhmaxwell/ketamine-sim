# Ketamine Trip Simulator

Research prototype: a probabilistic simulator of ketamine subjective-experience trajectories for clinical education, patient preparation, and research modeling.

> ## ⚠ Scope and intent
> **This is not a dosing guide. Not medical advice. Not a use guide.**
> The schema deliberately uses qualitative dose tiers (`subperceptual / low / moderate / high / dissociative`) instead of mg/kg values, to discourage repurposing as a dosing reference. Outputs are population-level plausible trajectories, not predictions for any individual. The simulator must not be used with patients without a clinician in the loop, regardless of any internal evaluation score.

## Status

| Phase | State |
|---|---|
| 1 — Scaffolding | done |
| 2 — Source survey | done; corpus of 8 `permitted` + 1 `paraphrase_only`, no Erowid |
| 3 — Extraction | 57 verified-verbatim records (Mollaahmetoglu 2021: 30; Kheirkhah 2025: 27) |
| 4 — Simulator | not started |
| 5 — Evaluation | not started |

Phase N+1 does not start until phase N has been reviewed.

## Layout

| File | Purpose |
|---|---|
| `trip_state_schema.json` | JSON Schema for a simulated trajectory (inputs → phase-bound state vectors → derived summaries). |
| `field_dictionary.md` | Definitions, scales, and annotation rubric for every field. |
| `source_vetting_checklist.md` | Per-source legal/ethics gate that runs before any extraction. |
| `evaluation_plan.md` | Four-pillar eval framework: distributional, human rater, psychometric, safety. |
| `bibliography.csv` | Vetted source list with license + `reuse_status` per source. |
| `source_survey_notes.md` | Phase 2 readout — headline findings, decisions, coverage gaps. |
| `extractions/EXTRACTION_TEMPLATE.md` | JSONL record schema and annotation rules. |
| `extractions/<source_id>.jsonl` | Per-source extraction output. |
| `extractions/PILOT_NOTES.md` | Phase 3 readout — annotation decisions, gaps, archetypes. |
| `extractions/verify_quotes.py` | Audit script: every `raw_excerpt` must appear verbatim in source HTML. |

## Reproducing the dataset

```bash
# Cache source HTML (required by verify_quotes.py)
curl -sL https://pmc.ncbi.nlm.nih.gov/articles/PMC8415567/  -o /tmp/mollaahmetoglu-2021.html
curl -sL https://pmc.ncbi.nlm.nih.gov/articles/PMC12439531/ -o /tmp/kheirkhah-2025.html

# Verify every JSONL excerpt against its source
python3 extractions/verify_quotes.py
```
The audit exits non-zero on any mismatch — wire it into a pre-commit or CI check before adding new records.

## Source rules (enforced in `source_vetting_checklist.md`)

- **Erowid:** **excluded by default.** Erowid Center's TOS explicitly forbids feeding report data into AI systems without prior written permission (`copyrights@erowid.org`).
- **Reddit / forum posts:** excluded for verbatim use.
- **Verbatim text** is only stored when `reuse_status == "permitted"` (CC-BY family). Restrictive licenses get `paraphrase_only` or `cite_only`, with the `raw_excerpt` field left empty.
- **Web extraction:** never trust an LLM summarizer for verbatim text. Use raw HTML (curl + grep + read), then run `verify_quotes.py`.

## Licensing

| Layer | License |
|---|---|
| Code & schemas in this repo | MIT (see `LICENSE`) |
| Verbatim excerpts inside JSONL files | inherited from source — almost all CC-BY-4.0; per-record attribution lives in the corresponding bibliography row via `source_id` |
| Annotation labels and rubric | MIT |

When using this dataset, attribute each excerpt to its original publication (the `source_id` field links to `bibliography.csv`).

## What this project is *not*

- Not a "trip generator." The architecture deliberately separates the state simulator from the narrative renderer so the same trajectory can produce structured, narrative, clinician-facing, or synthetic-patient outputs.
- Not validated for clinical use. The four-pillar evaluation in `evaluation_plan.md` defines what would have to pass before any external-facing product is built. None of those have been run yet.
- Not affiliated with Anthropic, any clinical institution, or any pharmaceutical company.
