# Source Vetting Checklist

Run this checklist on **every candidate source** before extraction. Record the result in the source bibliography with a `reuse_status` flag. No verbatim text gets stored from a source until it has cleared this checklist.

This is a phase-1 deliverable: it gates phase 2 (source survey) and phase 3 (extraction). Do not skip.

---

## Reuse statuses

| Flag | Meaning | What you may store |
|---|---|---|
| `permitted` | License explicitly allows redistribution / derivative works (e.g., CC-BY, CC-BY-SA, CC0, public domain). | Verbatim excerpts + structured fields. |
| `cite_only` | Source is readable but redistribution restricted (most paywalled journal articles, Erowid without explicit permission). | Structured fields + paraphrased `notes`. **No verbatim.** |
| `paraphrase_only` | Reuse permitted with attribution but verbatim excerpts not allowed at scale. | Structured fields + short paraphrase. |
| `excluded` | TOS prohibits scraping, fails ethics check, or content unsuitable. | Nothing. Log the exclusion reason. |

---

## Per-source checklist

For each candidate source, answer all of the following. Record answers in `bibliography.csv` (to be created in phase 2).

### A. Provenance
- [ ] Source has a stable identifier (DOI, PMID, ISBN, archived URL)?
- [ ] Author and publication date known?
- [ ] Source type categorized (clinical_lit / qualitative_interview / erowid / other)?

### B. Legal / licensing
- [ ] License explicitly stated on the source? Record the license string verbatim.
- [ ] If no explicit license: default to `cite_only`. Do not assume permission.
- [ ] If hosted on Erowid: **default to `excluded`**. Erowid's posted TOS forbids feeding report data into AI systems without prior written permission. Only re-classify after obtaining written permission from copyrights@erowid.org and recording the permission scope verbatim in the bibliography notes.
- [ ] If from PubMed Central: check the PMC license tag (Open Access vs. author manuscript). OA = potentially `permitted`; author manuscript = `cite_only`.
- [ ] If behind a publisher paywall: `cite_only` regardless of personal access.

### C. Robots / TOS (for web-fetched sources)
- [ ] `robots.txt` allows the path being fetched?
- [ ] TOS does not prohibit research extraction?
- [ ] Rate limiting respected? (Default: ≥2s between requests, single-threaded.)

### D. Ethics
- [ ] Source does not identify a private individual without consent?
- [ ] Source does not contain content that would require IRB approval to collect freshly (e.g., unpublished interviews, clinical records)? If yes → `excluded`.
- [ ] Source does not glorify, instruct, or facilitate non-clinical use? If yes → `excluded`.
- [ ] If a first-person report describes acute harm or self-harm: still extractable for clinical-relevance signal, but flag with `notes: "harm content"` and exclude verbatim from any patient-facing output.

### E. Quality
- [ ] Report is internally coherent enough to score on the rubric?
- [ ] Report mentions ketamine specifically (not a general dissociative)?
- [ ] Report distinguishes ketamine from other co-administered substances? If polypharmacy and effects can't be isolated → `excluded` for state extraction, retain for theme analysis only.

### F. Storage decision
- [ ] `reuse_status` recorded in bibliography.
- [ ] If `permitted`: which excerpt(s) are stored, with character offsets.
- [ ] If `cite_only` / `paraphrase_only`: confirm `raw_excerpt` field will be left empty in JSONL.
- [ ] If `excluded`: exclusion reason recorded, source still listed for transparency.

---

## Source-class defaults

Use these as **starting assumptions**, then verify per source:

| Source class | Default reuse_status | Notes |
|---|---|---|
| Peer-reviewed journal article (paywalled) | `cite_only` | Use abstract + your own paraphrase. |
| PMC Open Access article (CC-BY) | `permitted` | Verify license tag on the article page. |
| CC-BY qualitative study with quoted patient excerpts | `permitted` for the article framing, but treat patient quotes inside as a nested decision — usually `cite_only` for the quote. |
| Erowid experience report | **`excluded`** | Erowid's TOS (verified 2026-04-23) explicitly forbids users from "downloading, analyzing, distilling, reusing, digesting, or feeding into any AI-type system" report data without prior written permission from copyrights@erowid.org. Default to excluded until written permission is granted; if granted, status moves to `cite_only` (verbatim only as the permission specifies). |
| Reddit / forum post | `excluded` for verbatim; `paraphrase_only` for thematic signal at most. Reddit TOS restricts redistribution and consent is unclear. |
| Substack / personal blog | `cite_only` unless author explicitly licenses. |
| Book / chapter | `cite_only`. Fair-use paraphrase only. |
| Government / NIH / NIMH publication | Usually public domain → `permitted`. Verify per document. |
| Validated psychometric instruments (11D-ASC, MEQ, etc.) | Instrument items themselves are usually copyrighted. Cite the validation paper, do **not** reproduce items verbatim. `cite_only`. |

---

## Categorical exclusions

Always exclude:
- Sources that read primarily as use guides (dose, route, timing instructions).
- Sources describing use in minors.
- Sources that identify named non-public individuals describing illegal use.
- Anything obtained by circumventing a paywall, login, or scraper block.
- AI-generated trip reports presented as real (would contaminate the training distribution).

---

## Audit trail

Every extracted record carries `source_id` → bibliography row → vetting checklist outcome. If a source's status changes (e.g., a publisher rescinds OA), records derived from it must be re-evaluated, not silently kept.
