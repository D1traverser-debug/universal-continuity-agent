# Universal Continuity retirement record

The v3.7 Universal Continuity control plane was superseded by `D1traverser-debug/universal-agent-os` on 2026-10-14.

## Why it is retained

This repository contains historical audit evidence, requirements provenance, old task manifests, failure investigations and architecture research. Deleting it would remove useful provenance and could break historical references. It is therefore retained as read-only evidence rather than deleted.

## Cutover model

- UAOS is the only active cross-domain controller.
- Financial Writing, A-share, Novel and Video repositories remain business/domain providers.
- Each business repository exposes `continuity/UAOS_ADAPTER.json`.
- New tasks are UAOS-native.
- Existing unfinished tasks are imported one way when explicitly continued.
- Old universal leases, resume epochs, progress receipts and maintenance-controller state are not migrated as authority.
- After task import, continuity writes go to UAOS only.

This is a logical retirement. Repository archival/deletion is optional hygiene and is not required for correctness.
