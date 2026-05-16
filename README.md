# Privacy-Aware Corpus Intelligence Pipeline

This repository implements a local-first classification pipeline for large text exports that contain a mix of reusable knowledge and sensitive personal material.

Public presentation: <https://surya.vaddhiparthy.com/Privacy-Aware-Corpus-Intelligence-Pipeline>

## Implemented System

| Capability | Implementation |
| --- | --- |
| Split-export ingestion | Streams `conversations-*.json` files from a local export directory |
| Chunk recovery | Evaluates full conversations and smaller chunks so safe sections can be recovered from mixed threads |
| Private identifier detection | Deterministic checks for SSN-like strings, emails, phones, cards, addresses, and token-like values |
| Sensitive-domain routing | Excludes private health, immigration, resume, recruiter, interview, salary, and job-search material |
| Public topic classification | Scores retained content into explicit topic families with term evidence |
| Text signatures | Normalized terms, stopword removal, light stemming, and term-frequency metadata |
| Output artifacts | Writes Markdown review catalogs and JSON machine-readable outputs |
| Optional validation | Compares the policy classifier against strict rules, semantic scoring, Presidio, and spaCy when optional packages are installed |

## Processing Flow

```text
Local text export
  -> JSON conversation reader
  -> conversation and chunk units
  -> deterministic identifier checks
  -> sensitive-domain policy
  -> public-topic scoring
  -> public / private / low-signal output queues
  -> Markdown and JSON reports
```

The pipeline keeps raw private text local. It does not send the corpus to a hosted LLM or remote embedding service.

## Repository Layout

| Path | Purpose |
| --- | --- |
| `src/corpus_privacy_intelligence/reader.py` | Reads split JSON exports and builds text units |
| `src/corpus_privacy_intelligence/pii.py` | Detects hard private identifiers |
| `src/corpus_privacy_intelligence/taxonomy.py` | Public topic families and sensitive-domain terms |
| `src/corpus_privacy_intelligence/classifier.py` | Policy classifier and routing decisions |
| `src/corpus_privacy_intelligence/pipeline.py` | End-to-end scan orchestration |
| `src/corpus_privacy_intelligence/reports.py` | Markdown and JSON output writers |
| `src/corpus_privacy_intelligence/advanced_validation.py` | Optional multi-detector validation run |
| `src/corpus_privacy_intelligence/advanced_detectors.py` | Policy, strict, semantic, Presidio, and spaCy detector wrappers |
| `tests/` | Classifier regression tests |
| `docs/` | Architecture and validation notes |

## Install

Core pipeline:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
python -m pip install -e ".[dev]"
```

Optional validation packages:

```powershell
python -m pip install -e ".[nlp]"
```

The optional packages are not required for the main classifier.

## Run

```powershell
python -m corpus_privacy_intelligence.cli `
  --export-dir "C:\path\to\export" `
  --out-dir "C:\path\to\outputs" `
  --min-public-score 55 `
  --chunk-chars 9000
```

Expected input files are named like:

```text
conversations-000.json
conversations-001.json
```

## Outputs

| Output | Purpose |
| --- | --- |
| `public_candidates.md` | Reviewable public-safe candidates |
| `public_candidates.json` | Machine-readable public-safe rows with topic and term metadata |
| `excluded_private.md` | Excluded units with reasons |
| `excluded_private.json` | Machine-readable private exclusions |
| `skipped_low_signal.json` | Low-signal rows retained for audit |
| `topic_summary.md` | Topic counts and review schedule |
| `scan_summary.json` | Run-level counts, topic counts, exclusion counts, and identifier counts |

## Policy

Default exclusions:

- SSN-like identifiers;
- email addresses and phone numbers;
- card-like digit sequences;
- API key and token-like strings;
- identity-document context;
- street-address context;
- private health context;
- immigration and visa context;
- resume, recruiter, interview, salary, employer, and job-search context.

Default retainable categories include technical tutorials, infrastructure notes, software automation, AI systems, product research, general finance explainers, vehicle research, learning material, creative ideas, and philosophy.

## Advanced Validation

The optional validation command compares the primary policy with independent detectors:

```powershell
python -m corpus_privacy_intelligence.advanced_validation `
  --export-dir "C:\path\to\export" `
  --out-dir "outputs\advanced_validation" `
  --limit 300
```

Outputs:

- `advanced_validation_results.json`
- `advanced_validation_summary.json`
- `advanced_validation_report.md`

Presidio and spaCy are optional. If they are unavailable, the validation runner records them as unavailable instead of pretending they ran.

## Validation

```powershell
python -m pytest -q
python -m compileall src tests
```

## Privacy Notes

- Run against local exports only.
- Do not commit raw exports or generated output directories.
- Treat `public_candidates` as a review queue, not an automatic publishing decision.
- Keep policy changes explicit in `taxonomy.py`, `pii.py`, and classifier tests.
