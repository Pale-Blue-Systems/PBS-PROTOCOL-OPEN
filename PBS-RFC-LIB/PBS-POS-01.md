# PBS-POS-01  
## Position and Presence Signaling

**Status:** Core  
**Version:** 1.0  
**Applies to:** PBS Payloads (MUX Frames)  
**Related:** PBS-ENV-01, PBS-MUX-01, PBS-ADDR-01, PBS-ROUTE-01, PBS-SEC-A-01

---

## 1. Purpose

This document defines **Position and Presence (POS) signaling** for the Pale Blue Systems (PBS) Open Standard.

PBS-POS provides a lightweight, optional mechanism for endpoints to signal **presence state** and **position information** to peers, relays, or services. The model is designed for mobile, constrained, and delay-tolerant environments where continuous or high-precision positioning is not always available or required.

POS signaling supports:
- proximity-aware routing and forwarding
- relay and tower (pole) selection
- local situational awareness
- safe operation under partial or absent positioning data

---

## 2. Design Principles

PBS-POS follows these principles:

- **Optionality:** POS signaling is not required for PBS Core operation.
- **Graceful degradation:** Absence or imprecision of position data does not break communication.
- **Low overhead:** POS messages are compact and efficient.
- **Transport independence:** POS semantics are independent of physical positioning systems.
- **Authentication by envelope:** POS data is authenticated as part of the payload.

---

## 3. POS as a MUX Frame

POS information is carried as a **PBS-MUX frame** within the authenticated envelope.

Rules:
- POS frames MUST be encapsulated within a PBS-MUX container (PBS-MUX-01).
- POS frames inherit envelope authentication (PBS-SEC-A-01).
- Relays MUST NOT modify POS frames.

---

## 4. POS Frame Type

POS frames use the following MUX frame type:

- **Position and Presence Frame:** `type = 0x05`

The POS frame value is defined in this document.

---

## 5. POS Frame Value Encoding (TLV)

The POS frame value SHALL be encoded using a **Type-Length-Value (TLV)** structure to ensure deterministic parsing and safe skipping of unknown POS types.

All multi-byte fields in this document SHALL be encoded in **network byte order (big-endian)**.

| Field | Size | Description |
|------|------|-------------|
| `pos_type` | 1 byte | POS data type |
| `pos_length` | 1 byte | Length of `pos_value` in bytes |
| `pos_value` | Variable | Type-specific value |

Rules:
- Parsers MUST read `pos_type` and `pos_length` before interpreting `pos_value`.
- Unknown `pos_type` values MUST be safely skipped using `pos_length`.
- If `pos_length` exceeds the remaining frame boundary, the POS frame is malformed and MUST be discarded (without rejecting the envelope).

---

## 6. POS Data Types

### 6.1 Presence-Only (`pos_type = 0x01`)

Signals presence without positional coordinates.

Rules:
- Indicates that the endpoint is active and reachable.
- No location semantics are implied.
- Suitable for wearables, stationary assets, or privacy-restricted contexts.

`pos_length = 1`

`pos_value`:
- Single byte status code.

Defined values:
- `0x01` — Present / Active
- `0x02` — Idle
- `0x03` — Stationary
- `0x04` — Unknown

---

### 6.2 Stationary Marker (`pos_type = 0x02`)

Explicitly signals that the endpoint has not moved since the last POS update.

Rules:
- Indicates positional stability without coordinates.
- Allows relays and peers to avoid unnecessary routing updates.
- Useful for fixed infrastructure (e.g., habitats, poles).

`pos_length = 1`

`pos_value`:
- Single byte constant: `0x05`

---

### 6.3 Coordinate-Based Position (`pos_type = 0x03`)

Provides explicit positional coordinates.

Rules:
- Coordinates are relative to a locally defined reference frame.
- PBS does not mandate a global coordinate system.
- Each `scope` MUST define the coordinate reference frame and units used (e.g., meters, decameters, centimeters, or mission-defined units).
- Implementations MUST treat coordinate semantics as advisory unless validated by local policy.

`pos_length = 12`

`pos_value` format:

| Component | Size | Description |
|---------|------|-------------|
| `x` | int32 | X-axis coordinate |
| `y` | int32 | Y-axis coordinate |
| `z` | int32 | Z-axis coordinate |

Note:
- The int32 range is appropriate for local operational frames. If larger domains are required, scopes may define units that scale the represented range (e.g., decameters), or use higher-layer extensions outside PBS Core.

---

### 6.4 Proximity Hint (`pos_type = 0x04`)

Provides a relative proximity indicator rather than absolute position.

Rules:
- Used for relay selection and nearest-node heuristics.
- Does not expose precise coordinates.

`pos_length = 1`

`pos_value`:
- Unsigned integer proximity tier (lower = closer).

---

## 7. POS Update Semantics

Rules:
- POS frames MAY be sent periodically or event-driven.
- POS frames SHOULD be rate-limited according to endpoint capability and mission policy.
- Absence of POS frames MUST NOT be interpreted as failure.

POS data is advisory and non-authoritative.

---

## 8. Routing and Forwarding Interaction

POS data MAY influence routing and forwarding decisions.

Rules:
- Routing algorithms MAY consider POS data as a heuristic.
- POS data MUST NOT override explicit addressing or authority rules.
- Relays MAY ignore POS frames entirely.

Routing semantics are defined in PBS-ROUTE-01.

---

## 9. Security Considerations

POS data is authenticated as part of the envelope payload.

Rules:
- POS frames MUST NOT be modified in transit.
- Spoofed or altered POS data MUST be detectable via authentication.
- Implementations SHOULD minimize exposure of sensitive positional data via policy.

POS signaling does not imply trust in reported position accuracy.

---

## 10. Privacy Considerations

POS signaling is optional and policy-controlled.

Rules:
- Endpoints MAY omit coordinate-based POS entirely.
- Presence-only signaling SHOULD be used where privacy is required.
- Scope policy governs POS visibility, storage, and retention.

---

## 11. Error Handling

Implementations MUST:
- ignore unsupported POS types by skipping `pos_length` bytes
- discard malformed POS frames
- continue processing subsequent frames

POS errors MUST NOT invalidate the envelope.

---

## 12. Forward Compatibility

Rules:
- Unknown POS types MUST be safely skipped.
- Existing POS types MUST retain semantic meaning across versions.
- Extensions MUST preserve deterministic parsing.

---

## 13. Summary

PBS-POS-01 defines a **flexible, low-overhead Position and Presence signaling model** for the PBS Open Standard.

By encoding POS updates as TLV within authenticated envelopes and separating presence, stability, proximity, and coordinate signaling, PBS enables proximity-aware behavior while maintaining interoperability under partial or absent positioning data.
