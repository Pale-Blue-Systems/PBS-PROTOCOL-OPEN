# PBS-CONFORMANCE-01  
## Conformance, Interoperability, and Mandatory Baselines

**Status:** Core  
**Version:** 1.0  
**Applies to:** All PBS Core Implementations  
**Related:** PBS-ENV-01, PBS-ADDR-01, PBS-MUX-01, PBS-PRIO-01, PBS-SEC-A-01, PBS-POS-01, PBS-CAPS-01, PBS-DTN-MAP-01

---

## 1. Purpose

This document defines **conformance requirements** for implementations of the Pale Blue Systems (PBS) Open Standard.

Its purpose is to ensure that independently developed implementations can interoperate reliably across heterogeneous, multi-authority, and delay-tolerant environments, while preserving implementation freedom above the protocol layer.

PBS conformance focuses on:
- deterministic parsing and behavior
- interoperability across vendors and agencies
- minimum security and protocol correctness guarantees
- long-term stability of PBS Core semantics

---

## 2. Conformance Levels

PBS defines a single conformance level for PBS Core v1:

- **PBS Core Conformant Implementation**

An implementation is considered PBS Core conformant if it satisfies all **MUST** and **MUST NOT** requirements defined in the PBS Core specifications listed in Section 1.

Optional features (POS, CAPS, DTN mapping) do not affect core conformance unless explicitly claimed.

---

## 3. Mandatory Supported Specifications

A PBS Core conformant implementation MUST correctly implement the following specifications:

- PBS-ENV-01 — Core Message Envelope  
- PBS-ADDR-01 — Addressing and Identification  
- PBS-MUX-01 — Payload Multiplexing  
- PBS-PRIO-01 — Priority Classification  
- PBS-SEC-A-01 — Security Model A  

Implementations MAY additionally support:
- PBS-POS-01 — Position and Presence Signaling  
- PBS-CAPS-01 — Capability Advertisement  
- PBS-DTN-MAP-01 — DTN Mapping  

Optional specifications MUST be implemented fully if claimed.

---

## 4. Deterministic Parsing Requirements

To ensure interoperability, conformant implementations MUST:

- parse all TLV structures exactly as defined
- safely skip unknown types using declared length fields
- ignore padding as specified
- reject malformed frames without crashing or undefined behavior
- process frames sequentially and deterministically

Parsing behavior MUST NOT depend on implementation-specific assumptions.

---

## 5. Envelope Handling Requirements

A conformant implementation MUST:

- correctly encode and decode the PBS envelope (PBS-ENV-01)
- preserve all authenticated (immutable) fields end-to-end
- correctly decrement mutable fields (e.g., `ttl`)
- discard envelopes with invalid structure, expired TTL, or failed authentication
- preserve priority bits exactly as received

Relays MUST follow relay-specific rules defined in PBS Core documents.

---

## 6. Addressing Conformance

A conformant implementation MUST:

- support TLV-encoded addresses (PBS-ADDR-01)
- enforce scope-based identity separation
- reject unsupported or malformed address types
- preserve address semantics during forwarding and mapping

Address resolution behavior MAY be implementation-specific but MUST remain deterministic within a scope.

---

## 7. Security Baseline Requirements

### 7.1 Mandatory Security Model

PBS Core conformance REQUIRES support for:

- **Security Model A** (PBS-SEC-A-01)

Implementations MUST:
- correctly authenticate immutable envelope fields
- correctly exclude mutable fields (e.g., `ttl`) from authentication
- enforce replay protection semantics
- discard unauthenticated or tampered envelopes

### 7.2 Mandatory Baseline Algorithm

To ensure baseline interoperability, PBS Core v1 defines the following **mandatory-to-implement authentication algorithm**:

- **HMAC-SHA-256**

Rules:
- All PBS Core implementations MUST support HMAC-SHA-256.
- Implementations MAY support additional algorithms by local policy.
- Within a given scope, all participating nodes MUST share at least one common algorithm.

Algorithm negotiation mechanisms are outside the scope of PBS Core.

---

## 8. Priority and Scheduling Conformance

A conformant implementation MUST:

- correctly parse and preserve priority bits (PBS-PRIO-01)
- apply priority consistently to scheduling, storage, and forwarding decisions
- support all defined priority classes

The internal scheduling algorithm is implementation-defined and not subject to conformance testing.

---

## 9. Optional Feature Conformance

If an implementation claims support for optional specifications, it MUST fully conform to them:

- **PBS-POS-01:** Correct TLV parsing, authentication, and advisory use of POS data  
- **PBS-CAPS-01:** Correct TLV parsing, authentication, and advisory use of CAPS data  
- **PBS-DTN-MAP-01:** Correct semantic mapping without altering PBS Core behavior  

Partial or non-compliant support MUST NOT be claimed.

---

## 10. Interoperability Expectations

PBS Core conformance implies that:

- two independent conformant implementations can exchange envelopes correctly
- messages are parsed, authenticated, and forwarded predictably
- unknown extensions do not cause failures
- scope and authority boundaries are respected

Interoperability does not imply identical performance or routing behavior.

---

## 11. Testing and Validation

PBSF MAY publish:
- reference test vectors
- conformance test suites
- interoperability scenarios

Use of such tooling is RECOMMENDED but not required for conformance claims unless explicitly stated.

---

## 12. Versioning and Compatibility

Rules:
- PBS Core v1 semantics SHALL remain stable.
- Backward-incompatible changes require a new major version.
- Minor versions MAY add optional features without breaking conformance.

Implementations MUST reject unsupported major versions.

---

## 13. Conformance Claims

Implementations claiming PBS Core conformance SHOULD:

- identify the supported PBS Core version
- identify supported optional specifications
- identify supported security algorithms
- clearly distinguish proprietary extensions from PBS Core behavior

False or misleading conformance claims undermine interoperability.

---

## 14. Summary

PBS-CONFORMANCE-01 defines the **minimum, enforceable requirements** for interoperable implementations of the Pale Blue Systems Open Standard.

By establishing deterministic parsing rules, a mandatory security baseline, and clear boundaries between required and optional behavior, this document ensures that PBS Core remains reliable infrastructure while allowing innovation and differentiation above the protocol layer.
