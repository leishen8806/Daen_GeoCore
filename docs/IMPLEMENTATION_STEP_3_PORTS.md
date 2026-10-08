# Step 3 port note

Step 3 defines only provider-neutral Protocol contracts and typed port results for persistence boundaries, evidence support, recovery readiness, clock, policy, and observability. It does not implement adapters, storage, Domain behavior, mutation algorithms, or public APIs.

## Final Step 3 Contract Correction

- Commit knowledge is exactly three-state: COMMITTED, DEFINITELY_NOT_COMMITTED, or OUTCOME_UNKNOWN. A technical abort is a subordinate PortFailure reason for DEFINITELY_NOT_COMMITTED; semantic conflicts remain outside CommitPort.
- Technical failures are separately classified as retryable transaction abort, transient unavailable, or non-retryable technical failure.
- Evidence records use typed stable references and separate permanent reservation evidence from request/reference recovery mappings.
- Request mappings carry opaque client identity, request identity, intent fingerprint, operation key, typed references, and immutable replay metadata.
- EvidenceStore is key-addressed and distinguishes created, same existing, conflicting existing, found, absent, and unavailable; unavailable never becomes absent.
- RecoveryGate exposes READY, RECOVERY_REQUIRED, RECONCILING, and BLOCKED observations with derived serving/reference-issuance safety; READY requires an opaque RecoveryIncarnation.
- Clock is UTC-aware recorded-time metadata only; FakeClock rejects naive or non-UTC datetimes.
