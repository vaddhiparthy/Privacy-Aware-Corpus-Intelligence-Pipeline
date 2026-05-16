# Operations

This project is designed for local execution against private text exports.

## Core Run

```powershell
python -m corpus_privacy_intelligence.cli `
  --export-dir "C:\path\to\export" `
  --out-dir "C:\path\to\outputs" `
  --min-public-score 55 `
  --chunk-chars 9000
```

## Output Handling

Generated outputs may contain sensitive previews and should stay outside Git unless deliberately sanitized.

Recommended ignored output locations:

- `outputs/`
- `data/`
- `exports/`
- local review folders outside the repository

## Review Rule

`public_candidates` means "safe enough for human review." It does not mean "publish automatically."

Before publishing derived content, inspect:

- exclusion reasons;
- identifier hits;
- topic scores;
- preview text;
- source conversation title.

## Optional Validation

```powershell
python -m corpus_privacy_intelligence.advanced_validation `
  --export-dir "C:\path\to\export" `
  --out-dir "outputs\advanced_validation" `
  --limit 300
```

Use a bounded `--limit` first when optional NLP packages are installed because Presidio and spaCy can be slow on CPU.
