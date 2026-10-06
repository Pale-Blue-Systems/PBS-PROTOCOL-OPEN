# Solar System Internet Architecture and Governance  
**Architectural and Governance Reference with PBS Alignment**

---

## Source

Interplanetary Networking Special Interest Group (IPNSIG), Architecture and Governance Team. *Solar System Internet Architecture and Governance — from the Moon to Mars and beyond*. IPNSIG Inc., September 2023, 80 pp.  
<https://spi.elliott.gwu.edu/files/2023/10/Solar-System-Internet-Architecture-and-Governance.pdf>

IPNSIG functions as the interplanetary chapter of the Internet Society (ISOC). The report states that its views are IPNSIG's and do not necessarily reflect those of ISOC. The report is published by IPNSIG Inc.

---

## Overview

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

---

## References (MLA)

Interplanetary Networking Special Interest Group (IPNSIG). *Solar System Internet Architecture and Governance — from the Moon to Mars and beyond*. IPNSIG Inc., Sept. 2023, spi.elliott.gwu.edu/files/2023/10/Solar-System-Internet-Architecture-and-Governance.pdf.

Cerf, Vinton, et al. “Delay-Tolerant Networking Architecture.” *RFC 4838*, Internet Engineering Task Force, Apr. 2007, https://www.rfc-editor.org/rfc/rfc4838.

Burleigh, Scott, et al. “Delay-Tolerant Networking: An Approach to Interplanetary Internet.” *IEEE Communications Magazine*, vol. 41, no. 6, June 2003, pp. 128–136, doi:10.1109/MCOM.2003.1204759.

Burleigh, Scott, Kevin Fall, and Edward J. Birrane III. “Bundle Protocol Version 7.” *RFC 9171*, Internet Engineering Task Force, Feb. 2022, https://www.rfc-editor.org/rfc/rfc9171.

NASA Jet Propulsion Laboratory. *Interplanetary Overlay Network (ION)*. https://github.com/nasa-jpl/ION-DTN.
