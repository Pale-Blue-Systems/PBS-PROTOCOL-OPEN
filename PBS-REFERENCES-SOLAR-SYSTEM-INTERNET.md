# Solar System Internet Architecture and Governance  
**Architectural and Governance Reference with PBS Alignment**

---

## Source

Interplanetary Networking Special Interest Group (IPNSIG), Architecture and Governance Team. *Solar System Internet Architecture and Governance — from the Moon to Mars and beyond*. IPNSIG Inc., September 2023, 80 pp.  
<https://spi.elliott.gwu.edu/files/2023/10/Solar-System-Internet-Architecture-and-Governance.pdf>

IPNSIG functions as the interplanetary chapter of the Internet Society (ISOC). The report states that its views are IPNSIG's and do not necessarily reflect those of ISOC. The report is published by IPNSIG Inc.

---

## Overview

*Solar System Internet Architecture and Governance* is a scholarly architecture and policy paper produced by the **Architecture & Governance Working Group** of the **Interplanetary Networking Special Interest Group (IPNSIG)**, an official chapter of the **Internet Society (ISOC)**. The document addresses the technical, organizational, and governance challenges inherent in extending internetworking beyond Earth-centric assumptions into cislunar, planetary, and deep-space environments.

The paper builds upon decades of research and operational experience in **Delay/Disruption-Tolerant Networking (DTN)**, including work conducted under NASA, CCSDS, and international space agency collaborations. Rather than proposing a single network or operator model, the document establishes a principled architectural framework for interoperable internetworking across independently governed space systems.

The report examines the governance properties and structures needed to form a common, shared space network, and the technologies that support it (Executive Summary). It expects communication networks provided by different actors to join together in space, and uses the term Solar System Internet (SSI) for the result. It recommends:

- the Bundle Protocol (BP) suite, built on Delay- and Disruption-Tolerant Networking (DTN), for interplanetary networking;
- IPv6-based internets on other celestial bodies;
- a multistakeholder governance model inherited from the Internet.

Section 3 describes three phases: today, space-agency-led point-to-point communication; a transitional phase in which agencies procure commercial services, with LunaNet as an example; and a future in which commercial networks interconnect through private agreements similar to Internet peering.

---

## Principal Content

### DTN and Local IP (Sections 4.1 and 4.4)

BP suite nodes store bundles at intermediate relays until the next link is available. The Licklider Transmission Protocol (LTP) provides automatic repeat request below BP. BPSec provides integrity, authenticity and confidentiality between bundle processing nodes. On celestial bodies, where local delay is small, the IP suite can be used locally; the report concludes that IPv6 should be the only IP version used in space.

### Routing and Forwarding (Section 4.2)

Terrestrial routing and forwarding procedures do not adapt to long propagation delays, lapses of connectivity and orbit-driven topology changes. Open questions include how a routing technology causes high-value (nominally high-priority) data to be delivered before lower-value data. The report recommends four principles: autonomy and automation, standards, interoperability (the same inter-regional routing procedures adopted universally) and scalability.

### Security (Sections 4.3 and 7.2.4)

BPSec is one piece of the required SSI security architecture. Open challenges are delay-tolerant key management, establishment of trust (mutual key exchange becomes unmanageable even for small networks; decentralized certification authorities are considered a medium-term solution), definition and enforcement of network-wide security policies, and protection against malfunctioning nodes. In the short term, network users are expected to adopt the security measures required by the network provider and may add security to the data they transmit; interconnection between providers rests on bilateral agreements, which do not scale to larger networks.

### Identifiers, Time and Standards (Sections 7.2.2 and 7.2.3)

Critical resources such as spectrum and BP numbering identifiers require coordinated allocation. Determining time at each node is harder than on Earth because of distance and relativistic effects; the report discusses local barycentric time scales and a possible UTC (Moon) or UTC (Mars).

### Key Principles (Section 8)

Collaboration; fair and consistent allocation of resources such as spectrum and numbering identifiers; transparency of connectivity information and governance processes; interoperability, which the report calls the defining property of the SSI; security built in from the beginning; and multistakeholder policy decisions.

---

## Core Architectural Principles

### Federated Internetwork Model

The document defines the Solar System Internet as a **federation of autonomous networks**, each operated under its own administrative, legal, and policy authority. Interoperability is achieved through controlled interconnection rather than centralized ownership, reflecting early terrestrial Internet peering models adapted for space-scale latency and disruption.

This model recognizes that:
- Planetary, orbital, and mission networks operate independently
- Interconnection occurs selectively through agreed interfaces
- Governance is distributed across multiple authorities

---

### Gateway-Centric Interoperability

A central architectural construct in the paper is the **inter-network gateway**. Gateways serve as:
- Policy enforcement points
- Protocol translation boundaries
- Administrative and authority demarcation layers

The document emphasizes that gateways enable interoperability **without requiring endpoint uniformity**, allowing heterogeneous systems to exchange data while preserving internal architectures and constraints.

---

### Authority-Scoped Naming and Identity

The paper treats naming, addressing, and identity as governance-sensitive concerns. It establishes that:
- Flat, globally assigned namespaces are insufficient at interplanetary scale
- Identifiers must reflect administrative authority and scope
- Resolution and routing decisions are influenced by policy, not solely topology

This framing positions naming as a socio-technical system embedded within governance structures.

---

### Policy-Driven Routing and Data Exchange

Routing within the Solar System Internet is presented as inherently **policy-aware**. The document identifies legal, mission, commercial, and national constraints as first-class routing considerations alongside technical factors such as latency and link availability.

This approach reflects operational realities of space missions and multinational cooperation.

---

### Security and Trust Posture

Security is addressed through a **contextual trust model**, acknowledging that:
- No universal trust anchor exists across all space actors
- Trust relationships are authority-specific
- Gateways provide enforcement and mediation

Encryption and authentication are assumed, but governance-aware trust management is emphasized as equally essential.

---

## Scholarly and Technical Standing

Although not a peer-reviewed journal article, *Solar System Internet Architecture and Governance* is produced by a recognized Internet Society working group and is cited alongside foundational DTN literature in curated technical bibliographies and research repositories. It is positioned as a **reference architecture and governance framework**, informing ongoing work in space networking standards, DTN implementations, and inter-agency coordination.

The document is commonly discussed in conjunction with:
- DTN architecture research
- CCSDS networking standards
- NASA’s Interplanetary Overlay Network (ION)
- Academic studies on space internetworking and governance

---

## Relevance to Interoperability Standards

The paper provides a widely cited conceptual foundation for:
- Neutral interoperability layers
- Policy-aware gateways
- Multi-actor participation in space networking
- Long-term scalability of interplanetary communication systems

Its architectural framing supports the development of open standards and reference implementations that enable cooperation without centralization.

---

## PBS Alignment Identifier: PBS-ALIGN-SSIAG-01

This section maps statements in the report to PBS specification sections. The report does not mention PBS.

### Interconnected Provider Networks

The report expects networks of different providers to interconnect (Executive Summary, Section 3).

**PBS alignment:** PBS-LNIS-REQ-001 and PBS-LNIS-REQ-007 require PBS envelope fields, authority context, priority and Service Intent to be preserved across service-provider boundaries.

### Delivering High-Priority Data First

The report asks how routing delivers high-value data before lower-value data (Section 4.2).

**PBS alignment:** PBS-PRIO-01 Section 4 defines five priority classes in the envelope header. PBS-DTN-MAP-02 Section 5 preserves PBS priority end to end over BPv7 and leaves network treatment to BP QoS mechanisms and provider policy.

### End-User Security Above Provider Security

Users may add their own security to transmitted data, and source nodes may be required to add integrity protection so that inauthentic data can be dropped (Sections 4.3 and 7.2.4).

**PBS alignment:** PBS-SEC-B-01 provides application-layer source authentication, integrity, replay detection and optional confidentiality independent of BPSec (Sections 2 and 8). PBS-LNIS-REQ-008 requires both the mission and the network security profiles to be satisfied. PBS-SEC-B-01 Section 7 assigns trust anchors, key provisioning, rotation and revocation to mission security policy; PBS does not define DTN key management.

### Identifier Allocation

The report calls for coordinated allocation of numbering identifiers (Sections 7.2.2 and 8.1).

**PBS alignment:** PBS-AUTH-01 Section 4 defines authority-identifier namespaces and assigns new namespaces through PBS governance. PBS-SVC-01 Section 4 reserves data-class values 9–127 for PBSF assignment.

### Time References

The report identifies time determination across the solar system as an open standards issue (Section 7.2.3).

**PBS alignment:** PBS-PNT-CTX-01 requires time-bearing PNT data to identify its time reference (PBS-PNT-REQ-002) and LunaNet-aligned deployments to support the lunar time reference identifiers defined by governing LunaNet documents (PBS-PNT-REQ-006).

### Planned Architecture (in development)

Pale Blue Systems is building the PBS interoperability layer to the following architecture.

#### Federated Network Architecture

PBS adopts a **federated internetwork model** consistent with the paper’s framing of the Solar System Internet as a collection of autonomous networks interconnected through negotiated interfaces. PBS assumes that space, lunar, and terrestrial systems will continue to be operated by independent civil, commercial, and defense authorities, and it is designed to enable interoperability across these domains without requiring shared ownership, centralized control, or uniform internal architectures.

#### Gateway-Centric Design

In alignment with the document’s emphasis on gateways as the primary interoperability mechanism, PBS is architected around **policy-aware gateway components**. These gateways perform protocol translation, authority context resolution, and policy enforcement at network boundaries, allowing data to traverse heterogeneous systems while preserving mission-specific constraints and operational autonomy.

#### Authority-Scoped Naming and Identity

PBS reflects the paper’s treatment of naming and identity as governance-sensitive concerns by implementing **authority-scoped identifiers** and namespace separation within its interoperability layer. Rather than relying only on the flat 16-byte Source ID of the PBS-ENV-01 header, PBS enables naming and resolution decisions to be evaluated in the context of administrative authority, operational scope, and policy domain (PBS-AUTH-01, PBS-ADDR-01).

#### Policy-Driven Routing and Exchange

Consistent with the paper’s conclusion that routing in space networks is shaped by policy as much as by topology, PBS supports **policy-driven routing and data exchange**. Decisions regarding connectivity, data flow, and interoperability are mediated at gateway boundaries, allowing technical exchange to remain aligned with legal, mission, commercial, and organizational requirements.

#### Security and Trust Context

PBS aligns with the document’s contextual trust model by treating security as **authority-scoped and situational**. Trust relationships are established and enforced at interoperability boundaries rather than assumed globally, and encrypted payloads may traverse PBS gateways without requiring inspection or modification.

#### Long-Term Extensibility

In accordance with the paper’s emphasis on future-proofing early architectural decisions, PBS is designed as an extensible interoperability layer that can evolve alongside emerging transport protocols, mission architectures, and governance frameworks. Its position above specific transport implementations enables adaptation to future cislunar, planetary, and deep-space networking scenarios without requiring redesign of endpoint systems.

---

## References (MLA)

Interplanetary Networking Special Interest Group (IPNSIG). *Solar System Internet Architecture and Governance — from the Moon to Mars and beyond*. IPNSIG Inc., Sept. 2023, spi.elliott.gwu.edu/files/2023/10/Solar-System-Internet-Architecture-and-Governance.pdf.

Cerf, Vinton, et al. “Delay-Tolerant Networking Architecture.” *RFC 4838*, Internet Engineering Task Force, Apr. 2007, https://www.rfc-editor.org/rfc/rfc4838.

Burleigh, Scott, et al. “Delay-Tolerant Networking: An Approach to Interplanetary Internet.” *IEEE Communications Magazine*, vol. 41, no. 6, June 2003, pp. 128–136, doi:10.1109/MCOM.2003.1204759.

Burleigh, Scott, Kevin Fall, and Edward J. Birrane III. “Bundle Protocol Version 7.” *RFC 9171*, Internet Engineering Task Force, Jan. 2022, https://www.rfc-editor.org/rfc/rfc9171.

NASA Jet Propulsion Laboratory. *Interplanetary Overlay Network (ION)*. https://github.com/nasa-jpl/ION-DTN.
