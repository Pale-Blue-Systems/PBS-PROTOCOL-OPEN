# PBS-DTN-MAP-02
## Mapping to BPv7 Delay/Disruption Tolerant Networking

**Status:** Optional Interoperability Profile
**Version:** 1.4
**Applies to:** PBS gateways and endpoints using BPv7
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-SVC-01, PBS-SEC-B-01, PBS-LNIS-01

## 1. Purpose

PBS-DTN-MAP-02 defines deterministic carriage of PBS mission semantics over Bundle Protocol Version 7 (BPv7).

PBS remains application protocol data. BPv7 supplies disruption-tolerant network service. The binding preserves PBS mission semantics end-to-end while allowing BP nodes and service providers to apply standardized BP mechanisms and deployment policy.

## 2. Architectural Binding

```text
PBS application data
        |
PBS envelope + semantic frames
        |
BPv7 payload
        |
BP convergence-layer adapter
        |
LunaNet / DTN link service
```

One PBS protocol data unit SHOULD map to one BP application data unit unless a registered segmentation profile defines object segmentation and reassembly.

## 3. Endpoint Mapping

PBS endpoint/service addressing SHALL map deterministically to BP Endpoint Identifiers (EIDs) at the binding boundary. The mapping SHALL be stable for the duration required by the mission transaction and SHALL preserve authority scope in the mapping registry or binding context.

## 4. Lifetime and Freshness

BP bundle lifetime SHALL be selected so that network delivery cannot extend the PBS message beyond the effective mission deadline or expiry policy.

For finite PBS deadlines or freshness limits, the adapter SHALL calculate a BP lifetime bounded by the remaining permitted interval at bundle creation.

PBS application acceptance SHALL continue to evaluate PBS freshness independently of BP delivery status.

## 5. Priority and QoS

PBS priority is an end-to-end mission semantic.

The BPv7 adapter SHALL preserve PBS priority unchanged. Network treatment is selected through standardized BP QoS mechanisms available in the deployment and through local service-provider policy.

A mapping profile SHALL document:
- the BP QoS mechanism or extension used;
- queue/scheduling treatment;
- behavior under congestion;
- behavior when the requested treatment is unavailable.

Network treatment SHALL preserve the relative mission intent expressed by PBS policy subject to authorized resource-management policy.

## 6. Service Intent Mapping

| PBS Service Intent | BPv7 adapter behavior |
|---|---|
| STORE_FORWARD | BPv7 store-and-forward eligible |
| EITHER | BPv7 eligible according to path policy |
| finite deadline | bundle lifetime bounded to remaining deadline |
| UNTIL_EXPIRY | storage bounded to effective expiry |
| AT_LEAST_ONCE | duplicate detection maintained at PBS/application layer |
| EXACTLY_ONCE_TRANSACTION | transaction identity and replay state maintained end-to-end |
| acknowledgement requested | BP status information may contribute transport evidence; PBS acknowledgement remains application semantic |

## 7. Security

BPSec SHALL be applied when required by the applicable LunaNet, provider, or mission network-security profile. PBS-SEC-B SHALL be applied when the Service Intent or mission profile requires authenticated PBS mission semantics.

Layered security identities and key domains SHALL be documented in the deployment security profile.

## 8. Routing and Contacts

Contact plans, route computation, convergence-layer selection, custody-related operational policy, and provider path selection are DTN/network-service functions. PBS Service Intent supplies application requirements used as policy input.

## 9. Failure and Status

A BP forwarding or delivery-status event MAY be translated into a PBS service-status result. Such translation SHALL preserve the distinction between network status, PBS receipt, application acceptance, and transaction result.

## 10. Verification

Conformance tests SHALL verify:
- envelope preservation through BP encapsulation;
- EID mapping stability;
- deadline-to-lifetime bounding;
- priority semantic preservation;
- store-and-forward delivery;
- expiry during disruption;
- duplicate handling;
- PBS-SEC-B preservation with BPSec enabled.

## 11. Traceability

PBS-DTN-MAP-02 implements PBS-BPV7-001/002, PBS-NASA-1501-003, and supports PBS-NASA-1309-001/002.
