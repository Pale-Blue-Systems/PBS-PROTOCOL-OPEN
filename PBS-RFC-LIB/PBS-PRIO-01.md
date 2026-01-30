# PBS-PRIO-01

## Priority Classification and Deterministic Handling

**Status:** Core
**Version:** 1.3
**Applies to:** All PBS Core Messages
**Related:** PBS-ENV-01, PBS-ROUTE-01, PBS-SEC-A-01

---

## 1. Purpose

This document defines the **priority classification model** for the Pale Blue Systems (PBS) Open Standard.

PBS priority semantics enable deterministic handling of messages across constrained, intermittent, and delay-tolerant environments. The model ensures that life-, safety-, and mission-critical data is handled predictably without requiring continuous connectivity or centralized coordination.

---

## 2. Design Principles

PBS priority handling follows these principles:

- **Determinism:** Priority meaning is consistent across implementations.
- **Transport independence:** Priority semantics are independent of physical links.
- **Envelope authority:** Priority is expressed at the envelope boundary.
- **Graceful degradation:** Lower-priority data yields resources under contention.
- **Local policy enforcement:** Forwarding behavior may vary by node capability while preserving semantic intent.

---

## 3. Priority Model Overview

Priority in PBS is expressed using a **fixed ordinal class**, carried at the envelope level.

Rules:
- Priority applies to the entire envelope.
- All MUX frames within an envelope inherit the same priority class.
- Priority influences scheduling, forwarding, storage, and discard decisions.
- Priority does not imply delivery guarantees.

---

## 4. Priority Classes

PBS defines the following priority classes, ordered from highest to lowest:

| Value | Name | Description |
|------:|------|-------------|
| 0 | **CRITICAL** | Immediate life- or safety-critical data |
| 1 | **HIGH** | Mission-critical operational data |
| 2 | **NORMAL** | Routine mission data |
| 3 | **LOW** | Opportunistic or deferrable data |
| 4 | **BULK** | Non-urgent, high-volume data |

Rules:
- Lower numeric values indicate higher priority.
- Implementations MUST support all defined classes.
- Additional priority classes MUST NOT be introduced within PBS Core.

---

## 5. Envelope Encoding

Priority is encoded as a **dedicated byte field** in the PBS-ENV-01 v1.3 envelope header.

### 5.1 Header Field Layout

The `Priority` field occupies byte offset `0x01` in the 44-byte PBS envelope header:

| Offset | Field | Size | Type | Description |
|--------|-------|------|------|-------------|
| 0x00 | Magic | 1 | u8 | Fixed `0x10` |
| **0x01** | **Priority** | **1** | **u8** | **Priority class (0–4)** |
| 0x02 | Flags | 1 | u8 | `0x01`=ACK Requested |
| 0x03 | Reserved | 1 | u8 | Padding |

The Priority field is a single unsigned byte with defined values 0–4.

Rules:
- Priority values MUST conform to the defined class table (Section 4).
- Values 5–255 are reserved and MUST NOT be used.
- Envelopes with invalid or reserved priority values MUST be discarded.
- Relays MUST NOT modify the priority field.

---

## 6. Scheduling Behavior

When resources are constrained, implementations SHOULD schedule envelopes according to priority class.

Rules:
- Higher-priority envelopes SHOULD be forwarded before lower-priority envelopes.
- Implementations MAY apply fair-use, aging, or predictive mechanisms within a class.
- Lower-priority envelopes MAY be delayed or dropped under sustained congestion.

### 6.1 Preemption

Implementations MAY preempt (interrupt) the transmission of lower-priority envelopes in order to transmit higher-priority envelopes, provided that link-layer integrity is maintained.

Preemption behavior is implementation-specific and MUST NOT violate transport or physical-layer constraints.

---

## 7. Storage and Retention

PBS supports store-and-forward operation.

Rules:
- Higher-priority envelopes SHOULD receive preferential storage.
- Lower-priority envelopes MAY be discarded when storage is exhausted.
- TTL expiration (PBS-ENV-01) applies regardless of priority.

Priority does not override TTL.

---

## 8. Forwarding and Routing Interaction

Priority influences forwarding behavior but does not alter routing semantics.

Rules:
- Routing paths are selected independently of priority.
- Priority MAY influence queue selection and transmission order.
- Relays MUST preserve priority values end-to-end.

Routing behavior is defined in PBS-ROUTE-01.

---

## 9. Payload Priority

Priority applies at the envelope level and covers the entire payload.

Rules:
- The entire payload inherits the envelope's priority class.
- Payloads MUST NOT carry independent priority values.
- Mixing data of different urgency within a single envelope SHOULD be avoided.
- If mixed urgency is required, multiple envelopes SHOULD be used.

---

## 10. Security Considerations

Priority values are part of the authenticated envelope.

Rules:
- Priority bits MUST be covered by envelope authentication.
- Unauthorized modification of priority MUST result in message rejection.
- Relays MUST NOT elevate or downgrade priority.

Security mechanisms are defined in PBS-SEC-A-01.

---

## 11. Error Handling

Implementations MUST:
- discard envelopes with invalid or reserved priority values
- continue processing subsequent messages
- avoid persistent failure states caused by priority misclassification

---

## 12. Forward Compatibility

Rules:
- Priority class definitions SHALL remain stable for PBS Core v1.
- Reserved priority values MUST remain unused.
- Implementations MUST NOT assume future availability of unused values.

---

## 13. Summary

PBS-PRIO-01 defines a **fixed, envelope-encoded priority classification model** for the PBS Open Standard.

By encoding priority deterministically while leaving scheduling and optimization behavior implementation-defined, PBS enables predictable interoperability while supporting advanced, proprietary routing and congestion-management strategies.

---

## 14. NASA DSN Compatibility

This section documents the relationship between PBS priority classes and the NASA Deep Space Network (DSN) 7-level priority scheduling system.

### 14.1 Scope Differentiation

| Aspect | NASA DSN | PBS Protocol |
|--------|----------|--------------|
| **Scope** | Ground station antenna allocation | Packet transmission within a link |
| **Timescale** | Hours/days ahead | Milliseconds in real-time |
| **Decision Authority** | Ground scheduling team | Autonomous onboard software |

PBS operates at the **packet layer**, complementing DSN's macro-level ground scheduling. When an operator receives DSN antenna time, PBS determines which packets transmit first during that window.

### 14.2 Priority Mapping

| NASA DSN Level | DSN Description | Recommended PBS Mapping |
|----------------|-----------------|-------------------------|
| Level 1–2 | Spacecraft emergencies, human spaceflight | **CRITICAL (0)** |
| Level 3–4 | Launch/landing, orbit insertion, critical ops | **HIGH (1)** |
| Level 5–6 | Major/minor scientific events | **NORMAL (2)** / **LOW (3)** |
| Level 7 | Nominal tracking, routine science | **BULK (4)** |

Rules:
- This mapping is INFORMATIVE, not normative.
- Implementations MAY define mission-specific mappings.
- PBS priority values MUST remain as defined in Section 4.

### 14.3 Interoperability

PBS is designed for compatibility with DSN-serviced missions:
- Commercial operators implementing PBS can integrate with DSN ground infrastructure.
- PBS priority semantics align with DSN's safety-critical-first philosophy.
- No DSN software modification is required; PBS operates within allocated link time.