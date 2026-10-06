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
PBS-CONFORMANCE-02 verifies PBS at the application interface with test cases PBS-C02-T001 to PBS-C02-T015 (Section 3). Section 4 requires disruption tests covering complete outage, delayed contact, asymmetric link availability, constrained throughput and service restoration.

**Alignment Reference:** `PBS-ALIGN-LCRNS-VER-05`

---

### Extension Beyond the Moon

The paper states that the cislunar networking and interoperability approach lays the groundwork for similar capabilities for Mars and other deep-space missions (Section 1).

**PBS alignment:**  
PBS-PNT-CTX-01 covers lunar, cislunar, planetary, terrestrial and local mission frames (Section 1). PBS Core (PBS-ENV-01, PBS-PRIO-01, PBS-SEC-A-01) contains no body-specific field. LunaNet-specific requirements are confined to PBS-LNIS-01, PBS-CONFORMANCE-02 and PBS-PNT-REQ-006.

**Alignment Reference:** `PBS-ALIGN-LCRNS-FUT-06`

---

## Alignment Summary

Esper et al. describe LCRNS as commercially provided, LNIS-interoperable lunar relay and navigation services with onboard routing, store-and-forward storage and interface-level verification. PBS carries mission semantics over those services and specifies, for the user side, semantic preservation across providers (PBS-LNIS-01), disruption and lifetime handling (PBS-SVC-01, PBS-DTN-MAP-02), PNT reference identification (PBS-PNT-CTX-01) and interface-level verification (PBS-CONFORMANCE-02).

---

## Citation (MLA)

Esper, Jaime, et al. “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).” *18th International Conference on Space Operations (SpaceOps 2025)*, Montreal, 26–30 May 2025, NASA Technical Reports Server 20250003321, ntrs.nasa.gov/citations/20250003321.
