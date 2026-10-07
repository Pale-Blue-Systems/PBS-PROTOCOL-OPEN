# PBS Alignment Index  
## External Alignment Map for the PBS Specifications

**Document ID:** `PBS-ALIGN-INDEX-01`  
**Status:** Living Document  
**Scope:** Technical, Operational, Governance, and Architectural Alignment  
**Last Updated:** 2026-10-07

---

## Purpose

This index lists the PBS alignment documents in `PBS-ALIGNMENT-LIB/`. Each document identifies its external sources by DOI or official URL, summarizes what they state with section references, and maps those statements to PBS specification sections.

An alignment records correspondence between a source and PBS. No source names PBS, and no alignment claims endorsement by a source's authors or institutions.

---

## Alignment Index Table

| Alignment ID | External Source | Source Type | Domain | Alignment Summary |
|-------------|----------------|-------------|--------|------------------|
| [PBS-ALIGN-NASA-LCRNS-01](PBS-ALIGN-NASA-LCRNS-01.md) | Esper et al., SpaceOps 2025 (NTRS 20250003321) | Conference paper | Lunar Relay and Navigation Services | Commercial LCRNS relay and PNT services built to LNIS; PBS carries mission semantics across LNSPs |
| [PBS-ALIGN-NASA-LCRNS-02](PBS-ALIGN-NASA-LCRNS-02.md) | NASA FY26 Civil Space Shortfall Prioritization (2026); LNIS V005 (NASA, ESA, JAXA, 2025) | Agency documents | Lunar Network Services | Need statements 13.09, 15.01, 15.03, 24.05 and LNIS network services mapped to PBS v1.4 specifications |
| [PBS-ALIGN-IEEE-AEROCONF-2025-01](PBS-ALIGN-IEEE-AEROCONF-2025-01.md) | Templin et al., 2025 IEEE Aerospace Conference (doi:10.1109/AERO63441.2025.11068517) | Conference paper | DTN Convergence-Layer Performance | LTP throughput depends on segment size and path MTU; PBS is independent of the convergence layer |
| [PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01](PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01.md) | Verville and Eddy, 2025 IEEE Aerospace Conference (doi:10.1109/AERO63441.2025.11068727) | Conference paper | LunaNet Data Services | LCRNS relay data services and user-side coordination; PBS carries the user-side semantics |
| [PBS-ALIGN-CARBONARA-TNTN-01](PBS-ALIGN-CARBONARA-TNTN-01.md) | Carbonara et al., *IEEE Open Journal of the Communications Society* (2025) | Journal article | Integrated T/NTN Testbeds | Testbed tools for 3GPP T/NTNs; PBS rides above 3GPP links and records emulator configuration in verification |
| [PBS-ALIGN-NTONTIN-6G-01](PBS-ALIGN-NTONTIN-6G-01.md) | Ntontin et al., *Proceedings of the IEEE* (2025) | Journal article | 6G and Beyond Space Communications | LunaNet for lunar links, DTN for deep space, interoperability through standardization |
| [PBS-ALIGN-SPJ-LEO-2022-01](PBS-ALIGN-SPJ-LEO-2022-01.md) | Zhang et al., *Space: Science & Technology* (2022) | Journal article | Orbital Congestion and Space Governance | Sustainable LEO activity requires more rational surveillance and governance mechanisms |
| [PBS-ALIGN-TF-GOVERNANCE-2024-01](PBS-ALIGN-TF-GOVERNANCE-2024-01.md) | Beaumier et al., *Journal of European Public Policy* (2025, online 2024) | Journal article | Space Governance | Hybrid organisations such as ESA bridge clusters of diverse organisations in the space governance system |

| Alignment ID | External Source | Domain | Alignment Summary |
|-------------|----------------|--------|------------------|
| PBS-ALIGN-NASA-LCRNS-01 | NASA / DoD – LCRNS (Esper, 2025) | Lunar & Cislunar Networking | Identifies need for standardized, authority-aware relay and routing layers across lunar assets |
| PBS-ALIGN-IEEE-AEROCONF-2025-01 | IEEE Aerospace Conf. 2025 | Space Network Architecture | Validates modular, layered, non-monolithic comms architectures |
| PBS-ALIGN-IEEE-AEROCONF-OBP-02 | IEEE AeroConf – Onboard Processing | Edge / Onboard Computing | Confirms shift toward autonomous, local processing with constrained backhaul |
| PBS-ALIGN-IEEE-TNTN-2025-03 | IEEE Open Journal of ComSoc (2025) | T/NTN Testbeds | Demonstrates necessity of interoperable overlays across heterogeneous networks |
| PBS-ALIGN-SCIENCE-2022-SPACE-04 | *Science Partner Journal*, 2022 | Space–Air–Ground Integration | Aligns with PBS abstraction of Space–Air–Ground as a single interoperable system |
| PBS-ALIGN-TF-GOVERNANCE-2024-01 | *Journal of European Public Policy*, 2024 | Space Governance | Frames space as a fragmented, multi-actor domain requiring coordination without central authority |

Requirements traceability for the v1.4 NASA alignment is in [`PBS-TRACE-NASA-FY26-01`](PBS-TRACE-NASA-FY26-01.md), under the engineering assignment [`PBS-ALIGN-ASSIGNMENT-NASA-FY26-01`](PBS-ALIGN-ASSIGNMENT-NASA-FY26-01.md).

Alignment `PBS-ALIGN-SSIAG-01`, with the IPNSIG report *Solar System Internet Architecture and Governance* (2023), is recorded in [`PBS-REFERENCES-SOLAR-SYSTEM-INTERNET.md`](../PBS-REFERENCES-SOLAR-SYSTEM-INTERNET.md).

---

## Detailed Alignment Summaries

### 1. NASA Lunar Communications Relay and Navigation Systems (Esper et al., 2025)

**Alignment ID:** `PBS-ALIGN-NASA-LCRNS-01`

**Core Finding:**  
Cislunar space has no existing communications, PNT or timing infrastructure. LCRNS procures interoperable commercial relay and navigation services built to LNIS, with onboard routing and store-and-forward storage; NASA is expected to be one of many users of those services (Sections 1, 2 and 4).

NASA identifies the absence of a common, interoperable communications layer across lunar assets operated by multiple agencies and vendors.

**PBS Alignment:**  
PBS-LNIS-01 preserves PBS semantics across LunaNet Service Provider boundaries (PBS-LNIS-REQ-001, PBS-LNIS-REQ-007). PBS-SVC-01 and PBS-DTN-MAP-02 carry disruption, persistence and lifetime policy. PBS-PNT-CTX-01 identifies PNT reference frames and time references. PBS-CONFORMANCE-02 verifies PBS at the application interface.

**Planned architecture (in development):**  
PBS provides a neutral interoperability layer that enables routing, identity, and policy awareness across independently governed lunar systems without imposing mission redesign or centralized control.

**MLA Citation:**  
Esper, Jaime, et al. “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).” *18th International Conference on Space Operations (SpaceOps 2025)*, Montreal, 26–30 May 2025, NASA Technical Reports Server 20250003321, ntrs.nasa.gov/citations/20250003321.

---

### 2. NASA LCRNS, LunaNet, and FY26 Civil Space Shortfalls

**Alignment ID:** `PBS-ALIGN-NASA-LCRNS-02`

**Core Finding:**  
NASA's FY26 Civil Space Shortfall Prioritization contains need statements 13.09 (advanced networking for multi-spacecraft responsive operations), 15.01 (scalable, reliable lunar surface-to-surface communications), 15.03 (safe human-robot interaction, secure command and control over high-latency, bandwidth-limited networks, or reliable automated safing) and 24.05 (a scalable lunar PNT architecture). LNIS V005 defines LunaNet real-time IP network services and BPv7 DTN network services across multiple providers.

**PBS Alignment:**  
PBS-TRACE-NASA-FY26-01 derives 19 PBS requirements from these sources and RFC 9171 and allocates them to 11 specifications: PBS-ENV-01, PBS-PRIO-01, PBS-CAPS-01, PBS-SVC-01, PBS-AUTH-01, PBS-SEC-B-01, PBS-PNT-CTX-01, PBS-LNIS-01, PBS-DTN-MAP-02, PBS-QOS-MAP-01 and PBS-CONFORMANCE-02.

**MLA Citation:**  
NASA Space Technology Mission Directorate. *FY26 Civil Space Shortfall Prioritization*. NASA, May 2026, www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf.  
NASA, ESA, and JAXA. *LunaNet Interoperability Specification Document*, Version 5 (LNIS V005). NASA, 29 Jan. 2025, www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf.

---

### 3. High-Performance DTN Convergence Layers (Templin et al., 2025)

**Alignment ID:** `PBS-ALIGN-IEEE-AEROCONF-2025-01`

**Core Finding:**  
LTP throughput rises with segment size even when IP fragmentation occurs: a factor of 2 to 3 for HDTN depending on path MTU and a factor of 10 or more for ION. Segmentation offload and kernel-resident LTP segmentation are projected to give HDTN a factor of 4 over the LTP base case (Sections V, VI and X).

Future space systems require modular, layered architectures rather than tightly coupled, mission-specific stacks.

**PBS Alignment:**  
PBS-DTN-MAP-01 Section 5.1 maps each envelope to exactly one bundle; PBS-DTN-MAP-02 Section 2 specifies that one PBS protocol data unit SHOULD map to one BP application data unit unless a registered segmentation profile applies. PBS-DTN-MAP-02 Section 8 leaves convergence-layer selection to the DTN network service. Convergence-layer improvements apply beneath PBS without a PBS change.

**Planned architecture (in development):**  
PBS is explicitly layered, sitting above transport and below mission logic, enabling reuse across missions, orbits, and operators.

**MLA Citation:**  
Templin, Fred, et al. “High Performance DTN Using Larger Packets and Kernel Resident Convergence Layers.” *2025 IEEE Aerospace Conference*, IEEE, 2025, pp. 1–12, doi:10.1109/AERO63441.2025.11068517.

---

### 4. Onboard Processing for LunaNet Data Services (Verville and Eddy, 2025)

**Alignment ID:** `PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01`

**Core Finding:**  
LCRNS relays provide the LNIS real-time frame, real-time IP and store-and-forward Bundle Protocol services through onboard processing and routing. User missions coordinate endpoint identifiers, QoS treatment and storage policy with the LNSP and are responsible for the security of their own data (Sections 1, 3 and 4).

Onboard autonomy and edge processing are required due to latency, bandwidth, and resilience constraints.

**PBS Alignment:**  
PBS carries the user-side information with the data: disruption policy (PBS-SVC-01 Section 9), priority and data class (PBS-PRIO-01 Section 4, PBS-SVC-01 Section 4), endpoint-to-EID mapping (PBS-DTN-MAP-02 Section 3) and end-to-end authentication (PBS-SEC-B-01).

**Planned architecture (in development):**  
PBS assumes intermittent connectivity and supports autonomous operation with delayed synchronization, rather than continuous ground dependence.

**MLA Citation:**  
Verville, Jonathan, and Wesley Eddy. “Onboard Processing for LunaNet Data Services.” *2025 IEEE Aerospace Conference*, IEEE, 2025, pp. 1–12, doi:10.1109/AERO63441.2025.11068727.

---

### 5. Integrated Terrestrial and Non-Terrestrial Network Testbeds (Carbonara et al., 2025)

**Alignment ID:** `PBS-ALIGN-CARBONARA-TNTN-01`

**Core Finding:**  
Experimental testbeds for integrated T/NTNs are built from software-defined radios, channel emulators, commercial user equipment, open-source core and radio-access software and remotely accessible platforms. At the time of writing, few studies had tested specific T/NTN functions experimentally (Sections III to VII).

T/NTN integration demands interoperable overlays across SDRs, satellites, UAVs, and terrestrial infrastructure.

**PBS Alignment:**  
PBS is application data independent of the access technology, including 3GPP links (PBS-LNIS-01 Section 5, PBS-LNIS-REQ-004). PBS-CONFORMANCE-02 Section 4 requires the emulator and link-impairment configuration of each verification run to be recorded.

**Planned architecture (in development):**  
PBS operates as an overlay that allows proprietary and open systems to interoperate without altering their internal implementations.

**MLA Citation:**  
Carbonara, Salvatore, et al. “Hands-On Solutions for Testing Integrated Terrestrial and Non-Terrestrial Networks: A Comprehensive Survey.” *IEEE Open Journal of the Communications Society*, vol. 6, 2025, pp. 10729–10760, doi:10.1109/OJCOMS.2025.3646364.

---

### 6. Space Communications in the 6G and Beyond Era (Ntontin et al., 2025)

**Alignment ID:** `PBS-ALIGN-NTONTIN-6G-01`

**Core Finding:**  
Lunar use cases run over LunaNet, which the authors describe as a standardized, interoperable network for government, commercial and international partners. DTN, with BP end to end and LTP per hop, is the most mature networking technology for deep-space networks. Interoperability across vendors and owners depends on standardization (Sections II and III).

**PBS Alignment:**  
PBS-LNIS-01 defines PBS carriage over LunaNet. PBS-DTN-MAP-02 Section 5 preserves PBS priority end to end over BPv7. PBS-CONFORMANCE-01 and PBS-CONFORMANCE-02 publish the conformance requirements.

**MLA Citation:**  
Ntontin, Konstantinos, et al. “A Vision, Survey, and Roadmap Toward Space Communications in the 6G and Beyond Era.” *Proceedings of the IEEE*, vol. 113, no. 9, 2025, pp. 987–1023, doi:10.1109/JPROC.2024.3512934.

---

### 7. LEO Mega Constellations (Zhang et al., 2022)

**Alignment ID:** `PBS-ALIGN-SPJ-LEO-2022-01`

**Core Finding:**  
Unrestrained deployment of LEO mega constellations strains orbital resources and affects the safety of in-orbit operations. Sustainable LEO activity requires more rational surveillance and governance mechanisms; the paper reviews space situational awareness and end-of-life deorbiting as responses (Abstract).

Space, air, and ground systems are converging into a single operational domain requiring unified coordination models.

**PBS Alignment:**  
PBS-AUTH-01, PBS-POS-01 with PBS-PNT-CTX-01, and PBS-PRIO-01 define the authority, position and priority information exchanged between independently operated systems.

**Planned architecture (in development):**  
PBS treats Space–Air–Ground as a continuous system, enabling seamless message flow across domains while preserving domain-specific constraints.

**MLA Citation:**  
Zhang, Jingrui, et al. “LEO Mega Constellations: Review of Development, Impact, Surveillance, and Governance.” *Space: Science & Technology*, vol. 2022, 2022, doi:10.34133/2022/9865174.

---

### 8. Hybrid Organisations in Space Governance (Beaumier et al., 2025)

**Alignment ID:** `PBS-ALIGN-TF-GOVERNANCE-2024-01`

**Core Finding:**  
Organisations in governance systems multiply, diversify and cluster by type. Hybrid organisations such as ESA bridge those clusters as brokers and keep the space governance system cohesive (Abstract).

Space governance is fragmented, multi-actor, and coordination-based rather than centralized.

**PBS Alignment:**  
PBS-AUTH-01 carries the authority context of each protected message and requires authority translation across administrative domains to be explicit and policy-controlled (PBS-AUTH-REQ-004).

**Planned architecture (in development):**  
PBS embeds authority context and policy boundaries into its interoperability model, enabling coordination without governance collapse or forced unification.

**MLA Citation:**  
Beaumier, Guillaume, et al. “Hybrid Organisations and Governance Systems: The Case of the European Space Agency.” *Journal of European Public Policy*, vol. 32, no. 4, 2025, pp. 1004–1034, doi:10.1080/13501763.2024.2325647.

---

## What This Index Shows

- Every source is identified by DOI or by an official NASA or NTRS URL: four journal articles, three conference papers and one set of NASA and LunaNet program documents.
- The sources describe the conditions PBS is specified for: multi-provider lunar networks built to LNIS (alignments 1, 2 and 4), DTN carriage over BP and LTP (3 and 6), 3GPP non-terrestrial links (5) and multi-organisation operation and governance (7 and 8).
- Each alignment maps statements in its source to PBS specification sections.
- Requirements-level traceability exists for the NASA FY26 alignment only (PBS-TRACE-NASA-FY26-01). The other alignments are informative.
- PBS aligns with **independently identified needs**, not speculative futures.
- Alignment spans **technical**, **operational**, and **governance** layers.
- No dependency on a single agency, vendor, or political framework.
- Clear evidence that PBS fits naturally into emerging space and lunar ecosystems.


**End of Document**
