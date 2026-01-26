# PBS-MUX-01  
## Payload Multiplexing and Semantic Framing

**Status:** Core  
**Version:** 1.0  
**Applies to:** PBS Payloads  
**Related:** PBS-ENV-01, PBS-ADDR-01, PBS-PRIO-01, PBS-SEC-A-01

---

## 1. Purpose

This document defines the **Payload Multiplexing (MUX) container** for the Pale Blue Systems (PBS) Open Standard.

PBS-MUX enables multiple independent semantic units to be carried within a single PBS envelope, allowing efficient use of constrained links while preserving clear semantic boundaries, priority handling, and security properties.

---

## 2. Design Goals

PBS-MUX is designed to:

- enable multiple semantic messages per envelope  
- reduce transport overhead on constrained or intermittent links  
- preserve independent handling semantics per message  
- support deterministic parsing and skipping of unknown frame types  
- remain implementation-agnostic  

---

## 3. MUX Container Overview

The PBS payload carried in the envelope (`payload` field in PBS-ENV-01) SHALL be a **PBS-MUX container**.

The MUX container consists of:
- a container header
- exactly `frame_count` MUX frames
- optional trailing padding bytes

Padding bytes exist only to align payloads to transport or link-layer constraints.

---

## 4. MUX Container Structure

All multi-byte fields in this document SHALL be encoded in **network byte order (big-endian)**.

### 4.1 Container Header

| Field | Size | Description |
|------|------|-------------|
| `mux_version` | 1 byte | PBS-MUX version |
| `frame_count` | 1 byte | Number of frames in container |

Rules:
- Implementations MUST reject unsupported `mux_version` values.
- `frame_count` indicates the number of frames that follow.

---

### 4.2 MUX Frame Structure

Each MUX frame SHALL be encoded using a **Type-Length-Value (TLV)** structure.

| Field | Size | Description |
|------|------|-------------|
| `type` | 1 byte | Frame semantic type |
| `length` | 2 bytes | Length of `value` in bytes |
| `value` | Variable | Semantic payload |

Rules:
- The `length` field MUST be interpreted as an unsigned 16-bit integer in network byte order (big-endian).
- Frames MUST be parsed sequentially.
- Unknown `type` values MUST be safely skipped using `length`.
- Frames MUST NOT overlap or exceed container boundaries.
- Exactly `frame_count` frames MUST be parsed; any trailing bytes after the final frame are padding (Section 4.3).

---

### 4.3 Padding

After parsing exactly `frame_count` frames, any remaining bytes within the envelope payload length are padding.

Rules:
- Padding bytes MUST be ignored.
- Padding bytes MUST NOT be interpreted as an additional frame.
- A receiver MAY accept padding of any value.

---

## 5. Frame Types

PBS defines a core set of frame types. Additional frame types MAY be defined in future specifications.

### 5.1 Telemetry Frame (`type = 0x01`)

Carries measurement or state data.

Rules:
- Telemetry frames MAY be batched.
- Telemetry frames SHOULD be tolerant of loss or delay.

---

### 5.2 Command Frame (`type = 0x02`)

Carries control or instruction data.

Rules:
- Command frames SHOULD be processed in order.
- Command execution semantics are application-defined.

---

### 5.3 Status Frame (`type = 0x03`)

Carries system or health status information.

Rules:
- Status frames MAY be periodic or event-driven.
- Status frames SHOULD be low-bandwidth.

---

### 5.4 Event Frame (`type = 0x04`)

Carries discrete events or alerts.

Rules:
- Event frames SHOULD be prioritized appropriately.
- Event frames MAY trigger acknowledgements.

---

### 5.5 Application-Defined Frame (`type = 0x80–0xFF`)

Reserved for application-specific semantics.

Rules:
- Application-defined frames MUST NOT alter PBS Core behavior.
- Unsupported application frames MUST be ignored safely.

---

## 6. Priority Interaction

Frame-level priority MAY be expressed implicitly or explicitly.

Rules:
- Envelope-level priority applies to the container as a whole.
- Frame-level priority semantics are defined in PBS-PRIO-01.
- Implementations MAY reorder frames internally only if semantics allow.

---

## 7. Security Boundaries

Security processing applies at the envelope boundary.

Rules:
- The MUX container is authenticated as part of the envelope.
- Frames MUST NOT carry independent authentication unless explicitly defined.
- Encrypted payloads MAY encapsulate entire MUX containers.

Security mechanisms are defined in PBS-SEC-A-01.

---

## 8. Partial Processing and Forwarding

Implementations MAY process or forward subsets of frames.

Rules:
- Frame boundaries MUST be preserved.
- Discarding one frame MUST NOT invalidate others.
- Relays MUST NOT interpret frame semantics.

---

## 9. Error Handling

Implementations MUST:
- discard malformed frames
- skip unknown frame types using TLV length
- continue processing subsequent frames
- avoid persistent failure states

Malformed frames MUST NOT cause envelope rejection unless integrity is compromised.

---

## 10. Forward Compatibility

Rules:
- Unknown frame types MUST be safely ignored.
- Existing frame types MUST retain semantic meaning across versions.
- MUX container structure SHALL remain stable for PBS Core v1.

---

## 11. Summary

PBS-MUX-01 defines a **TLV-based multiplexing container** for PBS payloads.

By allowing multiple independent semantic frames to share a single envelope while preserving deterministic parsing, skipping, and padding behavior, PBS-MUX enables efficient, resilient communication across constrained and delay-tolerant environments.