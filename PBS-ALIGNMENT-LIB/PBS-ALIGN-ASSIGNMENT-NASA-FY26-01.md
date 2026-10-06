# PBS Alignment Assignment — NASA FY26 Civil Space Shortfalls / LunaNet

**Document ID:** PBS-ALIGN-ASSIGNMENT-NASA-FY26-01  
**Status:** Delivered in PBS v1.4 (2026-09-22; pull request #1, git tag v1.4.0)  
**Baseline Date:** 2026-09-22  
**Protocol Baseline:** PBS v1.3 (git tag v1.3.0)

## 1. Goal

The Pale Blue Systems Protocol (PBS) defines an open **mission-semantic interoperability standard** for heterogeneous lunar, cislunar, and deep-space systems operating across LunaNet-compatible IP and DTN/BPv7 network services.

PBS carries stable mission meaning across transport and provider boundaries, including identity and authority context, service intent, priority, freshness, delivery semantics, security requirements, capability context, PNT context, and deterministic degradation behavior.

## 2. Architectural Allocation

```text
Mission / Application Systems
        |
        v
Pale Blue Systems Protocol
Mission semantics + communications intent
        |
        v
LunaNet Network Services
IP / BPv7 / BPSec / CCSDS
        |
        v
Provider & Service Management
LNSPs / LCRNS / PExT / enterprise service management
        |
        v
Physical & Link Infrastructure
RF / optical / 3GPP / Wi-Fi / wired / relays
```

PBS provides the application-facing semantic contract used consistently across network technologies and service providers.

## 3. NASA Need Traceability Baseline

Need IDs and need statements are quoted from NASA's *FY26 Civil Space Shortfall Prioritization*, Appendix A (Section 7, source 1). Each need statement belongs to one of the 32 shortfall categories in that document.

| Need ID | NASA need statement | PBS alignment objective |
|---|---|---|
| 15.01 | “Provide scalable, reliable surface-to-surface communications between assets on the lunar surface that is usable by all participating elements.” | Common mission-semantic envelope and service-intent contract across surface links and LunaNet access points |
| 13.09 | “Provide advanced networking needed for multi-spacecraft responsive space operations.” | Transport-independent service intent, priority, freshness, capability, acknowledgement, and deterministic handling semantics |
| 15.03 | “Achieve safe, efficient human-robot interactions for exploration missions, secure command and control over high-latency, bandwidth-limited networks, or implement reliable automated safing sequences.” | Authenticated authority context, replay protection, command delivery semantics, deadlines, acknowledgements, and deterministic handling |
| 24.05 | “Develop a lunar position, navigation, and timing architecture capable of scaling to long term operational needs.” | Reference-frame, time-reference, provenance, uncertainty, validity, and PNT-context bindings carried with mission data |

## 4. Work Packages

### WP-1 — Evidence Baseline and Requirements Traceability
Establish the authoritative NASA/CCSDS source baseline and a bidirectional source-to-PBS requirements matrix. Each derived requirement receives a verification method.

### WP-2 — LunaNet Application Alignment Profile
Define PBS operation above LunaNet IP and BPv7 network services and across LNIS-compatible surface access technologies and provider boundaries.

### WP-3 — Mission Service Intent
Define transport-independent semantics for mission data class, priority, freshness/deadline, persistence, acknowledgement, delivery mode, disruption tolerance, degradation policy, security requirements, and PNT context.

### WP-4 — Security and Authority Profile
Define source authentication, authority validation, payload integrity, replay protection, priority authorization, confidentiality profiles, and BPSec binding.

### WP-5 — PNT Context Profile
Define reference-frame identifier, time-reference identifier, epoch, uncertainty, provenance, validity interval, quality indicator, and LunaNet Reference Time binding.

### WP-6 — DTN/BPv7 Mapping
Define PBS service-intent mapping into current BPv7-compatible mechanisms and local policy while preserving PBS semantic intent end-to-end.

### WP-7 — Conformance and Verification
Define PBS Core, LunaNet, BPv7, security, PNT, mixed-provider, mixed-transport, disrupted-link, and bandwidth-constrained conformance profiles.

### WP-8 — Repository Consistency Review
Apply the architecture consistently across normative specifications, alignment documents, references, developer guidance, and protocol terminology.

## 5. Engineering Controls

Every normative requirement:

1. uses a unique requirement identifier;
2. uses SHALL, SHOULD, and MAY according to RFC 2119 / RFC 8174 semantics;
3. traces to an authoritative source, derived system requirement, or explicit PBS design requirement;
4. defines verification by Analysis, Inspection, Demonstration, or Test;
5. preserves compatibility within the declared major version;
6. defines deterministic error and degraded-mode behavior;
7. maintains transport and provider independence.

## 6. Acceptance Criteria

Acceptance criteria:

- each targeted NASA need has bidirectional traceability to PBS requirements;
- the PBS/LunaNet interface is explicit and testable;
- Mission Service Intent is normatively specified;
- cryptographic security and authority semantics are normatively specified;
- PNT context binds cleanly to LunaNet reference/time concepts;
- BPv7 mapping reflects the current CCSDS architecture;
- conformance scenarios cover nominal, disrupted, degraded, multi-provider, and security-critical operation;
- NASA/CCSDS claims are source-controlled and citation-backed.

## 7. Authoritative Source Set

1. NASA Space Technology Mission Directorate. *FY26 Civil Space Shortfall Prioritization*. May 2026. <https://www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf>
2. NASA, ESA, and JAXA. *LunaNet Interoperability Specification Document*, Version 5 (LNIS V005), Baseline, 29 January 2025. <https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf>
3. NASA Goddard Space Flight Center, Exploration and Space Communications. *LCRNS*. <https://www.nasa.gov/goddard/esc/lcrns/>; Esper, J., G. Heckler, J. Verville, and G. Ryden. “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).” SpaceOps 2025. <https://ntrs.nasa.gov/citations/20250003321>
4. NASA Space Communications and Navigation. *Delay/Disruption Tolerant Networking*. <https://www.nasa.gov/communicating-with-missions/delay-disruption-tolerant-networking/>
5. Kearns, M. “NASA Wideband Demo Completes Primary Mission, Extends Operations” (PExT). NASA, 1 June 2026. <https://www.nasa.gov/blogs/smallsatellites/2026/06/01/nasa-wideband-demo-completes-primary-mission-extends-operations/>
6. NASA. *2026 Civil Space Shortfalls*. Released 12 January 2026. <https://www.nasa.gov/wp-content/uploads/2026/03/2026-civil-space-shortfalls.pdf>
7. IETF. RFC 9171, *Bundle Protocol Version 7*, and RFC 9172, *Bundle Protocol Security (BPSec)*. <https://www.rfc-editor.org/rfc/rfc9171>, <https://www.rfc-editor.org/rfc/rfc9172>
8. CCSDS 734.2-P-1.1, *CCSDS Bundle Protocol Specification* (draft Recommended Standard), cited by LNIS V005 as applicable document [AD19].

## 8. Configuration Management

Normative protocol requirements reside in `PBS-RFC-LIB/`. Alignment evidence resides in `PBS-ALIGNMENT-LIB/`. Requirements traceability is maintained as a controlled engineering artifact. Informative source interpretation remains separate from normative protocol language.
