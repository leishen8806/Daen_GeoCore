# DAEN Geo Core — Phase 05B Identifier and Reference Contract

## Status

`PHASE 05B IDENTIFIER AND RESOLUTION CONTRACT = HUMAN FROZEN`

## GeoID

GeoID is for Place only. It is DAEN-controlled, stable and immutable for the Place, non-reassignable, non-reusable, provider-independent, opaque, and resolvable after merge, split, closure and T1 withdrawal. Equality is defined only within the typed GeoID contract. UUID/ULID/integer choice, prefix, length, checksum, country/shard encoding and canonical textual normalization remain deferred.

## Typed references

- `PlaceRef = GeoID`
- `SourceAssertionRef`
- `AccessPointRef`
- `SelectionRecordRef`

`SelectionRecordRef` is a stable opaque history reference for one material Current DAEN Representation selection-history record. It is not a GeoID, not a top-level resource and not a new Domain identity. Standalone retrieval remains deferred. ResolutionRecordRef, CorrectionRecordRef and ContainmentRecordRef remain deferred.

## Logical namespaces

Each reference type has a logical namespace. Logical namespace is not a serialized prefix. Consumers must not inspect token structure to infer reference type.

## Stability and no-aliasing

Stable references continue to denote their originally referenced resource or record. SourceAssertionRef, SelectionRecordRef and AccessPointRef are non-reassigned and non-reused. Superseded assertions and selections remain inspectable as themselves. An AccessPointRef has record-level stability; real-world AP continuity remains TBD. Authorized data removal may affect detail availability but never transfers a reference to another object.

Retained relationship/history records preserve the references originally recorded. Future policy may create an explicit new or superseding relation, but may not silently rewrite an old relation to another identity.

## Identity matrix

| Identifier/reference | Domain identity | API addressability |
|---|---|---|
| GeoID / PlaceRef | Place identity | exact Place resource |
| SourceAssertionRef | no new Domain identity | Source Assertion resource |
| AccessPointRef | no new Domain identity | Access Point resource |
| SelectionRecordRef | no new Domain identity | history reference; standalone retrieval deferred |
| Provider reference | external assertion/provenance value | not a DAEN reference |

No reference format is frozen in 05B.
