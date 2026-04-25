# Phase 3 Extraction Notes

Date: 2026-04-24
Annotator: Claude (claude-opus-4-7-2026-04-24)

## Files

| File | Records | Source license |
|---|---|---|
| `mollaahmetoglu-2021.jsonl` | 30 | CC-BY |
| `kheirkhah-2025.jsonl` | 27 | CC-BY |

All 57 records have been **audited via `verify_quotes.py`** (substring match against the raw PMC HTML with tags stripped and unicode normalized). Every `raw_excerpt` is present verbatim in the source. All records use `raw_excerpt_completeness: "full"`.

To re-run the audit:
```
curl -sL https://pmc.ncbi.nlm.nih.gov/articles/PMC8415567/  -o /tmp/mollaahmetoglu-2021.html
curl -sL https://pmc.ncbi.nlm.nih.gov/articles/PMC12439531/ -o /tmp/kheirkhah-2025.html
python3 extractions/verify_quotes.py
```
Exit code is non-zero on any mismatch — safe to wire as a pre-commit / CI check.

---

## Methodology note: WebFetch is not safe for verbatim extraction

**Critical finding from this phase.**

WebFetch's downstream summarizer model has a hidden ~125-char-per-quote limit and silently paraphrases, abbreviates with ellipses, and misattributes when the source contains anything longer. The pilot v1 extraction (now overwritten) contained these errors:

1. **Silent paraphrase.** WebFetch returned `"I left every session feeling happy...feeling lighter...clearer thoughts"` attributed to P10. The actual paper text is `"I just found I left every session, kind of, you know, feeling happy. Feeling, you know… feeling lighter… Feeling like clearer thoughts"`. WebFetch had stripped the connective tissue and replaced with ellipses without flagging.
2. **Misattribution.** `"one of the best experiences of my life"` was attributed to P09; the paper actually attributes it to P04 (and as a paraphrased aggregate, not a direct quote).
3. **Title-as-quote.** `"This is something that changed my life"` (the paper's title) was returned as a P12 verbatim quote; P12's actual quote is `"In a non-cheesy way, it actually probably changed my life around and kept me alive."`

**Workflow established for all subsequent extractions:**

1. `curl -sL <PMC URL> -o /tmp/<source_id>.html` to get the raw page.
2. `Grep` for distinctive phrases inside the HTML to locate quote blocks.
3. `Read` the surrounding lines to capture the full verbatim quote with its participant attribution.
4. Cross-check participant codes against the paper's text — same code (e.g., "P05") must consistently refer to the same person.
5. Only then build the JSONL record with `raw_excerpt_completeness: "full"`.

WebFetch remains acceptable for **license verification** and **structural overview** (themes, sample sizes, study design) — but not for verbatim text.

---

## Source-level findings

### Kheirkhah 2025 does NOT use 11D-ASC

Earlier verification said it "uses 11D-ASC." On full reading, it only **references** Farnes et al. who used 11D-ASC in a different study. Kheirkhah uses qualitative coding + standard depression scales (MADRS, HAM-D, QIDS, MAAS, DSES, PTQ). This means:

- Studerus 2010 remains the only psychometric anchor.
- The intended Kheirkhah-vs-rubric calibration check from the source-survey notes is not possible.
- Kheirkhah is still load-bearing as **the only RCT testing setting effects** (intervention vs control), so the records carry an explicit `setting.music` and `setting.eye_mask` value, which is rare across the corpus.

`bibliography.csv` should be updated to remove the "uses 11D-ASC" claim. Will do that as a follow-up.

### Mollaahmetoglu setting

The paper describes "soothing music" and dim lighting in the setup, with a therapist present. All records carry `music: true`, `eye_mask: null` (not described), `therapist_present: true`, `alone: false`. This may slightly under-represent setting variability — a single setting condition for the whole study.

### Dose tier abstraction

Mollaahmetoglu uses 0.8 mg/kg IV. Kheirkhah uses subanesthetic ketamine (typically 0.5 mg/kg IV per standard antidepressant protocol). Both map to `dose_tier: "moderate"` per the schema. The schema's intentional abstraction means both studies appear at the same dose tier, even though Mollaahmetoglu is slightly higher.

---

## Coverage from these two sources

### Phases
| Phase | Records | Notes |
|---|---|---|
| pre_session | 3 | All Mollaahmetoglu — Kheirkhah doesn't separate pre-session content |
| onset | 0 | Gap in both sources |
| ascent | 0 | Gap in both sources |
| peak | 47 | Most records |
| k_hole | 0 | After verification, no record cleanly meets the k_hole threshold (deep dissociation + total agency loss + low narrative coherence). Pilot v1 incorrectly marked one P05 record k_hole; downgraded. |
| return | 0 | Gap |
| afterglow | 6 | Mollaahmetoglu transformational + Kheirkhah lingering well-being |

**Onset / ascent / return are not represented.** This is a structural gap in qualitative literature: patients tend to describe the peak content, not the transitions. Will need to either find onset/return-focused sources in phase 3 continuation, or accept that the simulator's transition model has to interpolate these phases.

### Setting variability
| Setting condition | Records |
|---|---|
| music + eye_mask + mindfulness (Kheirkhah intervention) | 14 |
| no music + no eye_mask (Kheirkhah control) | 11 |
| music only, no eye_mask (Mollaahmetoglu) | 28 |

Three distinct setting profiles represented. Good for setting_profile sensitivity in the simulator.

### Dimension anchors emerging

Single-dimension high-confidence anchors (where one dimension is clearly dominant):

| Dimension | Anchor record | Score |
|---|---|---|
| body_detachment=1.0 | kheirkhah-2025_P1_peak_04 ("It didn't feel like I had a body.") | 1.0 |
| time_distortion=1.0 | mollaahmetoglu-2021_P06_peak_01 ("time just goes bananas") | 1.0 |
| meaningfulness=1.0 | mollaahmetoglu-2021_P07_peak_01, P09_peak_02, P09_peak_03; kheirkhah-2025_P33_peak_01 | 1.0 |
| insight=1.0 | mollaahmetoglu-2021_P10_peak_01 ("answered a lot of questions...how little importance") | 1.0 |
| visual_imagery=1.0 | mollaahmetoglu-2021_P09_peak_01 (synapse → cosmos), P09_peak_02 (neon-light God) | 1.0 |
| emotional_valence=+1.0 | kheirkhah-2025_P10_peak_01 ("at peace with myself and the world for the first time in my life") | +1.0 |
| fear=0.75 | mollaahmetoglu-2021_P03_peak_01 (breathing/scary), P04_peak_04 (paranoid trial), kheirkhah-2025_P11_peak_01 (heart racing) | 0.75 |

These anchors are the calibration set for any future psychometric mapping.

### Archetypes confirmed

Three peak archetypes from pilot v1 are reinforced and a fourth emerges:

1. **Mystical-positive** (P07, P09 spiritual; Kheirkhah P9, P15, P25, P33): high meaningfulness, low fear, identity_shift=true, often cosmic_scale.
2. **Visual-only** (P07_peak_02, P04_peak_03; Kheirkhah P1, P2): high sensory/visual, low dissociation, low meaningfulness.
3. **Fear-dominant** (P03, P04_peak_04; Kheirkhah P11): high fear, often medical_anxiety, negative valence.
4. **Calm-embodied (NEW)** (Mollaahmetoglu P04_peak_01; Kheirkhah P9, P26_peak_02, P30): low fear, positive valence, **preserved** body awareness, mild dissociation. This is the "gentle peak" that mindfulness-anchored or experienced subjects produce.

The simulator's transition model needs to support all four as distinct outcomes, not converge to a single mean.

---

## Recommended next steps (phase 3 continuation)

1. **Update bibliography.csv** to remove the misleading "uses 11D-ASC" claim on Kheirkhah.
2. **Pick the next source.** Recommend **Trimmel 2024 meta-synthesis** (paraphrase_only) — it summarizes 24 studies into a three-stage framework that maps onto our phase model. It would let us populate the onset/return gaps via paraphrase even though we can't quote verbatim.
3. **OR** prioritize Walaszek 2025 next for more verbatim quotes — but it overlaps thematically with Mollaahmetoglu more than Trimmel does.

Phase 3 is paused for your review of the rewritten Mollaahmetoglu and the new Kheirkhah JSONL.
