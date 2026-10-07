# PBS Alignment  
## NASA Lunar Communications Relay and Navigation Systems (LCRNS)

**Alignment Identifier:** `PBS-ALIGN-NASA-LCRNS-01`

---

## Aligned Work

Esper, Jaime, Gregory Heckler, Jonathan Verville, and Grant Ryden.  
“NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).”  
*18th International Conference on Space Operations (SpaceOps 2025)*, Montreal, Canada, 26–30 May 2025, paper ID 257.  
NASA Technical Reports Server 20250003321, <https://ntrs.nasa.gov/citations/20250003321>.

---

## Alignment Overview

Esper et al. describe the LCRNS project of NASA's Space Communications and Navigation (SCaN) program. Cislunar space has no existing communications, position, navigation or timing infrastructure (Section 1). The LCRNS charter is to enable an interoperable commercial lunar communications and navigation orbiting service infrastructure that meets NASA's needs and extends to Moon-to-Mars missions (Abstract). Intuitive Machines was selected in 2024 through the Near Space Network Services (NSNS) call as the first commercial LCRNS service provider; NASA is expected to be one of many users of LCRNS services (Section 2).

PBS is application-layer protocol data carried over the network services such relays provide (PBS-LNIS-01 Section 2). The dimensions below map statements in the paper to PBS specification sections.

**Planned architecture (in development):** Pale Blue Systems (PBS) aligns with the LCRNS architecture by providing a governance-aware interoperability and translation layer capable of operating across independently governed lunar, cislunar, and terrestrial networks. PBS complements LCRNS by enabling policy-aware coordination among heterogeneous systems without imposing centralized control or constraining internal provider architectures.

---

## Alignment Dimensions

### Network of Cooperating Networks

LCRNS follows the LunaNet Interoperability Specification (LNIS). LunaNet is envisioned as a network of cooperating networks on which providers deliver communications, PNT and other services. LCRNS, ESA's Moonlight and JAXA's Lunar Navigation Satellite System providers are expected to be interoperable. Commercial providers may offer services outside LNIS (Section 2).

**PBS alignment:**  
PBS-LNIS-REQ-001 requires PBS envelope and Service Intent semantics to be preserved across LunaNet Service Provider (LNSP) boundaries. PBS-LNIS-REQ-007 requires provider transitions to preserve Source ID, authority context, priority, Service Intent and protected payload.

**Alignment Reference:** `PBS-ALIGN-LCRNS-ARCH-01`

---

### Interoperability as an Operational Requirement

LCRNS standardization is LNIS, which includes CCSDS and IETF networking standards (Table 1). The paper records the early design study (DRM-0) as the point at which interoperability became an operational requirement (Section 3.1).

**PBS alignment:**  
PBS defines user-application semantics above those standards and does not replace them (PBS-GOV-01 Section 9). PBS-LNIS-REQ-002 and PBS-LNIS-REQ-003 bind PBS to the LunaNet BPv7 and IP network services.

**Alignment Reference:** `PBS-ALIGN-LCRNS-INT-02`

---

### Onboard Routing and Store-and-Forward Service

LCRNS relays perform onboard modulation and coding, route bundles and packets digitally based on user data, and offer real-time and store-and-forward data services at the link layer or over IP or DTN (Table 1). Earth–Moon transmission latency drives onboard processing and storage into the relays (Section 4).

**PBS alignment:**  
PBS-SVC-01 Section 9 carries the application's disruption policy (`CONTINUOUS_PATH`, `STORE_FORWARD`, `EITHER`) and Section 7 its persistence policy. PBS-DTN-MAP-02 Section 4 bounds bundle lifetime by the remaining PBS deadline or expiry, so store-and-forward retention does not extend a message beyond its mission validity.

**Alignment Reference:** `PBS-ALIGN-LCRNS-DTN-03`

---

### Lunar PNT Services

LCRNS provides a one-way Augmented Forward Service (AFS) broadcast, the Lunar Augmented Navigation Service (four or more satellites in view) and a peer-to-peer ranging service. The LCRNS PNT Instrument (LPI) estimates relay state against GPS time; predicted states are transformed into the Moon principal-axis (Moon-PA) body frame for broadcast (Section 6).

**PBS alignment:**  
PBS-PNT-CTX-01 requires coordinate-bearing PNT data to identify its spatial reference frame (PBS-PNT-REQ-001) and time-bearing data its time reference (PBS-PNT-REQ-002), and requires LunaNet-aligned deployments to support identifiers for the governing lunar reference system and time reference (PBS-PNT-REQ-006).

**Alignment Reference:** `PBS-ALIGN-LCRNS-PNT-04`

---

### Verification at the Interface

LCRNS is developing an Interoperability and Performance Validation Capability. Its Interoperability and Performance Testbed (IPT) is a hardware-in-the-loop testbed emulating a universal lunar user terminal. The IPT tests each LNSP segment at its interface; LNSP-internal links are not tested (Section 5).

**PBS alignment:**  
PBS-CONFORMANCE-02 verifies PBS at the application interface with test cases PBS-C02-T001 to PBS-C02-T016 (Section 3). Section 4 requires disruption tests covering complete outage, delayed contact, asymmetric link availability, constrained throughput and service restoration.

**Alignment Reference:** `PBS-ALIGN-LCRNS-VER-05`

---

### Extension Beyond the Moon

The paper states that the cislunar networking and interoperability approach lays the groundwork for similar capabilities for Mars and other deep-space missions (Section 1).

**PBS alignment:**  
PBS-PNT-CTX-01 covers lunar, cislunar, planetary, terrestrial and local mission frames (Section 1). PBS Core (PBS-ENV-01, PBS-PRIO-01, PBS-SEC-A-01) contains no body-specific field. LunaNet-specific requirements appear only in optional specifications: PBS-LNIS-01, PBS-CONFORMANCE-02, PBS-PNT-CTX-01 (PBS-PNT-REQ-006), PBS-POS-01 Section 13 and PBS-DTN-MAP-02 Section 7.

**Alignment Reference:** `PBS-ALIGN-LCRNS-FUT-06`

---

## Planned Architecture (in development)

Pale Blue Systems is building PBS to the following architecture for LCRNS and LunaNet environments.

### Network-of-Networks Architecture

PBS is architected to operate within network-of-networks environments, enabling interoperable data exchange across autonomous systems while preserving operational independence. PBS provides a neutral interstitial layer that allows cooperating networks to coordinate without requiring shared internal designs.

### Interoperability and Open Standards

PBS operates above CCSDS, IETF, DTN, IP, and related standards, enabling translation and coordination across compliant systems without requiring identical implementations. PBS preserves payload opacity while mediating routing and exchange context across domains.

### Commercial Multi-Provider Ecosystem

NASA positions LCRNS as a commercially provided service environment, where NASA acts as one customer among many. Providers retain independent internal architectures and compete on performance, coverage, and service offerings.

**PBS alignment:**  
PBS is designed to support commercial multi-provider ecosystems by enabling interoperability at defined exchange boundaries. It allows providers to maintain proprietary internal systems while participating in a shared interoperable lunar communications environment.

### Governance, Authority, and Safety

PBS provides explicit authority-context handling and policy-aware routing, enabling deterministic interoperability across independently governed systems. Its design supports auditability and safety without requiring payload inspection or centralized trust.

### Strategic Extensibility: Moon to Mars

NASA frames LCRNS as a foundational architecture extensible beyond lunar operations toward future Moon-to-Mars and deep-space networked missions.

**PBS alignment:**  
PBS is orbit-agnostic and mission-agnostic, designed to persist across mission eras and celestial domains. Its architecture supports progressive expansion without requiring architectural reset as operational scope evolves.

---

## Alignment Summary

Esper et al. describe LCRNS as commercially provided, LNIS-interoperable lunar relay and navigation services with onboard routing, store-and-forward storage and interface-level verification. PBS carries mission semantics over those services and specifies, for the user side, semantic preservation across providers (PBS-LNIS-01), disruption and lifetime handling (PBS-SVC-01, PBS-DTN-MAP-02), PNT reference identification (PBS-PNT-CTX-01) and interface-level verification (PBS-CONFORMANCE-02).

**Planned architecture (in development):** Pale Blue Systems aligns with this architecture by providing a governance-aware interoperability layer that enables policy-consistent data exchange across autonomous lunar, cislunar, and terrestrial networks. Together, LCRNS defines the interoperable lunar infrastructure, while PBS enables scalable, multi-authority coordination within that environment.

---

## Citation (MLA)

Esper, Jaime, et al. “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).” *18th International Conference on Space Operations (SpaceOps 2025)*, Montreal, 26–30 May 2025, NASA Technical Reports Server 20250003321, ntrs.nasa.gov/citations/20250003321.
