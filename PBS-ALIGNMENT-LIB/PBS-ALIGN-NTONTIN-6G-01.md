# PBS Alignment  
## Space Communications in the 6G and Beyond Era

**Alignment Identifier:** `PBS-ALIGN-NTONTIN-6G-01`

---

## Aligned Work

Ntontin, Konstantinos, Eva Lagunas, Jorge Querol, Junaid ur Rehman, Joel Grotz, Symeon Chatzinotas, and Björn Ottersten.  
“A Vision, Survey, and Roadmap Toward Space Communications in the 6G and Beyond Era.”  
*Proceedings of the IEEE*, vol. 113, no. 9, 2025, pp. 987–1023.  
doi:10.1109/JPROC.2024.3512934. Open access (CC BY 4.0).

---

## Alignment Overview

Ntontin et al. (University of Luxembourg SnT, KFUPM, SES) present a vision of satellite communications beyond 2030. The paper covers use cases (Section II), including near-Earth, lunar, deep-space and proximity links; enabling technologies (Section III), including delay-tolerant networking; three technologies treated in depth, namely AI, space-enabled quantum networks and joint communications and positioning (Section IV); and open challenges (Section V).

The paper's subject is the satellite and radio layer. PBS operates above it as application data. The dimensions below cover the statements in the paper that bear on PBS.

**Planned architecture (in development):** Pale Blue Systems (PBS) aligns with this vision by addressing interoperability and governance challenges that arise at the architectural level in such an environment. PBS operates above evolving physical and network layers, enabling policy-aware data exchange across independently governed systems consistent with the future ecosystem described in the study.

---

## Alignment Dimensions

### Lunar Communications over LunaNet

Lunar use cases include direct-to-Earth communications, communication among lunar surface assets, and links to the lunar Gateway via LunaNet. The authors describe LunaNet as a standardized, interoperable network for lunar operations among government, commercial and international partners. Round-trip light times between Earth and the Moon or Lagrangian points are 2.5 to 10 s, and orbiting relays are necessary for continuous communication from the lunar South Pole (Section II).

**PBS alignment:**  
PBS-LNIS-01 defines PBS operation over LunaNet IP and BPv7 network services and requires PBS semantics to be preserved across LunaNet Service Provider boundaries (PBS-LNIS-REQ-001, PBS-LNIS-REQ-007).

**Alignment Reference:** `PBS-ALIGN-NTONTIN-LUNAR-01`

---

### DTN Bundle Layer Below the Application

The paper describes DTN as the most mature networking technology for deep-space networks. The bundle layer sits between the application and transport layers and provides store-and-forward delivery; BP provides end-to-end delivery and LTP reliable single-hop transmission. DTN operates with or without the terrestrial IP suite and prioritizes the receipt of crucial data over less important information (Section III).

**PBS alignment:**  
PBS is application data in the BPv7 payload (PBS-DTN-MAP-02 Section 2). PBS priority is an end-to-end mission semantic that the BPv7 adapter preserves unchanged while network treatment is selected through BP QoS mechanisms and provider policy (PBS-DTN-MAP-02 Section 5; PBS-BPV7-002 in PBS-TRACE-NASA-FY26-01).

**Alignment Reference:** `PBS-ALIGN-NTONTIN-DTN-02`

---

### Interoperability Through Standardization

The authors identify the lack of inter-satellite link standardization as a fundamental challenge to optical ISL deployment, and state that interoperability and standardization are key where operators, user equipment and infrastructure belong to different vendors and owners (Section III).

**PBS alignment:**  
PBS specifications are public under the Apache License 2.0, and PBS-CONFORMANCE-01 defines the requirements an implementation must meet to claim PBS Core conformance; PBS-CONFORMANCE-02 defines the verification profile for the NASA/LunaNet alignment.

**Alignment Reference:** `PBS-ALIGN-NTONTIN-STD-03`

---

### Multi-Operator Market

The satellite communications market, once limited to governments and a few large corporations, now attracts investment from venture capital funds and terrestrial telecom operators (Section I).

**PBS alignment:**  
PBS-AUTH-01 carries the administrative domain and role under which a protected message is issued, for authorization across civil, commercial, international and mission boundaries (Section 1).

**Alignment Reference:** `PBS-ALIGN-NTONTIN-MULTI-04`

---

## Planned Architecture (in development)

Pale Blue Systems is building PBS to the following architecture for space communications in the 6G-and-beyond era.

### System-Level Framing of Space Communications

PBS adopts this system-level framing by treating space, lunar, and terrestrial networks as interoperable components of a unified internetworked ecosystem, while preserving their operational independence and distinct constraints.

### Heterogeneity as a Foundational Condition

PBS is architected with heterogeneity as a first-order assumption. Its interoperability layer functions above diverse and evolving substrates, enabling coordination without requiring uniform technologies, continuous connectivity, or symmetric capabilities.

### Multi-Actor, Multi-Authority Participation

PBS is designed to support interoperability across autonomous, authority-scoped networks. Its architecture enables collaboration among independently governed systems without imposing centralized ownership or shared control structures.

### Layered and Evolvable Architecture

PBS is positioned as a higher-layer interoperability and governance mechanism that remains agnostic to lower-layer implementations. This enables continued innovation in space communication technologies without disrupting inter-system interoperability.

### Long-Term Scalability and Sustainability

PBS supports long-term scalability through a federated, gateway-based model that allows incremental growth, onboarding of new participants, and extension into future cislunar and deep-space environments without architectural redesign.

### Governance and Coordination as Core Requirements

PBS directly addresses these requirements by providing a governance-aware interoperability layer that enables policy-aware data exchange across independently operated systems, aligning with the study’s emphasis on coordination as a foundational concern.

---

## Alignment Summary

Ntontin et al. place lunar communications on LunaNet, identify DTN as the most mature networking technology for deep space, and tie interoperability to standardization in a multi-vendor, multi-owner market. PBS adds an application layer above those networks: LunaNet carriage (PBS-LNIS-01), end-to-end priority over BPv7 (PBS-DTN-MAP-02), public conformance definitions (PBS-CONFORMANCE-01, PBS-CONFORMANCE-02) and authority context (PBS-AUTH-01).

**Planned architecture (in development):** Pale Blue Systems aligns with this vision by providing an architectural interoperability and governance layer that enables policy-aware coordination across autonomous space, lunar, and terrestrial networks consistent with the 6G-and-beyond roadmap.

---

## Citation (MLA)

Ntontin, Konstantinos, et al. “A Vision, Survey, and Roadmap Toward Space Communications in the 6G and Beyond Era.” *Proceedings of the IEEE*, vol. 113, no. 9, 2025, pp. 987–1023, doi:10.1109/JPROC.2024.3512934.
