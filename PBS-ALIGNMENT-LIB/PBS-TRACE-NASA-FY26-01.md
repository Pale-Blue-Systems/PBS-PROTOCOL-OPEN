# PBS NASA FY26 Requirements Traceability Matrix

**Document ID:** PBS-TRACE-NASA-FY26-01  
**Status:** Working Baseline  
**Baseline Date:** 2026-09-22

## Verification Codes

- **A** — Analysis
- **I** — Inspection
- **D** — Demonstration
- **T** — Test

## Source-to-PBS Traceability

| PBS Req ID | Source | PBS requirement | Verification | Allocation |
|---|---|---|---|---|
| PBS-NASA-1501-001 | NASA 15.01 | PBS SHALL provide transport-independent mission message semantics usable across heterogeneous lunar surface communications links. | I/T | ENV, SVC, LNIS |
| PBS-NASA-1501-002 | NASA 15.01 | PBS SHALL preserve mission semantic fields across provider and link transitions. | T | LNIS, CONFORMANCE |
| PBS-NASA-1501-003 | NASA 15.01 | PBS SHALL support deterministic operation across intermittent and scheduled connectivity. | T/D | SVC, DTN |
| PBS-NASA-1309-001 | NASA 13.09 | PBS SHALL express mission service intent independently of routing algorithm and physical transport. | I/T | SVC |
| PBS-NASA-1309-002 | NASA 13.09 | PBS SHALL express priority, freshness, persistence, delivery, acknowledgement, and degradation semantics as independently interpretable properties. | I/T | SVC, PRIO |
| PBS-NASA-1309-003 | NASA 13.09 | PBS SHALL support capability context for responsive interaction among distributed mission elements. | T | CAPS |
| PBS-NASA-1503-001 | NASA 15.03 | The mission security profile SHALL provide cryptographic source authentication and payload integrity. | T | SEC-B |
| PBS-NASA-1503-002 | NASA 15.03 | The mission security profile SHALL provide replay detection. | T | SEC-B |
| PBS-NASA-1503-003 | NASA 15.03 | The mission security profile SHALL provide authority validation for protected command messages. | T | AUTH, SEC-B |
| PBS-NASA-1503-004 | NASA 15.03 | PBS SHALL express command freshness/deadline and acknowledgement requirements independently. | T | SVC |
| PBS-NASA-1503-005 | NASA 15.03 | PBS SHALL define deterministic handling when required service conditions cannot be satisfied. | T/D | SVC, CONFORMANCE |
| PBS-NASA-2405-001 | NASA 24.05 | PBS PNT context SHALL identify the applicable spatial reference frame. | I/T | PNT-CTX |
| PBS-NASA-2405-002 | NASA 24.05 | PBS PNT context SHALL identify the applicable time reference. | I/T | PNT-CTX |
| PBS-NASA-2405-003 | NASA 24.05 | PBS PNT context SHALL support uncertainty, provenance, epoch, and validity information. | T | PNT-CTX |
| PBS-LNIS-001 | LNIS V005 | PBS SHALL operate as an application-layer semantic protocol over LunaNet-supported IP and BPv7 network services. | A/T | LNIS |
| PBS-LNIS-002 | LNIS V005 | PBS SHALL preserve its application semantics across LunaNet Service Provider boundaries. | T | LNIS, CONFORMANCE |
| PBS-LNIS-003 | LNIS V005 | PBS SHALL support explicit binding of PNT context to LunaNet-compatible lunar reference and time systems. | T | PNT-CTX, LNIS |
| PBS-BPV7-001 | RFC 9171 / CCSDS | PBS-to-BPv7 mapping SHALL preserve PBS service intent while using standardized BP mechanisms and deployment policy for network treatment. | A/T | DTN-MAP |
| PBS-BPV7-002 | RFC 9171 / CCSDS | PBS priority SHALL remain an end-to-end mission semantic across BPv7 transport. | T | PRIO, DTN-MAP |

## Bidirectional Traceability Rule

Each normative requirement introduced by this assignment SHALL reference one or more requirement identifiers from this matrix or an explicitly documented PBS design requirement. Each source requirement SHALL map to one or more normative PBS requirements and corresponding verification evidence.

## Verification Evidence

Verification artifacts will identify:
- implementation or test-vector version;
- requirement identifier;
- test configuration;
- expected behavior;
- observed behavior;
- pass/fail result;
- evidence location.
