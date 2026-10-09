# Migration Checkpoint

- Migration: `continuity-library-to-github-20261009`
- Status: `IN_PROGRESS`
- Source: ChatGPT Library `/00_跨对话继承系统/` plus `/00_跨对话继承_唯一入口.md`
- Destination: `D1traverser-debug/universal-continuity-agent`
- Engineering authority after cutover: GitHub `main`
- ChatGPT Library after cutover: retain only a thin bootstrap pointer to this repository
- Business domain state remains with its own owner/runtime/repository; Continuity stores routing metadata and pointers only.

## Safety gate
Do not delete the full Library continuity tree until the GitHub import, cold-start harness, task/system manifests, and bootstrap pointer are verified from the repository copy.

## Next action
Materialize the complete Library continuity tree, import it into this repository, normalize repo-relative paths, run the harness/tests, then cut over authority and clean the Library copy.