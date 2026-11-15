# PBS-MAP-VDA5050-01
## Mapping Profile: VDA 5050 Mobile Robot Messages over PBS

**Status:** Draft (proposed Optional Interoperability Profile; not part of any PBS release)
**Version:** 0.2
**Changes:** 0.2 replaces PBS-MAP-21423-01 v0.1. The profile now targets VDA 5050, whose specification is public, and every row of Section 4 was checked against VDA 5050 version 3.0.0. ISO 21423 alignment moved to Section 9 as an unverified intention.
**Applies to:** Gateways that carry VDA 5050 messages between a mobile robot and a fleet control across intermittent links
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-SVC-01, PBS-AUTH-01, PBS-SEC-B-01, PBS-MUX-01, PBS-ADDR-02, PBS-SUITE-01, PBS-DTN-MAP-02, PBS-PROX-01

> **Reference checked.** VDA 5050 version 3.0.0, *Interface for the Communication between Mobile Robots and a Fleet Control*, markdown document and JSON schemas at <https://github.com/VDA5050/VDA5050> (revision `f480c40`, 2026-11-11). Section and topic names below are from that document. Nothing in this profile claims conformance to VDA 5050 or endorsement by VDA or VDMA.

---

## 1. Purpose

VDA 5050 defines how mobile robots and a fleet control exchange orders, actions and state. Its transport is MQTT with JSON (VDA 5050 Section 4), which needs a broker the robot can reach.

VDA 5050 already expects connection loss: a robot that disconnects keeps its order and continues to the last released node (VDA 5050 Section 4.1). What it does not define is how messages travel while the broker is out of reach. Robots work in such places: yards, mines, farms, disaster sites, long corridors with dead zones, and facilities whose network has failed.

This profile lets a pair of bridges carry the same messages inside PBS envelopes across a link that comes and goes. The robot and the fleet control keep using VDA 5050 unchanged.

VDA 5050 leaves protocol security to broker configuration (Section 4.1). This profile adds PBS-SEC-B-01 authentication and PBS-AUTH-01 authority to fleet-control messages crossing the intermittent segment.

---

## 2. Architecture

```text
Mobile robot                          Fleet control
(MQTT client)                         (MQTT client)
     |                                     |
Edge broker                           Site broker
     |                                     |
Edge bridge  == PBS envelopes over ==  Site bridge
               intermittent links
               (PBS-PROX-01, BPv7)
```

- The **edge bridge** runs or attaches to a broker on the robot side, so the robot always has a broker to publish to.
- The **site bridge** republishes arriving robot messages to the site broker and collects fleet-control messages for the robot.
- Topics keep their VDA 5050 form, `interfaceName/majorVersion/manufacturer/serialNumber/topic` (VDA 5050 Section 4.2), on both sides.

---

## 3. Envelope Construction

- **PBS-MVDA-REQ-001:** A bridge SHALL create one envelope per MQTT message, with Timestamp set to the time it received the message from its local broker, and its own Source ID.
- **PBS-MVDA-REQ-002:** The payload SHALL be a PBS-MUX-01 container with a Service Intent frame, one message frame (Section 3.1), and a PBS-ADDR-02 destination frame naming the peer bridge.
- **PBS-MVDA-REQ-003:** Envelopes carrying `order`, `instantActions`, `responses` or `zoneSet` SHALL also carry an Authority Context frame and a Security frame (PBS-SEC-B-01, PBS-SUITE-01), and the edge bridge SHALL verify both before publishing to the robot.
- **PBS-MVDA-REQ-004:** The receiving bridge SHALL apply PBS-SVC-01 freshness validation (PBS-SVC-REQ-004) before republishing and SHALL NOT republish an expired message.
- **PBS-MVDA-REQ-005:** A bridge SHALL NOT alter the JSON body. The VDA 5050 `headerId` and `timestamp` fields stay as the sender set them, so the receiver can still detect gaps per topic.

### 3.1 Message frame

The message frame uses the PBS-MUX-01 frame type from Section 4. Its value is:

| Field | Size | Content |
|---|---:|---|
| map_version | 1 | `0x02` |
| encoding | 1 | `0x00` JSON, verbatim UTF-8. `0x01` CBOR (RFC 8949), converted under Section 5. |
| qos_retain | 1 | Bits 1–0: MQTT QoS to use when republishing. Bit 2: retain flag. |
| topic_len | 1 | Length of topic |
| topic | variable | MQTT topic, UTF-8, as published |
| body | remainder | Message body in the stated encoding |

---

## 4. Message Classes

VDA 5050 Section 4.3 defines eight topics. Section 4.1 assigns QoS 0 to all of them except `connection`, which uses QoS 1; `connection` and `factsheet` messages are retained (Sections 6.5 and 6.10).

| Topic | Direction | MUX type | Data class | Priority | Delivery mode | TTL | max_age | Identity |
|---|---|---|---|---|---|---:|---:|---|
| `order` | fleet control → robot | `0x02` Command | COMMAND | HIGH | EXACTLY_ONCE_TRANSACTION | site policy, not `0` | site policy | `orderId` + `orderUpdateId` |
| `instantActions` | fleet control → robot | `0x02` Command | COMMAND | HIGH | EXACTLY_ONCE_TRANSACTION | 30 s | 30 s | each `actionId` |
| `responses` | fleet control → robot | `0x02` Command | COMMAND | HIGH | EXACTLY_ONCE_TRANSACTION | Section 4.2 | Section 4.2 | `requestId` + `grantType` |
| `zoneSet` | fleet control → robot | `0x02` Command | SERVICE_CONTROL | NORMAL | AT_LEAST_ONCE | 3600 s | none | `zoneSetId` |
| `state` | robot → fleet control | `0x03` Status | STATE | NORMAL | LATEST_STATE | 60 s | 30 s | topic |
| `visualization` | robot → visualization | `0x01` Telemetry | TELEMETRY | LOW | LATEST_STATE | 10 s | 5 s | topic |
| `factsheet` | robot → fleet control | `0x03` Status | STATE | LOW | LATEST_STATE | 86400 s | none | topic |
| `connection` | generated (Section 6) | — | — | — | — | — | — | — |

Values are defaults. A deployment MAY change TTL and max_age and SHALL document what it uses. The 30 s `state` max_age matches the VDA 5050 Section 6.6 rule that state is published at least every 30 seconds.

### 4.1 Rules

- **PBS-MVDA-REQ-010:** For LATEST_STATE messages, a bridge or relay holding an older message with the same Source ID and topic SHALL replace it with the newer one (PBS-SVC-01 Section 5).
- **PBS-MVDA-REQ-011:** The receiving bridge SHALL NOT republish a message whose Identity value it has already republished with identical content. This keeps a retransmitted `zoneSet` from raising the robot's 'DUPLICATE_ZONE_SET' warning (VDA 5050 Section 6.4.2).
- **PBS-MVDA-REQ-012:** An `order` TTL SHALL NOT be `0`.
- **PBS-MVDA-REQ-013:** The edge bridge SHALL publish orders for one robot in increasing `orderUpdateId` within an `orderId`. It SHALL NOT withhold a late order on its own judgment: the robot already rejects an outdated update with 'OUTDATED_ORDER_UPDATE' and ignores an identical duplicate (VDA 5050 Sections 6.1.4.4 and 6.1.4.5), and that report must reach fleet control.

### 4.2 Responses and leases

A `responses` message grants, queues, rejects or revokes a request the robot made in its state, and a grant MAY carry a `leaseExpiry` (VDA 5050 Section 6.9).

- **PBS-MVDA-REQ-020:** The envelope for a `responses` message SHALL expire no later than the earliest `leaseExpiry` it carries. With no `leaseExpiry`, the default TTL and max_age are 30 s.
- **PBS-MVDA-REQ-021:** A 'REVOKED' response SHALL be sent at priority CRITICAL.

A robot that receives no response behaves as if the request was not granted (VDA 5050 Section 6.9), so a response lost or expired in transit fails safe. Interactive zones and corridor requests therefore work over this profile only where the round trip fits inside the application's timeout; sites with long outages should plan orders that do not depend on them.

### 4.3 Orders across an outage

VDA 5050 splits an order into released nodes (the base) and planned ones (the horizon) (Section 6.1.1). The length of the base is how far a robot can go without hearing from fleet control. A site using this profile SHOULD release enough of each order to cover its expected outages, and no more than it is prepared to have executed unsupervised.

---

## 5. Encoding

- **PBS-MVDA-REQ-030:** Encoding `0x00` carries the JSON body byte for byte.
- **PBS-MVDA-REQ-031:** Encoding `0x01` converts JSON to CBOR by the RFC 8949 Section 6.2 rules and back by Section 6.1. The result is the same JSON value, not necessarily the same bytes: member order and number formatting can differ. A bridge SHALL use `0x00` when any consumer depends on the exact bytes.

A later revision MAY register a field dictionary built from the VDA 5050 JSON schemas to shorten member names.

---

## 6. Connection State

In VDA 5050 the robot publishes `connectionState` 'ONLINE' and sets a last will of 'CONNECTION_BROKEN'; the values are 'ONLINE', 'OFFLINE', 'HIBERNATING' and 'CONNECTION_BROKEN', sent retained at QoS 1 (Sections 4.1, 6.5 and 7). Behind a bridge, the robot's own connection is to the edge broker, and its last will never reaches the site.

- **PBS-MVDA-REQ-040:** The edge bridge SHALL NOT forward `connection` messages as envelopes, except that it SHALL forward 'OFFLINE' and 'HIBERNATING', which the robot sends deliberately, using the `state` row of Section 4 at priority HIGH.
- **PBS-MVDA-REQ-041:** The site bridge SHALL publish the robot's `connection` topic on the site broker, retained at QoS 1. It publishes 'ONLINE' only while the last `state` it republished is within max_age, 'CONNECTION_BROKEN' when that age is exceeded, and a forwarded 'OFFLINE' or 'HIBERNATING' as received.
- **PBS-MVDA-REQ-042:** The site bridge SHOULD expose, in a deployment-defined way, the age of the last state it republished.

VDA 5050 notes that the `connection` topic is not for checking robot health (Section 4.3); fleet control judges that from `state`. VDA 5050 has no value meaning "reachable through an intermittent link". Raising that as an issue on the VDA 5050 repository is preferable to a private extension.

---

## 7. Safety

- **PBS-MVDA-REQ-050:** Functions that protect people or equipment in real time, including emergency stop and collision avoidance, SHALL NOT depend on this profile. They remain on the robot and its local safety systems.
- **PBS-MVDA-REQ-051:** A robot receiving a message through this profile applies the same validation it applies to one received directly. This profile adds checks at the edge bridge and removes none.

Traffic coordination that assumes current positions degrades when positions are late. A site SHOULD treat a robot whose state is older than max_age as occupying its last reported area until it reports again.

---

## 8. Relationship to BPv7

Where the bridges are also bundle nodes, envelopes are carried under PBS-DTN-MAP-02. Where they meet directly, they use PBS-PROX-01 sessions. The MQTT-facing behavior is the same in both cases.

---

## 9. ISO 21423 (Unverified)

ISO 21423:2026 is reported by its publisher to build on VDA 5050 and the MassRobotics Interoperability Standard, to use MQTT and JSON, and to extend to building systems such as lifts, automated doors and alarms. Its text has not been consulted for this profile.

The intention is that this profile extends to ISO 21423 with additional rows in Section 4 and no change to Sections 3, 5, 6 or 7. Expected additions, to be confirmed by a contributor with access to the standard:

| Message | Expected treatment |
|---|---|
| Building system request (lift, door) | As `instantActions` |
| Building system status | As `state` |
| Alarm | MUX `0x04` Event, ALERT, CRITICAL, AT_LEAST_ONCE, TTL `0` |

Until then, this profile makes no statement about ISO 21423 messages.

---

## 10. Open Issues

1. Confirm Section 9 against ISO 21423:2026.
2. A field dictionary for compact encoding on low-rate links (Section 5).
3. Messages addressed to several robots at once.
4. Whether the site bridge needs one MQTT client per robot so that each robot's retained `connection` message has its own last will if the bridge itself fails.
5. Carriage of the MassRobotics Interoperability Standard messages.
