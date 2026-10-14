# Universal Continuity — RETIRED

Status: `RETIRED_READ_ONLY`
Successor: `D1traverser-debug/universal-agent-os@main`
Successor entrypoint: `ENTRYPOINT.md`
Retired on: 2026-10-14

This repository is no longer an active control plane.

## Required behavior

- Do not create new tasks here.
- Do not acquire or refresh leases/resume_epoch ownership here.
- Do not create new maintenance-controller runs here.
- Do not use `OWNER_REGISTRY.json` or the v3.7 protocol as current routing authority.
- Do not write new business continuity checkpoints here.

For all new work, continuation, requirements, multi-Agent coordination and system maintenance, bootstrap:

`D1traverser-debug/universal-agent-os@main:ENTRYPOINT.md`

Historical files in this repository remain readable as audit/provenance evidence and migration input only. The four business Agent repositories remain available as domain code/rule/artifact providers, but their cross-domain control plane is UAOS.

If a historical task still points here, follow the UAOS Agent Registry and task cutover rules. Legacy v3.7 lease/progress-receipt semantics are compatibility evidence, not active authority.
