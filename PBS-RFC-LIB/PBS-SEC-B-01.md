# PBS-SEC-B-01
## Authenticated Mission Messaging

**Status:** Optional Security Profile
**Version:** 1.4
**Related:** PBS-ENV-01, PBS-AUTH-01, PBS-SVC-01, PBS-DTN-MAP-02

## 1. Purpose

PBS-SEC-B-01 defines authenticated mission messaging for PBS deployments requiring cryptographic source authentication, payload integrity, replay protection, authority validation, and optional confidentiality.

## 2. Security Properties

A PBS-SEC-B protected message provides:
- cryptographic integrity of protected PBS fields and application payload;
- source authentication;
- replay detection;
- authenticated priority and Service Intent;
- authenticated authority context when present;
- optional confidentiality.

## 3. Cryptographic Agility

Algorithms are selected by registered security suites. A suite identifier SHALL define the authentication or AEAD algorithm, key identifier format, nonce requirements, tag/signature length, and canonicalization rules.

Mission profiles SHALL select approved suites appropriate to mission assurance and cryptographic lifecycle requirements.

## 4. Security Frame

Security metadata is carried as PBS-MUX frame type `0x0A`.

| Field | Size | Meaning |
|---|---:|---|
| version | 1 | `0x01` |
| suite_id | 2 | Registered cryptographic suite |
| flags | 1 | Security services enabled |
| key_id_len | 1 | Key identifier length |
| nonce_len | 1 | Nonce length |
| auth_len | 2 | Authentication data length |
| security_sequence | 8 | Monotonic anti-replay sequence |
| key_id | variable | Key identifier |
| nonce | variable | Suite nonce |
| auth_data | variable | MAC, signature, or AEAD authentication data |

## 5. Protected Data

The security suite SHALL authenticate a canonical representation containing:
1. PBS envelope fields that express origin, priority, sequencing, timestamp, size, and lifetime;
2. Service Intent when present;
3. Authority Context when present;
4. PNT Context when the application marks PNT context as protected;
5. application payload.

Mutable network-layer fields are excluded according to the applicable binding profile.

## 6. Requirements

- **PBS-SECB-REQ-001:** A SEC-B receiver SHALL authenticate protected data before application acceptance.
- **PBS-SECB-REQ-002:** A SEC-B receiver SHALL reject a message whose authentication validation fails.
- **PBS-SECB-REQ-003:** A SEC-B receiver SHALL perform replay validation using security sequence, nonce state, transaction identity, or a suite-defined equivalent.
- **PBS-SECB-REQ-004:** Priority and Service Intent SHALL be authenticated.
- **PBS-SECB-REQ-005:** A protected command SHALL include authenticated PBS-AUTH-01 context.
- **PBS-SECB-REQ-006:** A receiver SHALL authorize a protected command before application execution.
- **PBS-SECB-REQ-007:** Security failures SHALL be auditable according to mission logging policy.
- **PBS-SECB-REQ-008:** Confidentiality profiles SHALL use authenticated encryption or an equivalently authenticated confidentiality construction defined by the selected suite.

## 7. Key Lifecycle

Mission security policy SHALL define trust anchors, provisioning, activation, rotation, revocation, compromise response, and end-of-life handling. `key_id` selects the applicable cryptographic material without embedding secret key material in PBS messages.

## 8. BPv7 / BPSec Binding

When PBS is carried over BPv7, BPSec may provide bundle-layer integrity and confidentiality according to the LunaNet/network security profile. PBS-SEC-B remains the end-to-end application security profile for PBS mission semantics. A deployment profile MAY bind PBS security identity to BPSec security-source identity and SHALL define the validation relationship explicitly.

## 9. Traceability

PBS-SEC-B-01 implements PBS-NASA-1503-001/002/003 and PBS-LNIS-008.
