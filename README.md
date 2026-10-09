# Universal Continuity Agent

Cross-chat task continuity infrastructure for the user.

## Authority

- **GitHub `main`** is the engineering source of truth for contracts, resolver/harness, templates, tests, and continuity manifests when stored here.
- **Domain owners** remain authoritative for business logic and stronger runtime checkpoints.
- **ChatGPT Library** retains only a thin bootstrap pointer after migration.
- Registries are rebuildable caches; per-task/per-system owner state is authoritative.

Start with [`ENTRYPOINT.md`](ENTRYPOINT.md), then [`PROTOCOL.md`](PROTOCOL.md).

## Repository boundary

This repository owns only universal continuity infrastructure. Financial Writing, A-share, Video Growth and other business logic remain in their own agents/repos. Live user task state belongs to the corresponding private domain owner or another private durable store; it must not be exposed merely to centralize continuity.

## Tests

```bash
python -m pytest -q
```
