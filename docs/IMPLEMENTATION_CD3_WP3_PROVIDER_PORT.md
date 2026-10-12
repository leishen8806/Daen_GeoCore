# DAEN Geo Core — CD-3 WP3 Provider-Neutral Port

## Status

`CD-3 WP3 PROVIDER PORT = IMPLEMENTATION CANDIDATE / R2 NOT YET PASSED`

This package defines only provider-neutral query, result, and failure values plus
one `GeocodingProvider` protocol. It contains no transport, application,
provider SDK, persistence, cache, authentication, rate limiting, or identity
semantics.

## Contract

- `GeoLocation` validates finite latitude/longitude bounds.
- `GeocodeQuery` and `ReverseGeocodeQuery` contain only provider query inputs.
- `consumerPurposeCode` and gateway `requestId` deliberately do not enter these
  provider queries.
- `ProviderLookup` with an empty result tuple is a valid provider-level
  zero-results success.
- `ExternalProviderReference` is an external transient value, not a DAEN
  reference or identity authority.
- `GeocodingProviderFailureKind` contains only upstream conditions: timeout,
  unavailable, capacity unavailable, configuration failure, and invalid
  response.
- `PortSuccess(ProviderLookup)` is successful lookup, including zero results.
  `PortSuccess(GeocodingProviderFailure)` represents a recognized upstream
  condition. `PortError` remains an unexpected technical port failure.

The single protocol exposes only `geocode` and `reverse_geocode`.

## WP2 alignment

Python values use snake_case equivalents of the WP2 fields:
`provider_reference`, `formatted_address`, `name`, `location`,
`precision_class`, `partial_match`, and `display_requirements`.

The WP2 R2 notes remain open and are not changed here:

- R2-N1: `ZERO_RESULTS` is documented as `results=[]`, but the OpenAPI schema
  does not structurally enforce that relationship.
- R2-N2: the common error schema exposes the full error-code enum to each HTTP
  error response; the Markdown mapping is stricter.

Q2 and Q3 remain OPEN. S1 and T1 remain OPEN. Phase 06F remains NOT AUTHORIZED.
