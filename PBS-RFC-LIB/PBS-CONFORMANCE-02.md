# PBS-CONFORMANCE-02
## NASA/LunaNet Alignment Conformance and Verification Profile

**Status:** Optional Conformance Profile
**Version:** 1.4
**Related:** PBS-CONFORMANCE-01, PBS-SVC-01, PBS-LNIS-01, PBS-SEC-B-01, PBS-PNT-CTX-01, PBS-DTN-MAP-02, PBS-QOS-MAP-01

## 1. Purpose

PBS-CONFORMANCE-02 defines verification requirements for PBS implementations claiming the NASA/LunaNet alignment profile.

## 2. Profile Declaration

A conformance claim SHALL identify:
- PBS Core version;
- supported alignment-profile specifications;
- cryptographic suite(s);
- BPv7 implementation/profile;
- PNT reference/time identifiers supported;
- policy-adapter version;
- test-suite version.

## 3. Verification Matrix

| Test ID | Requirement area | Method | Acceptance condition |
|---|---|---|---|
| PBS-C02-T001 | IP carriage | T | PBS semantic fields preserved end-to-end |
| PBS-C02-T002 | BPv7 carriage | T | PBS semantic fields preserved through store-and-forward |
| PBS-C02-T003 | Provider/path transition | D/T | Source, authority, priority, intent, security context preserved |
| PBS-C02-T004 | Deadline expiration | T | Expired message is withheld from application acceptance |
| PBS-C02-T005 | Latest-state degradation | T | Superseded state is retired according to profile |
| PBS-C02-T006 | Authentication | T | Modified protected field or payload is rejected |
| PBS-C02-T007 | Replay protection | T | Replayed protected transaction is rejected or identified per profile |
| PBS-C02-T008 | Command authorization | T | Authorized command accepted; unauthorized authority/role rejected |
| PBS-C02-T009 | PNT context | T | Frame, time, provenance, uncertainty, validity preserved |
| PBS-C02-T010 | QoS policy | A/T | Deterministic mapping produced for each defined network state |
| PBS-C02-T011 | Disruption | D/T | Store-forward data retained/delivered according to persistence and expiry |
| PBS-C02-T012 | Capacity constraint | D/T | Priority and authorized degradation policy applied deterministically |
| PBS-C02-T013 | Security layering | T | PBS-SEC-B remains valid across BPSec-enabled BP path |
| PBS-C02-T014 | Unknown extension | T | Unknown optional frame safely skipped without semantic corruption |
| PBS-C02-T015 | Auditability | I/T | Required security/service dispositions produce traceable event evidence |

## 4. Test Environment

The test environment SHALL record endpoint implementations, gateway implementations, transport/network emulators, clock source and uncertainty, link impairment model, contact plan, service-policy version, cryptographic suite, and test-vector hashes.

Disruption tests SHALL include complete outage, delayed contact, asymmetric link availability, constrained throughput, and service restoration.

## 5. Evidence Package

Each verification record SHALL contain:
- test ID and requirement IDs;
- configuration identifier;
- procedure revision;
- input vectors;
- expected result;
- observed result;
- pass/fail disposition;
- logs or packet captures sufficient to reproduce the determination.

## 6. Traceability

This profile supplies verification evidence for PBS-TRACE-NASA-FY26-01 and the normative requirements in the NASA/LunaNet alignment specifications.
