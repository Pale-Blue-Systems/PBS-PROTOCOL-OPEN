# PBS-ADDR-01  
## Addressing and Identification

**Status:** Core  
**Version:** 1.0  
**Applies to:** All PBS Core Messages  
**Related:** PBS-ENV-01, PBS-ROUTE-01, PBS-DTN-MAP-01

---

## 1. Purpose

This document defines the **addressing and identification model** for the Pale Blue Systems (PBS) Open Standard.

PBS addressing is designed to support **multi-actor, multi-authority environments** where civil, commercial, and international systems operate concurrently across space, lunar, and planetary domains.

The addressing model ensures:
- global uniqueness without central vendor control  
- coexistence of multiple authorities  
- deterministic parsing and routing behavior  
- compatibility with delay-tolerant and store-and-forward architectures  

---

## 2. Design Principles

PBS addressing follows these core principles:

- **Authority-scoped identity:** Addresses are interpreted within an explicit authority context.
- **Transport independence:** Address semantics are independent of physical or link-layer technologies.
- **Deterministic wire format:** All addresses are encoded in a parseable, self-describing format.
- **Extensibility:** New address types may be introduced without breaking existing implementations.
- **DTN compatibility:** Addressing maps cleanly to Delay/Disruption Tolerant Networking constructs.

---

## 3. Authority Context and Scope

All PBS addresses exist within an **authority context**, identified by the `scope` field in the PBS envelope (PBS-ENV-01).

Rules:
- A scope defines an independent administrative namespace.
- Address uniqueness is enforced within a scope, not globally.
- The same address value MAY exist in multiple scopes without collision.
- Inter-scope communication requires explicit translation or agreement.

Scope governance and assignment are defined outside this specification.

---

## 4. Address Structure

A PBS address is a structured identifier encoded within the PBS envelope.

### 4.1 Canonical Wire Encoding (TLV)

All PBS addresses SHALL be encoded using a **Type-Length-Value (TLV)** structure to ensure deterministic parsing and interoperability.

| Field | Size | Description |
|------|------|-------------|
| `type` | 1 byte | Address type identifier |
| `length` | 1 byte | Length of `value` field in bytes |
| `value` | Variable | Type-specific address value |

Rules:
- Parsers MUST read `type` and `length` before interpreting `value`.
- Unknown `type` values MUST be safely ignored or rejected.
- Multiple address TLVs MAY appear only where explicitly allowed by higher-level specifications.
- TLV encoding applies uniformly across all PBS implementations.

---

## 5. Address Types

### 5.1 Unicast Address (`type = 0x01`)

Identifies a single endpoint.

Rules:
- Messages are delivered to exactly one recipient.
- Delivery guarantees are best-effort unless higher-layer semantics apply.
- Unicast addresses are routable and relayable.

---

### 5.2 Group Address (`type = 0x02`)

Identifies a logical group of endpoints.

Rules:
- Messages MAY be delivered to multiple recipients.
- Group membership is defined by local policy.
- Relays MAY forward group-addressed messages without enumerating recipients.

---

### 5.3 Broadcast Address (`type = 0x03`)

Identifies all endpoints within a defined scope or region.

Rules:
- Broadcast delivery is bounded by scope.
- Relays MAY restrict broadcast propagation based on policy or capability.
- Broadcast usage SHOULD be limited due to resource impact.

---

### 5.4 Service Address (`type = 0x04`)

Identifies a function or service rather than a physical endpoint.

Rules:
- Resolution to physical endpoints is implementation-specific.
- Multiple endpoints MAY respond to a service address.
- Service addresses enable role-based and functional communication patterns.

---

## 6. Address Resolution

Address resolution maps an abstract PBS address to a concrete forwarding action.

Rules:
- Resolution MAY occur at endpoints, relays, or gateways.
- Resolution behavior is deterministic within a given scope.
- Resolution MUST NOT require global state or centralized coordination.

Resolution mechanisms are outside the scope of this specification.

---

## 7. Address Validation

Implementations MUST validate addresses before processing.

Validation includes:
- correct TLV structure  
- supported address type  
- valid length for the declared type  

Invalid addresses MUST result in message discard.

---

## 8. Address Stability

PBS addresses are **stable identifiers**, not transient network locators.

Rules:
- Address meaning MUST remain stable over time within a scope.
- Physical movement of an endpoint MUST NOT require address reassignment.
- Routing and reachability are handled separately from identity.

---

## 9. Addressing and Mobility

PBS explicitly supports mobile endpoints.

Rules:
- Address identity is decoupled from physical location.
- Mobility does not affect address validity.
- Routing updates MUST NOT alter address semantics.

---

## 10. Address Privacy and Exposure

Address visibility and disclosure are policy-controlled.

Rules:
- Address values MUST NOT embed sensitive operational metadata.
- Implementations MAY apply additional privacy-preserving mechanisms.
- Security considerations are defined in PBS-SEC-A-01.

---

## 11. Interoperability with DTN

PBS addresses are designed to map cleanly to DTN endpoint identifiers when required.

Rules:
- Address translation MUST preserve scope and identity semantics.
- DTN encapsulation does not alter PBS address meaning.
- Mapping behavior is defined in PBS-DTN-MAP-01.

---

## 12. Error Handling

Implementations MUST:
- discard messages with invalid or unsupported address types
- continue processing subsequent messages
- avoid persistent error states caused by address resolution failures

---

## 13. Forward Compatibility

Rules:
- Unknown address types MUST be ignored or rejected safely.
- Existing address types MUST retain semantic meaning across versions.
- Extensions MUST NOT break deterministic address parsing.

---

## 14. Summary

PBS-ADDR-01 defines a **scope-aware, TLV-encoded addressing model** for the PBS Open Standard.

By enforcing a deterministic wire format while separating identity from routing and location, PBS addressing enables interoperable, multi-actor communication across space and extreme environments while allowing implementation-specific optimization above the protocol layer.
