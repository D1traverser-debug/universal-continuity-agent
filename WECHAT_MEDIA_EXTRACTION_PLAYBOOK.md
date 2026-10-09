# WeChat Media Extraction Playbook

Status: ACTIVE
Purpose: maximize autonomous learning from public WeChat/Weixin media while minimizing dependence on user login, manual export, mirrors, or screen recording.

## 0. Default posture

For a user-provided public `weixin.qq.com` / `weixin.qq.com/sph/...` link, do not ask for WeChat login or file upload first.

Default ladder:

`public page -> embedded state -> direct media request -> public share resolver -> public playback/network capture -> exact same-author mirror -> authenticated playback -> user file upload`

The last two steps are fallbacks, not assumptions.

Only process content the user is entitled to access. Do not bypass paywalls, private-account restrictions, DRM, regional blocks, or other access controls.

## 1. Zero-login original-page pass

Try this before any mirror or login path:

1. Fetch the original share/article page.
2. Resolve title, author, duration, publication time, page identity and media identity.
3. Inspect HTML/embedded JavaScript/player state for:
   - `wxv_*` or other media identifiers;
   - `objectId` / `objectNonceId` when present;
   - player bootstrap data;
   - direct MP4 URLs;
   - HLS/M3U8 URLs;
   - separate video/audio requests;
   - caption/transcript endpoints;
   - signed CDN/media references.
4. Treat `blob:` URLs only as browser-local handles. Find the underlying network request instead.
5. If an original transcript/caption track exists, retrieve the complete timeline directly.

Success here requires no user login.

## 2. Direct media retrieval

When a public direct media request is discoverable:

- prefer direct MP4 or HLS over screen recording;
- preserve only the request context actually required (for example Referer/User-Agent); do not expose tokens/cookies in chat;
- distinguish single-file MP4, HLS, and split audio/video streams;
- remux/merge without transcoding when possible;
- validate duration, codecs, dimensions and audio presence;
- perform a full decode/readability check before calling the media complete when tooling allows.

Signed URLs may expire. Re-resolve them from the public page rather than treating an expired URL as permanent failure.

## 3. Public share-resolution path

For ordinary public `weixin.qq.com/sph/...` links, public share-link resolvers are a legitimate accelerator when the original page does not expose a convenient media URL.

Rules:

- prefer transparent/open-source implementations whose behavior can be audited;
- do not upload cookies, authenticated sessions, personal chat data or packet captures to third parties;
- a public share URL may be sent to a resolver only when doing so is consistent with the user's request and privacy expectations;
- verify the returned object is actual media, not an HTML landing page;
- verify output metadata against the original WeChat page before trusting it.

Public resolver failure does not imply login is required; continue down the ladder.

## 4. Public playback/network path

If the share page plays publicly but hides the source behind a browser `blob:` URL or dynamic player:

1. Start playback long enough for media requests to appear.
2. Inspect network/media requests for `video/*`, `audio/*`, MP4, M3U8 or media segments.
3. Recover the real request(s) behind the `blob:` handle.
4. Reuse only the minimum non-sensitive headers needed for the public playback request.
5. Download, merge/remux and validate the result.

A public browser playback session is still a no-login path if no WeChat account authentication is involved.

## 5. Transport-obfuscated/encrypted media

Some WeChat Channels implementations expose a media URL together with playback metadata such as a `decode_key` in the authorized/public playback response.

If the media is public/authorized and the playback response itself provides all material required to reconstruct the playable file, that transport representation may be normalized locally for analysis.

Do not use this as a way to bypass DRM, paywalls, private-account restrictions or missing authorization. If access depends on circumventing a technical access control rather than reconstructing already-authorized playback, stop.

## 6. Same-author mirror

A YouTube/Bilibili/other mirror is optional acceleration, never a dependency.

Use only after verifying multiple identity signals such as author, title, duration, chapter order, description and publication window.

A mirror can provide easier transcript/media access, but the original WeChat page remains the identity anchor.

## 7. Authenticated playback fallback

Only reach this stage when the content is genuinely session-bound and prior zero-login paths failed.

If a connected browser already has an authorized playback session, use that session to inspect the media request without asking the user to copy cookies or credentials.

Do not ask the user to log in merely because it is easier than trying the zero-login ladder.

## 8. User-file fallback

Ask for an uploaded original video/audio file only when all accessible page, public resolver, public playback, mirror and available authorized-session paths fail.

This is the guaranteed final fallback for analysis, not the default workflow.

## 9. Learning pipeline after media acquisition

Once media is available:

1. Validate media/container completeness.
2. Extract or obtain the full audio track.
3. Produce or retrieve a full transcript with timeline coverage.
4. Review the full visual timeline when the user asks to learn the video itself; otherwise mark visual sampling explicitly.
5. Cross-check same-author companion material separately.
6. Distill observations into principles; separate facts, heuristics and invariants.
7. Keep only principles relevant to the target Agent/system.
8. Record rejected/out-of-scope claims so they are not repeatedly rediscovered.

## 10. Evidence labels

Always report separately:

- `ORIGINAL_PAGE_RESOLVED`
- `DIRECT_MEDIA_RESOLVED`
- `AUDIO_TRANSCRIPT_FULL` / `AUDIO_PARTIAL`
- `VISUAL_FULL_STREAM_REVIEW` / `VISUAL_SCENE_SAMPLED` / `VISUAL_UNAVAILABLE`
- `SAME_AUTHOR_COMPANION_FULL` when applicable
- `MIRROR_USED_AS_ACCELERATOR` when applicable
- `LOGIN_REQUIRED` only after earlier no-login tiers are exhausted

Never collapse these into a vague statement like “完整看过” when only some layers are complete.

## 11. Engineering references distilled into this playbook

Public implementations reviewed while hardening this workflow include:

- `shaom/wechat-channels-download-skill`: recover real media requests behind browser playback/blob handles; handle MP4/HLS/split streams; verify with media tooling.
- `joeseesun/qiaomu-wx-video`: `weixin.qq.com/sph/...` workflow with a no-install/public-share-resolution path before local authenticated capture.
- `jianminggan/wechat-video-subtitle`: download/transcription workflow and evidence that some replay paths need local playback state, while ordinary video extraction/transcription can be automated.
- `Evil0ctal/WeChat-Channels-Video-File-Decryption` and related analyses: documents current Channels transport-obfuscation/decode-key mechanics; use only within the authorized/public-playback boundary described above.

These projects are research references, not runtime dependencies. The playbook must continue working conceptually if any one repository or service disappears.
