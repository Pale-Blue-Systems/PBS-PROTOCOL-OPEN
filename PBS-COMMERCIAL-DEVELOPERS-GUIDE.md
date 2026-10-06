# PBS-COMMERCIAL-DEVELOPERS-GUIDE.md

## A Practical Guide for Commercial Developers and Decision Makers

**Status:** Informational  
**Applies to:** Commercial, Industrial, and Infrastructure Developers Operating in Space, Lunar, and Extreme Environments  
**Related:** PBS-OPEN-STANDARD.md, PBS-CONFORMANCE-01, PBS-ENV-01, PBS-DTN-MAP-01, PBS-DTN-MAP-02, PBS-LNIS-01, PBS-REFERENCES-RESOURCES.md

---

## 1. Purpose

This document is for **commercial developers, architects, and technical managers** building systems that operate in space, on the Moon, in cislunar space, or in other environments with delayed or intermittent connectivity.

It explains:

- what the Pale Blue Systems Open Standard (PBS) defines at a system level
- how a commercial system integrates with PBS while keeping its internal design proprietary
- which PBS specifications apply at each integration step
- how PBS relates to NASA and LunaNet architectures

The normative requirements are in `PBS-RFC-LIB/`; this guide does not change them.

---

## 2. The Problem Commercial Developers Face

Systems beyond Earth operate under conditions that terrestrial networks do not impose:

- intermittent or scheduled connectivity
- long and variable communication delays
- multiple independent operators sharing infrastructure
- safety- and mission-critical data flows
- integration with civil and international systems

Without a shared message format, each pair of operators must agree on bespoke conventions for identity, priority, lifetime and authority. PBS defines those conventions once, as public specifications.

---

## 3. What PBS Provides

PBS defines a **message envelope and extensions** between your internal systems and the transport links used in space.

PBS specifies:

- how a message identifies its source: the 16-byte Source ID of PBS-ENV-01, with optional authority context (PBS-AUTH-01) and addressing (PBS-ADDR-01)
- how a message is packaged and integrity-checked: a fixed 44-byte header protected by a CRC32 (PBS-ENV-01, PBS-SEC-A-01), with cryptographic authentication when the PBS-SEC-B-01 profile applies
- how priority is expressed and preserved: five classes, 0 CRITICAL to 4 BULK, in the header byte at offset 0x01 (PBS-PRIO-01)
- how a message behaves when connections are delayed or unavailable: TTL and timestamp (PBS-ENV-01), Service Intent persistence, deadline and disruption policy (PBS-SVC-01)
- how PBS is carried over DTN/BPv7 and LunaNet services (PBS-DTN-MAP-01, PBS-DTN-MAP-02, PBS-LNIS-01)

PBS does **not** dictate how your internal systems are built.

---

## 4. PBS as an External Interface

**PBS is an external interoperability layer.**

Your system:
- continues to use proprietary data models internally
- retains full control over routing, optimization, and autonomy
- exposes only what is necessary at the PBS boundary

At that boundary PBS gives your system a common format to:
- exchange data with other operators' systems
- integrate with civil infrastructure
- operate in shared environments without a separate adapter per partner

---

## 5. Where PBS Fits in a Commercial Architecture

```text
      Your Applications & Services
   (Proprietary Logic, IP, Optimization)
                 ▲
                 |
      PBS Interface Layer
(Envelope, Priority, Integrity,
 Optional Extensions)
                 ▲
                 |
    Radios / Lasers / Relays /
   DTN Gateways / Ground Links
```

PBS standardizes the **contract between applications and transports**. It replaces neither.

---

## 6. Integration Path for Commercial Developers

### Step 1: Identify the PBS Boundary

Determine where external communication leaves your system:
- uplinks
- cross-vendor interfaces
- shared infrastructure
- civil or international gateways

PBS applies at these points.

---

### Step 2: Build PBS Envelopes

At the boundary:
- wrap outgoing data in a PBS envelope: the 44-byte PBS-ENV-01 header (Magic `0x10`, Priority, Flags, Sequence, Source ID, Timestamp in Unix microseconds, payload Size, TTL in seconds, CRC32) followed by the payload
- set the Priority class (PBS-PRIO-01 Section 4) and TTL
- compute the CRC32 over header bytes 0x00–0x2B with the CRC32 field set to zero (PBS-ENV-01 Section 13.1)
- add optional extensions where the mission profile requires them: Service Intent (PBS-SVC-01), authority context (PBS-AUTH-01), authenticated mission messaging (PBS-SEC-B-01), PNT context (PBS-PNT-CTX-01)

The header CRC32 does not cover the payload and provides no authentication (PBS-ENV-01 Section 16.2, PBS-SEC-A-01). Payload integrity and authentication come from PBS-SEC-B-01 or the application.

The PBS_LINK Python SDK (<https://github.com/Pale-Blue-Systems/PBS_LINK>, version 0.1.3; `from PBS_LINK import PBSLink`) implements the PBS-ENV-01 envelope.

Internally, your data remains unchanged.

---

### Step 3: Optional Capability and Presence Signaling

Where your operation requires it:
- advertise capabilities (PBS-CAPS-01)
- provide presence or position signals (PBS-POS-01)

Both are optional and policy-controlled.

---

### Step 4: DTN and LunaNet Interoperability

If your system interfaces with DTN infrastructure:
- PBS-DTN-MAP-01 defines a gateway translation that places each complete envelope unmodified in one BPv7 payload block
- PBS-DTN-MAP-02 defines BPv7 carriage of v1.4 mission semantics, with bundle lifetime bounded by the PBS deadline or expiry
- PBS-LNIS-01 defines operation over LunaNet IP and BPv7 network services

Your internal systems do not need to be DTN-native; translation happens at the gateway.

---

## 7. Risk Reduction

PBS changes integration cost and dependency in specific ways:

- **Integration:** one published envelope format replaces per-partner conventions
- **Vendor dependency:** internal implementations can change without changing the PBS interface
- **Stability:** the 44-byte header and PBS Core semantics are stable for all v1.x releases (PBS-CONFORMANCE-01 Section 12)
- **Verification:** conformance requirements are public (PBS-CONFORMANCE-01, PBS-CONFORMANCE-02)

---

## 8. What Remains Proprietary

PBS standardizes **inputs and outputs**, not internal behavior.

What remains proprietary:
- routing algorithms
- scheduling and optimization
- autonomy and AI systems
- performance tuning
- commercial service models

Two PBS-conformant systems interoperate at the PBS boundary while differing in all of the above.

---

## 9. Considerations for Technical Management

PBS adoption affects:

- partner onboarding: a partner that implements PBS needs no bespoke message format
- integration cost: one interface implementation serves multiple partners
- NASA/LunaNet traceability: PBS v1.4 traces to NASA FY26 need statements 13.09, 15.01, 15.03 and 24.05 and to LNIS V005 (PBS-TRACE-NASA-FY26-01). No PBS-CONFORMANCE-02 verification records are published.

---

## 10. References

PBS v1.4 traces to:
- NASA *FY26 Civil Space Shortfall Prioritization* need statements 13.09, 15.01, 15.03 and 24.05 (PBS-TRACE-NASA-FY26-01)
- LunaNet Interoperability Specification Version 5 (PBS-LNIS-01)
- IETF RFC 9171, Bundle Protocol Version 7 (PBS-DTN-MAP-01, PBS-DTN-MAP-02)

Start with:
- `PBS-OPEN-STANDARD.md`
- `PBS-RFC-LIB/PBS-ENV-01.md`
- `PBS-RFC-LIB/PBS-CONFORMANCE-01.md`
- `PBS-RFC-LIB/PBS-DTN-MAP-02.md`
- `PBS-REFERENCES-RESOURCES.md`

All referenced documents are publicly available.

---

## 11. Summary

PBS is an open communication standard that commercial systems implement at their external interfaces. Inside that boundary, each system keeps its own design, data models and intellectual property.
