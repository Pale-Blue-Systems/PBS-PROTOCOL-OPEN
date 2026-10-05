# PBS-SVC-01
## Mission Service Intent

**Status:** Optional Extension
**Version:** 1.4
**Applies to:** PBS systems requiring explicit mission delivery semantics
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-MUX-01, PBS-SEC-B-01, PBS-DTN-MAP-02, PBS-LNIS-01

## 1. Purpose

PBS-SVC-01 defines transport-independent Mission Service Intent carried with PBS mission data. Service Intent expresses the operational treatment requested by the originating application in stable semantics that remain meaningful across local links, LunaNet access points, IP paths, BPv7 paths, relays, and independently operated service-provider networks.

Service Intent separates operational meaning into independently testable properties: data class, priority, freshness, persistence, delivery mode, acknowledgement, disruption tolerance, degradation policy, and security requirement.

## 2. Requirements

- **PBS-SVC-REQ-001:** A conformant implementation SHALL encode each Service Intent property independently.
- **PBS-SVC-REQ-002:** Service Intent SHALL remain unchanged by transport selection.
- **PBS-SVC-REQ-003:** Network adapters SHALL treat Service Intent as policy input and SHALL preserve its end-to-end semantic value.
- **PBS-SVC-REQ-004:** A receiver SHALL apply freshness validation before application delivery when a finite maximum age is present.
- **PBS-SVC-REQ-005:** A sender SHALL select a delivery mode compatible with the application transaction model.
- **PBS-SVC-REQ-006:** An implementation SHALL produce a deterministic disposition when a mandatory Service Intent property cannot be satisfied.

## 3. Encoding

Service Intent is carried as PBS-MUX frame type `0x07`.

The frame value uses a fixed 20-byte structure in network byte order:

| Offset | Field | Size | Meaning |
|---:|---|---:|---|
| 0 | version | 1 | `0x01` |
| 1 | data_class | 1 | Mission data classification |
| 2 | delivery_mode | 1 | Delivery semantic |
| 3 | ack_mode | 1 | Acknowledgement semantic |
| 4 | persistence | 1 | Persistence policy |
| 5 | disruption | 1 | Disruption policy |
| 6 | degradation | 1 | Degradation policy |
| 7 | security_profile | 1 | Required PBS security profile |
| 8 | max_age_ms | 4 | Maximum age at delivery; `0xFFFFFFFF` = mission-defined unbounded |
| 12 | deadline_ms | 4 | Relative delivery deadline; `0xFFFFFFFF` = no delivery deadline |
| 16 | intent_flags | 4 | Reserved intent flags; undefined bits SHALL be zero |

Priority remains encoded by PBS-ENV-01 / PBS-PRIO-01 and is interpreted together with this frame.

## 4. Data Classes

| Value | Class |
|---:|---|
| 0 | COMMAND |
| 1 | ALERT |
| 2 | STATE |
| 3 | TELEMETRY |
| 4 | PNT |
| 5 | SCIENCE |
| 6 | MEDIA |
| 7 | BULK_DATA |
| 8 | SERVICE_CONTROL |

Values 9-127 are reserved for PBSF assignment. Values 128-255 are deployment-defined.

## 5. Delivery Modes

| Value | Mode | Semantics |
|---:|---|---|
| 0 | DATAGRAM | Independent application unit |
| 1 | AT_LEAST_ONCE | Delivery may repeat; duplicate recognition is supported where transaction semantics require it |
| 2 | EXACTLY_ONCE_TRANSACTION | Application transaction identifier and replay state ensure one accepted transaction |
| 3 | LATEST_STATE | Newer state supersedes older queued state for the same application key |
| 4 | ORDERED | Receiver delivers accepted units in application sequence order |
| 5 | COMPLETE_OBJECT | Application delivers after all required object segments validate |

## 6. Freshness and Deadline

`max_age_ms` specifies maximum acceptable information age at application delivery. `deadline_ms` specifies maximum interval from message creation to successful delivery under the requested service.

A receiver SHALL expire or quarantine a message whose finite maximum age has elapsed according to mission policy. A network adapter SHALL use a finite deadline as policy input where the underlying service exposes deadline, lifetime, scheduling, or queue controls.

Priority and freshness are independent mission properties.

## 7. Persistence

| Value | Policy |
|---:|---|
| 0 | TRANSIENT - retain while an immediate forwarding opportunity exists |
| 1 | UNTIL_DEADLINE - retain through disruption until deadline |
| 2 | UNTIL_EXPIRY - retain through disruption until freshness/TTL expiration |
| 3 | DURABLE - retain according to mission durable-delivery policy |

## 8. Acknowledgement

| Value | Policy |
|---:|---|
| 0 | NONE |
| 1 | RECEIPT |
| 2 | APPLICATION_ACCEPTANCE |
| 3 | TRANSACTION_RESULT |

Acknowledgement semantics are end-to-end application semantics. Transport status reports may contribute evidence to an acknowledgement service.

## 9. Disruption Policy

| Value | Policy |
|---:|---|
| 0 | CONTINUOUS_PATH |
| 1 | STORE_FORWARD |
| 2 | EITHER |

## 10. Degradation Policy

| Value | Policy |
|---:|---|
| 0 | EXACT |
| 1 | PROFILED |
| 2 | LATEST_STATE_ONLY |

A registered degradation profile SHALL identify transformations authorized by the application and SHALL preserve safety, authority, and security semantics.

## 11. Security Requirement

`security_profile` identifies the minimum PBS security profile required for application acceptance:

- `0` - PBS-SEC-A integrity baseline
- `1` - PBS-SEC-B authenticated mission messaging
- `2` - PBS-SEC-B authenticated plus confidentiality profile

A receiver SHALL validate the required profile before application acceptance.

## 12. Deterministic Disposition

When a mandatory Service Intent requirement cannot be satisfied, the implementation SHALL select a mission-policy disposition: retain pending service availability, use an authorized alternate service, apply an authorized degradation profile, expire, or return a service-status result.

The disposition SHALL be observable to mission software when acknowledgement or transaction-result semantics request it.

## 13. Traceability

PBS-SVC-01 implements PBS-NASA-1309-001/002, PBS-NASA-1503-004/005, PBS-LNIS-001/002, and PBS-BPV7-001 from PBS-TRACE-NASA-FY26-01.
