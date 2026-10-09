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
- original video stream with frame/scene access;
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

## 2. Fast extraction order

For a user-provided media URL:

1. Resolve canonical identity: author, title, duration, date, stable media ID.
2. Look for the same author's public mirror of the exact media (for example WeChat -> YouTube) using title/author/duration/chapter alignment.
3. Prefer platform-native full transcript/captions when available.
4. Try direct audio/video stream extraction only when needed for missing evidence.
5. Read same-author canonical companion material for structure, links and technical details.
6. Use page metadata and third-party material only to fill clearly labeled gaps.

If the user prohibits a retrieval tool, do not use it.

## 3. Same-media identity check

A mirror may be treated as the same media only when multiple independent signals align, such as:
- exact or near-exact title;
- same author/channel;
- matching duration;
- matching chapter sequence/timestamps;
- same description/topic and publication window.

If identity is uncertain, label it as a related source rather than the same video.

## 4. Completion claims

Allowed claims:
- “完整读完音轨/字幕”: only when transcript/audio coverage spans the full media timeline.
- “完整看完视频画面”: only when the original video stream/scene sequence was actually reviewed across the full duration.
- “视觉抽样完成”: when representative chapter boundaries/scene changes were inspected but the full stream was not.

Forbidden shortcut:
- author article + description + partial transcript -> “完整看完原视频”.

## 5. Distillation pipeline — 取其精华，去其糟粕

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

## 6. Context-recovery principles currently accepted

These are durable architectural principles, not copied wording:
- Handoff should describe current execution truth, not reproduce chat history.
- Existing specs, plans, issues, commits, artifacts and checkpoints should be referenced, not duplicated into handoff text.
- Resume should progressively disclose context: metadata -> short handoff -> exact artifacts -> selective history only when needed.
- A large context window is capacity, not a reason to preload everything.
- Same task and same goal should keep one task identity; a genuinely new major goal becomes a separate child/new task rather than contaminating the existing task.
- Temporary side questions should not mutate durable task stage unless they change the task itself.
- Verification scope should match change/risk rather than always expanding to unrelated full-system checks.
- Reversible internal work should proceed autonomously; irreversible/external actions keep their approval boundary.

## 7. Explicit non-adoptions

Do NOT turn these media-specific claims into Universal Continuity invariants without separate evidence:
- a fixed “smart-zone” token threshold such as 150K;
- a universal model-switch/cache-cost rule;
- a hard-coded model-selection ladder;
- automatic installation of third-party browser/model bridges;
- broad testing rules unrelated to continuity changes.

Those may be useful heuristics in their own domains, but they are outside Continuity's core authority or may change with products/models.

## 8. Current reference case

Reference media: Jason Efficiency Lab / “4 个必须学习的 GPT-6 核心技巧：让你把 Codex 发挥到极致”.

Evidence state at adoption time:
- original WeChat page resolved;
- exact same-author YouTube mirror resolved by title/author/duration/topic/chapter alignment;
- full YouTube transcript obtained for the complete 20:14 timeline;
- same-author companion article fully read;
- full visual stream review not yet claimed.

This reference case exists to enforce evidence honesty, not to make the media itself an authority over the Agent.
