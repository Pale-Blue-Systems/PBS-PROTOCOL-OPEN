# PBS Open Standard  
## Scope, Stewardship, and Open Standard Model

This document defines the **Pale Blue Systems (PBS) Open Standard**: its scope, intent, stewardship model, and relationship to commercial implementations.

It is an informational document describing how the PBS Open Standard is governed and evolved.  
It does **not** define protocol behavior and does **not** supersede any normative specification in `PBS-RFC-LIB/`.

---

## Purpose of the PBS Open Standard

The PBS Open Standard defines a **shared communication language** for systems operating in space, lunar, planetary, and other delay- and disruption-prone environments.

Its purpose is to let independently developed systems—civil, commercial, and international—exchange data with consistent meaning across heterogeneous networks without shared vendors, shared hardware, or proprietary disclosure.

---

## Scope of the Open Standard

The PBS Open Standard encompasses:

- the 44-byte message envelope (PBS-ENV-01) and priority classification (PBS-PRIO-01)  
- header integrity verification (PBS-SEC-A-01) and the optional authenticated mission messaging profile (PBS-SEC-B-01)  
- optional authority, addressing, Service Intent, PNT context, position, capability and routing extensions  
- mappings to DTN/BPv7 (PBS-DTN-MAP-01, PBS-DTN-MAP-02) and LunaNet network services (PBS-LNIS-01)  
- conformance requirements (PBS-CONFORMANCE-01, PBS-CONFORMANCE-02) and governance (PBS-GOV-01)  

These elements together define **how messages behave and are interpreted**, independent of physical transport, hardware platform, or implementation language.

---

## What Constitutes the PBS Core

All PBS specifications are maintained in the `PBS-RFC-LIB/` directory.

The **PBS Core** is the set of specifications a PBS Core conformant implementation must implement: PBS-ENV-01, PBS-PRIO-01 and PBS-SEC-A-01 (PBS-CONFORMANCE-01 Section 3). The other specifications are optional extensions and profiles; an implementation that claims one implements it fully (PBS-CONFORMANCE-01 Section 3.1).

PBS Core covers:

- protocol semantics  
- on-wire behavior  
- interoperability rules  

The 44-byte header structure and PBS Core semantics remain stable for all v1.x releases; a backward-incompatible change requires a new major version (PBS-CONFORMANCE-01 Section 12, PBS-GOV-01 Section 6).

---

## Open Standard Model

PBS is released and maintained as an **open standard**.

In this context, “open standard” means:

- the protocol specifications are publicly available under the Apache License 2.0  
- the semantics and wire formats are versioned and reviewable  
- no single commercial entity controls the evolution of the standard (PBS-GOV-01 Section 3.2)  
- independent implementations are permitted, open or proprietary (PBS-GOV-01 Section 10)  

---

## Stewardship and Governance

The PBS Open Standard is stewarded by the **Pale Blue Systems Foundation (PBSF)** (PBS-GOV-01 Section 3.1).

PBSF is responsible for:

- maintaining the PBS Core specifications  
- reviewing and accepting changes to the standard  
- managing versioning and backward compatibility  
- publishing conformance guidance  
- ensuring long-term neutrality and interoperability  

PBSF does not develop mission-specific software, operate networks, or deploy infrastructure (PBS-GOV-01 Section 3.1).

---

## Relationship to Commercial Implementations

Commercial entities may build products, services, and mission systems that implement or extend the PBS Open Standard.

This includes, but is not limited to, products and services developed by **Pale Blue Systems Inc.**

Commercial implementations may:

- optimize performance  
- integrate with mission-specific hardware or software  
- provide tooling, support, or managed services  
- extend functionality above the protocol layer  

Commercial implementations may not alter the PBS Core semantics or claim ownership of the standard itself.

---

## Separation of Roles

The separation between standard stewardship and commercial activity is intentional.

- **PBSF** stewards the open standard and protects its neutrality  
- **Commercial entities** compete and innovate through implementations  

Under this separation, an implementer depends on the published specifications, not on a particular vendor's implementation.

---

## Evolution of the Standard

Changes to the PBS Open Standard follow the RFC lifecycle of PBS-GOV-01 Section 5. Changes to PBS Core are governed by:

- technical review  
- interoperability impact  
- backward-compatibility guarantees  

Experimental features, mission-specific adaptations, and proprietary extensions are not part of PBS Core (PBS-GOV-01 Section 7).

---

## Relationship to This Repository

This repository is the **authoritative public source** of the PBS Open Standard.

It contains:

- the current version of every PBS specification  
- governance and stewardship documentation  
- version history, alignment records and traceability  

It does not contain mission software or commercial implementations. The PBS_LINK Python reference SDK is maintained separately at <https://github.com/Pale-Blue-Systems/PBS_LINK>.

---

## Summary

The PBS Open Standard defines a vendor-neutral message envelope and extensions for space and other delay- and disruption-prone environments.

It is stewarded by the Pale Blue Systems Foundation (PBSF) under PBS-GOV-01 and may be implemented by any party.
