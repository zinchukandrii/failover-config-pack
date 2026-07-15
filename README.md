# Resilient Runtime Failover Configuration

A small, provider-neutral Python tool for validating ordered runtime failover policies and simulating recovery paths **without calling any provider**.

## Why it exists

Runtime failover configuration is often copied as an untested list of model or provider names. That makes a timeout, rate-limit event, or credential failure difficult to reason about under pressure.

This project turns the policy into a checked contract:

```text
validated configuration → declared outcome → deterministic route simulation → auditable decision
```

![Scope](https://img.shields.io/badge/scope-provider--neutral-176B5B)
![Safety](https://img.shields.io/badge/external%20calls-none-176B5B)

## What it demonstrates

- Strict JSON validation before simulation.
- Ordered candidates with explicit tiers.
- Retryable and non-retryable outcomes.
- Fail-closed behavior for unknown or non-retryable failures.
- Deterministic output suitable for tests, reviews and incident runbooks.

It deliberately does **not** store credentials, resolve providers, probe live models, or modify runtime configuration.

## Quick start

```bash
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -e '.[dev]'

runtime-failover validate examples/runtime-failover.json
runtime-failover simulate examples/runtime-failover.json quality examples/outcomes-recovery.json
```

Expected simulation summary:

```json
{
  "route_id": "quality",
  "status": "SELECTED",
  "selected": "provider-c/fast"
}
```

The example declares two retryable failures (`timeout`, `rate_limited`) before selecting the third candidate. No network request is made.

## Configuration contract

```json
{
  "version": "1.0",
  "policy": {
    "request_timeout_seconds": 15,
    "retryable_outcomes": ["timeout", "rate_limited", "unavailable"]
  },
  "routes": [
    {
      "id": "quality",
      "candidates": [
        {"id": "provider-a/quality", "tier": 1},
        {"id": "provider-b/balanced", "tier": 2}
      ]
    }
  ]
}
```

Validation rejects malformed JSON, an unsupported version, empty routes, duplicate route IDs, duplicate candidate IDs and invalid tier/timeout values.

## Safety boundaries

| Boundary | Behavior |
|---|---|
| Provider calls | Not implemented. The simulator consumes supplied outcomes only. |
| Credentials | Not accepted, stored or logged. |
| Unknown outcomes | `BLOCKED` — no silent success assumption. |
| Exhausted route | `EXHAUSTED` with the complete deterministic attempt list. |
| Configuration defects | Fail closed before a route is simulated. |

## Quality checks

```bash
.venv/bin/python -m pytest -q
.venv/bin/python -m ruff check .
```

## Limitations

This is a policy-validation and simulation demonstrator, not a production traffic router. Production adoption needs approved provider adapters, secrets management, telemetry, operational ownership and an explicit rollback plan.

## Repository hygiene

The public example uses fictional provider identifiers only. Do not commit account names, workspace paths, API keys, live health reports or production routing details.

## License

MIT — see [LICENSE](LICENSE).
