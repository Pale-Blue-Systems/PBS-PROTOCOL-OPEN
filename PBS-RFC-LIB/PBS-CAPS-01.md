# PBS-CAPS-01  
## Capability Advertisement and Discovery

**Status:** Core  
**Version:** 1.0  
**Applies to:** PBS Payloads (MUX Frames)  
**Related:** PBS-ENV-01, PBS-MUX-01, PBS-ADDR-01, PBS-POS-01, PBS-ROUTE-01, PBS-SEC-A-01

---

## 1. Purpose

This document defines **Capability Advertisement and Discovery (CAPS)** for the Pale Blue Systems (PBS) Open Standard.

PBS-CAPS provides a lightweight, optional mechanism for endpoints to advertise **what they can do**—services, roles, resources, and constraints—without requiring centralized registries or continuous connectivity.

CAPS enables:
- service discovery in disconnected or delay-tolerant environments
- informed routing and relay selection
- role- and function-based interaction
- graceful operation when capabilities change or are unavailable

---

## 2. Design Principles

PBS-CAPS follows these principles:

- **Optionality:** Capability signaling is not required for PBS Core operation.
- **Deterministic parsing:** Capability data is self-describing and safely skippable.
- **Low overhead:** Advertisements are compact and rate-limited.
- **Scope awareness:** Capability meaning is interpreted within an authority scope.
- **Authentication by envelope:** Capability data is authenticated end-to-end.

---

## 3. CAPS as a MUX Frame

Capability information is carried as a **PBS-MUX frame** within the authenticated envelope.

Rules:
- CAPS frames MUST be encapsulated within a PBS-MUX container (PBS-MUX-01).
- CAPS frames inherit envelope authentication (PBS-SEC-A-01).
- Relays MUST NOT modify CAPS frames.
- Relays MAY use CAPS data as a forwarding heuristic.

---

## 4. CAPS Frame Type

CAPS frames use the following MUX frame type:

- **Capability Advertisement Frame:** `type = 0x06`

The CAPS frame value is defined in this document.

---

## 5. CAPS Frame Value Encoding (TLV)

The CAPS frame value SHALL be encoded using a **Type-Length-Value (TLV)** structure to ensure deterministic parsing and forward compatibility.

All multi-byte fields in this document SHALL be encoded in **network byte order (big-endian)**.

| Field | Size | Description |
|------|------|-------------|
| `cap_type` | 1 byte | Capability type |
| `cap_length` | 1 byte | Length of `cap_value` in bytes |
| `cap_value` | Variable | Type-specific value |

Rules:
- Parsers MUST read `cap_type` and `cap_length` before interpreting `cap_value`.
- Unknown `cap_type` values MUST be safely skipped using `cap_length`.
- If `cap_length` exceeds remaining frame boundaries, the CAPS frame is malformed and MUST be discarded (without rejecting the envelope).

---

## 6. Capability Types

### 6.1 Service Capability (`cap_type = 0x01`)

Advertises availability of a service or function.

Rules:
- Services are identified by a scope-defined identifier.
- Service semantics are not defined by PBS Core.

`cap_value`:
- Variable-length service identifier (opaque to PBS Core).

---

### 6.2 Role Capability (`cap_type = 0x02`)

Advertises the operational role of the endpoint.

Examples:
- relay
- habitat
- rover
- wearable
- gateway

Rules:
- Role interpretation is scope-defined.
- Multiple role capabilities MAY be advertised.

`cap_value`:
- Variable-length role identifier.

---

### 6.3 Resource Capability (`cap_type = 0x03`)

Advertises available or constrained resources.

Examples:
- storage capacity
- compute availability
- power state

Rules:
- Resource units and semantics are scope-defined.
- Resource values are advisory.

`cap_value` format:
- Implementation-defined structured value.

---

### 6.4 Transport Capability (`cap_type = 0x04`)

Advertises supported transport or link characteristics.

Examples:
- low-latency link available
- store-and-forward only
- scheduled uplink windows

Rules:
- Transport capability does not override routing semantics.
- Used as a hint for forwarding decisions.

`cap_value`:
- Implementation-defined structured value.

---

### 6.5 Security Capability (`cap_type = 0x05`)

Advertises supported security features.

Examples:
- supported authentication models
- encryption availability (informational)

Rules:
- Security capabilities do not alter PBS Core security requirements.
- Negotiation is outside the scope of this specification.

`cap_value`:
- Variable-length identifier set.

---

### 6.6 Application-Defined Capability (`cap_type = 0x80–0xFF`)

Reserved for application- or mission-specific capabilities.

Rules:
- Application-defined capabilities MUST NOT alter PBS Core semantics.
- Unsupported capability types MUST be ignored safely.

---

## 7. Advertisement Semantics

Rules:
- CAPS frames MAY be sent periodically or event-driven.
- CAPS frames SHOULD be rate-limited to avoid congestion.
- CAPS frames MAY be cached by receivers for local decision-making.
- Absence of a capability MUST NOT be interpreted as lack of support.

Capability data is advisory and non-authoritative.

---

## 8. Interaction with POS

CAPS and POS complement each other.

Rules:
- POS answers “Where am I / am I present?”
- CAPS answers “What can I do?”
- Implementations MAY use both signals together for routing or selection heuristics.

Neither POS nor CAPS overrides explicit addressing.

---

## 9. Routing and Forwarding Interaction

CAPS data MAY influence routing and forwarding decisions.

Rules:
- Routing algorithms MAY consider CAPS as a heuristic.
- CAPS MUST NOT override authority, scope, or addressing rules.
- Relays MAY ignore CAPS frames entirely.

Routing semantics are defined in PBS-ROUTE-01.

---

## 10. Security Considerations

CAPS data is authenticated as part of the envelope payload.

Rules:
- CAPS frames MUST NOT be modified in transit.
- Spoofed or altered capability data MUST be detectable via authentication.
- Implementations SHOULD treat CAPS data as informational unless verified by policy.

---

## 11. Privacy Considerations

Capability advertisement is optional and policy-controlled.

Rules:
- Endpoints MAY limit advertised capabilities.
- Sensitive capabilities SHOULD be omitted or generalized.
- Scope policy governs CAPS visibility and retention.

---

## 12. Error Handling

Implementations MUST:
- ignore unsupported capability types by skipping `cap_length` bytes
- discard malformed CAPS frames
- continue processing subsequent frames

CAPS errors MUST NOT invalidate the envelope.

---

## 13. Forward Compatibility

Rules:
- Unknown capability types MUST be safely skipped.
- Existing capability types MUST retain semantic meaning across versions.
- Extensions MUST preserve deterministic parsing.

---

## 14. Summary

PBS-CAPS-01 defines a **flexible, optional capability advertisement model** for the PBS Open Standard.

By allowing endpoints to advertise services, roles, resources, and constraints using authenticated, TLV-encoded frames, PBS enables informed, cooperative behavior across distributed and delay-tolerant environments without central coordination.
