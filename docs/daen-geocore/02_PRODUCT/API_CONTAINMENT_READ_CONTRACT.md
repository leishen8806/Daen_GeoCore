# DAEN Geo Core — API Containment Read Contract

Containment is the minimal directional relation `Place contains Place`. A caller-relative read can expose requested PlaceRef, related PlaceRef, `contains` or `contained-by` perspective, and Provenance. These perspectives do not create two Domain relationship types.

Canonical read:

`GET /v1/places/{placeRef}/containment`

No current/historical state, validity interval, transitivity, ancestor/descendant traversal, inheritance, parent policy, taxonomy, ContainmentRecordRef or write mutation is frozen.
