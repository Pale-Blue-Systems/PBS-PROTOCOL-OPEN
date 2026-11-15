# PBS-SUITE-01
## Security Suite Registry for PBS-SEC-B-01

**Status:** Draft (proposed Optional Security Profile; not part of any PBS release)
**Version:** 0.1
**Applies to:** Implementations of PBS-SEC-B-01
**Related:** PBS-SEC-B-01, PBS-SEC-A-01, PBS-MUX-01, PBS-AUTH-01, PBS-HW-ID-01, PBS-CONFORMANCE-02

---

## 1. Purpose

PBS-SEC-B-01 Section 3 requires each `suite_id` to define the algorithm, key identifier format, nonce requirements, authentication data length and canonicalization rules. PBS v1.5.0 registers no suite, so two independent implementations cannot authenticate each other's messages from the specifications alone.

PBS-SUITE-01 opens the registry with three authentication suites and one canonicalization shared by all of them. Suites `0x0001` and `0x0002` adopt, without change, the choices that the two PBS-ION-DEMO endpoints (Python and C) already implement and agree on under the test identifiers `0xFF01` and `0xFF02`.

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

Suite `0x0003` exists for links where PBS-CLP-01 segmentation is costly. It gives a 128-bit tag and is intended for telemetry and state. A deployment SHOULD use `0x0002` for commands that cross an authority boundary, because a signature does not require the receiver to hold a secret that could forge commands.

---

## 3. Security Frame Fields

For all three suites:

- `version` is `0x01`.
- `flags` is `0x01`: bit 0 = authentication. Bits 1–7 are reserved, sent as zero, and a receiver rejects any other value. (PBS-SEC-B-01 Section 4 names the field without assigning bits; this assignment is proposed for that section.)
- `nonce_len` is `0`. HMAC and pure Ed25519 are deterministic.
- `key_id` is 1 to 255 bytes chosen by the authority that issued the key, and contains no secret (PBS-SEC-B-01 Section 7). A `key_id` of 16 bytes or fewer is RECOMMENDED. The key is looked up by (`suite_id`, `key_id`).
- All multi-byte fields are big-endian.

The Security frame value is `16 + key_id_len + auth_len` bytes.

- **PBS-SUITE-REQ-010:** The key that signs under suite `0x0002` is an operational key. The PBS-HW-ID-01 tag key signs only challenges with the `PBS-HWID-v1-CHALLENGE` prefix and cannot be used directly; an operational key MAY be bound to a master device ID by a certificate (PBS-HW-ID-01 Section 6, REQ-091).

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

A 64-value window tolerates the reordering that store-and-forward paths produce. A deployment with longer reordering MAY configure a larger window.

---

## 6. Overhead (Informative)

With an 8-byte `key_id`, the Security frame including its 3-byte MUX header is 91 bytes under `0x0002`, 59 under `0x0001` and 43 under `0x0003`.

---

## 7. Verification

The PBS-ION-DEMO test vectors (`docs/test-vectors.json`, section `sec_b`) apply to suites `0x0001` and `0x0002` with `suite_id` changed from `0xFF01` and `0xFF02`. Because `suite_id` is inside `auth_input`, the `auth_data` values differ and new vectors are required before this document leaves Draft. No vectors exist yet for `0x0003`.

---

## 8. Open Issues

1. Confidentiality (PBS-SECB-REQ-008): an AEAD suite needs a rule for which frames are encrypted and how the result is framed. Not defined here.
2. Whether `0x0003` should be limited by data class in normative text.
3. Post-quantum signature suites and their size on constrained links.
4. Key provisioning and revocation remain mission policy (PBS-SEC-B-01 Section 7); a common certificate format for operational keys would help interoperability.
