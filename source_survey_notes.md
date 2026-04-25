# Source Survey — Phase 2 Readout

Date: 2026-04-23
Bibliography file: `bibliography.csv`

This is the readout from the first pass of the source survey. It is **not** an extraction yet — it identifies and vets candidate sources so phase 3 can proceed safely.

---

## Headline finding: Erowid is excluded by default

The original `source_vetting_checklist.md` defaulted Erowid to `cite_only`. **That was wrong.** Verified against Erowid Center's posted policy on 2026-04-23:

> Users agree not to download, analyze, distill, reuse, digest, or feed into any AI-type system the report data without first contacting Erowid Center and receiving written permission.

The checklist has been updated. **Default is now `excluded`**. Erowid reports cannot be used as a corpus for this simulator unless we file a written permission request with `copyrights@erowid.org` and document the granted scope verbatim in the bibliography.

This is a significant scoping change. The original architecture leaned on Erowid as one of three primary data layers. With Erowid excluded by default, the dataset's first-person depth comes from:

- Verbatim patient quotes embedded in CC-BY qualitative studies (Mollaahmetoglu, Kheirkhah, etc.)
- Paraphrased themes synthesized from CC-BY-NC-ND meta-analyses (Trimmel)
- Methodological precedent from NLP papers that *did* obtain Erowid permission (Hase et al.)

We can still build a credible simulator from these. We just can't directly ingest Erowid.

**Decision needed from you:** Do we file a written-permission request with Erowid Center now, or proceed with the published-literature corpus only? My recommendation is to proceed without Erowid for v0.1 and revisit only if the eval reveals a coverage gap that Erowid would specifically fill.

---

## Confirmed `permitted` sources (CC-BY family)

These are the load-bearing sources for phase 3 extraction:

| Source | Why it matters |
|---|---|
| **Kheirkhah et al. 2025** — RCT of mindfulness/music/eye-mask during ketamine | Directly informs the `setting_profile` → state-vector relationship. Uses 11D-ASC. CC-BY with verbatim patient quotes. |
| **Mollaahmetoglu et al. 2021** — qualitative interviews, ketamine for AUD | n=12 in clinical setting. CC-BY with quotable verbatim material. Strong for narrative_features (oneness, peacefulness, identity_shift). |
| **Studerus, Gamma & Vollenweider 2010** — OAV/11D-ASC validation | Anchor paper for the psychometric pillar. CC-BY. **Important constraint: the questionnaire items are not reproduced in the paper, and we must not reproduce them either** — cite factor names + thematic content only. |
| **Marguilho, Figueiredo & Castro-Rodrigues 2022** — unified model of ketamine | CC-BY-4.0 review/theory. Best single source for justifying the dose-tier abstraction and for grouping dissociative-vs-psychedelic dimensions in the state vector. |
| **Hase et al. 2022** — NLP analysis of recreational reports | CC-BY-equivalent. Methodological precedent. We cite their **findings** (Erowid-derived statistics) without re-deriving from the underlying corpus. |

## Confirmed `paraphrase_only`

| Source | Why it's restricted |
|---|---|
| **Trimmel et al. 2024** — meta-synthesis of 24 qualitative studies | CC-BY-NC-ND. Three-stage framework (pre/acute/post) maps cleanly onto our phase model. We can paraphrase, cite, and structurally borrow the framework, but cannot reproduce text or figures. |

## Excluded

| Source | Reason |
|---|---|
| Erowid Experience Vaults | TOS forbids AI ingestion without written permission. Default excluded. |
| Reddit / forum posts | TOS + consent issues (see checklist). |

## TODO — needs license verification

Six candidates flagged in `bibliography.csv` with `TODO-` prefix. Verify before phase 3 uses them.

---

## Coverage check against simulator requirements

Mapping confirmed sources back to what the simulator needs:

| Simulator need | Covered by | Gap? |
|---|---|---|
| Person profile → state distributions | Mollaahmetoglu, Kheirkhah, Trimmel | Limited variation in `prior_experience` — clinical samples are mostly naive. |
| Setting profile → state distributions | Kheirkhah (directly tests this) | Single RCT; would benefit from 1–2 more. |
| Administration profile (route, dose tier) → trajectory shape | Marguilho theoretical framework | Empirical dose-tier comparisons are thin in CC-BY literature. |
| Phase model (onset/ascent/peak/return/afterglow) | Trimmel three-stage framework, Mollaahmetoglu phase descriptions | Adequate for v0.1. |
| Narrative features (entity/cosmic/death-rebirth) | Mollaahmetoglu quotes; Marguilho theoretical mapping | Thin without Erowid. May need to expand search. |
| Psychometric mapping (11D-ASC subscales) | Studerus 2010 + Kheirkhah usage | Good — but verify the 3D-ASCr 2025 revalidation paper. |
| NLP/distributional method precedent | Hase et al. 2022 | Adequate. |

## Recommended phase 3 entry criteria

Before starting extraction:

1. You decide whether to file the Erowid permission request or proceed without.
2. Verify the six `TODO-` sources in the bibliography (license + coverage).
3. Add at least 2 more clinical-trial qualitative studies to reduce single-source dependence on Mollaahmetoglu and Kheirkhah.
4. Confirm annotator(s): same person across all records initially, second-pass IRR comes during evaluation per the eval plan.

When those four items are checked off, phase 3 can begin with the JSONL extraction template.

---

## Phase 2 close-out (2026-04-24)

All four entry criteria resolved:

1. **Erowid: WITHOUT.** Proceeding without Erowid for v0.1. Recorded in bibliography. Revisit only if eval shows a coverage gap Erowid would specifically fill.
2. **TODO sources verified** (best-effort):
   - **Verified `permitted` (CC-BY-4.0):** Walaszek et al. 2025 (`Patients' Voices` review with verbatim quotes), Greenway et al. 2025 (BJP music RCT, n=32, uses MEQ + EBI).
   - **Could not auto-verify (publisher fetch blocked):** Stocker 2025 (3D-ASCr, Sage 403), Breeksema 2023 (Springer 303), Griffiths 2021 'Ketamine and me' (ScienceDirect 403), Nature SR comparing-NLP 2025 (303). All defaulted to `cite_only` until manually verified — none are load-bearing.
3. **Additional qualitative studies added:** Walaszek 2025, Greenway 2025, Jilka 2021. Corpus is no longer single-source-dependent.
4. **Annotator: Claude (this session).** User confirmed 2026-04-24.

### Final phase-2 corpus (8 `permitted` + 1 `paraphrase_only`)

| Source | Status | Why it's load-bearing |
|---|---|---|
| Kheirkhah 2025 | permitted | RCT testing setting effects, uses 11D-ASC, verbatim quotes |
| Studerus 2010 | permitted | 11D-ASC factor structure (psychometric anchor) |
| Mollaahmetoglu 2021 | permitted | Clinical qualitative, n=12, verbatim quotes |
| Marguilho 2022 | permitted | Theoretical mapping (dose tier → network → state) |
| Hase 2022 | permitted | NLP precedent (cite findings, not corpus) |
| Walaszek 2025 | permitted | Narrative review with verbatim quotes; CADSS critique |
| Greenway 2025 | permitted | RCT n=32; MEQ + EBI cross-instrument validation |
| Jilka 2021 | permitted | Prospective patient-view focus groups (informs expectancy_valence) |
| Trimmel 2024 | paraphrase_only | 24-study meta-synthesis; three-stage framework |

### Cleared to begin phase 3 extraction.

---

## Phase 2 expansion (2026-04-24, after phase 3 pilot revealed coverage gaps)

PILOT_NOTES showed onset/return/k_hole all with zero records and only IV route represented. Targeted search for sources that fill those gaps:

| Source | Status | Why added |
|---|---|---|
| **Breeksema 2023** (PMC10271905) | upgraded TODO → `permitted` (CC-BY-4.0) | n=17 IPA on **oral esketamine**, **explicit return-phase coverage** ("Lifting the blanket" 1–4 day post-session + "Feeling hungover and fatigued"). Fills both gaps simultaneously. |
| **Breeksema 2022** (Frontiers, oral esketamine) | new `permitted` | Same author group, complementary acute-phase focus, control/context/care themes. |
| **Klysing 2025** (PMC11907890, BMC Nursing) | new `permitted` (CC-BY-4.0) | n=20 **intranasal esketamine** — fills the route gap; person-centred-care framework. |
| **Di Nicola 2025 / REAL-ESKperience** | new `permitted` (CC-BY-4.0) but low priority | n=236 intranasal esketamine, **no verbatim quotes** (used AI thematic analysis). Useful for population-level prevalence stats, not for trajectory extraction. |
| **Muetzelfeldt 2008** "Journey through the K-hole" | new `cite_only` (paywalled Elsevier) | n=90 recreational users with hair-sample-verified drug use. **K-hole-depth phenomenology** that fills the deepest dissociation gap — by paraphrase only. |

Final corpus is now **11 `permitted` + 1 `paraphrase_only` + 1 `cite_only` (k-hole)** sources, no Erowid. Onset/return/k_hole gaps are addressable in phase 3 continuation.

Recommended phase 3 next-source order:
1. **Breeksema 2023** — biggest gap-filler (oral route + return phase + IPA verbatim).
2. **Klysing 2025** — intranasal route.
3. **Trimmel 2024** (paraphrase_only) — to populate transition phases via meta-synthesis paraphrase.
4. **Muetzelfeldt 2008** — paraphrase only, k-hole content.
