# PBS Alignment
## NASA LCRNS, LunaNet, and FY26 Civil Space Shortfalls

**Alignment Identifier:** `PBS-ALIGN-NASA-LCRNS-02`
**Revision:** 2026-10-06 (PBS v1.4.1); first issued 2026-09-22 (PBS v1.4)

## Aligned Architecture

NASA's Lunar Communications Relay and Navigation Systems (LCRNS) project [6] procures commercially provided lunar relay communications and PNT services built to the LunaNet Interoperability Specification (LNIS) [3, 4]. LNIS V005 describes LunaNet as a network of cooperating networks on which LunaNet Service Providers (LNSPs) deliver communications, PNT and other services [3, Preface]. It defines real-time IP network services (Section 3.1.1.2) and DTN network services, for which Bundle Protocol version 7 (BPv7) shall be used (Section 3.1.2). LCRNS relays process link-layer and higher-layer protocols onboard and route frames, packets and bundles to provide these services [5].

PBS defines the mission semantics that applications carry over those network services: identity and authority, priority, Service Intent, freshness, security requirements and PNT context.

## Architectural Allocation

| Layer | Allocation |
|---|---|
| Mission applications | Mission logic, payload schemas, commands, telemetry, science, media, autonomy |
| **PBS** | Identity/authority, mission service intent, priority, freshness, persistence, delivery semantics, security requirements, capability context, PNT context, deterministic degradation |
| LunaNet network services | IP and BPv7 network connectivity and interoperable LNSP services |
| Service management | Network/service planning, provider selection, resource coordination, contact/path management |
| Physical/link systems | RF, optical, 3GPP, Wi-Fi, wired, relay and direct-with-Earth (DWE) connectivity |

## FY26 Need Statement Alignment

NASA's *FY26 Civil Space Shortfall Prioritization* [1] consolidates the shortfalls into 32 categories. Each category (shortfall, SF) contains need statements identified by a Need ID. PBS v1.4 traces to four need statements, quoted from [1] Appendix A and listed in the *2026 Civil Space Shortfalls* [2]. The final 1–32 rank of the parent shortfall and membership in the STMD Top 40 Focus Areas for FY26 are from [1].

| Need ID | Need statement | Parent shortfall (rank of 32) | STMD Top 40 |
|---|---|---|---|
| 13.09 | “Provide advanced networking needed for multi-spacecraft responsive space operations.” | SF13 Perform advanced remote sensing and science measurements with improved sensing capabilities and autonomy (7) | Yes |
| 15.01 | “Provide scalable, reliable surface-to-surface communications between assets on the lunar surface that is usable by all participating elements.” | SF15 Operate multi-agent robotic and crewed systems in cooperative planetary surface activities (10) | Yes |
| 15.03 | “Achieve safe, efficient human-robot interactions for exploration missions, secure command and control over high-latency, bandwidth-limited networks, or implement reliable automated safing sequences.” | SF15 (10) | No |
| 24.05 | “Develop a lunar position, navigation, and timing architecture capable of scaling to long term operational needs.” | SF24 Provide tracking and navigation of crew and assets in space (8) | Yes |

### Need 15.01 — Lunar Surface Communications

PBS supplies a common application semantic contract across participating elements and preserves it across surface access technologies and LunaNet access points (PBS-LNIS-REQ-001, PBS-LNIS-REQ-004).

**PBS allocations:** PBS-SVC-01, PBS-LNIS-01, PBS-CONFORMANCE-02.

### Need 13.09 — Responsive Multi-Spacecraft Networking

PBS Service Intent expresses priority, freshness, deadline, persistence, delivery mode, acknowledgement, disruption tolerance, degradation policy and security requirement as independently encoded application semantics (PBS-SVC-REQ-001). PBS-QOS-MAP-01 converts these semantics into authorized network-treatment requests.

**PBS allocations:** PBS-SVC-01, PBS-QOS-MAP-01, PBS-DTN-MAP-02.

### Need 15.03 — Secure Command and Control

PBS authenticated mission messaging binds command data to source identity, authority context, priority, Service Intent, anti-replay state and payload integrity (PBS-SEC-B-01 Sections 2 and 5). A receiver authorizes a protected command against mission policy before execution (PBS-SECB-REQ-006, PBS-AUTH-REQ-003).

**PBS allocations:** PBS-AUTH-01, PBS-SEC-B-01, PBS-SVC-01, PBS-CONFORMANCE-02.

### Need 24.05 — Scalable Lunar PNT

PBS carries reference-frame, time-reference, epoch, uncertainty, provenance, validity and quality context with mission PNT data. LunaNet-aligned deployments bind these identifiers to the lunar reference system and LunaNet Reference Time defined by governing LunaNet documents (PBS-PNT-REQ-006; LNIS V005 Section 2.1).

**PBS allocations:** PBS-PNT-CTX-01, PBS-LNIS-01.

## Multi-Provider Interoperability

LCRNS, ESA's Moonlight and JAXA's Lunar Navigation Satellite System providers are expected to provide interoperable services under LNIS; NASA is expected to be one of many users of LCRNS services [4, Section 2]. PBS keeps application semantics unchanged as data crosses provider and path boundaries (PBS-LNIS-REQ-007). Network and service management select resources; PBS supplies the application requirements as policy input (PBS-SVC-REQ-003).

NASA's Polylingual Experimental Terminal (PExT) completed its primary objectives in December 2025 by returning data through NASA's Tracking and Data Relay Satellite system and commercial relay networks operated by Viasat and SES Space and Defense. Its extended mission, through April 2027, includes direct-to-Earth links through SSC Space ground stations and a planned enterprise service management demonstration with Aalyria's Spacetime software [7]. PBS operates at the application semantic boundary above such service-management functions.

## Verification Alignment

LCRNS is developing an Interoperability and Performance Testbed (IPT), a hardware-in-the-loop testbed that emulates a universal lunar user terminal to verify by test LCRNS relay service performance and interoperability requirements [4, Section 5]. PBS-CONFORMANCE-02 verifies PBS at the application interface: test cases PBS-C02-T001 to PBS-C02-T015 cover IP and BPv7 carriage, provider transition, deadline expiration, authentication, replay protection, command authorization, PNT context, QoS policy, disruption, capacity constraint and BPSec layering (Section 3).

## Traceability

The source-to-requirement mapping is maintained in [`PBS-TRACE-NASA-FY26-01`](PBS-TRACE-NASA-FY26-01.md).

## References

[1] NASA Space Technology Mission Directorate. *FY26 Civil Space Shortfall Prioritization*. May 2026. <https://www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf>

[2] NASA. *2026 Civil Space Shortfalls*. Released 12 January 2026. <https://www.nasa.gov/wp-content/uploads/2026/03/2026-civil-space-shortfalls.pdf>

[3] NASA, ESA, and JAXA. *LunaNet Interoperability Specification Document*, Version 5 (LNIS V005), Baseline, 29 January 2025. <https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf>

[4] Esper, Jaime, Gregory Heckler, Jonathan Verville, and Grant Ryden. “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).” *18th International Conference on Space Operations (SpaceOps 2025)*, Montreal, May 2025. <https://ntrs.nasa.gov/citations/20250003321>

[5] Verville, Jonathan, and Wesley Eddy. “Onboard Processing for LunaNet Data Services.” *2025 IEEE Aerospace Conference*, 2025, pp. 1–12, doi:10.1109/AERO63441.2025.11068727.

[6] NASA Goddard Space Flight Center, Exploration and Space Communications. *LCRNS*. <https://www.nasa.gov/goddard/esc/lcrns/>

[7] Kearns, Molly. “NASA Wideband Demo Completes Primary Mission, Extends Operations.” NASA Small Satellite Missions blog, 1 June 2026. <https://www.nasa.gov/blogs/smallsatellites/2026/06/01/nasa-wideband-demo-completes-primary-mission-extends-operations/>
