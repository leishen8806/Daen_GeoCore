# DAEN Geo Core — Implementation Step 12: Selection Mutations

Step 12 provides two transport-neutral operations: `AddSelection` with
`selection.add` and `ReplaceSelection` with `selection.replace`. They accept
only explicit scopes with an established equality key and derive the exact
`SelectionSlotKey` from Place, fact purpose, scope type, and equality key.

Add requires an exact empty-slot `MutationBasisToken`; Replace requires the
current slot witness and names the prior immutable `SelectionRecordRef`.
Both operations create a new immutable SelectionRecord, validate one or more
exact supporting SourceAssertionRefs for same Place, standing-head presence,
and absence of `source_assertion.withdrawn`. Superseded support remains valid,
and selected values need not equal support values.

Recovery and reservation cover only the new SelectionRecordRef. Mapping
retries reuse the recorded reference, witness, and UTC timestamp. The
authoritative unit of work captures the slot and support read-set, inserts
support links, uses Add slot insertion or Replace slot CAS, writes audit and
committed replay binding, and maps commit unknown without hidden retry.

Selection operations do not mutate assertions or Places, do not append
assertion history, add no HTTP route, and require no schema migration.
