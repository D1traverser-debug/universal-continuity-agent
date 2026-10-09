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

Rules:
1. USER/default-visible tasks may participate in bare inheritance only while ACTIVE/WAITING/BLOCKED.
2. Infrastructure/test/fixture/eval/migration lanes are never default candidates.
3. Generic lanes do not duplicate a domain state machine.
4. New-chat takeover supersedes the old chat writer lease.
5. Checkpoint the latest execution truth, not a transcript.
