# CD-3 Gateway Error Contract

## Status

`CD-3 WP2 CONTRACT CANDIDATE / NOT R2 ACCEPTED`

This contract is separate from the frozen Phase-05 `API_ERROR_CONTRACT.md`.
Phase-05 HTTP status mappings do not automatically govern `/gateway/v1`.
These mappings are contract-candidate decisions and become accepted only after
R2.

## Common error envelope

Every gateway error response contains:

```json
{
  "requestId": "gateway-request-001",
  "error": {
    "code": "PROVIDER_TIMEOUT",
    "message": "The provider did not respond within the gateway timeout.",
    "retryable": true,
    "retryAfterSeconds": 5
  }
}
```

`requestId` is gateway-generated. Error payloads never include raw address,
coordinates, normalized query, provider payload, secrets, billing/account data,
or stack traces. Retry hints are returned only when safely known; the contract
does not promise automatic retries.

## Candidate taxonomy and status mapping

| HTTP | Code(s) | Meaning | Retryable guidance |
|---:|---|---|---|
| 400 | `INVALID_REQUEST` | Malformed or unparseable request structure | false |
| 422 | `INVALID_FIELD` | Structurally valid request with invalid field semantics, including coordinate range or purpose-code validation | false |
| 401 | `AUTHENTICATION_REQUIRED` | Authentication required; mechanism remains OPEN | false |
| 403 | `FORBIDDEN` | Authenticated caller is forbidden; policy remains OPEN | false |
| 429 | `RATE_LIMITED` | Gateway consumer-facing rate limit exceeded; topology remains OPEN | possibly true |
| 502 | `PROVIDER_RESPONSE_INVALID`, `PROVIDER_CONFIGURATION_FAILURE` | Provider response unusable or provider configuration rejection | false by default |
| 503 | `PROVIDER_UNAVAILABLE`, `PROVIDER_CAPACITY_UNAVAILABLE` | Provider unavailable, circuit open, or upstream capacity/quota unavailable | true |
| 504 | `PROVIDER_TIMEOUT` | Provider timeout | true |
| 500 | `INTERNAL_ERROR` | Unexpected gateway-internal failure | false by default |

429 is gateway/consumer rate limiting. 503 is upstream provider availability or
capacity/quota. Caller behavior must not depend on provider billing-account
details.

## Privacy and authority boundary

Examples use synthetic data only. Provider answers are transient and are not
persisted or promoted to Source Assertion, Current Representation, GeoID,
locating basis, Resolution Link, or Succession. Q2 and Q3 remain OPEN.
Telemetry follows the R1 engineering constraint and open P1/P2 gates. No error
message echoes request location or provider content.
