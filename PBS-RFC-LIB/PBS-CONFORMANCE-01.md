# PBS-CONFORMANCE-01
## Conformance, Interoperability, and Mandatory Baselines

**Status:** Core
**Version:** 1.3
**Errata:** 2026-10-06 (PBS v1.4.1): Sections 4.3 and 5.1 corrected to compute CRC32 over bytes 0x00–0x2B (44 bytes) with the CRC32 field zeroed, as PBS-ENV-01 Section 13 and PBS-SEC-A-01 Section 3 specify; Section 3 updated to cite PBS-PRIO-01 v1.4 (PBS-PRIO-01 v1.4 added no MUST requirements to v1.3; PBS-PRIO-01 Section 10 is corrected by its own v1.4.1 erratum), to list PBS-ADDR-01 and PBS-MUX-01 as optional, as the v1.3.0 changelog records, to list the seven optional specifications added in v1.4, and to use each specification's declared title, and to refer implementations claiming the v1.4 alignment profile to PBS-CONFORMANCE-02; Section 11.1 linked to the PBS_LINK SDK. Wire format unchanged.
**Applies to:** All PBS Core Implementations
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-SEC-A-01

---

## 1. Purpose

This document defines **conformance requirements** for implementations of the Pale Blue Systems (PBS) Open Standard.

Its purpose is to ensure that independently developed implementations can interoperate reliably across heterogeneous, multi-authority, and delay-tolerant environments, while preserving implementation freedom above the protocol layer.

PBS conformance focuses on:
- deterministic parsing and behavior
- interoperability across vendors and agencies
- minimum integrity and protocol correctness guarantees
- long-term stability of PBS Core semantics

---

## 2. Conformance Levels

PBS defines a single conformance level for PBS Core v1.x:

- **PBS Core Conformant Implementation**

An implementation is considered PBS Core conformant if it satisfies all **MUST** and **MUST NOT** requirements defined in the PBS Core specifications.

---

## 3. Mandatory Specifications

A PBS Core conformant implementation MUST correctly implement the following specifications:

| Specification | Description | Status |
|---------------|-------------|--------|
| PBS-ENV-01 v1.3 | Core Message Envelope (44-byte header) | Mandatory |
| PBS-PRIO-01 v1.4 | Priority Classification and Deterministic Handling | Mandatory |
| PBS-SEC-A-01 v1.3 | Integrity Verification and Security Boundaries (CRC32) | Mandatory |

### 3.1 Optional Specifications

Implementations MAY additionally support:

| Specification | Description | Status |
|---------------|-------------|--------|
| PBS-ADDR-01 | Addressing and Identification | Optional |
| PBS-MUX-01 | Payload Multiplexing and Semantic Framing | Optional |
| PBS-ROUTE-01 | Routing and Forwarding Semantics | Optional |
| PBS-DTN-MAP-01 | Mapping to Delay/Disruption Tolerant Networking (DTN) | Optional |
| PBS-POS-01 | Position and Presence Signaling | Optional |
| PBS-CAPS-01 | Capability Advertisement and Discovery | Optional |
| PBS-SVC-01 | Mission Service Intent | Optional |
| PBS-AUTH-01 | Authority and Scope Context | Optional |
| PBS-SEC-B-01 | Authenticated Mission Messaging | Optional |
| PBS-PNT-CTX-01 | Position, Navigation, and Timing Context | Optional |
| PBS-LNIS-01 | LunaNet Application Alignment Profile | Optional |
| PBS-DTN-MAP-02 | Mapping to BPv7 Delay/Disruption Tolerant Networking | Optional |
| PBS-QOS-MAP-01 | Mission Intent to Network Treatment Mapping | Optional |

Optional specifications MUST be implemented fully if claimed.

PBS-CONFORMANCE-02 defines the verification requirements for implementations claiming the PBS v1.4 NASA/LunaNet alignment profile.

---

## 4. Envelope Conformance Requirements

A conformant implementation MUST correctly handle the 44-byte PBS envelope:

### 4.1 Header Structure

Implementations MUST:
- Parse the fixed 44-byte header exactly as defined in PBS-ENV-01 v1.3
- Use big-endian byte order for all multi-byte fields
- Respect 4-byte alignment boundaries
- Preserve reserved fields as zero

### 4.2 Field Validation

Implementations MUST:
- Verify Magic byte equals `0x10`
- Verify Priority is in range 0–4 (reject 5–255)
- Verify CRC32 before processing
- Verify TTL has not expired

### 4.3 Encoding

Implementations MUST:
- Set Magic to `0x10`
- Set Priority to valid value (0–4)
- Set reserved bytes to `0x00`
- Calculate CRC32 over header bytes 0x00–0x2B (44 bytes) with the CRC32 field (0x28–0x2B) set to zero, and store it big-endian at 0x28 (PBS-ENV-01 Section 13.1)
- Encode Source ID as null-padded UTF-8

---

## 5. Integrity Baseline Requirements

### 5.1 Mandatory CRC32

PBS Core v1.3 conformance REQUIRES support for CRC32 integrity verification.

Implementations MUST:
- Calculate CRC32 using IEEE 802.3 polynomial (0xEDB88320, reflected)
- Compute CRC32 over header bytes 0x00–0x2B (44 bytes) with the CRC32 field (0x28–0x2B) set to zero
- Verify CRC32 before processing any envelope
- Discard envelopes failing CRC32 verification

### 5.2 CRC32 Recalculation

When modifying the TTL field, implementations MUST:
- Recalculate CRC32 after TTL modification
- Update the CRC32 field at offset 0x28

---

## 6. Priority Conformance

A conformant implementation MUST:

- Parse Priority field at offset 0x01
- Support all defined priority classes (0–4)
- Reject envelopes with reserved priority values (5–255)
- Preserve priority during forwarding
- Apply priority to scheduling decisions

The internal scheduling algorithm is implementation-defined and not subject to conformance testing.

---

## 7. Sequence Number Handling

A conformant implementation MUST:

- Parse Sequence field at offset 0x04 as u16 big-endian
- Increment sequence monotonically when sending
- Handle rollover from 65535 to 0 correctly

Implementations SHOULD:
- Track sequence numbers per Source ID for gap detection
- Report sequence gaps for diagnostics

---

## 8. Relay and Gateway Conformance

Relay and gateway implementations MUST:

- Verify CRC32 before forwarding
- Discard envelopes with invalid CRC32
- Decrement TTL appropriately during store-and-forward
- Recalculate CRC32 after TTL modification
- Preserve all header fields except TTL
- Discard envelopes with expired TTL

Relays MUST NOT:
- Modify Priority, Flags, Sequence, Source ID, Timestamp, or Size
- Forward envelopes with invalid structure

---

## 9. Error Handling Conformance

Implementations MUST:

- Discard envelopes with invalid Magic byte
- Discard envelopes failing CRC32 verification
- Discard envelopes with reserved Priority values
- Discard envelopes with expired TTL
- Continue processing subsequent envelopes
- Avoid persistent failure states from malformed input

---

## 10. Interoperability Expectations

PBS Core conformance implies that:

- Two independent conformant implementations can exchange envelopes correctly
- Messages are parsed, verified, and forwarded predictably
- Unknown payload content does not cause failures
- Priority semantics are consistent across implementations

Interoperability does not imply identical performance or routing behavior.

---

## 11. Testing and Validation

### 11.1 Reference Implementation

The PBS_LINK reference SDK (<https://github.com/Pale-Blue-Systems/PBS_LINK>, version 0.1.2) implements PBS-ENV-01 v1.3 in Python. The import package is `PBS_LINK` (`from PBS_LINK import PBSLink`).

- Envelope encoder and parser: `PBS_LINK/core.py`
- Unit tests (55): `TESTS/test_torture.py`

PBS-ENV-01 Section 13.2 provides a CRC32 test vector.

### 11.2 Conformance Testing

PBSF MAY publish:
- Reference test vectors
- Conformance test suites
- Interoperability scenarios

Use of such tooling is RECOMMENDED but not required for conformance claims unless explicitly stated.

---

## 12. Versioning and Compatibility

Rules:
- PBS Core v1.x semantics SHALL remain stable
- The 44-byte header structure SHALL remain unchanged for v1.x
- Backward-incompatible changes require a new major version
- Minor versions MAY add optional features without breaking conformance

Implementations MUST:
- Reject envelopes with unrecognized Magic byte
- Support the full v1.3 header structure

---

## 13. Conformance Claims

Implementations claiming PBS Core conformance SHOULD:

- Identify the supported PBS Core version (e.g., "PBS Core v1.3 Conformant")
- Identify supported optional specifications
- Identify any proprietary extensions
- Distinguish proprietary behavior from PBS Core behavior

False or misleading conformance claims undermine interoperability.

---

## 14. Summary

PBS-CONFORMANCE-01 v1.3 defines the **minimum, enforceable requirements** for interoperable implementations of the Pale Blue Systems Open Standard.

Key requirements:
- Fixed 44-byte header (PBS-ENV-01 v1.3)
- CRC32 integrity verification
- 5-level priority classification (0–4)
- Sequence-based gap detection
- Big-endian, 4-byte aligned encoding

This document defines the parsing, CRC32 verification and conformance-claim rules for PBS Core implementations.
