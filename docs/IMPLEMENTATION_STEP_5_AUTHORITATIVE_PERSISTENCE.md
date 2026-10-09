# Step 5 Authoritative Persistence

Step 5 introduces the first PostgreSQL Core persistence structures for the
frozen identity, assertion, and representation contracts.

- Identity owns `identity_place`, append-oriented `identity_place_history`, and rebuildable `identity_place_head`.
- Assertions owns immutable `assertions_source_assertion`, append-oriented `assertions_history`, and rebuildable `assertions_standing_head`.
- Representation owns immutable `representation_selection_record`, immutable support links, and the exact-slot `representation_selection_slot_head`.
- Stable references are opaque application-supplied TEXT values. Value, scope, provenance, quality, and attribution payloads use opaque TEXT identifiers plus BYTEA payloads.
- Recorded times are explicit timezone-aware values; no database clock or generated identifiers are used.
- Same-owner foreign keys are used for history and head integrity. Cross-module Place and assertion FKs remain application commit invariants.
- Heads are rebuildable current structures; immutable material and history records remain authoritative.
- No cascade deletion, Domain mutation behavior, repositories, APIs, Access Point, Containment, Extent, idempotency, or evidence schema is included. Repositories remain Step 6 work.
