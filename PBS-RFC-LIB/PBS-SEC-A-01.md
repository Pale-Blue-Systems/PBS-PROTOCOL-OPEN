# PBS-SEC-A-01
## Integrity Verification and Security Boundaries

**Status:** Core
**Version:** 1.5
**Changes:** <release date> (PBS v1.5.0): Section 5 requires relays and gateways to preserve every header field, including TTL and CRC32; Section 5.1 replaces CRC32 recalculation after a TTL decrement with end-to-end verification of the originator's CRC32 (PBS-ENV-01 Sections 12.3 and 15). The PBS v1.4.1 errata to Sections 4.1, 5.1, 8 and 11 are incorporated (PBS-PROTOCOL-CHANGELOG.md, [1.4.1]). Wire format unchanged.
**Applies to:** All PBS Core Messages
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-CONFORMANCE-01, PBS-SEC-B-01

---

## 1. Purpose

This document defines the **integrity verification and security model** for the Pale Blue Systems (PBS) Open Standard.

PBS-SEC-A-01 specifies how PBS envelopes are protected against transmission errors and corruption, and establishes the framework for optional cryptographic authentication.

---

## 2. Security Objectives

PBS Security Model is designed to achieve the following objectives:

- **Header integrity:** Detect transmission errors, bit-flips, and corruption in the envelope header.
- **Routing safety:** Validate header integrity before trusting routing instructions.
- **Radiation resilience:** Detect single-event upsets (SEUs) and cosmic ray bit-flips.
- **Low computational overhead:** Support resource-constrained and low-power embedded systems.
- **Extensibility:** Allow optional cryptographic authentication for higher-security applications.

---

## 3. Integrity Model: CRC32

PBS-ENV-01 v1.3 provides mandatory integrity verification using CRC32 checksum.

### 3.1 CRC32 Coverage

The `CRC32` field at offset `0x28` provides integrity verification for the header.

| Coverage | Bytes | Description |
|----------|-------|-------------|
| CRC32 Input | 0x00–0x2B | All 44 bytes (with CRC32 field set to zero) |
| CRC32 Field | 0x28–0x2B | Checksum value |

### 3.2 CRC32 Algorithm

Rules:
- CRC32 uses the standard IEEE 802.3 polynomial (0xEDB88320, reflected).
- CRC32 is computed over header bytes 0x00–0x2B (44 bytes) with the CRC32 field set to zero.
- Result is stored as a 32-bit unsigned integer, big-endian, at 0x28–0x2B.
- The CRC32 does not cover the payload (Section 10).

### 3.3 CRC32 Limitations

CRC32 provides:
- Detection of transmission errors (noise, interference)
- Detection of bit-flips (radiation, SEUs)
- Validation of header structure before processing

CRC32 does NOT provide:
- Cryptographic authentication (source verification)
- Tamper detection (malicious modification)
- Payload integrity (header-only coverage)

---

## 4. Integrity Processing

Receivers MUST verify CRC32 before processing any envelope.

### 4.1 Verification Steps

The receiver procedure is identical to PBS-ENV-01 Section 13.1:

1. Extract CRC32 value from bytes 0x28–0x2B
2. Set bytes 0x28–0x2B to `0x00000000`
3. Compute CRC32 over all 44 bytes
4. Compare computed value with extracted value
5. Discard envelope if values do not match

### 4.2 Failure Handling

Rules:
- Envelopes failing CRC32 verification MUST be discarded.
- Implementations SHOULD log or count CRC failures for diagnostics.
- CRC failures MUST NOT cause persistent failure states.
- Processing MUST continue with subsequent envelopes.

---

## 5. Relay and Gateway Behavior

Relays and gateways MUST maintain header integrity across forwarding.

Rules:
- Relays MUST verify CRC32 before forwarding.
- Relays MUST NOT forward envelopes with invalid CRC32.
- All header fields, including TTL and CRC32, MUST be preserved unmodified (PBS-ENV-01 Sections 12.3 and 15).

### 5.1 End-to-End CRC32

Relays and gateways do not recalculate CRC32. The originator computes CRC32 once (PBS-ENV-01 Section 13.1), and the value remains valid at every hop. A relay verifies it with the Section 4.1 procedure applied to a copy of the header, and forwards the 44 header bytes as received. Header corruption after origination, including corruption in a relay's storage after that relay verified the CRC32, is therefore subject to CRC32 verification at the next relay or receiver, within the limits stated in Section 3.3.

---

## 6. Sequence-Based Gap Detection

PBS provides packet-loss detection through sequence numbers.

### 6.1 Sequence Tracking

The `Sequence` field at offset 0x04 enables receivers to detect lost packets.

Rules:
- Sequence numbers increase monotonically per source device.
- Sequence numbers roll over from 65535 to 0.
- Receivers SHOULD track sequence numbers per Source ID.
- Gaps in sequence indicate lost packets.

### 6.2 Gap Reporting

Receivers MAY report sequence gaps to enable retransmission or diagnostics:
- "Packets #502–#505 from Rover-Alpha were lost"
- Gap detection is informational; PBS does not mandate retransmission.

---

## 7. Security Extension: Cryptographic Authentication

For applications requiring cryptographic security, implementations MAY extend PBS with authentication.

### 7.1 Extension Approaches

Cryptographic authentication MAY be implemented via:

1. **Payload-level authentication:** Authenticated payload containing MAC/signature
2. **Gateway authentication:** Gateway adds cryptographic wrapper for transit
3. **Transport-layer security:** TLS/DTLS on underlying transport

### 7.2 Recommended Algorithm

For implementations requiring cryptographic authentication:
- HMAC-SHA-256 is RECOMMENDED for symmetric authentication.
- Ed25519 is RECOMMENDED for asymmetric authentication.
- Authentication SHOULD cover: Magic, Priority, Flags, Sequence, Source ID, Timestamp, Size, TTL, and Payload.

### 7.3 Key Management

Cryptographic key management is outside the scope of this specification. Implementations requiring authentication SHOULD:
- Define key distribution mechanisms appropriate to deployment.
- Establish trust anchors per deployment scope.
- Document key rotation and revocation procedures.

---

## 8. Threat Model

PBS-SEC-A-01 addresses the following threats:

| Threat | Mitigation | Coverage |
|--------|------------|----------|
| Transmission errors | CRC32 | Header |
| Bit-flips (radiation) | CRC32 | Header |
| Packet loss | Sequence numbers | Detection only |
| Malicious modification | Extension required | Not baseline |
| Source spoofing | Extension required | Not baseline |
| Replay attacks | Extension required | Not baseline |

For deployments requiring protection against malicious actors, cryptographic authentication (Section 7 or PBS-SEC-B-01) is REQUIRED.

---

## 9. Priority and Security Interaction

Priority values are protected by CRC32.

Rules:
- Priority field corruption is detected via CRC32 failure.
- Envelopes with corrupted priority MUST be discarded.
- Relays MUST preserve priority values unmodified.

---

## 10. Payload Security

The baseline PBS-ENV-01 v1.3 CRC32 covers the header only, not the payload.

Payload integrity options:
- **Application-level checksums:** Payload includes its own integrity check.
- **End-to-end encryption:** Payload encrypted with authenticated encryption (e.g., AES-GCM).
- **Gateway encapsulation:** Gateway wraps payload in authenticated container.

Payload security is application-defined and outside the scope of PBS Core.

---

## 11. Forward Compatibility

Rules:
- CRC32 integrity verification SHALL remain mandatory for PBS Core v1.x.
- Cryptographic extensions MUST NOT alter baseline header structure.
- PBS-SEC-B-01 (PBS v1.4) defines authenticated mission messaging as an optional security profile.
- Further security models MAY be defined as additional PBS-SEC specifications.

---

## 12. Summary

PBS-SEC-A-01 defines a **CRC32-based integrity verification model** for the PBS envelope header.

Key features:
- Mandatory CRC32 verification for all envelopes
- Detection of transmission errors and bit-flips
- Sequence-based gap detection for packet loss
- Extensibility framework for cryptographic authentication

This model provides efficient, low-overhead integrity verification suitable for embedded systems, while allowing mission-specific security extensions for applications requiring cryptographic guarantees.
