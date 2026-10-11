# Skill Distillation 01 — `find-skills`

Date: 2026-10-11
Series: 2026 Global AI Skills Top10 distillation
Subject: `vercel-labs/skills` → `skills/find-skills/SKILL.md`
Disposition: **PARTIAL_ADOPTION_AS_METHOD__NO_NEW_AGENT__NO_NEW_ROOT_POLICY**

## 1. Source evidence

Primary source inspected:

- repository: `vercel-labs/skills`
- observed `main`: `13e4063a1cf913f5606d57d42ab83a86f5001e04`
- skill: `skills/find-skills/SKILL.md`
- skill blob: `a41bdd074bb587afd861332cf2f473f3154de4d7`
- executable search implementation: `src/find.ts`
- implementation blob: `9fe60ce81be21a65508299b469519af4b67155b2`
- regression surface: `src/find.test.ts`
- regression blob: `c11d9ec081cfa1724ea2d025e3004ab71c78a451`

External current listing observed on `skills.sh` on 2026-10-11:

- `find-skills`: approximately 3.8M installs
- repository: `vercel-labs/skills`
- repository stars displayed by skills.sh: approximately 33.6K

Popularity is treated as a discovery prior only, not quality proof.

## 2. What the Skill actually does

The Skill is not mainly a search command. Its useful behavior is a **capability acquisition funnel**:

1. Detect latent or explicit capability demand.
2. Decompose need into domain + concrete task.
3. Look at a curated/popular pool first.
4. Fall back to targeted search.
5. Optionally scope search by trusted owner/source.
6. Rank/shortlist candidates.
7. Verify before recommending.
8. Present provenance plus an executable acquisition path.
9. Install/use the selected capability.
10. If no adequate capability exists, fall back to general capability or create a new Skill.

The implementation adds several important operational details that the prose alone understates:

- results are sanitized before display;
- API results are sorted by install count;
- owner-scoped search is normalized and validated;
- non-interactive / agent execution does not enter the interactive selector path;
- API/search failure returns an empty result rather than fabricating a candidate;
- interactive discovery can hand directly into installation;
- private/public repository behavior is distinguished;
- the broader CLI supports use-without-install, project/global installation, update, remove and multiple source formats.

## 3. Reusable principles accepted

### A. Latent capability-gap detection

Do not wait for the user to literally say “find a plugin/Skill”. A request such as “can you do X?” or repeated struggle in a specialized domain can itself be a discovery trigger.

**Accepted form for our system:** when a specialized capability, external app, reusable workflow or established tool could materially improve execution, check whether an existing supported capability already solves it before designing another custom mechanism.

### B. Reuse-before-build

Search/reuse should happen before creating another permanent Agent, policy, runtime adapter or custom Skill.

This is stronger than merely “browse for inspiration”. It is an architecture-economy rule:

> existing fit-for-purpose capability → adapt/reuse → only then build.

### C. Progressive discovery

Use a widening funnel rather than a blind global search:

1. known installed/built-in capabilities;
2. trusted/curated sources;
3. owner-scoped search;
4. broader ecosystem search;
5. custom creation only if no adequate candidate survives verification.

This reduces search noise and supply-chain exposure.

### D. Discovery is not adoption

Search result rank, install count and repository popularity are **candidate signals**, not execution/quality evidence.

Before adoption, verify at least:

- source/provenance;
- scope fit;
- current maintenance/activity when material;
- requested permissions/tool surface;
- compatibility with the current execution environment;
- whether it duplicates an already-owned capability;
- failure containment/reversibility;
- evidence appropriate to the claim being made.

### E. Agent/non-interactive path must be deterministic

The actual CLI deliberately avoids interactive selector behavior when running inside an agent/non-TTY environment. This is a useful general rule: automation paths should produce structured deterministic candidates rather than depend on an interactive picker.

### F. No-result is a valid result

Failure to find a suitable capability must not be converted into a weak recommendation. The valid fallback sequence is:

- use existing general capability if sufficient;
- create a narrowly scoped custom capability only if repetition/value justifies it;
- otherwise continue without adding architecture.

## 4. What is rejected or narrowed

### 4.1 Fixed popularity thresholds are not global truth

The source Skill suggests preferring 1K+ installs and being skeptical below 100 installs / 100 GitHub stars.

**Rejected as a universal hard rule.**

Reason: popularity is domain- and age-dependent, can be gamed, penalizes excellent new/niche capabilities and says little about correctness for a specific task.

Retained only as a weak prior.

### 4.2 “Official source” is not sufficient trust proof

Vendor/official provenance is useful, but it does not eliminate the need to inspect capability scope, permissions, compatibility and evidence.

### 4.3 Search → global install is too aggressive as a default

The Skill's happy path ends in `-g -y` installation. For a control plane, the safer preference is:

1. inspect/use without install when possible;
2. project/local scope before global scope when practical;
3. global install only when cross-project persistence is actually desired.

The Vercel CLI itself supports `skills use` without installation, which is a better evaluation lane than the original Skill emphasizes.

### 4.4 A “find-skills Agent” would be architecture bloat here

Universal already has:

- a continuous-learning scout;
- plugin/connector discovery at product level;
- an authority-surface admission gate;
- an explicit recurring research lane for Agent Skills/capability discovery.

Therefore the correct distillation is a reusable method, not a new permanent supervisory Agent.

## 5. Mapping to current Universal Continuity

Current authority already says:

- learning may inspect Agent Skills and capability discovery;
- non-trivial changes require external/internal evidence scouting;
- new permanent Agents/root surfaces are rejected if an existing authority can own the responsibility;
- hot-path/startup bloat must be avoided.

`find-skills` therefore does **not** justify a new root policy or Agent.

The genuinely useful delta is the explicit **reuse-before-build capability acquisition funnel**. This is recorded here as provenance-bearing LEARNING_EVIDENCE and should be used as a candidate method during future capability/architecture decisions.

Promotion rule for later Top10 synthesis:

- if the same discovery/reuse pattern is independently reinforced by later Skills, promote the compact invariant into the existing learning/maintenance authority;
- if not, keep it as research evidence rather than enlarging the kernel.

## 6. Distilled method — Universal form

`NEED → DECOMPOSE → CHECK_EXISTING → CURATED_SEARCH → SCOPED_SEARCH → BROAD_SEARCH → VERIFY → TRY_REVERSIBLY → ADOPT_OR_REJECT → BUILD_ONLY_IF_NEEDED`

Verification must remain separate from popularity ranking.

A compact decision model:

- **DISCOVER**: Can an existing capability plausibly solve the need?
- **FILTER**: Is source/scope/compatibility acceptable?
- **VERIFY**: What evidence supports using it for this exact task?
- **TRIAL**: Can it be tested with low persistence / low blast radius?
- **ADOPT**: Does it outperform the current path without creating worse coupling?
- **CREATE**: Only when reuse fails and recurring value justifies a new capability.

## 7. Second-order challenge

Potential failure if adopted naively: the system could start searching for a Skill on every ordinary request, increasing latency and turning capability discovery into browsing theater.

Boundary:

- capability discovery is triggered only when a specialized/reusable capability could materially change execution quality, access or cost;
- it is not a mandatory web search on normal business turns;
- installed/built-in capabilities should be checked before external ecosystem search;
- no capability is installed merely because it ranks highly.

Evidence ceiling:

- source behavior and implementation have been inspected;
- reusable method has been distilled;
- no claim is made that adopting this method improves real task outcomes yet;
- no global popularity/security claim is inferred from the 3.8M install figure.

## 8. Series progress

Completed: **1 / 10**

1. `find-skills` — DONE / PARTIAL ADOPTION AS METHOD
2. `grill-me` — pending
3. `grill-with-docs` — pending
4. `improve-codebase-architecture` — pending
5. `agent-browser` — pending
6. `tdd` — pending
7. `setup-matt-pocock-skills` — pending
8. `frontend-design` — pending
9. `handoff` — pending
10. `triage` — pending
