# WeChat Media Extraction — Live Validation

Status: ACTIVE EVIDENCE
Validated: 2026-10-09
Reference public share: `https://weixin.qq.com/sph/ASGIjLXVta`

## What was actually tested

This is a live test of the original WeChat share URL, not a mirror-only inference.

### PASS — anonymous original page
The public share page resolves without WeChat login to:
`https://channels.weixin.qq.com/finder-preview/pages/sph?id=ASGIjLXVta`

Anonymous browser state exposes the author/description/date/cover and loads the Finder Preview application.

### PASS — real WeChat feed request identified
The live page makes:
`POST /finder-preview/api/feed/get_feed_info`

Observed request body for the first-stage lookup:
```json
{"baseReq":{"generalToken":""},"shortUri":"ASGIjLXVta"}
```

The response succeeds and contains author/feed metadata plus `sceneInfo.dynamicExportId`.

### IMPORTANT — public metadata is not the same as public media
For this validation case the anonymous first-stage response does **not** expose `feedInfo.mediaList`, `h264VideoInfo.videoUrl`, `h265VideoInfo.videoUrl`, or a direct playable MP4/HLS source. It exposes metadata/cover only.

A second live call was tested with the returned `dynamicExportId` and empty anonymous `generalToken`:
```json
{"baseReq":{"generalToken":""},"exportId":"<dynamicExportId>"}
```

The endpoint returned an application-level playback message equivalent to `此内容暂时无法播放` and still did not disclose the media stream.

Therefore the playbook must not assume:
`public share page == anonymous direct media URL`.

### Public resolver status observed during the same test
The formerly open `sph.litao.workers.dev/api/fetch_video_profile` endpoint returned HTTP 401 in this test. Current upstream documentation also describes authenticated/private deployment for that parser path. A historical claim that this particular public worker is always a no-login parser must not be treated as a durable invariant.

## Evidence interpretation

For this exact WeChat link:
- `ORIGINAL_PAGE_RESOLVED = true`
- `ANONYMOUS_FEED_METADATA_RESOLVED = true`
- `ANONYMOUS_DYNAMIC_EXPORT_ID_RESOLVED = true`
- `DIRECT_MEDIA_RESOLVED_FROM_WECHAT_ANONYMOUS_PATH = false`
- `PUBLIC_PARSER_ENDPOINT_AVAILABLE_ANONYMOUSLY = false` at validation time
- `LOGIN_REQUIRED = NOT_YET_PROVEN_AS_UNIVERSAL_REQUIREMENT`

The failure of this anonymous direct-media path does not imply every WeChat Channels link requires login. Continue through other public/authorized tiers when available. Conversely, do not claim a direct WeChat video download unless a real media URL/file has actually been obtained and validated.

## Reference-case learning completion

The media-learning task for this content was still completed through an exact same-author same-media mirror after identity verification. That mirror provided the complete audio transcript and full-duration visual stream review. This does **not** retroactively convert the WeChat anonymous extraction result into a direct-media success.

## Durable lesson

Separate three states that were previously easy to conflate:
1. public page accessible;
2. feed metadata accessible;
3. original media stream accessible.

Only state 3 permits `DIRECT_MEDIA_RESOLVED = true`.
