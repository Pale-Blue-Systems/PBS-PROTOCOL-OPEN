# PBS-SUITE-01
## Security Suite Registry for PBS-SEC-B-01

**Status:** Draft (proposed Optional Security Profile; not part of any PBS release)
**Version:** 0.1
**Applies to:** Implementations of PBS-SEC-B-01
**Related:** PBS-SEC-B-01, PBS-SEC-A-01, PBS-MUX-01, PBS-AUTH-01, PBS-HW-ID-01, PBS-CONFORMANCE-02

---

## 1. Purpose

PBS-SEC-B-01 Section 3 requires each `suite_id` to define the algorithm, key identifier format, nonce requirements, authentication data length and canonicalization rules. PBS v1.5.0 registers no suite, so two independent implementations cannot authenticate each other's messages from the specifications alone.

PBS-SUITE-01 proposes opening the registry with three authentication suites and one canonicalization shared by all of them. For suites `0x0001` and `0x0002`, the algorithm, Security frame parameters and canonicalization are those documented in PBS-ION-DEMO `docs/SPEC-DIGEST.md` Section 6 for its test suites `0xFF01` and `0xFF02`. Section 5 differs from the demo in two respects, stated there. Section 7 states what the demo does and does not show.

---

## 2. Registry

| suite_id | Name | Algorithm | auth_len | nonce_len |
|---|---|---|---:|---:|
| `0x0000` | Reserved | — | — | — |
| `0x0001` | PBS-HMAC-SHA256 | HMAC-SHA-256 (RFC 2104), 32-byte key, full tag | 32 | 0 |
| `0x0002` | PBS-ED25519 | Ed25519 (RFC 8032, pure) | 64 | 0 |
| `0x0003` | PBS-HMAC-SHA256-128 | HMAC-SHA-256, 32-byte key, tag truncated to the first 16 bytes | 16 | 0 |
| `0x0004`–`0xFEFF` | Unassigned | Assigned through PBS-GOV-01 Section 5 | | |
| `0xFF00`–`0xFFFF` | Test and experimental | Never used operationally | | |

- **PBS-SUITE-REQ-001:** An implementation claiming PBS-SEC-B-01 SHALL implement suite `0x0002` for verification. Suites `0x0001` and `0x0003` are optional.
- **PBS-SUITE-REQ-002:** A receiver SHALL reject a message whose `suite_id` it does not implement, or whose `auth_len` or `nonce_len` differs from the registered value.
- **PBS-SUITE-REQ-003:** A receiver SHALL NOT accept suites `0xFF00`–`0xFFFF` outside a test configuration.

Suite `0x0003` is proposed for links where PBS-CLP-01 segmentation is costly. It gives a 128-bit tag, which is within the truncation RFC 2104 Section 5 allows (no less than half the hash output), and is intended for telemetry and state. No implementation of it exists. A deployment SHOULD use `0x0002` for commands that cross an authority boundary, because a signature does not require the receiver to hold a secret that could forge commands.

---

## 3. Security Frame Fields

For all three suites:

- `version` is `0x01`.
- `flags` is `0x01`: bit 0 = authentication. Bits 1–7 are reserved, sent as zero, and a receiver rejects any other value. (PBS-SEC-B-01 Section 4 names the field without assigning bits; this assignment is proposed for that section.)
- `nonce_len` is `0`. HMAC and pure Ed25519 are deterministic.
- `key_id` is 1 to 255 bytes chosen by the authority that issued the key, and contains no secret (PBS-SEC-B-01 Section 7). A `key_id` of 16 bytes or fewer is RECOMMENDED. The key is looked up by (`suite_id`, `key_id`).
- All multi-byte fields are big-endian.

The Security frame value is `16 + key_id_len + auth_len` bytes.

- **PBS-SUITE-REQ-010:** The key that signs under suite `0x0002` is an operational key, not the PBS-HW-ID-01 tag key. The tag signs only challenges carrying the `PBS-HWID-v1-CHALLENGE` prefix (PBS-HW-ID-01 Section 5.5) and cannot sign `auth_input`.

PBS-HW-ID-01 defines no way to bind an operational key to a master device ID. Its binding certificate (Section 6) carries a Source ID, node number and operator, not a key, and PBS-HWID-REQ-091 only constrains where operational keys are stored. That binding is an open issue (Section 8).

---

## 4. Canonicalization

```text
auth_input = envelope[0 : 44 + Size − auth_len]
auth_data  = envelope[44 + Size − auth_len : 44 + Size]
```

`auth_input` is the 44 header bytes, CRC32 included, followed by the payload up to `auth_data`: the PBS-MUX-01 container header, every frame before the Security frame, and the Security frame's type, length and value through `nonce`.

- **PBS-SUITE-REQ-020:** A protected envelope SHALL carry a PBS-MUX-01 container with exactly one Security frame. It SHALL be the last frame, and no padding SHALL follow it.
- **PBS-SUITE-REQ-021:** A sender SHALL set every header field, including Size and CRC32, before computing `auth_data`.
- **PBS-SUITE-REQ-022:** A receiver SHALL verify `auth_data` over `auth_input` exactly as received, before acting on any frame.

This protects every header field and every frame, which includes everything PBS-SEC-B-01 Section 5 lists. PNT Context is always protected under these suites, whether or not the application marks it. Because relays forward the header and payload unmodified (PBS-ENV-01 Section 15, PBS-ROUTE-01 Section 12), no field needs to be excluded.

A node that forwards only some frames of a container (PBS-MUX-01 Section 8) invalidates `auth_data`. Such a node is acting as an application gateway and SHALL originate a new envelope under its own identity.

---

## 5. Replay Protection

- **PBS-SUITE-REQ-030:** A sender SHALL keep `security_sequence` per key, start it at 1, and increase it by 1 for each protected message. It SHALL NOT reuse a value under the same key.
- **PBS-SUITE-REQ-031:** A receiver SHALL keep, per (Source ID, `suite_id`, `key_id`), the highest accepted value `H` and the accepted values in `(H − 64, H]`. It accepts `s` when `s > H`, or when `H − 64 < s <= H` and `s` has not been accepted. It rejects `s = 0`, `s <= H − 64` and repeats.
- **PBS-SUITE-REQ-032:** Replay state SHALL be updated after authentication succeeds and SHALL survive restart for keys that remain valid.

The window size and acceptance rule are those of the PBS-ION-DEMO endpoints. Two things here are not: the demo keys replay state by (Source ID, `key_id`) without `suite_id`, and it does not address persistence across restart (PBS-SUITE-REQ-032). Whether a 64-value window is enough for the reordering of real store-and-forward paths has not been measured; a deployment MAY configure a larger one.

---

## 6. Overhead (Informative)

With an 8-byte `key_id`, the Security frame including its 3-byte MUX header is 91 bytes under `0x0002`, 59 under `0x0001` and 43 under `0x0003`.

---

## 7. Verification

The PBS-ION-DEMO report of 2026-10-07 records its two endpoints, one in Python and one in C, passing the authenticated-command scenario (S6, 8 of 8 criteria) and the cross-implementation scenario (S7, 9 of 9 criteria) using test suites `0xFF01` and `0xFF02`. That run was on a single host, with test keys derived from public labels, and with ION built without BPSec. It shows that two implementations written from one digest agree on the canonicalization of Section 4. It is not a security evaluation and not evidence about operational key handling.

The demo's test vectors (`docs/test-vectors.json`, section `sec_b`) do not carry over: `suite_id` is inside `auth_input`, so `auth_data` differs under the registered identifiers. New vectors are required before this document leaves Draft. None exist for `0x0003`.

---

## 8. Open Issues

1. Confidentiality (PBS-SECB-REQ-008): an AEAD suite needs a rule for which frames are encrypted and how the result is framed. Not defined here.
2. Whether `0x0003` should be limited by data class in normative text.
3. Post-quantum signature suites and their size on constrained links.
4. Key provisioning and revocation remain mission policy (PBS-SEC-B-01 Section 7). No PBS document binds an operational key to a master device ID or to an authority (Section 3); a common certificate format would be needed for that.
5. The suites and canonicalization have had no cryptographic review.

---

## 9. References

- RFC 2104, *HMAC: Keyed-Hashing for Message Authentication*.
- RFC 8032, *Edwards-Curve Digital Signature Algorithm (EdDSA)*.
- PBS-ION-DEMO, `docs/SPEC-DIGEST.md` and `REPORT.md`, <https://github.com/Pale-Blue-Systems/PBS-ION-DEMO>.
