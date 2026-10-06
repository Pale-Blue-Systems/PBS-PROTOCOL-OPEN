# PBS NASA FY26 Requirements Traceability Matrix

**Document ID:** PBS-TRACE-NASA-FY26-01  
**Status:** Working Baseline  
**Baseline Date:** 2026-09-22  
**Errata:** 2026-10-06 (PBS v1.4.1): Allocation column restated as specification identifiers and reconciled with the specification Traceability sections, adding PBS-LNIS-01 (PBS-NASA-1501-003), PBS-QOS-MAP-01 (PBS-NASA-1309-001/002, PBS-BPV7-001) and PBS-SVC-01 (PBS-LNIS-001/002, PBS-BPV7-001), which state that they implement those rows. Requirement text unchanged.

## Verification Codes

- **A** — Analysis
- **I** — Inspection
- **D** — Demonstration
- **T** — Test

## Source-to-PBS Traceability

| PBS Req ID | Source | PBS requirement | Verification | Allocation |
|---|---|---|---|---|
| PBS-NASA-1501-001 | NASA 15.01 | PBS SHALL provide transport-independent mission message semantics usable across heterogeneous lunar surface communications links. | I/T | PBS-ENV-01, PBS-SVC-01, PBS-LNIS-01 |
| PBS-NASA-1501-002 | NASA 15.01 | PBS SHALL preserve mission semantic fields across provider and link transitions. | T | PBS-LNIS-01, PBS-CONFORMANCE-02 |
| PBS-NASA-1501-003 | NASA 15.01 | PBS SHALL support deterministic operation across intermittent and scheduled connectivity. | T/D | PBS-SVC-01, PBS-DTN-MAP-02, PBS-LNIS-01 |
| PBS-NASA-1309-001 | NASA 13.09 | PBS SHALL express mission service intent independently of routing algorithm and physical transport. | I/T | PBS-SVC-01, PBS-QOS-MAP-01 |
| PBS-NASA-1309-002 | NASA 13.09 | PBS SHALL express priority, freshness, persistence, delivery, acknowledgement, and degradation semantics as independently interpretable properties. | I/T | PBS-SVC-01, PBS-PRIO-01, PBS-QOS-MAP-01 |
| PBS-NASA-1309-003 | NASA 13.09 | PBS SHALL support capability context for responsive interaction among distributed mission elements. | T | PBS-CAPS-01 |
| PBS-NASA-1503-001 | NASA 15.03 | The mission security profile SHALL provide cryptographic source authentication and payload integrity. | T | PBS-SEC-B-01 |
| PBS-NASA-1503-002 | NASA 15.03 | The mission security profile SHALL provide replay detection. | T | PBS-SEC-B-01 |
| PBS-NASA-1503-003 | NASA 15.03 | The mission security profile SHALL provide authority validation for protected command messages. | T | PBS-AUTH-01, PBS-SEC-B-01 |
| PBS-NASA-1503-004 | NASA 15.03 | PBS SHALL express command freshness/deadline and acknowledgement requirements independently. | T | PBS-SVC-01 |
| PBS-NASA-1503-005 | NASA 15.03 | PBS SHALL define deterministic handling when required service conditions cannot be satisfied. | T/D | PBS-SVC-01, PBS-CONFORMANCE-02 |
| PBS-NASA-2405-001 | NASA 24.05 | PBS PNT context SHALL identify the applicable spatial reference frame. | I/T | PBS-PNT-CTX-01 |
| PBS-NASA-2405-002 | NASA 24.05 | PBS PNT context SHALL identify the applicable time reference. | I/T | PBS-PNT-CTX-01 |
| PBS-NASA-2405-003 | NASA 24.05 | PBS PNT context SHALL support uncertainty, provenance, epoch, and validity information. | T | PBS-PNT-CTX-01 |
| PBS-LNIS-001 | LNIS V005 | PBS SHALL operate as an application-layer semantic protocol over LunaNet-supported IP and BPv7 network services. | A/T | PBS-LNIS-01, PBS-SVC-01 |
| PBS-LNIS-002 | LNIS V005 | PBS SHALL preserve its application semantics across LunaNet Service Provider boundaries. | T | PBS-LNIS-01, PBS-SVC-01, PBS-CONFORMANCE-02 |
| PBS-LNIS-003 | LNIS V005 | PBS SHALL support explicit binding of PNT context to LunaNet-compatible lunar reference and time systems. | T | PBS-PNT-CTX-01, PBS-LNIS-01 |
| PBS-BPV7-001 | RFC 9171 / CCSDS | PBS-to-BPv7 mapping SHALL preserve PBS service intent while using standardized BP mechanisms and deployment policy for network treatment. | A/T | PBS-DTN-MAP-02, PBS-SVC-01, PBS-QOS-MAP-01 |
| PBS-BPV7-002 | RFC 9171 / CCSDS | PBS priority SHALL remain an end-to-end mission semantic across BPv7 transport. | T | PBS-PRIO-01, PBS-DTN-MAP-02 |

## Bidirectional Traceability Rule

Each normative requirement introduced by this assignment SHALL reference one or more requirement identifiers from this matrix or an explicitly documented PBS design requirement. Each source requirement SHALL map to one or more normative PBS requirements and corresponding verification evidence.

The Allocation column lists every specification whose Traceability section states that it implements the row, and each listed specification states it. A specification that contributes to a row without implementing it says "supports" or "contributes to" and is not listed.

## Verification Evidence

Verification artifacts will identify:
- implementation or test-vector version;
- requirement identifier;
- test configuration;
- expected behavior;
- observed behavior;
- pass/fail result;
- evidence location.
