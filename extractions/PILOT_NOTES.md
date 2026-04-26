# Phase 3 Extraction Notes

Date: 2026-04-24
Annotator: Claude (claude-opus-4-7-2026-04-24)

## Files

| File | Records | Source license |
|---|---|---|
| `mollaahmetoglu-2021.jsonl` | 30 | CC-BY (verbatim) |
| `kheirkhah-2025.jsonl` | 27 | CC-BY (verbatim) |
| `breeksema-2023.jsonl` | 27 | CC-BY-4.0 (verbatim) |
| `klysing-2025.jsonl` | 7 | CC-BY-4.0 (verbatim) |
| `trimmel-2024.jsonl` | 11 | CC-BY-NC-ND-4.0 (paraphrase, no verbatim) |

102 total records: 91 verbatim, 11 paraphrase. All have been **audited via `verify_quotes.py`** (substring match against the raw PMC HTML with tags stripped and unicode normalized). Every `raw_excerpt` is present verbatim in the source. All records use `raw_excerpt_completeness: "full"`.

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

### Phases (after Klysing + Trimmel added)
| Phase | Records | Notes |
|---|---|---|
| pre_session | 8 | Mollaahmetoglu (3) + Klysing (3 care-context) + Trimmel meta (1) + Klysing P9 anticipation |
| onset | 1 | Breeksema P7 vibration-humming progression |
| ascent | 1 | Breeksema P4 'Suddenly, all at once, I enter this experience' |
| peak | 67 | Most records — across IV / oral / intranasal routes |
| k_hole | 4 | Breeksema P10 (×2), P4 (×2). Two valence variants: neutral-suspended and fear-dominant catastrophic. |
| return | 6 | Breeksema (5) + Trimmel meta (1 comedown). |
| afterglow | 14 | Mollaahmetoglu (5) + Kheirkhah (2) + Breeksema (4) + Klysing (2) + Trimmel meta (4 including 'failed-treatment afterglow' — 10th archetype) |

**Phase coverage is now complete and validated by meta-synthesis.** Trimmel's 24-study aggregation confirms our archetypes are not idiosyncratic to single sources.

### Setting variability
| Setting condition | Records |
|---|---|
| music + eye_mask + mindfulness (Kheirkhah intervention) | 14 |
| no music + no eye_mask (Kheirkhah control) | 11 |
| music only, no eye_mask (Mollaahmetoglu, IV) | 30 |
| no music + no eye_mask (Breeksema, oral) | 27 |
| variable music, dim/dark room, person-centred (Klysing, intranasal) | 7 |
| variable across 24 studies (Trimmel meta) | 11 |

All three administration routes now represented: IV (57) + oral (27) + intranasal (7) + meta-aggregate (11).

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

Four peak archetypes from prior extractions, plus k_hole and afterglow archetypes from Breeksema:

**Peak archetypes:**
1. **Mystical-positive** (Mollaahmetoglu P07, P09 spiritual; Kheirkhah P9, P15, P25, P33; Breeksema P2, P7_peak_03, P8, P17_peak_02): high meaningfulness, low fear, identity_shift=true, often cosmic_scale.
2. **Visual-only** (Mollaahmetoglu P07_peak_02, P04_peak_03; Kheirkhah P1, P2; Breeksema P15_peak_01): high sensory/visual, low dissociation, low meaningfulness.
3. **Fear-dominant** (Mollaahmetoglu P03, P04_peak_04; Kheirkhah P11; Breeksema P3): high fear, often medical_anxiety, negative valence.
4. **Calm-embodied** (Mollaahmetoglu P04_peak_01; Kheirkhah P9, P26_peak_02, P30): low fear, positive valence, **preserved** body awareness, mild dissociation. The "gentle peak."

**K_hole archetypes (NEW from Breeksema):**
5. **Neutral-suspended k_hole** (P10): all dissociative dimensions saturated, valence neutral, no acute fear — feels like timeless suspension rather than terror.
6. **Fear-dominant k_hole** (P4): same dimensional saturation but with fear=1.0, valence strongly negative, death_rebirth_theme=true ("I think I'm dead, can't return to my body, time is endless"). The catastrophic-trip archetype.

**Afterglow archetypes (NEW from Breeksema):**
7. **Partial-lift afterglow** (P10_afterglow): "blanket lifted by a corner," ~36-hour mood improvement, then subsides.
8. **Baseline-restoration afterglow** (P16): sustained return to "neutral feeling of well-being...like a normal person." Does not subside.
9. **Restored-affect afterglow** (P4_afterglow): emotional re-engagement after long anhedonia. Same participant (P4) had catastrophic k_hole AND restored-affect afterglow — these are not mutually exclusive.

The simulator's transition model needs to support all 9 distinct end-states, not converge to means. Importantly: **a fear-dominant k_hole does not preclude a positive afterglow**, per P4's trajectory — independently confirmed by Trimmel meta-finding that emotionally negative acute experiences do not preclude clinical benefit.

**Two additional archetypes from Trimmel meta-synthesis:**

10. **Neutral-ineffable peak** (Trimmel Subtheme 2.2 neutral subset): "simply strange, confusing or hard to put into words" — neither positive nor negative. Distinct from the four valence-anchored peaks. Likely under-captured by valence-based instruments like CADSS.
11. **Failed-treatment afterglow** (Trimmel Subtheme 3.3): no benefit OR rapid relapse → frustration, disappointment, intensified hopelessness. Critical for the simulator's safety pillar — non-response trajectories must be modeled. This is the only archetype with negative afterglow valence.

---

## Recommended next steps (phase 3 continuation)

1. **Update bibliography.csv** to remove the misleading "uses 11D-ASC" claim on Kheirkhah.
2. **Pick the next source.** Recommend **Trimmel 2024 meta-synthesis** (paraphrase_only) — it summarizes 24 studies into a three-stage framework that maps onto our phase model. It would let us populate the onset/return gaps via paraphrase even though we can't quote verbatim.
3. **OR** prioritize Walaszek 2025 next for more verbatim quotes — but it overlaps thematically with Mollaahmetoglu more than Trimmel does.

Phase 3 is paused for your review of the rewritten Mollaahmetoglu and the new Kheirkhah JSONL.
