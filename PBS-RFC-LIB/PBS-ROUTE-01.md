# PBS-ROUTE-01  
## Routing and Forwarding Semantics

**Status:** Core  
**Version:** 1.0  
**Applies to:** All PBS Core Implementations  
**Related:** PBS-ENV-01, PBS-ADDR-01, PBS-MUX-01, PBS-PRIO-01, PBS-SEC-A-01, PBS-POS-01, PBS-CAPS-01, PBS-DTN-MAP-01

---

## 1. Purpose

This document defines the **routing and forwarding semantics** for the Pale Blue Systems (PBS) Open Standard.

PBS routing specifies *what decisions are allowed and what behaviors are required* when forwarding envelopes across heterogeneous, multi-hop, and delay-tolerant environments. It intentionally avoids prescribing routing algorithms, metrics, or control planes.

The goal is to ensure **deterministic, interoperable behavior** while preserving implementation freedom for routing intelligence and optimization.

---

## 2. Design Principles

PBS routing adheres to the following principles:

- **Separation of semantics from algorithms:** Routing meaning is standardized; routing strategy is not.
- **Store-and-forward first:** Disconnection is normal and expected.
- **Authority-aware operation:** Routing respects scope and authority boundaries.
- **Deterministic safety:** Unknown or unsupported features do not cause failure.
- **Implementation neutrality:** No requirement for centralized control or global state.

---

## 3. Routing vs. Forwarding

PBS distinguishes between **routing** and **forwarding**:

- **Routing** determines *where an envelope should go next*.
- **Forwarding** is the act of *moving an envelope toward its destination*.

PBS Core defines forwarding obligations and routing constraints but does not define routing protocols.

---

## 4. Forwarding Eligibility

An envelope is eligible for forwarding if and only if:

- the envelope structure is valid (PBS-ENV-01)
- authentication succeeds (PBS-SEC-A-01)
- the TTL has not expired
- the destination address is not local

Envelopes failing eligibility checks MUST be discarded.

---

## 5. Authority and Scope Constraints

Routing decisions MUST respect authority context.

Rules:
- Envelopes MUST NOT be forwarded across scope boundaries without explicit translation.
- Relays operating in multiple scopes MUST treat each scope independently.
- Scope-based policy MAY restrict forwarding paths.

Scope translation behavior is outside the scope of this specification.

---

## 6. Address-Based Routing

Routing decisions are primarily guided by destination address semantics.

Rules:
- Address interpretation follows PBS-ADDR-01.
- Unicast addresses route toward a single endpoint.
- Group and broadcast addresses MAY result in multiple forwarding actions.
- Service addresses require resolution before forwarding.

Address resolution mechanisms are implementation-defined.

---

## 7. Priority Interaction

Priority influences forwarding behavior but does not alter routing semantics.

Rules:
- Higher-priority envelopes SHOULD be forwarded preferentially under contention.
- Priority MUST NOT override scope or authority constraints.
- Priority MAY influence queue selection, storage preference, and transmission order.

Priority semantics are defined in PBS-PRIO-01.

---

## 8. Store-and-Forward Behavior

PBS routing assumes intermittent connectivity.

Rules:
- Nodes MAY store envelopes until forwarding becomes possible.
- Storage decisions SHOULD consider priority and TTL.
- Envelopes MAY be forwarded opportunistically when links become available.

No assumption of continuous end-to-end connectivity is permitted.

---

## 9. POS and CAPS Interaction

POS and CAPS data MAY inform routing decisions.

Rules:
- POS MAY be used for proximity-based heuristics.
- CAPS MAY be used to select relays or service-capable nodes.
- POS and CAPS data are advisory and non-authoritative.

Routing MUST remain correct in the absence of POS or CAPS.

---

## 10. Loop Prevention

PBS relies on TTL-based loop prevention.

Rules:
- TTL MUST be decremented at each forwarding hop (PBS-ENV-01).
- Envelopes with expired TTL MUST be discarded.
- Implementations MAY employ additional loop detection mechanisms.

No global loop-free topology is assumed.

---

## 11. Multi-Path and Replication

PBS allows controlled replication.

Rules:
- Group and broadcast addresses MAY result in envelope replication.
- Replication MUST respect TTL and priority.
- Excessive replication SHOULD be avoided by local policy.

Replication behavior is implementation-defined.

---

## 12. Relay Obligations

Relays MUST:

- preserve all authenticated envelope fields
- decrement TTL correctly
- preserve priority bits end-to-end
- forward envelopes without interpreting payload semantics
- discard envelopes violating policy or eligibility rules

Relays MUST NOT:
- modify payload contents
- alter authenticated fields
- reinterpret envelope semantics

---

## 13. Error Handling

Routing and forwarding errors MUST be handled safely.

Rules:
- Envelopes that cannot be forwarded MAY be stored, delayed, or discarded.
- Errors MUST NOT propagate as protocol failures.
- Routing failure MUST NOT affect processing of unrelated envelopes.

---

## 14. Forward Compatibility

Rules:
- Unknown address types or optional data MUST be ignored safely.
- New routing hints MUST NOT break existing behavior.
- PBS Core routing semantics SHALL remain stable for v1.

---

## 15. Summary

PBS-ROUTE-01 defines **routing and forwarding semantics** for the PBS Open Standard.

By standardizing *what routing decisions mean*—while leaving *how those decisions are made* to implementations—PBS enables interoperable, resilient communication across distributed and delay-tolerant environments without constraining innovation or optimization above the protocol layer.
