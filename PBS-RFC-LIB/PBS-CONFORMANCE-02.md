# PBS-CONFORMANCE-02
## NASA/LunaNet Alignment Conformance and Verification Profile

**Status:** Optional Conformance Profile
**Version:** 1.5
**Changes:** <release date> (PBS v1.5.0): Section 3 test PBS-C02-T002 requires the PBS-ENV-01 header, including TTL and CRC32, to arrive byte-identical, and test PBS-C02-T016 (no-expiry bundle lifetime, PBS-DTN-MAP-02 Section 4) is added. The PBS v1.4.1 Section 6 erratum is incorporated (PBS-PROTOCOL-CHANGELOG.md, [1.4.1]). Wire format unchanged.
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
| PBS-C02-T002 | BPv7 carriage | T | PBS semantic fields preserved through store-and-forward; the PBS-ENV-01 header, including TTL and CRC32, is byte-identical at the receiving endpoint |
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
| PBS-C02-T016 | No-expiry lifetime | I/T | Message to which no finite limit applies (PBS-DTN-MAP-02 Section 4) is carried with the no-expiry lifetime documented in the mapping profile; the value is greater than 0 ms, not greater than `4294967295000` ms and not less than the lifetime assigned to any message with a finite limit, and the BP agent does not expire the bundle at creation |

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

PBS-CONFORMANCE-02 implements the following rows of PBS-TRACE-NASA-FY26-01:

| PBS Req ID | Test cases |
|---|---|
| PBS-NASA-1501-002 | PBS-C02-T001, PBS-C02-T002, PBS-C02-T003 |
| PBS-NASA-1503-005 | PBS-C02-T004, PBS-C02-T005, PBS-C02-T012 |
| PBS-LNIS-002 | PBS-C02-T003 |

This profile defines the tests and verification records for PBS-TRACE-NASA-FY26-01 and the normative requirements of the NASA/LunaNet alignment specifications. No verification records are published.
