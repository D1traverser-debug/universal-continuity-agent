# Media Distillation Protocol

Status: ACTIVE
Purpose: learn from external video/audio/media without overstating what was actually reviewed, then distill only validated principles into Universal Continuity.

## 1. Evidence levels

Media-derived claims MUST preserve source level. Do not collapse different evidence types into one statement such as “I watched the whole video”.

### L1 — Original media evidence
Strongest evidence.

Examples:
- full platform transcript or official captions covering the complete timeline;
- original audio track or direct media stream;
- original video stream with full-duration visual/scene analysis;
- time-addressable transcript or frame evidence.

Sub-status MUST be separate:
- `AUDIO_TRANSCRIPT_FULL`
- `AUDIO_PARTIAL`
- `VISUAL_FULL_STREAM_REVIEW`
- `VISUAL_SCENE_SAMPLED`
- `VISUAL_UNAVAILABLE`

A complete transcript is sufficient to claim the spoken/audio content was fully reviewed. It is NOT sufficient to claim every visual element of the video was fully reviewed.

### L2 — Same-author canonical companion material
Examples:
- author's same-topic article;
- author's published knowledge note;
- author's slides or repository linked from the video.

Useful for cross-checking, citations and structured details, but MUST NOT be presented as the original video's verbatim content unless compared against L1 evidence.

### L3 — Platform metadata/page evidence
Examples:
- title, author, duration, upload date;
- chapter timestamps;
- description;
- page source/API metadata.

Good for identity resolution and navigation, not for reconstructing the full content.

### L4 — Third-party summaries/transcripts
Use only as corroboration or discovery hints. Never allow L4 to silently override L1/L2.

## 2. Platform-independent extraction order

For a user-provided media URL, the original platform is the default path. A mirror is an optimization, never a dependency.

1. Resolve canonical identity on the original platform: author, title, duration, date, stable media/page identity.
2. Inspect original-platform page state for transcript/captions, media metadata, embedded player state, media IDs and stream references.
3. Prefer an original-platform full transcript/caption track when available.
4. If transcript is absent, obtain the original audio/video stream when technically accessible and produce a full transcript from the audio.
5. When the user wants the video itself learned, review the full visual timeline or explicitly mark the result as visual sampling only.
6. Read same-author companion material for structure, links and technical detail, but keep it separate from original-media evidence.
7. An exact same-author mirror may be used to accelerate extraction only after identity is verified; it must not be required for completion.
8. Use third-party material only to fill clearly labeled gaps.

If the user prohibits a retrieval tool, do not use it.

## 3. WeChat-only path

WeChat/Weixin content is a first-class source. Do NOT require YouTube, Bilibili or another mirror.

For a WeChat Official Account article/video or Weixin video page:

1. Open and parse the original WeChat page first.
2. Resolve page/media identity and inspect the page's embedded state for player metadata, media IDs, caption/transcript references and signed media/stream references.
3. If the original page exposes transcript/captions, retrieve the complete timeline directly.
4. If no transcript is exposed but an original media stream is accessible, retrieve that media, extract the audio, transcribe the full duration, and analyze the video timeline.
5. If the stream URL is session-bound, use an authenticated/connected browser session to resolve and play the original media rather than immediately searching for a mirror.
6. If the original media can be played but cannot be exported, perform browser-based visual review and capture time-addressable evidence where the available browser tooling permits it; do not claim audio/full-visual completion beyond what was actually reviewed.
7. If WeChat blocks extraction behind login/session/anti-automation and no connected browser path can expose the media, the guaranteed fallback is the user-provided original video/audio file. This is the last resort, not the default request.
8. Only after the original-platform path is attempted may an exact same-author mirror be used as an accelerator. If no mirror exists, the WeChat-only path remains valid.

Completion labels for WeChat-only work remain identical to every other platform. There is no weaker standard merely because the source is WeChat.

## 4. Same-media identity check

A mirror may be treated as the same media only when multiple independent signals align, such as:
- exact or near-exact title;
- same author/channel;
- matching duration;
- matching chapter sequence/timestamps;
- same description/topic and publication window.

If identity is uncertain, label it as a related source rather than the same video.

A mirror is never promoted above the original source merely because it is easier to scrape.

## 5. Completion claims

Allowed claims:
- “完整读完音轨/字幕”: only when transcript/audio coverage spans the full media timeline.
- “完整看完视频画面”: only when the original/same-media video scene sequence was actually analyzed across the full duration.
- “视觉抽样完成”: when representative chapter boundaries/scene changes were inspected but the full stream was not.

Forbidden shortcut:
- author article + description + partial transcript -> “完整看完原视频”.

## 6. Distillation pipeline — 取其精华，去其糟粕

Do not copy external advice directly into the Agent.

For each candidate principle:
1. Extract the claim from the strongest available evidence.
2. Separate observation, heuristic and hard invariant.
3. Verify important OpenAI/product claims against current first-party documentation when the claim affects system behavior.
4. Check scope fit: Universal Continuity owns task continuity, not general model routing, pricing strategy or arbitrary coding preferences.
5. Reject brittle numeric heuristics as hard policy unless authoritative and stable.
6. Convert accepted ideas into a small contract/policy change.
7. Add regression tests or mechanical acceptance evidence when the change is executable.
8. Record what was rejected or kept as heuristic so future agents do not repeatedly rediscover the same distinction.

## 7. Context-recovery principles currently accepted

These are durable architectural principles, not copied wording:
- Handoff should describe current execution truth, not reproduce chat history.
- Existing specs, plans, issues, commits, artifacts and checkpoints should be referenced, not duplicated into handoff text.
- Resume should progressively disclose context: metadata -> short handoff -> exact artifacts -> selective history only when needed.
- A large context window is capacity, not a reason to preload everything.
- Same task and same goal should keep one task identity; a genuinely new major goal becomes a separate child/new task rather than contaminating the existing task.
- Temporary side questions should not mutate durable task stage unless they change the task itself.
- Verification scope should match change/risk rather than always expanding to unrelated full-system checks.
- Reversible internal work should proceed autonomously; irreversible/external actions keep their approval boundary.
- Routing/instruction surfaces should primarily define goals, context, constraints, completion/decision boundaries and where to load deeper knowledge, rather than micromanaging every reasoning step.

## 8. Explicit non-adoptions

Do NOT turn these media-specific claims into Universal Continuity invariants without separate evidence:
- a fixed “smart-zone” token threshold such as 150K;
- a fixed long-context pricing threshold;
- a universal model-switch/cache-cost rule;
- a hard-coded Astra/Sol/Luna model-selection ladder;
- automatic installation of third-party browser/model bridges;
- anecdotal account-ban claims as system policy;
- experimental Codex feature availability as a durable dependency;
- broad testing rules unrelated to continuity changes.

Those may be useful observations in their own domains, but they are outside Continuity's core authority, may change with products/models, or require separate verification.

## 9. Current reference case

Reference media: Jason Efficiency Lab / “4 个必须学习的 GPT-6 核心技巧：让你把 Codex 发挥到极致”.

Evidence state at adoption time:
- original WeChat page resolved;
- exact same-author YouTube mirror resolved by title/author/duration/topic/chapter alignment;
- full YouTube transcript obtained for the complete 20:14 timeline;
- same-author companion article fully read;
- full-duration visual scene analysis completed from 00:00 through 20:14 on the same YouTube media;
- visual walkthrough covered the actual displayed Obsidian canvas, source/document lists, benchmark/pricing tables, decision tree, handoff skill, experimental config/issue, model/source examples, ChatGPT-Codex integration diagrams, Prompt/AGENTS.md/Skills examples, agent/subagent/testing guidance, and final migration checklist;
- audio/transcript and visual evidence were compared with the same-author article; only Continuity-scope principles survived adoption.

Reference-case disposition:
- `AUDIO_TRANSCRIPT_FULL = true`
- `VISUAL_FULL_STREAM_REVIEW = true`
- `SAME_AUTHOR_COMPANION_FULL = true`
- `EVIDENCE_LEVELS_KEPT_DISTINCT = true`

Important: YouTube was an accelerator for this reference case, not a required dependency of the protocol. A future WeChat-only source must follow section 3 and can still reach L1 without any external mirror.

This reference case exists to enforce evidence honesty, not to make the media itself an authority over the Agent.
