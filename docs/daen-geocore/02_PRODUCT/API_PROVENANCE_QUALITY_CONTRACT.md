# DAEN Geo Core — Phase 05D Provenance and Quality Contract

Every material mutation is attributable. Mutation provenance can express who/what recorded the act, context/time, affected references, evidence/reason where applicable, and resulting refs/history. No Actor resource or authorization schema is defined.

Quality applies to facts: Source Assertions, selected facts, and Access Point attributable facts when such writes are later defined. Merge, split, closure and withdrawal actions do not receive Quality merely because they are mutations. No mutation-confidence score is defined.

Originating source Provenance and mutation Provenance remain distinct. Existing fact-level Provenance/Quality rules from Phase 05C remain in force.

## M1–M18 invariants

M1 non-destructive history; M2 no reassignment/reuse/aliasing; M3 correction creates a new assertion; M4 same-subject supersession preserves subject and fact/purpose; M5 replacement creates a new SelectionRecordRef; M6 replacement requires same Place/fact-purpose/explicit scope; M7 merge does not rewrite retired GeoID references; M8 true-division children do not inherit parent GeoID; M9 T1 preserves resolution and marks not-valid-for-new-use; M10 T2 does not automatically alter Place or Current Representation; M11 every material mutation is attributable; M12 newer conflicts are not silently overwritten; M13 idempotent retry has no duplicate effects; M14 logical multi-record mutation is coherent; M15 no ordinary destructive history deletion; M16 exact references only; M17 supersession is explicit; M18 deferred operations are never approximated by another mutation.

The 25 Phase 05D coherence cases are supported subject to the Human Freeze, with AP mutations correctly deferred and no generic Place-create case authorized.
