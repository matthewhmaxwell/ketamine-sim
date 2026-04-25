# JSONL Extraction Template

One file per source. One JSONL line per **annotation unit** (typically one identifiable quote or one explicitly themed claim attributable to a participant or to the paper's authors).

The format below is the canonical record. Annotators (Claude or human) must apply `field_dictionary.md` rubric anchors when scoring dimensions and must obey the hard rules in section 6 of that document.

## Record schema

```json
{
  "record_id": "string — unique within file, e.g. mollaahmetoglu-2021_P07_peak_01",
  "source_id": "string — must match an entry in bibliography.csv",
  "source_class": "clinical_lit | qualitative_interview | erowid | psychometric | other",
  "reuse_status": "permitted | cite_only | paraphrase_only | excluded",

  "participant_id": "string — paper's label (P01, P07, etc.) or 'unlabeled' or 'authors' for theoretical claims",
  "n_in_source": "integer — total participants in source if known",

  "context": {
    "clinical": "boolean",
    "route": "unknown | IV | IM | intranasal | oral | sublingual",
    "dose_tier": "subperceptual | low | moderate | high | dissociative | unknown",
    "infusion_profile": "bolus | slow_infusion | repeated | single | unknown",
    "setting": {
      "music": "boolean | null",
      "eye_mask": "boolean | null",
      "therapist_present": "boolean | null",
      "alone": "boolean | null"
    }
  },

  "reported_phase": "onset | ascent | peak | k_hole | return | afterglow | pre_session | unattributable",
  "phase_inference_basis": "string — why we assigned this phase",

  "subjective_dimensions": {
    "dissociation": "number 0-1",
    "body_detachment": "number 0-1",
    "time_distortion": "number 0-1",
    "sensory_distortion": "number 0-1 — optional",
    "visual_imagery": "number 0-1 — optional",
    "auditory_change": "number 0-1 — optional",
    "cognitive_coherence": "number 0-1 — optional, INVERSE of fragmentation",
    "emotional_valence": "number -1 to 1",
    "fear": "number 0-1",
    "meaningfulness": "number 0-1 — optional",
    "insight": "number 0-1 — optional",
    "loss_of_agency": "number 0-1",
    "narrative_coherence": "number 0-1 — optional"
  },

  "narrative_features": {
    "identity_shift": "boolean",
    "death_rebirth_theme": "boolean",
    "cosmic_scale": "boolean",
    "medical_anxiety": "boolean",
    "childhood_memory": "boolean",
    "entity_or_presence": "boolean",
    "floating_or_falling": "boolean",
    "tunnel_void_space_imagery": "boolean"
  },

  "raw_excerpt": "string — only populated if reuse_status == permitted. Verbatim text from source.",
  "raw_excerpt_completeness": "full | abbreviated_with_ellipses | paraphrased",
  "source_theme_label": "string — paper's own theme/section label for this content",

  "notes": "string — annotator paraphrase, ambiguities, follow-up flags",
  "annotator_id": "string",
  "annotated_at": "ISO 8601 datetime"
}
```

## Required vs optional fields

**Required:** `record_id`, `source_id`, `reuse_status`, `participant_id`, `context.clinical`, `context.route`, `reported_phase`, `phase_inference_basis`, `subjective_dimensions.{dissociation, body_detachment, time_distortion, emotional_valence, fear, loss_of_agency}`, `narrative_features.*` (all booleans), `annotator_id`, `annotated_at`.

**Optional:** All other `subjective_dimensions`, `raw_excerpt` (only if permitted), `source_theme_label`, `n_in_source`.

## Hard rules (recap from field_dictionary.md §6)

1. **Do not extrapolate.** Score 0 for any dimension not directly evidenced by the quote/claim. Do not impute from setting or paper context.
2. **`raw_excerpt` only if `reuse_status == permitted`.** Otherwise leave empty and rely on `notes`.
3. **Mark truncated/abbreviated text** with `raw_excerpt_completeness: "abbreviated_with_ellipses"` so a reader knows it is not the full quote.
4. **No dose values in any field.** Tier labels only.
5. **Flag ambiguous records** with `notes: "AMBIGUOUS — needs review"` and assign 0 for unclear dimensions.

## Phase assignment guidance

| Quote content cue | Phase |
|---|---|
| Pre-treatment expectations, motivations, fears | `pre_session` |
| First few minutes, body sensations beginning | `onset` |
| Rising intensity, "going somewhere" | `ascent` |
| Peak imagery, dissociation, ego dissolution, mystical content | `peak` |
| Deep dissociation, total loss of agency, near-total fragmentation | `k_hole` |
| Coming back, reorienting | `return` |
| Days-after reflections, lasting changes | `afterglow` |
| Generalization across the whole experience | `unattributable` |

Use `phase_inference_basis` to record what cue made you pick the phase. If the cue is weak, prefer `unattributable`.

## File naming

`extractions/<source_id>.jsonl` — one source per file. Match `source_id` to bibliography.csv exactly.
