# Pale Blue Systems – Open Communication Standards

This repository contains the **open communication standards stewarded by the Pale Blue Systems Foundation (PBSF)**: the PBS protocol specifications, their conformance profiles, the governance documents, and the alignment and traceability records that relate PBS to external sources.

The standards in this repository define a shared **mission-semantic interoperability language** that allows spacecraft, rovers, habitats, autonomous systems, and ground applications to preserve mission meaning, authority, service intent, priority, freshness, security requirements, and PNT context across heterogeneous networks and independently operated service providers.

The PBS specifications define a fixed 44-byte message envelope and a set of optional extensions. Together they carry mission semantics with the data: source identity, priority, timestamp and lifetime, Service Intent, authority context, security profile and PNT context. The specifications define the same semantics over IP, BPv7 and mission-specific links and across independently operated service providers.

---

## Context and Intent

Pale Blue Systems publishes these standards in anticipation of a future space environment that includes **multiple space agencies, commercial operators, scientific missions, private infrastructure, and long-lived off-Earth systems operating concurrently**.

PBS addresses an operating environment in which space agencies, commercial operators and science missions run independently built systems that exchange data over shared relays and networks. For the Moon, the LunaNet Interoperability Specification (LNIS V005, NASA, ESA and JAXA, 29 January 2025) describes LunaNet as a network of cooperating networks on which LunaNet Service Providers deliver communications, PNT and other services, and expects user needs to be met by a combination of interoperable providers (LNIS V005 Preface and Section 1).

This repository establishes a durable mission-semantic interoperability standard for the multi-provider lunar, cislunar, planetary, and deep-space operating environment. It makes interoperability, authority, service intent, and coordination requirements **explicit and addressable early**, before architectural assumptions become embedded in deployed infrastructure.

Additional context on why this work is published now, and the long-term architectural motivations behind it, is available in [`WHY-NOW.md`](WHY-NOW.md).

---

## Why This Repository Exists

As space operations move toward sustained lunar presence, cislunar infrastructure, and Mars exploration, missions increasingly depend on distributed systems operating across:

- long and variable communication delays
- intermittent or scheduled connectivity
- multiple independent authorities and vendors
- human-rated, safety-critical environments

Under these conditions, data must be stored and forwarded between contacts, and its meaning, priority and authority must survive the transfer between organizations.

Strategic analysis has formally identified communications, networking, and coordination as critical technology shortfalls for future exploration architectures, including the need for systems that operate reliably across deep-space and planetary environments.

PBSF exists to steward open standards that directly address these conditions.

NASA's *FY26 Civil Space Shortfall Prioritization* (Space Technology Mission Directorate, May 2026) includes four need statements that PBS v1.4 traces to:

| Need ID | Need statement |
|---|---|
| 13.09 | “Provide advanced networking needed for multi-spacecraft responsive space operations.” |
| 15.01 | “Provide scalable, reliable surface-to-surface communications between assets on the lunar surface that is usable by all participating elements.” |
| 15.03 | “Achieve safe, efficient human-robot interactions for exploration missions, secure command and control over high-latency, bandwidth-limited networks, or implement reliable automated safing sequences.” |
| 24.05 | “Develop a lunar position, navigation, and timing architecture capable of scaling to long term operational needs.” |

Source: <https://www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf>. The requirements PBS derives from them are in [`PBS-TRACE-NASA-FY26-01`](PBS-ALIGNMENT-LIB/PBS-TRACE-NASA-FY26-01.md).

---

## What This Repository Contains

### Specifications

[`PBS-RFC-LIB/`](PBS-RFC-LIB/) contains 19 specifications. PBS Core comprises four specifications with Status Core. A PBS Core conformant implementation implements PBS-ENV-01, PBS-PRIO-01 and PBS-SEC-A-01 (PBS-CONFORMANCE-01 Section 3) and meets the further MUST requirements of PBS-CONFORMANCE-01 Sections 4–9 and 12. The remaining specifications are optional extensions, interoperability and conformance profiles, and governance.

### Reference Implementation

The PBS_LINK Python SDK (<https://github.com/Pale-Blue-Systems/PBS_LINK>, distribution `pbs-link` 0.1.3, import package `PBS_LINK`) implements the PBS-ENV-01 v1.3 envelope. It is maintained in its own repository.

### Hardware Reference Designs

[`PBS-HW-LIB/`](PBS-HW-LIB/) holds open reference designs for hardware that carries PBS traffic: a swappable surface communication module (PBS-HW-SCM-01) and a master device identity tag that can be fitted to any unit (PBS-HW-ID-01). They are informational and do not affect PBS conformance.

### Governance and Alignment

[`PBS-OPEN-STANDARD.md`](PBS-OPEN-STANDARD.md) and [`PBS-GOV-01`](PBS-RFC-LIB/PBS-GOV-01.md) define the stewardship and change process. [`PBS-ALIGNMENT-LIB/`](PBS-ALIGNMENT-LIB/) holds the alignment documents and the NASA FY26 traceability matrix.

---

## Architectural Context

PBS operates at the boundary between mission applications and network services.

```text
Mission Applications
(Rovers, Landers, Habitats, Robots, Ops Software)
          │
          ▼
Pale Blue Systems Open Standards
(Mission Semantics, Service Intent, Authority,
 Security Requirements, PNT Context)
          │
          ▼
Interoperable Network Services
(LunaNet, IP, BPv7, BPSec, CCSDS)
          │
          ▼
Provider / Link Infrastructure
(LNSPs, Relays, RF, Optical, 3GPP, Wi-Fi, Ground)
```

PBS envelopes are user-application data to the network services below them (PBS-LNIS-01 Section 2). PBS-LNIS-REQ-007 requires provider transitions to preserve Source ID, authority context, priority, Service Intent and protected application payload.

---

## Relationship to DTN and BPv7

PBS operates over IP, over BPv7, or through a gateway that selects between them (PBS-LNIS-01 Sections 2 and 4). Two optional specifications define carriage over BPv7. Neither supersedes the other. PBS-DTN-MAP-01 references PBS-DTN-MAP-02 Section 4 for the lifetime bound and Section 5 for the mapping profile of priority-based network treatment.

- **PBS-DTN-MAP-01** (v1.5) defines a gateway translation between PBS-native domains and DTN domains. Each PBS envelope maps to exactly one bundle (Section 5.1). The complete envelope, 44-byte header and payload, is placed unmodified in a single BPv7 payload block (Section 6.2). The bundle lifetime does not exceed the time remaining until the envelope expires, and an envelope with TTL 0 takes the gateway's documented no-expiry lifetime unless a PBS-DTN-MAP-02 Section 4 finite limit applies (Sections 6.1 and 6.1.1). The gateway's bundle protocol agent assigns the creation timestamp (Section 6.1). No primary block field carries priority; a gateway that requests network treatment covers all five priority classes and documents the mechanism in a mapping profile (Section 6.3). Source IDs map deterministically to endpoint identifiers (Section 8).
- **PBS-DTN-MAP-02** (v1.5) defines carriage of v1.4 mission semantics over BPv7 for gateways and endpoints. One PBS protocol data unit SHOULD map to one BP application data unit (Section 2). Bundle lifetime SHALL be bounded by the remaining PBS deadline or expiry; when no finite limit applies it is the no-expiry lifetime documented in the mapping profile (Section 4). The adapter preserves PBS priority unchanged; network treatment is selected through BP QoS mechanisms and provider policy (Section 5). Section 6 maps Service Intent values to BPv7 adapter behavior.

PBS-CONFORMANCE-01 Section 3.1 lists both PBS-DTN-MAP-01 and PBS-DTN-MAP-02 as optional. PBS-ENV-01, PBS-ADDR-01 and PBS-ROUTE-01 reference PBS-DTN-MAP-01. PBS-DTN-MAP-01, PBS-SVC-01, PBS-SEC-B-01, PBS-LNIS-01, PBS-QOS-MAP-01, PBS-CONFORMANCE-02 and the NASA FY26 traceability matrix reference PBS-DTN-MAP-02.

---

## External Alignment

Each alignment document identifies its external sources, summarizes what they state, and maps those statements to PBS specification sections. No source names PBS, and no alignment claims endorsement.

| Alignment ID | Source | Identifier |
| :--- | :--- | :--- |
| [PBS-ALIGN-NASA-LCRNS-02](PBS-ALIGNMENT-LIB/PBS-ALIGN-NASA-LCRNS-02.md) | NASA STMD, *FY26 Civil Space Shortfall Prioritization* (2026); NASA, ESA and JAXA, *LunaNet Interoperability Specification*, V005 (2025) | [FY26 PDF](https://www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf), [LNIS V005 PDF](https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf) |
| [PBS-ALIGN-NASA-LCRNS-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-NASA-LCRNS-01.md) | Esper, Heckler, Verville and Ryden, “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS)”, SpaceOps 2025 | [NTRS 20250003321](https://ntrs.nasa.gov/citations/20250003321) |
| [PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01.md) | Verville and Eddy, “Onboard Processing for LunaNet Data Services”, 2025 IEEE Aerospace Conference | doi:10.1109/AERO63441.2025.11068727 |
| [PBS-ALIGN-IEEE-AEROCONF-2025-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-IEEE-AEROCONF-2025-01.md) | Templin et al., “High Performance DTN Using Larger Packets and Kernel Resident Convergence Layers”, 2025 IEEE Aerospace Conference | doi:10.1109/AERO63441.2025.11068517 |
| [PBS-ALIGN-CARBONARA-TNTN-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-CARBONARA-TNTN-01.md) | Carbonara et al., “Hands-On Solutions for Testing Integrated Terrestrial and Non-Terrestrial Networks: A Comprehensive Survey”, *IEEE Open Journal of the Communications Society*, 2025 | doi:10.1109/OJCOMS.2025.3646364 |
| [PBS-ALIGN-NTONTIN-6G-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-NTONTIN-6G-01.md) | Ntontin et al., “A Vision, Survey, and Roadmap Toward Space Communications in the 6G and Beyond Era”, *Proceedings of the IEEE*, 2025 | doi:10.1109/JPROC.2024.3512934 |
| [PBS-ALIGN-SPJ-LEO-2022-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-SPJ-LEO-2022-01.md) | Zhang et al., “LEO Mega Constellations: Review of Development, Impact, Surveillance, and Governance”, *Space: Science & Technology*, 2022 | doi:10.34133/2022/9865174 |
| [PBS-ALIGN-TF-GOVERNANCE-2024-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-TF-GOVERNANCE-2024-01.md) | Beaumier, Couette and Morin, “Hybrid Organisations and Governance Systems: The Case of the European Space Agency”, *Journal of European Public Policy*, 2025 | doi:10.1080/13501763.2024.2325647 |

[PBS-ALIGN-INDEX-01](PBS-ALIGNMENT-LIB/PBS-ALIGN-INDEX-01.md) summarizes each alignment. [PBS-TRACE-NASA-FY26-01](PBS-ALIGNMENT-LIB/PBS-TRACE-NASA-FY26-01.md) traces 19 PBS requirements to the FY26 need statements, LNIS V005 and RFC 9171.

---

## External Alignment & Validation

The Pale Blue Systems Open Standard is explicitly aligned with authoritative, peer-reviewed architectures from major space agencies and technical bodies.

| Alignment ID | External Source | Domain |
| :--- | :--- | :--- |
| **PBS-ALIGN-NASA-LCRNS-01** | NASA LCRNS (Esper, 2025) | Lunar & Cislunar Networking |
| **PBS-ALIGN-IEEE-AEROCONF-2025** | IEEE Aerospace Conference | Space Network Architecture |
| **PBS-ALIGN-IEEE-TNTN-2025** | IEEE ComSoc | Integrated T/NTN Networks |

---

## Open Standards and Stewardship

PBSF is intentionally structured as a neutral foundation stewarding open standards and reference specifications.

- The specifications are public under the Apache License 2.0.
- PBS-GOV-01 Sections 2 and 3 separate stewardship of the specifications from commercial implementation.
- Changes to PBS Core follow the RFC lifecycle of PBS-GOV-01 Section 5. A backward-incompatible change requires a new major version, except a corrective change, which leaves the wire format unchanged and is released in a patch or minor version with migration guidance where needed (PBS-GOV-01 Sections 5.2 and 6).
- Implementations may extend PBS above the protocol layer. Proprietary extensions are not PBS Core (PBS-GOV-01 Section 7).
- Commercial products and mission systems may implement or extend the standards without altering the core language.

This model enables adoption across civil, commercial, and international space programs while allowing innovation and competition above the protocol layer.

---

## Repository Structure

```text
/
├── README.md
├── WHY-NOW.md                              → Reasons for publishing now
├── PBS-OPEN-STANDARD.md                    → Open standard scope and stewardship model
├── PBS-PROTOCOL-CHANGELOG.md               → Release history
├── PBS-COMMERCIAL-DEVELOPERS-GUIDE.md      → Guide for commercial implementers
├── PBS-REFERENCES-RESOURCES.md             → External references
├── PBS-REFERENCES-SOLAR-SYSTEM-INTERNET.md → IPNSIG Solar System Internet report and PBS-ALIGN-SSIAG-01
├── CONTRIBUTING.md, CLA.md, TRADEMARK-USAGE-POLICY.md, LICENSE
├── PRESS/                                  → Press releases
├── PBS-ALIGNMENT-LIB/                      → Alignment documents and NASA FY26 traceability
│   ├── PBS-ALIGN-INDEX-01.md               → Alignment Index
│   ├── PBS-ALIGN-NASA-LCRNS-01.md          → NASA LCRNS (Esper et al., SpaceOps 2025)
│   ├── PBS-ALIGN-NASA-LCRNS-02.md          → NASA LCRNS, LunaNet, and FY26 Civil Space Shortfalls
│   ├── PBS-ALIGN-IEEE-AEROCONF-2025-01.md  → High-Performance DTN Convergence Layers (Templin et al.)
│   ├── PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01.md → Onboard Processing for LunaNet Data Services (Verville and Eddy)
│   ├── PBS-ALIGN-CARBONARA-TNTN-01.md      → Integrated Terrestrial and Non-Terrestrial Network Testbeds
│   ├── PBS-ALIGN-NTONTIN-6G-01.md          → Space Communications in the 6G and Beyond Era
│   ├── PBS-ALIGN-SPJ-LEO-2022-01.md        → LEO Mega Constellations
│   ├── PBS-ALIGN-TF-GOVERNANCE-2024-01.md  → Space Governance and Hybrid Organisations
│   ├── PBS-ALIGN-ASSIGNMENT-NASA-FY26-01.md → NASA FY26 / LunaNet Alignment Assignment
│   └── PBS-TRACE-NASA-FY26-01.md           → NASA FY26 Requirements Traceability Matrix
└── PBS-RFC-LIB/                            → Protocol specifications
    ├── PBS-ENV-01.md                       → Core Message Envelope
    ├── PBS-ADDR-01.md                      → Addressing and Identification
    ├── PBS-MUX-01.md                       → Payload Multiplexing and Semantic Framing
    ├── PBS-PRIO-01.md                      → Priority Classification and Deterministic Handling
    ├── PBS-SEC-A-01.md                     → Integrity Verification and Security Boundaries
    ├── PBS-POS-01.md                       → Position and Presence Signaling
    ├── PBS-CAPS-01.md                      → Capability Advertisement and Discovery
    ├── PBS-ROUTE-01.md                     → Routing and Forwarding Semantics
    ├── PBS-DTN-MAP-01.md                   → Mapping to Delay/Disruption Tolerant Networking (DTN)
    ├── PBS-CONFORMANCE-01.md               → Conformance, Interoperability, and Mandatory Baselines
    ├── PBS-SVC-01.md                       → Mission Service Intent
    ├── PBS-AUTH-01.md                      → Authority and Scope Context
    ├── PBS-SEC-B-01.md                     → Authenticated Mission Messaging
    ├── PBS-PNT-CTX-01.md                   → Position, Navigation, and Timing Context
    ├── PBS-LNIS-01.md                      → LunaNet Application Alignment Profile
    ├── PBS-DTN-MAP-02.md                   → Mapping to BPv7 Delay/Disruption Tolerant Networking
    ├── PBS-QOS-MAP-01.md                   → Mission Intent to Network Treatment Mapping
    ├── PBS-CONFORMANCE-02.md               → NASA/LunaNet Alignment Conformance and Verification Profile
    └── PBS-GOV-01.md                       → Governance, Stewardship, and Evolution of the PBS Open Standard
```

---

### Quick Links

| Document | Title | Version | Status |
| ------- | ----------- | ---: | ----------- |
| [PBS-OPEN-STANDARD.md](PBS-OPEN-STANDARD.md) | Scope, Stewardship, and Open Standard Model | — | Informational |
| [PBS-ENV-01](PBS-RFC-LIB/PBS-ENV-01.md) | Core Message Envelope | 1.5 | Core |
| [PBS-PRIO-01](PBS-RFC-LIB/PBS-PRIO-01.md) | Priority Classification and Deterministic Handling | 1.4 | Core |
| [PBS-SEC-A-01](PBS-RFC-LIB/PBS-SEC-A-01.md) | Integrity Verification and Security Boundaries | 1.5 | Core |
| [PBS-CONFORMANCE-01](PBS-RFC-LIB/PBS-CONFORMANCE-01.md) | Conformance, Interoperability, and Mandatory Baselines | 1.5 | Core |
| [PBS-ADDR-01](PBS-RFC-LIB/PBS-ADDR-01.md) | Addressing and Identification | 1.3 | Optional Extension |
| [PBS-MUX-01](PBS-RFC-LIB/PBS-MUX-01.md) | Payload Multiplexing and Semantic Framing | 1.4 | Optional Extension |
| [PBS-POS-01](PBS-RFC-LIB/PBS-POS-01.md) | Position and Presence Signaling | 1.4 | Optional Extension |
| [PBS-CAPS-01](PBS-RFC-LIB/PBS-CAPS-01.md) | Capability Advertisement and Discovery | 1.3 | Optional Extension |
| [PBS-ROUTE-01](PBS-RFC-LIB/PBS-ROUTE-01.md) | Routing and Forwarding Semantics | 1.5 | Optional |
| [PBS-DTN-MAP-01](PBS-RFC-LIB/PBS-DTN-MAP-01.md) | Mapping to Delay/Disruption Tolerant Networking (DTN) | 1.5 | Optional (Interoperability) |
| [PBS-SVC-01](PBS-RFC-LIB/PBS-SVC-01.md) | Mission Service Intent | 1.4 | Optional Extension |
| [PBS-AUTH-01](PBS-RFC-LIB/PBS-AUTH-01.md) | Authority and Scope Context | 1.4 | Optional Extension; Required by PBS-SEC-B command profile |
| [PBS-SEC-B-01](PBS-RFC-LIB/PBS-SEC-B-01.md) | Authenticated Mission Messaging | 1.5 | Optional Security Profile |
| [PBS-PNT-CTX-01](PBS-RFC-LIB/PBS-PNT-CTX-01.md) | Position, Navigation, and Timing Context | 1.4 | Optional Extension |
| [PBS-LNIS-01](PBS-RFC-LIB/PBS-LNIS-01.md) | LunaNet Application Alignment Profile | 1.4 | Optional Interoperability Profile |
| [PBS-DTN-MAP-02](PBS-RFC-LIB/PBS-DTN-MAP-02.md) | Mapping to BPv7 Delay/Disruption Tolerant Networking | 1.5 | Optional Interoperability Profile |
| [PBS-QOS-MAP-01](PBS-RFC-LIB/PBS-QOS-MAP-01.md) | Mission Intent to Network Treatment Mapping | 1.4 | Optional Adapter Profile |
| [PBS-CONFORMANCE-02](PBS-RFC-LIB/PBS-CONFORMANCE-02.md) | NASA/LunaNet Alignment Conformance and Verification Profile | 1.5 | Optional Conformance Profile |
| [PBS-GOV-01](PBS-RFC-LIB/PBS-GOV-01.md) | Governance, Stewardship, and Evolution of the PBS Open Standard | 1.5 | Informational (Normative Governance) |

---

## Status

The current release is PBS v1.5.0 (2026-10-06), a corrective release (PBS-GOV-01 Section 5.2) that resolves the six known issues recorded in PBS v1.4.1. PBS v1.5.0 does not change the wire format; it changes relay, gateway and BPv7 mapping requirements, and [`PBS-PROTOCOL-CHANGELOG.md`](PBS-PROTOCOL-CHANGELOG.md) gives the migration.

Each specification carries its own version, the minor release in which it last changed. Documents unchanged since v1.3 remain at 1.3 and documents unchanged since v1.4 remain at 1.4; an erratum does not change a specification's version. Errata are recorded in the header of each corrected specification (**Errata** line); a specification revised in v1.5.0 records its changes in a **Changes** line. Both are recorded in [`PBS-PROTOCOL-CHANGELOG.md`](PBS-PROTOCOL-CHANGELOG.md). Defects in normative text that v1.5.0 does not correct are listed under [Known issues](PBS-PROTOCOL-CHANGELOG.md#known-issues-not-corrected-in-v150).

The specifications define wire formats and behavior independent of hardware, transport and implementation language. The 44-byte PBS-ENV-01 header structure and PBS Core semantics remain stable for all v1.x releases. A backward-incompatible change requires a new major version, except a corrective change, which leaves the wire format unchanged and is released in a patch or minor version with migration guidance where needed, as in PBS v1.5.0 (PBS-CONFORMANCE-01 Section 12, PBS-GOV-01 Sections 5.2 and 6).

---

## Legal and Governance

### License
The Pale Blue Systems Open Standard and reference implementations are released under the **Apache License 2.0**.  
See [`LICENSE`](LICENSE) for details.

### Intellectual Property & Contribution
To ensure long-term neutrality and availability, all contributions are subject to the Pale Blue Systems Foundation **Contributor License Agreement (CLA)**.  
See [`CLA.md`](CLA.md) for full terms.

### Trademark Usage
"Pale Blue Systems", "PBSF", and the PBS logo are trademarks of the Pale Blue Systems Foundation.  
See [`TRADEMARK-USAGE-POLICY.md`](TRADEMARK-USAGE-POLICY.md) for guidelines.

---

## About the Foundation

The Pale Blue Systems Foundation stewards open, interoperable communication standards to support humanity’s expansion into space through cooperation, reliability, and technical clarity. It stewards the PBS specifications in this repository under the governance model of PBS-GOV-01.
