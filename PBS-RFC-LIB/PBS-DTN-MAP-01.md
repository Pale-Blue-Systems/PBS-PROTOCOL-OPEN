# PBS-DTN-MAP-01

## Mapping to Delay/Disruption Tolerant Networking (DTN)

**Status:** Core (Interoperability)  
**Version:** 1.0  
**Applies to:** PBS Core Implementations Interfacing with DTN / BPv7  
**Related:** PBS-ENV-01, PBS-ADDR-01, PBS-MUX-01, PBS-PRIO-01, PBS-SEC-A-01, PBS-ROUTE-01, PBS-CONFORMANCE-01

---

## 1. Purpose

This document defines the **normative mapping** between the Pale Blue Systems (PBS) Open Standard and **Delay/Disruption Tolerant Networking (DTN)** environments, including **CCSDS Bundle Protocol Version 7 (BPv7)**.

PBS-DTN-MAP-01 enables PBS-native systems to interoperate with NASA, international space agencies, and other operators that employ DTN infrastructure, without requiring PBS Core to adopt DTN semantics internally.

The goal is **semantic preservation with minimal compute and power overhead**.

---

## 2. Scope

This specification applies **only at DTN boundaries**:

- PBS-native domains (e.g., intralunar surface mesh, habitat networks)
- DTN-enabled links (e.g., Earth relay, lunar relay, deep-space backbone)

Within PBS-native domains, **DTN wrapping is NOT required**.

---

## 3. Design Principles

PBS-to-DTN mapping follows these principles:

- **Boundary translation, not replacement:** PBS remains the primary protocol.
- **Minimal transformation:** Preserve PBS semantics wherever possible.
- **No semantic leakage:** DTN concepts MUST NOT alter PBS Core behavior.
- **Store-and-forward alignment:** Mapping respects DTN operational assumptions.
- **Energy efficiency:** Avoid unnecessary re-encoding or re-signing.

---

## 4. Architectural Position

PBS-DTN-MAP operates at a **gateway boundary**, typically implemented as a relay or edge node.

    PBS Native Domain            DTN Domain

    +------------------+     +----------------------+
    |  PBS Envelopes   | --> |  BPv7 Bundles        |
    |  (PBS-ENV-01)    |     |  (CCSDS / ION)       |
    +------------------+     +----------------------+
             ▲                          |
             |                          ▼
    +------------------+     +----------------------+
    |  PBS Envelopes   | <-- |  BPv7 Bundles        |
    +------------------+     +----------------------+

PBS-DTN-MAP nodes act as **protocol translators**, not originators.

---

## 5. Mapping Overview

### 5.1 One-to-One Envelope Mapping

Each PBS Envelope SHALL map to **exactly one BPv7 Bundle**.

Rules:
- PBS envelopes MUST NOT be fragmented across multiple bundles.
- Bundle fragmentation MAY be performed by DTN layers below BPv7 if required.

---

## 6. PBS to BPv7 Mapping (Outbound)

### 6.1 Primary Block

| PBS Field | BPv7 Field | Mapping Rule |
|---------|------------|--------------|
| `src` | Source EID | Mapped via PBS-ADDR-01 |
| `dst` | Destination EID | Mapped via PBS-ADDR-01 |
| `ttl` | Lifetime | Converted to DTN lifetime |
| `counter` | Bundle ID | Used as unique identifier |
| `priority` | Class of Service | See Section 6.3 |

---

### 6.2 Payload Block

Rules:
- The **entire PBS envelope payload** (including PBS-MUX content) SHALL be placed into a single BPv7 Payload Block.
- PBS payload contents MUST NOT be interpreted or altered.

---

### 6.3 Priority Mapping

PBS Priority Classes SHALL map to DTN Class of Service (CoS):

| PBS Priority | DTN CoS |
|-------------|---------|
| Critical | Expedited |
| High | Expedited |
| Normal | Normal |
| Bulk | Bulk |

Mapping preserves **relative urgency**, not scheduling behavior.

---

### 6.4 Security Handling (Outbound)

Rules:
- PBS authentication (PBS-SEC-A-01) MUST be preserved end-to-end.
- DTN security mechanisms (e.g., BPSEC) MAY be applied additionally.
- DTN security MUST NOT replace PBS authentication.

PBS envelopes MUST NOT be re-signed during DTN encapsulation.

---

## 7. BPv7 to PBS Mapping (Inbound)

### 7.1 Bundle Validation

Upon receipt of a BPv7 bundle:

- DTN-layer validation MUST occur first.
- Invalid bundles MUST be discarded before PBS processing.

---

### 7.2 Envelope Restoration

Rules:
- The PBS envelope payload SHALL be extracted verbatim.
- No modification to PBS envelope fields is permitted.
- The envelope SHALL be reintroduced into PBS-native routing.

---

### 7.3 TTL Handling

Rules:
- DTN lifetime expiration MUST result in envelope discard.
- PBS `ttl` MUST NOT be incremented or reset.
- PBS `ttl` continues decrementing within PBS-native hops.

---

## 8. Address Translation

PBS addresses MUST be translated to and from **DTN Endpoint Identifiers (EIDs)**.

Rules:
- Address-to-EID mapping MUST be deterministic.
- Authority scope MUST be preserved.
- Service addresses MAY map to service-specific EIDs.

Exact EID syntax is implementation-defined but MUST be stable within a scope.

---

## 9. Store-and-Forward Semantics

PBS-DTN-MAP nodes MUST support store-and-forward behavior.

Rules:
- Envelopes MAY be stored until DTN contact is available.
- Storage decisions SHOULD consider PBS priority and TTL.
- DTN custody transfer MAY be used if supported.

DTN storage does not alter PBS routing semantics.

---

## 10. Failure Handling

Rules:
- Failure to forward via DTN MUST NOT invalidate the PBS envelope.
- Envelopes MAY be retried, delayed, or discarded based on policy.
- DTN errors MUST NOT propagate as PBS protocol errors.

---

## 11. Interoperability Expectations

A PBS Core conformant system implementing PBS-DTN-MAP-01 can:

- communicate with NASA DTN infrastructure (e.g., ION)
- interoperate with international and commercial DTN-enabled systems
- preserve PBS semantics across interplanetary links

PBS-DTN-MAP ensures **compatibility without coupling**.

---

## 12. Power and Compute Considerations

PBS-DTN-MAP is designed for constrained environments.

Rules:
- Mapping SHOULD avoid envelope reserialization where possible.
- Cryptographic operations MUST NOT be duplicated unnecessarily.
- Gateways SHOULD minimize buffer copies.

---

## 13. Forward Compatibility

Rules:
- New PBS envelope fields MUST NOT break DTN mapping.
- DTN extensions MUST NOT leak into PBS Core semantics.
- Major DTN version changes MAY require a new mapping document.

---

## 14. Summary

PBS-DTN-MAP-01 defines a **clean, minimal, and deterministic bridge** between PBS Core and DTN environments.

By treating DTN as a boundary transport rather than an internal dependency, PBS enables commercial, civil, and international systems to interoperate across Earth, lunar, and deep-space domains while preserving performance, security, and architectural independence.