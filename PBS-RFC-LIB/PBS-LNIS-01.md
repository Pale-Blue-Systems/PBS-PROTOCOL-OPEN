# PBS-LNIS-01
## LunaNet Application Alignment Profile

**Status:** Optional Interoperability Profile
**Version:** 1.4
**Applies to:** PBS systems using LunaNet-compatible communications services
**Related:** PBS-ENV-01, PBS-SVC-01, PBS-DTN-MAP-02, PBS-PNT-CTX-01, PBS-SEC-B-01

## 1. Purpose

PBS-LNIS-01 defines the application-layer integration profile for carrying PBS mission semantics across LunaNet-compatible communications services.

LunaNet supplies cooperative network services and interoperable provider interfaces. PBS supplies a stable mission-semantic contract used by applications across those services.

## 2. Architectural Position

```text
PBS Mission Application
        |
PBS ENV / SVC / AUTH / PNT / SEC
        |
LunaNet Network Service
BPv7 or IP
        |
LNSP / access network / relay
```

PBS envelopes are user-application protocol data. A PBS implementation may operate over IP, BPv7, or a gateway that selects between available LunaNet-compatible network services.

## 3. Requirements

- **PBS-LNIS-REQ-001:** A PBS/LunaNet implementation SHALL preserve PBS envelope and Service Intent semantics across LNSP boundaries.
- **PBS-LNIS-REQ-002:** A PBS/LunaNet implementation SHALL support BPv7 as a network-service binding when disruption-tolerant service is required by the mission profile.
- **PBS-LNIS-REQ-003:** A PBS/LunaNet implementation MAY support IP network-service bindings for contemporaneous connectivity.
- **PBS-LNIS-REQ-004:** Surface access technology SHALL remain transparent to PBS application semantics.
- **PBS-LNIS-REQ-005:** PBS PNT context SHALL identify the reference frame and time reference used by application data.
- **PBS-LNIS-REQ-006:** Network-service status MAY inform PBS adapter policy while application semantic fields remain end-to-end stable.
- **PBS-LNIS-REQ-007:** Provider transitions SHALL preserve PBS Source ID, authority context, priority, Service Intent, and protected application payload.
- **PBS-LNIS-REQ-008:** Security processing SHALL satisfy both the selected PBS mission security profile and applicable network security profile.

## 4. Network-Service Selection

The PBS adapter selects a compatible network service using Service Intent, current connectivity, contact availability, provider service capabilities, mission policy, security profile, deadline, and freshness state.

For STORE_FORWARD or EITHER disruption policy, BPv7 is an eligible binding. For CONTINUOUS_PATH, an IP or real-time LunaNet service is eligible when mission service constraints are satisfied.

## 5. Surface and Local Networks

PBS application semantics are preserved across local and surface connectivity including 3GPP, Wi-Fi, wired, UHF, S-band, Ka-band, optical, and mission-specific links when those links connect to a PBS endpoint or gateway.

A gateway SHALL preserve the PBS semantic contract while adapting link framing and network encapsulation.

## 6. Multi-Provider Operation

PBS addressing and authority context remain stable across service-provider transitions. Provider-specific identifiers and locators are maintained by the network adapter.

The adapter SHALL expose provider transition events to mission observability systems when mission policy requires service provenance or performance accounting.

## 7. PNT Integration

PBS-PNT-CTX-01 carries application-level PNT context. LunaNet PNT measurements and derived solutions may populate that context with the applicable lunar reference frame, time reference, uncertainty, provenance, epoch, and validity.

## 8. Verification Profile

Conformance SHALL include PBS exchange over IP, PBS exchange over BPv7, provider/path transition with semantic preservation, disrupted-link store-and-forward delivery, deadline expiration during disruption, PNT-context preservation, and authenticated mission-message preservation across the network boundary.

## 9. Traceability

PBS-LNIS-01 implements PBS-NASA-1501-001/002/003, PBS-LNIS-001/002/003, and contributes to PBS-NASA-1309-001 from PBS-TRACE-NASA-FY26-01.

## 10. References

NASA, ESA, and JAXA. *LunaNet Interoperability Specification*, Version 5, 29 Jan. 2025.

NASA Goddard Space Flight Center. *Lunar Communications Relay and Navigation Systems (LCRNS)*.
