# Architecture

## Objective

The system converts a large private text archive into reviewable content catalogs without exposing the full corpus to a language model. It is designed for cases where the archive contains a mix of publishable knowledge and sensitive personal material.

## Processing Flow

1. **Ingest**

   The reader streams split JSON files from disk. Each conversation is parsed into ordered messages.

2. **Build Units**

   Every conversation is represented as a full unit and as smaller chunk units. Chunking prevents one private section from eliminating an entire long conversation.

3. **Normalize Text**

   The text layer removes common stopwords, applies light stemming, and builds compact term signatures. These signatures support classification, review, and later clustering.

4. **Detect Private Identifiers**

   The PII layer applies deterministic patterns for identifiers that should not enter public workflows.

5. **Apply Sensitive-Domain Rules**

   The classifier excludes health, immigration, and resume/job-search material. These are intentionally separated from broad public domains such as finance or data systems.

6. **Classify Public Topics**

   Retained content is mapped to review categories such as AI systems, software automation, infrastructure, product guides, vehicles, consumer finance explainers, learning, and philosophy.

7. **Score and Route**

   Each unit is routed into one of three queues:

   - public candidate
   - excluded private
   - skipped low signal

8. **Report**

   The report layer writes Markdown catalogs for reviewers and JSON files for downstream tools.

## Design Principles

- Keep raw private text local.
- Prefer deterministic privacy controls for hard identifiers.
- Keep sensitive-domain policy explicit and auditable.
- Salvage safe chunks instead of deleting entire conversations too aggressively.
- Generate artifacts that a reviewer can inspect without opening the full archive.

## Extension Points

- Replace taxonomy scoring with embedding similarity.
- Add a NER layer before reporting.
- Add a redaction stage after classification.
- Add a vector index for approved public chunks.
- Add reviewer feedback and active learning.

