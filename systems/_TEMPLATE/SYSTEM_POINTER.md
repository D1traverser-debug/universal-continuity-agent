# System Pointer Template

Use this only when a domain does not yet have a stronger dedicated owner/runtime.

Required fields:
- system_id
- domain
- owner
- system_home
- persistence_mode
- current authority

Rules:
1. Continuity stores routing and recovery identity, not full business logic.
2. Once a dedicated domain owner/runtime exists, move business rules there and keep this as a pointer/tombstone only.
3. A system pointer must never become a second state machine.
