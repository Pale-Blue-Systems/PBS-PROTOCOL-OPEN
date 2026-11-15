# Draft Specifications

The documents listed here are proposals under PBS-GOV-01 Section 5.1, step 1. They are not part of PBS v1.5.0, are not listed in PBS-CONFORMANCE-01, and may change or be withdrawn. None of them changes the PBS-ENV-01 wire format or PBS Core semantics.

Together they extend PBS from scheduled space links to opportunistic, low-rate and terrestrial links.

| Draft | Title | Addresses |
|---|---|---|
| [PBS-PROX-01](PBS-PROX-01.md) | Proximity Sessions: Discovery, Authentication and Envelope Handover | No PBS specification defines how two nodes in range find, authenticate and hand over to each other |
| [PBS-TIME-01](PBS-TIME-01.md) | Open Clock Network: Time Distribution, Quality and Holdover | PBS-ENV-01 Section 15 requires a synchronized clock at every relay and names no source for it |
| [PBS-CLP-01](PBS-CLP-01.md) | Constrained Link Profile: Link Dispatch, Header Compression and Segmentation | A protected envelope exceeds one frame on low-rate radios; PBS-DTN-MAP-02 Section 2 refers to a segmentation profile that does not exist |
| [PBS-SUITE-01](PBS-SUITE-01.md) | Security Suite Registry for PBS-SEC-B-01 | PBS-SEC-B-01 defines `suite_id` and registers no values |
| [PBS-ADDR-02](PBS-ADDR-02.md) | Address Frame for PBS-MUX Containers | PBS-ADDR-01 Section 3.1 and PBS-MUX-01 Section 3 both claim the start of the payload |
| [PBS-MAP-21423-01](PBS-MAP-21423-01.md) | Mapping Profile: Mobile Robot Fleet Messages over PBS | Carrying ISO 21423 and VDA 5050 messages across intermittent links |

## Dependencies

```text
PBS-MAP-21423-01 ──> PBS-ADDR-02, PBS-SUITE-01, PBS-PROX-01
PBS-PROX-01 ──────> PBS-CLP-01 (dispatch, segmentation), PBS-TIME-01, PBS-HW-ID-01
PBS-TIME-01 ──────> PBS-PROX-01 (session), PBS-ENV-01 Section 15
PBS-CLP-01 ───────> PBS-ENV-01 (header), PBS-PROX-01 (context)
```

## Assignments Requested

| Registry | Value | For |
|---|---|---|
| PBS-MUX-01 frame type | `0x0B` | PBS-ADDR-02 Address frame |
| PBS-SEC-B-01 `suite_id` | `0x0001`, `0x0002`, `0x0003` | PBS-SUITE-01 |
| PBS-SEC-B-01 `flags` | bit 0 = authentication | PBS-SUITE-01 Section 3 |
| Link dispatch byte | `0x20`–`0x29`, `0x40`–`0xFF` | PBS-CLP-01, PBS-PROX-01, PBS-TIME-01 |

## What Has Been Checked

- The PBS-CLP-01 Section 4.4 vectors were produced by a script that rebuilds the PBS-ENV-01 Section 13.2 and 12.5 headers, confirms CRC32 `0x588721ED` and `0x8757080E`, compresses them, and confirms that decompression returns the identical 44 bytes. The same script confirms that a wrong context ID or time base fails CRC32 verification, and that segmentation round-trips with segments delivered out of order.
- Message sizes in PBS-PROX-01, PBS-TIME-01 and PBS-SUITE-01, the holdover table and the offset example in PBS-TIME-01 were computed by that script.
- The PBS-PROX-01 Section 6 challenge was exercised with Ed25519 keys: a signature over the initiator's challenge does not verify as the responder's.

## What Has Not

- No implementation of PBS-PROX-01, PBS-TIME-01 or PBS-CLP-01 has run on radio hardware. Timers, MTU values and default thresholds are engineering estimates.
- PBS-SUITE-01 has no test vectors under the registered suite identifiers.
- PBS-MAP-21423-01 has not been checked against the text of ISO 21423:2026.
- None of the drafts has had security review.
