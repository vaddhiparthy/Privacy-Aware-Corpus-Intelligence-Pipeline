# Validation

## Test Commands

```powershell
python -m pytest -q
python -m compileall src tests
```

## Covered Behaviors

The current tests validate that:

- SSN-like identifiers are excluded;
- immigration context is excluded;
- general technical content is retained;
- general finance explanatory content is retained when no private identifier is present.

## Policy Review Areas

When changing classifier behavior, add fixtures for:

- one hard-private example;
- one sensitive-domain example;
- one legitimate public example from a nearby vocabulary;
- one borderline example that should remain low signal or review-only.

This keeps broad terms such as finance, technology, health, or immigration from becoming accidental blanket filters.
