# PBS Alignment
## NASA LCRNS, LunaNet, and FY26 Civil Space Shortfalls

**Alignment Identifier:** `PBS-ALIGN-NASA-LCRNS-01`
**Revision:** 2026-09-22

## Aligned Architecture

NASA's Lunar Communications Relay and Navigation Systems (LCRNS) establishes interoperable commercial lunar communications and PNT services using the LunaNet Interoperability Specification (LNIS). LNIS defines cooperative network services across independent providers and supports network-based user applications over IP and Bundle Protocol.

PBS provides the mission-semantic interoperability standard used by mission applications across those network services. PBS gives independently developed spacecraft, rovers, habitats, robots, sensors, autonomous systems, and ground applications a common representation for mission intent and application-level handling requirements.

## Architectural Allocation

| Layer | Allocation |
|---|---|
| Mission applications | Mission logic, payload schemas, commands, telemetry, science, media, autonomy |
| **PBS** | Identity/authority, mission service intent, priority, freshness, persistence, delivery semantics, security requirements, capability context, PNT context, deterministic degradation |
| LunaNet network services | IP and BPv7 network connectivity and interoperable LNSP services |
| Service management | Network/service planning, provider selection, resource coordination, contact/path management |
| Physical/link systems | RF, optical, 3GPP, Wi-Fi, wired, relay and DWE connectivity |

## FY26 Shortfall Alignment

### Need 15.01 — Lunar Surface Communications

NASA identifies scalable, reliable lunar surface-to-surface communications usable by participating elements as a civil space need.

PBS supplies a common application semantic contract across participating elements and preserves that contract across surface access technologies and LunaNet access points.

**PBS allocations:** PBS-SVC-01, PBS-LNIS-01, PBS-CONFORMANCE-02.

### Need 13.09 — Responsive Multi-Spacecraft Networking

PBS Service Intent expresses priority, freshness, deadline, persistence, delivery mode, acknowledgement, disruption tolerance, degradation policy, and security requirement as stable application semantics. PBS-QOS-MAP-01 converts these semantics into authorized network-treatment requests.

**PBS allocations:** PBS-SVC-01, PBS-QOS-MAP-01, PBS-DTN-MAP-02.

### Need 15.03 — Secure Command and Control

PBS authenticated mission messaging binds command data to source identity, authority context, mission priority, Service Intent, anti-replay state, and payload integrity. Command acceptance includes local authorization against mission policy.

**PBS allocations:** PBS-AUTH-01, PBS-SEC-B-01, PBS-SVC-01, PBS-CONFORMANCE-02.

### Need 24.05 — Scalable Lunar PNT

PBS carries reference-frame, time-reference, epoch, uncertainty, provenance, validity, and quality context with mission PNT data. LunaNet-aligned deployments bind these identifiers to the governing lunar reference and time systems.

**PBS allocations:** PBS-PNT-CTX-01, PBS-LNIS-01.

## Multi-Provider Interoperability

LCRNS uses LNIS so agencies and commercial providers deliver compatible services. PBS maintains stable application semantics as data crosses provider and path boundaries. Network/service management selects resources; PBS supplies the application requirements and preserves mission meaning end-to-end.

NASA's PExT demonstrations further establish multi-network terminal operation and enterprise service management across government and commercial communications services. PBS integrates at the application semantic boundary above those service-management functions.

## Verification Alignment

NASA's LCRNS Interoperability & Performance Testbed validates commercial relay performance and LunaNet interoperability. PBS-CONFORMANCE-02 applies the same engineering principle at the application-semantic boundary through hardware/software-in-the-loop capable tests for IP, BPv7, disruption, provider transition, security, PNT context, deadline handling, and constrained-capacity operation.

## Traceability

The controlled source-to-requirement mapping is maintained in `PBS-TRACE-NASA-FY26-01.md`.

## References

NASA. *FY26 Civil Space Shortfall Prioritization*. May 2026.

NASA, ESA, and JAXA. *LunaNet Interoperability Specification*, Version 5, 29 Jan. 2025.

Esper, Jaime, et al. "NASA's Lunar Communications Relay and Navigation Systems (LCRNS)." *18th International Conference on Space Operations*, 2025.

NASA Goddard Space Flight Center. *Lunar Communications Relay and Navigation Systems*.

NASA. "NASA Wideband Demo Completes Primary Mission, Extends Operations." 1 June 2026.
