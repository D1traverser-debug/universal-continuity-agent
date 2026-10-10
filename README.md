# Universal Continuity Agent

Cross-chat task continuity infrastructure for the user.

## Authority

- **GitHub `main`** is the engineering source of truth for contracts, resolver/harness, templates, tests, and continuity manifests when stored here.
- **Domain owners** remain authoritative for business logic and stronger runtime checkpoints.
- **ChatGPT Library / Notion / Google Drive / other connected stores are not implicit control-plane authority.** They may be references or owner-designated artifact stores, but Continuity correctness must not depend on their presence.
- Registries are rebuildable caches; per-task/per-system owner state is authoritative.

## Bootstrap

The repository hot path begins with only:

1. [`ENTRYPOINT.md`](ENTRYPOINT.md)
2. [`CURRENT_PROTOCOL.json`](CURRENT_PROTOCOL.json)

Everything else is loaded by the event-driven matrix in `ENTRYPOINT.md`. [`PROTOCOL.md`](PROTOCOL.md) is a human-readable protocol reference, not mandatory bootstrap input.

## Repository boundary

This repository owns only universal continuity infrastructure. Financial Writing, A-share, Novel Writing, Video Growth and other business logic remain in their own agents/repos. Universal may validate routing, compatibility, execution-readiness and shared methodology conformance, but it must not steal an owner lease or rewrite domain business truth.

## Audit and tests

Every CI run performs the local cross-surface control-plane preflight before pytest:

```bash
python -m runtime.system_audit --repo-root . --trigger routine_change
python -m pytest -q
```

Audit depth is risk-tiered by `SYSTEM_MAINTENANCE_POLICY.json`: routine changes use core + impact-scoped checks; cross-cutting changes or explicit deep audits escalate to full control-plane/owner-metadata review, with synthetic fault injection when justified. Full owner business pipelines are not run by default.
