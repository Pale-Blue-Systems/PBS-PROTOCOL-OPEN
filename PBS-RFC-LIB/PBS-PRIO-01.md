# PBS-PRIO-01

## Priority Classification and Deterministic Handling

**Status:** Core  
**Version:** 1.0  
**Applies to:** All PBS Core Messages  
**Related:** PBS-ENV-01, PBS-MUX-01, PBS-ROUTE-01, PBS-SEC-A-01

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

Priority is encoded within the **Flags field** of the PBS envelope as defined in PBS-ENV-01.

### 5.1 Flags Field Mapping

The **three most significant bits** (Bits 5–7) of the `flags` field SHALL represent the Priority Class as a 3-bit unsigned integer.

```text
Bit:    7   6   5   4   3   2   1   0
      +---+---+---+---+---+---+---+---+
flags:| P | P | P | R | R | R | R | A |
      +---+---+---+---+---+---+---+---+
```

Where:
- `PPP` encodes the priority class (0–4 defined; 5–7 reserved)
- `R` represents reserved bits (Must be 0)
- `A` represents the ACK_REQ flag (PBS-ENV-01)

Rules:
- Priority values MUST conform to the defined class table.
- Values 5–7 are reserved and MUST NOT be used.
- Envelopes with invalid or reserved priority values MUST be discarded.
- Relays MUST NOT modify priority bits.

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

## 9. Interaction with MUX

Priority applies at the envelope level.

Rules:
- Frames within a MUX container MUST NOT carry independent priority values.
- Mixing semantic frames of different urgency SHOULD be avoided.
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