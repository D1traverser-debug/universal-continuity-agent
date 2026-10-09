# Generic Continuity Lane Template

Use only when no stronger domain owner exists.

Required metadata:
- task_id
- task_class
- domain
- title
- status
- resume_eligible
- resume_visibility
- recovery_owner
- updated_at
- current_stage
- next_action
- checkpoint_ref
- contract_version
- manifest_ref
- resume_epoch
- active_lease

For persisted USER tasks also include:
- display_name_zh

Checkpoint/HANDOFF should contain only current execution truth needed to resume safely:
- current_stage
- exact next_action
- blockers/waiting state
- authority/contract context
- stable artifact refs needed for the next action
- recent material decisions only when they are not already authoritative elsewhere

Rules:
1. USER/default-visible tasks may participate in bare inheritance only while ACTIVE/WAITING/BLOCKED.
2. Infrastructure/test/fixture/eval/migration lanes are never default candidates.
3. Generic lanes do not duplicate a domain state machine.
4. New-chat takeover supersedes the old chat writer lease.
5. Checkpoint the latest execution truth, not a transcript.
6. Reference existing specs/plans/issues/commits/diffs/artifacts instead of copying them into HANDOFF.
7. Resume progressively: metadata -> HANDOFF -> exact artifact refs -> selective history; old chat transcript is last resort.
8. Temporary side questions do not mutate durable stage unless they materially change the task.
9. A materially different major goal becomes a child/new task instead of contaminating the existing task.
10. Do not use a fixed token threshold as a hard context-health rule.
