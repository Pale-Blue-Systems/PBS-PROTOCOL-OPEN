# PBS-ENV-01  
## Core Message Envelope

**Status:** Core  
**Version:** 1.0  
**Applies to:** All PBS Core Messages  
**Related:** PBS-ADDR-01, PBS-MUX-01, PBS-PRIO-01, PBS-SEC-A-01

---

## 1. Purpose

This document defines the **Pale Blue Systems (PBS) Core Message Envelope**.

The envelope provides a stable, transport-agnostic container for all PBS messages. It defines addressing, authority context, lifetime, sequencing, and authentication boundaries required for interoperable operation across heterogeneous and delay-tolerant environments.

---

## 2. Envelope Overview

Every PBS message SHALL be transmitted within a PBS envelope.

The envelope:
- establishes administrative and authority context
- defines message lifetime and ordering semantics
- carries a multiplexed semantic payload
- provides a boundary for authentication

The envelope does not define transport, routing, or physical-layer behavior.

---

## 3. Envelope Structure

A PBS envelope consists of a fixed header followed by a payload and authentication data.

| Field | Type | Description |
|------|------|-------------|
| `version` | uint8 | PBS protocol version |
| `scope` | uint16 | Authority context identifier |
| `src` | address | Source address (PBS-ADDR-01) |
| `dst` | address | Destination address (PBS-ADDR-01) |
| `counter` | uint32 | Monotonic message counter |
| `ttl` | uint16 | Time-to-live |
| `flags` | uint8 | Envelope control flags |
| `payload_len` | uint16 | Length of payload (bytes) |
| `payload` | bytes | PBS-MUX container |
| `auth_tag` | bytes | Authentication tag |

All multi-byte fields SHALL be encoded in network byte order.

---

## 4. Versioning

The `version` field identifies the PBS Core version.

Rules:
- Implementations MUST reject envelopes with unsupported major versions.
- Minor version differences MUST be handled according to backward-compatibility rules defined by PBSF.
- PBS Core v1 implementations MUST set `version = 1`.

---

## 5. Authority Context (`scope`)

The `scope` field identifies the administrative authority context in which the message is valid.

Rules:
- Authority contexts are independent namespaces.
- The same address values MAY appear in different scopes without collision.
- Replay protection and sequencing are enforced per (`scope`, `src`).

The assignment and governance of scope values are defined outside this specification.

---

## 6. Addressing

The `src` and `dst` fields encode source and destination addresses.

Rules:
- Address encoding and semantics are defined in PBS-ADDR-01.
- Implementations MUST validate address encoding before processing.
- Destination behavior SHALL be interpreted according to address type.

---

## 7. Counter (`counter`)

The `counter` field provides monotonic sequencing for messages from a given source.

Rules:
- Counters MUST increase monotonically per (`scope`, `src`).
- Receivers SHOULD track recent counters to detect replays.
- Counter rollover behavior is implementation-defined but MUST NOT violate monotonicity guarantees.

---

## 8. Time-to-Live (`ttl`)

The `ttl` field defines the remaining lifetime of the envelope.

Rules:
- TTL is decremented as the message traverses time and/or hops.
- Envelopes with expired TTL MUST be discarded.
- TTL semantics are independent of transport-layer mechanisms.

TTL values represent relative lifetime, not absolute timestamps.

---

## 9. Envelope Flags (`flags`)

The `flags` field provides envelope-level control information.

Defined bits:

| Bit | Name | Meaning |
|----:|------|--------|
| 0 | ACK_REQ | Acknowledgement requested |
| 1–7 | RESERVED | Reserved for future use |

Undefined bits MUST be ignored.

---

## 10. Payload

The `payload` field SHALL contain a **PBS-MUX container** as defined in PBS-MUX-01.

Rules:
- The payload MUST be parsed only after successful envelope validation.
- Payload semantics are independent of envelope routing and transport.
- The payload MAY contain zero or more semantic subframes.

---

## 11. Authentication Tag (`auth_tag`)

The `auth_tag` field carries authentication data for the envelope.

Rules:
- Authentication structure and processing are defined in PBS-SEC-A-01.
- Authentication MUST cover all envelope fields except `auth_tag`.
- Envelopes failing authentication MUST be discarded.
- Relays MUST NOT modify authenticated fields.

---

## 12. Processing Order

Receivers MUST process envelopes in the following order:

1. Version validation  
2. Scope validation  
3. Address validation  
4. TTL validation  
5. Authentication verification  
6. Payload parsing  

Failure at any step MUST result in envelope discard.

---

## 13. Relay Behavior

Relays MUST:
- preserve envelope integrity
- preserve authenticated fields
- decrement TTL appropriately
- forward envelopes without semantic interpretation

Relays MUST NOT:
- alter payload semantics
- reorder authenticated fields
- regenerate authentication tags

---

## 14. Error Handling

Implementations MUST:
- discard malformed envelopes
- discard envelopes failing authentication
- discard envelopes with expired TTL
- continue processing subsequent messages

Envelope-level errors MUST NOT cause persistent failure states.

---

## 15. Forward Compatibility

Rules:
- Unknown envelope flags MUST be ignored.
- Unsupported major versions MUST be rejected.
- Envelope structure defined in this document SHALL remain stable for PBS Core v1.

---

## 16. Summary

PBS-ENV-01 defines the core message envelope for PBS Core.

It establishes a stable, authoritative boundary for addressing, lifetime, sequencing, and authentication, enabling interoperable communication across distributed and delay-tolerant environments.
