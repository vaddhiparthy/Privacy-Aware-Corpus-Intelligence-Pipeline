# Architecture

The system converts a local text export into reviewable content catalogs without exposing the full corpus to a hosted language model.

## Pipeline

```text
Split JSON export
  -> conversation reader
  -> conversation units and chunk units
  -> identifier detector
  -> sensitive-domain policy
  -> public-topic scorer
  -> output router
  -> Markdown and JSON reports
```

## Runtime Components

| Component | Path | Role |
| --- | --- | --- |
| Reader | `src/corpus_privacy_intelligence/reader.py` | Streams split JSON files and extracts ordered messages |
| Text layer | `src/corpus_privacy_intelligence/text.py` | Normalizes terms, removes stopwords, stems terms, and builds previews |
| PII detector | `src/corpus_privacy_intelligence/pii.py` | Applies deterministic private-identifier patterns |
| Taxonomy | `src/corpus_privacy_intelligence/taxonomy.py` | Defines public topic families and sensitive-domain terms |
| Classifier | `src/corpus_privacy_intelligence/classifier.py` | Routes each unit into public, private, or low-signal queues |
| Pipeline | `src/corpus_privacy_intelligence/pipeline.py` | Coordinates scanning, chunk recovery, classification, and summaries |
| Reports | `src/corpus_privacy_intelligence/reports.py` | Writes Markdown and JSON artifacts |
| Advanced validation | `src/corpus_privacy_intelligence/advanced_validation.py` | Runs detector comparison across policy, strict, semantic, Presidio, and spaCy signals |

## Routing Decisions

Each unit is assigned one of the practical queues:

| Queue | Meaning |
| --- | --- |
| `public_candidate` | Content passed privacy gates and met public-topic score threshold |
| `exclude_private_identifier` | Hard private identifier was detected |
| `exclude_sensitive_domain` | Sensitive personal domain was detected |
| low signal | Unit did not meet public score threshold and was retained for audit |

## Chunk Recovery

The scanner evaluates full conversations first. If a full conversation is excluded, the pipeline also evaluates smaller chunks from that conversation. This prevents one sensitive section from discarding unrelated safe technical content in a long thread.

## Validation Layer

The advanced validation path is intentionally separate from the production policy. It is used to compare classifier behavior against additional free NLP detectors and identify disagreement rows for review.

Optional detectors:

- Microsoft Presidio;
- spaCy;
- strict rule detector;
- semantic token-family scorer.

Unavailable optional detectors are reported as unavailable rather than treated as passing signals.
