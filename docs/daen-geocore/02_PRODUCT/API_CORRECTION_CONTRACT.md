# DAEN Geo Core — API Correction Contract

Correction is an explicit semantic mutation intent distinct from ordinary supersession.

A Correction creates a new Source Assertion, retains the old assertion, records supersession, and records explicit Correction history and attribution. Every material mutation remains attributable, non-destructive and exact-target. `CorrectionRecordRef` remains deferred.

Canonical mapping:

`POST /v1/source-assertions/{sourceAssertionRef}/actions/correct`

Ordinary supersession remains separate. Not every supersession asserts that the older value was wrong. No endpoint, schema or authorization mechanism is defined here.
