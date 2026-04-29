# Privacy-Aware Corpus Intelligence Pipeline

A local-first pipeline for mining large text exports while keeping sensitive material out of downstream publishing or analysis workflows.

The project solves a practical problem: useful ideas, research notes, technical explanations, and product comparisons are often mixed with private identifiers, health details, immigration records, resume edits, and job-search material. A basic keyword search either misses risk or throws away too much. This pipeline separates those concerns with an auditable classification flow.

## What It Does

- Reads split JSON conversation exports without loading the whole corpus into an LLM context.
- Breaks long conversations into chunks so safe content can be recovered from otherwise sensitive threads.
- Detects hard private identifiers with deterministic patterns.
- Excludes sensitive personal domains such as private health, immigration, and resume/job-search content.
- Builds compact NLP signatures with normalized terms, stopword removal, light stemming, and term frequencies.
- Classifies retained content into topic families for review and scheduling.
- Produces Markdown and JSON outputs for both human review and downstream automation.

## Why It Is Built This Way

The pipeline treats privacy detection as a control system, not a writing prompt.

Hard identifiers such as emails, phone numbers, SSN-like strings, card-like numbers, and API-key shapes are handled with deterministic rules. Sensitive domains are handled separately so general content is not discarded just because it mentions broad words like finance, technology, or data.

The result is conservative where it matters and useful where it should be: private material is filtered out, while public technical and explanatory content remains available for review.

## Project Structure

```text
src/corpus_privacy_intelligence/
  classifier.py    Decision logic for topics, exclusions, scoring, and freshness
  cli.py           Command-line entry point
  models.py        Data structures shared across the pipeline
  pii.py           Deterministic private identifier detection
  pipeline.py      Orchestration and summary generation
  reader.py        Export parsing and chunk construction
  reports.py       Markdown and JSON output writers
  taxonomy.py      Public topic families and sensitive-domain terms
  text.py          Token cleanup, stopword removal, and term counting
tests/
  test_classifier.py
docs/
  architecture.md
```

## Usage

```powershell
python -m corpus_privacy_intelligence.cli `
  --export-dir "C:\path\to\export" `
  --out-dir "C:\path\to\outputs" `
  --min-public-score 55
```

The export directory should contain files named like `conversations-000.json`, `conversations-001.json`, and so on.

## Outputs

- `public_candidates.md`: reviewable public-safe candidates.
- `public_candidates.json`: machine-readable public-safe candidates with topic and term metadata.
- `excluded_private.md`: excluded items with reasons.
- `excluded_private.json`: machine-readable excluded items.
- `skipped_low_signal.json`: low-signal units retained for audit.
- `topic_summary.md`: topic counts and draft review schedule.
- `scan_summary.json`: run-level metrics.

## Current Privacy Policy

The default policy excludes:

- SSN-like identifiers
- emails and phone numbers
- card-like digit sequences
- API-key and token-like strings
- identity document context
- street-address context
- private health details
- immigration and visa details
- resume, recruiter, interview, salary, employer, and job-search material

The default policy retains general public content such as technical tutorials, product research, general finance explainers, infrastructure notes, vehicle research, creative ideas, philosophy, and learning material.

## Roadmap

- Add embedding-based topic clustering.
- Add named-entity recognition for people, organizations, dates, and locations.
- Add a redaction preview stage for borderline content.
- Add active-learning feedback so reviewer decisions improve future runs.
- Add evaluation fixtures with precision and recall reporting.
- Add optional integrations with mature PII frameworks such as Microsoft Presidio.

