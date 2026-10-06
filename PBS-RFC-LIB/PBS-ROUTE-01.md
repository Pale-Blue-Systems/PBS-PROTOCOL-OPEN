# PBS-ROUTE-01  
## Routing and Forwarding Semantics

**Status:** Optional
**Version:** 1.5
**Changes:** <release date> (PBS v1.5.0): Section 10 forbids TTL modification at any hop, states the expiry instant, and adds loop detection with bounded state for envelopes with TTL `0`. Section 12 requires relays to preserve every header field, including TTL and CRC32 (PBS-ENV-01 Sections 12.3 and 15), and supersedes the PBS v1.4.1 Section 12 erratum. The PBS v1.4.1 Section 4 erratum is incorporated (PBS-PROTOCOL-CHANGELOG.md, [1.4.1]). Wire format unchanged.
**Applies to:** PBS Relay and Gateway Implementations
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-SEC-A-01, PBS-DTN-MAP-01

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
- header CRC32 verification succeeds (PBS-SEC-A-01)
- the TTL has not expired
- the local node is not the envelope's destination (Section 6)

Envelopes failing the structure, CRC32 or TTL checks MUST be discarded. Envelopes destined for the local node are delivered locally and are not forwarded.

---

## 5. Authority and Scope Constraints

Routing decisions MUST respect authority context.

Rules:
- Envelopes MUST NOT be forwarded across scope boundaries without explicit translation.
- Relays operating in multiple scopes MUST treat each scope independently.
- Scope-based policy MAY restrict forwarding paths.

Scope translation behavior is outside the scope of this specification.

---

## 6. Source-Based Routing

PBS-ENV-01 v1.3 identifies message origin via the 16-byte Source ID field.

Rules:
- Source ID identifies the originating device (e.g., "Rover-Alpha").
- Routing to destinations is handled by gateway-level protocols.
- Gateways MAY maintain routing tables mapping Source IDs to endpoints.
- Destination routing is implementation-defined above PBS Core.

For systems requiring explicit destination addressing, see PBS-ADDR-01 (Optional Extension).

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

PBS relies on TTL-based loop prevention. An envelope with `TTL > 0` expires at `timestamp / 1_000_000 + TTL` in Unix epoch seconds (PBS-ENV-01 Section 12.2), however many hops it traverses. A forwarding loop therefore cannot keep it past that instant at any node, measured by that node's clock.

Rules:
- TTL MUST NOT be modified at any forwarding hop (PBS-ENV-01 Section 12.3).
- Envelopes with expired TTL MUST be discarded.
- Expiry does not bound the forwarding of an envelope with TTL `0` (PBS-ENV-01 Section 12.1). Implementations that forward envelopes with TTL `0` SHOULD employ an additional loop detection mechanism. A mechanism that suppresses an envelope repeating the Source ID, Sequence and Timestamp of an envelope already forwarded SHOULD keep that state only for a locally configured interval, so that it does not suppress a later retransmission of the same envelope.
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

- forward all envelope header fields unchanged, including TTL and CRC32 (PBS-ENV-01 Section 15)
- evaluate TTL expiration against the unchanged Timestamp and TTL (PBS-ENV-01 Sections 12.2 and 12.3)
- preserve the Priority byte end-to-end
- forward envelopes without interpreting payload semantics
- discard envelopes violating policy or eligibility rules

Relays MUST NOT:
- modify payload contents
- alter any header field
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
