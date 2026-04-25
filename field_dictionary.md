# Field Dictionary — Ketamine Trip Simulator

Definitions, scales, and operationalization rules for every field in `trip_state_schema.json` and the source-extraction JSONL. Use this as the canonical reference when annotating reports or writing the simulator's transition model.

All scalar dimensions are normalized to **[0, 1]** unless explicitly noted as signed **[-1, 1]**. Annotators should map qualitative report language onto the rubric below; do not invent precision the source does not support.

---

## 1. Inputs

### person_profile

| Field | Type | Definition |
|---|---|---|
| `trait_anxiety` | low/medium/high | Baseline anxiety disposition prior to session. Source: self-report, STAI-T, or clinical chart if available. |
| `prior_experience` | none/some/extensive | Lifetime ketamine exposure. `some` = 1–5 prior sessions; `extensive` = 6+. |
| `depression_context` | bool | True if session indication is treatment-resistant depression or similar mood indication. |
| `trauma_salience` | low/medium/high | Degree to which trauma material is psychologically active going into the session. |
| `need_for_control` | low/medium/high | Tolerance for surrendering agency; low tolerance predicts higher fear at peak dissociation. |
| `expectancy_valence` | negative/neutral/positive | Pre-session framing/expectations. Distinct from preparation_quality. |

### setting_profile

| Field | Type | Definition |
|---|---|---|
| `clinical_support` | bool | Medical or therapeutic personnel present and trained. |
| `therapist_present` | bool | A psychotherapist (not just a nurse) is in the room. |
| `music` | bool | Curated music protocol active during session. |
| `eye_mask` | bool | Visual occlusion used to encourage interoception. |
| `preparation_quality` | low/medium/high | Adequacy of pre-session psychoeducation, intention-setting, and trust-building. |
| `perceived_safety` | low/medium/high | Subject's reported felt safety, not objective setting safety. |
| `alone` | bool | No other person physically present. |

### administration_profile

Schema deliberately uses **dose tiers**, not mg/kg values. This is to discourage the artifact from being repurposed as a dosing guide.

| Field | Type | Definition |
|---|---|---|
| `route` | unknown/IV/IM/intranasal/oral/sublingual | Administration route as reported. |
| `dose_tier` | subperceptual / low / moderate / high / dissociative | Qualitative tier as labeled in source literature. |
| `infusion_profile` | bolus / slow_infusion / repeated / single / unknown | Pharmacokinetic shape, not amount. |

---

## 2. State vector

Each `trajectory[i].state` is a snapshot at one phase. Annotators should treat values as **rubric-anchored ordinals**, not measurements.

### Anchor rubric (applies to all [0, 1] dimensions)

| Value | Meaning |
|---|---|
| 0.0 | Dimension absent / not mentioned / explicitly denied. |
| 0.25 | Mild, fleeting, or background presence. |
| 0.5 | Clearly present, sustained, but not dominant. |
| 0.75 | Dominant feature of this phase. |
| 1.0 | Total / overwhelming / saturating. |

### Dimension definitions

| Dimension | Range | Definition | Example language |
|---|---|---|---|
| `dissociation` | [0,1] | Sense of separation from self, body, or surroundings as a unified experience. | "I wasn't there", "watching from outside" |
| `body_detachment` | [0,1] | Specifically: loss of body ownership or proprioception. Subset of dissociation. | "no body", "limbs disappeared", "floating" |
| `time_distortion` | [0,1] | Perceived elapsed time diverges from clock time. | "lasted forever", "no time at all" |
| `sensory_distortion` | [0,1] | General perceptual change across modalities (excluding pure visual/auditory, captured separately). | "everything felt textured / liquid / wrong" |
| `visual_imagery` | [0,1] | Closed- or open-eye visuals, geometric patterns, scenes, vistas. | "fractals", "tunnel", "landscapes" |
| `auditory_change` | [0,1] | Music distortion, auditory hallucination, or hyperacuity. | "the music became the room" |
| `cognitive_coherence` | [0,1] | Inverse of fragmentation. **High = coherent, low = fragmented.** Note polarity. | High: "thoughts moved clearly". Low: "couldn't hold a thought". |
| `emotional_valence` | [-1,1] | Signed affect. -1 = terror/despair, 0 = neutral, +1 = bliss/love. | — |
| `fear` | [0,1] | Distinct from negative valence: fear specifically (panic, dread, threat). | "I thought I was dying" |
| `meaningfulness` | [0,1] | Subjective sense that the experience matters / is profound. | "the most important moment of my life" |
| `insight` | [0,1] | Specific noetic content the subject endorses post-session. | "I understood why I push people away" |
| `loss_of_agency` | [0,1] | Perceived inability to direct attention, intention, or movement. | "couldn't choose anything" |
| `narrative_coherence` | [0,1] | Whether the experience forms a story the subject can tell linearly. Distinct from cognitive_coherence (in-the-moment thinking). |

### Polarity warnings

- `cognitive_coherence` is the **inverse** of "cognitive_fragmentation" used in the original task spec. The schema uses coherence so all "more = more present" semantics align, except `emotional_valence`, which is signed.
- `emotional_valence` and `fear` are **independent**. A subject can have positive valence with high fear (awe), or negative valence with low fear (sadness). Do not collapse.

---

## 3. Phases

| Phase | Definition | Typical duration cue |
|---|---|---|
| `onset` | First perceptible effects; body sensations begin to shift. | Minutes 0–5 IV; 5–15 IM/IN. |
| `ascent` | Effects intensify rapidly; subject reports rising dissociation. | Brief — minutes. |
| `peak` | Maximum subjective intensity; dominant phase for narrative themes. | 10–30 minutes typical at clinical doses. |
| `k_hole` | Reserved label for deep dissociative states with near-total loss of agency, embodiment, and narrative coherence. Usually only at high or recreational dose tiers. Not all peaks are k-holes. |
| `return` | Decline of acute effects; subject reorients to body and room. | 10–20 minutes. |
| `afterglow` | Post-acute period; mood, insight, fatigue, integration needs. | Hours to days. |

`duration_bin` (early/middle/peak/late/post) is a **coarse temporal slot**, not a clock value, and is provided so annotators can mark phase-position without committing to minutes.

---

## 4. Narrative features (boolean)

Each is **present / absent** for a given phase.

| Feature | Definition |
|---|---|
| `identity_shift` | Subject reports change in who they are, ego dissolution, or merger. |
| `death_rebirth_theme` | Explicit dying-and-returning content. |
| `cosmic_scale` | Universe / infinity / vast scale imagery. |
| `medical_anxiety` | Worry about the body, the dose, the procedure, dying for medical reasons. |
| `childhood_memory` | Vivid retrieval of childhood scene. |
| `entity_or_presence` | Sense of another being, intelligence, or watcher. |
| `floating_or_falling` | Vestibular/spatial motion themes. |
| `tunnel_void_space_imagery` | Specific tunnel, void, or empty-space imagery. |

---

## 5. Source-extraction record fields (JSONL dataset)

These are fields stored per source document, not per simulated trajectory.

| Field | Notes |
|---|---|
| `source` | clinical_lit / qualitative_interview / erowid / other |
| `source_id` | DOI, PMID, URL, or stable identifier |
| `reuse_status` | permitted / cite_only / paraphrase_only / excluded — see source-vetting checklist |
| `route` | as reported |
| `context.clinical` | bool |
| `reported_phase` | phase label if attributable |
| `subjective_dimensions.*` | per-dimension scores using the anchor rubric |
| `narrative_features.*` | booleans |
| `raw_excerpt` | **Only populated if `reuse_status == permitted` for verbatim quotation.** Otherwise leave empty and rely on `notes`. |
| `notes` | annotator paraphrase / observations |
| `annotator_id` | who scored it |
| `annotated_at` | timestamp |

---

## 6. Hard rules for annotators

1. **Do not extrapolate.** If a report does not mention a dimension, score it 0 and note absence — do not impute from context.
2. **Do not store verbatim text from non-permitted sources.** Paraphrase into `notes`, leave `raw_excerpt` empty.
3. **One annotator per record initially.** A second pass for inter-rater reliability comes during evaluation (see `evaluation_plan.md`).
4. **No dose values, no preparation instructions, no use guidance** anywhere in the dataset. Tier labels only.
5. **Flag ambiguous reports** with `notes: "AMBIGUOUS — needs review"` rather than guessing.
