# PBS-DTN-MAP-01

## Mapping to Delay/Disruption Tolerant Networking (DTN)

**Status:** Optional (Interoperability)
**Version:** 1.5
**Changes:** 2026-10-06 (PBS v1.5.0): Section 6.1 bounds the bundle lifetime by the time remaining until the envelope expires, assigns the creation timestamp to the gateway's bundle protocol agent (RFC 9171 Section 4.2.7), maps neither `Sequence` nor `Priority` to a primary block field, and does not encapsulate an envelope with less than 1 ms remaining; new Section 6.1.1 sets the bundle lifetime for TTL `0` where no PBS-DTN-MAP-02 Section 4 finite limit applies. Section 6.3 covers all five PBS-PRIO-01 priority classes, LOW included, prohibits conveying priority in reserved or unassigned bundle processing control flags, and requires a mapping profile for priority-based network treatment (PBS-DTN-MAP-02 Section 5) in which no priority class requests a more favorable treatment than a higher-priority class. Section 7.3 evaluates PBS expiry against Timestamp and forbids TTL modification. Related adds PBS-DTN-MAP-02. Wire format unchanged.
**Applies to:** PBS Gateway Implementations Interfacing with DTN / BPv7
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-SEC-A-01, PBS-ROUTE-01, PBS-DTN-MAP-02

---

## 1. Purpose

This document defines the **normative mapping** between the Pale Blue Systems (PBS) Open Standard and **Delay/Disruption Tolerant Networking (DTN)** environments, including **Bundle Protocol Version 7 (BPv7, IETF RFC 9171)**.

PBS-DTN-MAP-01 enables PBS-native systems to interoperate with NASA, international space agencies, and other operators that employ DTN infrastructure, without requiring PBS Core to adopt DTN semantics internally.

The goal is **semantic preservation with minimal compute and power overhead**.

---

## 2. Scope

This specification applies **only at DTN boundaries**:

- PBS-native domains (e.g., intralunar surface mesh, habitat networks)
- DTN-enabled links (e.g., Earth relay, lunar relay, deep-space backbone)

Within PBS-native domains, **DTN wrapping is NOT required**.

---

## 3. Design Principles

PBS-to-DTN mapping follows these principles:

- **Boundary translation, not replacement:** PBS remains the primary protocol.
- **Minimal transformation:** Preserve PBS semantics wherever possible.
- **No semantic leakage:** DTN concepts MUST NOT alter PBS Core behavior.
- **Store-and-forward alignment:** Mapping respects DTN operational assumptions.
- **Energy efficiency:** Avoid unnecessary re-encoding or re-signing.

---

## 4. Architectural Position

PBS-DTN-MAP operates at a **gateway boundary**, typically implemented as a relay or edge node.

    PBS Native Domain            DTN Domain

    +------------------+     +----------------------+
    |  PBS Envelopes   | --> |  BPv7 Bundles        |
    |  (PBS-ENV-01)    |     |  (CCSDS / ION)       |
    +------------------+     +----------------------+
             ▲                          |
             |                          ▼
    +------------------+     +----------------------+
    |  PBS Envelopes   | <-- |  BPv7 Bundles        |
    +------------------+     +----------------------+

PBS-DTN-MAP nodes act as **protocol translators**, not originators.

---

## 5. Mapping Overview

### 5.1 One-to-One Envelope Mapping

Each PBS Envelope SHALL map to **exactly one BPv7 Bundle**.

Rules:
- PBS envelopes MUST NOT be fragmented across multiple bundles.
- Bundle fragmentation MAY be performed by DTN layers below BPv7 if required.

---

## 6. PBS to BPv7 Mapping (Outbound)

### 6.1 Primary Block

| PBS Field | BPv7 Field | Mapping Rule |
|---------|------------|--------------|
| `Source ID` | Source EID | 16-byte device name mapped to EID (e.g., "Rover-Alpha" → "ipn:99.1") |
| Gateway Config | Destination EID | Configured at gateway (not in PBS envelope) |
| `TTL` | Lifetime | `TTL > 0`: no greater than the interval remaining until the envelope expires (rules below). `TTL = 0`: the no-expiry lifetime, unless a PBS-DTN-MAP-02 Section 4 finite limit applies (Section 6.1.1) |
| Gateway BPA | Creation Timestamp | Assigned by the gateway's bundle protocol agent (BPA) per RFC 9171 Section 4.2.7 (not from PBS envelope fields) |
| `Sequence` | None | Not mapped to a primary block field; carried in the encapsulated envelope (Section 6.2) |
| `Priority` | None | Not mapped to a primary block field; carried in the encapsulated envelope (Section 6.2). Network treatment: Section 6.3 |

Rules:
- For an envelope with `TTL > 0`, the bundle lifetime SHALL NOT exceed `⌊(TTL × 1_000_000 − max(0, c_us − Timestamp)) / 1000⌋` milliseconds, where `c_us` is the bundle creation time converted to Unix epoch microseconds, `(creation_time_ms + 946_684_800_000) × 1000` (RFC 9171 Sections 4.2.6 and 4.2.7), or the gateway's Unix epoch time in microseconds at bundle creation when the creation time is `0`. RFC 9171 Section 4.3.1 counts lifetime in milliseconds past the creation time and PBS-ENV-01 Section 12.2 counts TTL from `Timestamp`, so the bundle expires no later than the envelope (PBS-DTN-MAP-02 Section 4). An envelope for which this value is less than `1` has expired or has less than 1 ms remaining before it expires, and SHALL NOT be encapsulated. A gateway that computes the lifetime before its BPA assigns the creation time meets this bound by using for `c_us` a time not earlier than that creation time, such as its clock reading plus the maximum latency of the transmission request.
- The no-expiry lifetime is not less than any lifetime the gateway assigns (Section 6.1.1), so the bundle lifetime for an envelope with `TTL > 0` does not exceed it. Where the bound of the first rule is larger, the bundle can expire before the envelope; that deletion is not TTL expiry (PBS-ENV-01 Section 12.1).
- The bundle creation timestamp, comprising the bundle creation time and the sequence number, SHALL be assigned as specified in RFC 9171 Section 4.2.7 by the BPA of the gateway, which creates the bundle.
- The gateway MUST NOT derive the creation timestamp sequence number from the PBS `Sequence` field. The PBS `Sequence` field is assigned by the PBS source, is 16 bits wide and rolls over from 65535 to 0 (PBS-ENV-01 Sections 4 and 8); RFC 9171 Section 4.2.7 requires the latest value of a monotonically increasing positive integer counter managed by the source node's BPA.
- The PBS `Sequence` field is carried unchanged in the encapsulated envelope (Sections 6.2 and 6.4). PBS sequence tracking (PBS-ENV-01 Section 8) applies to the `Sequence` field of the extracted envelope (Section 7.2), not to the bundle creation timestamp.

#### 6.1.1 Lifetime for TTL 0

An envelope with TTL `0` never expires (PBS-ENV-01 Section 12.1). BPv7 encodes bundle lifetime as an unsigned integer number of milliseconds past the creation time and defines no value for an unlimited lifetime (RFC 9171 Section 4.3.1).

For an envelope with TTL `0`, the gateway SHALL set the bundle lifetime to its no-expiry lifetime, unless the gateway also implements PBS-DTN-MAP-02 and a finite deadline, maximum age or mission expiry limit applies to the message (PBS-DTN-MAP-02 Section 4); the bundle lifetime is then bounded as PBS-DTN-MAP-02 Section 4 specifies. The no-expiry lifetime:
- SHALL be greater than `0` ms;
- SHALL NOT be less than the lifetime the gateway assigns to any envelope with TTL greater than `0` or to which a PBS-DTN-MAP-02 Section 4 finite limit applies;
- SHALL NOT exceed `4294967295000` ms, the largest lifetime Section 6.1 permits for an envelope with TTL greater than `0` (TTL `4294967295` s);
- SHALL be a value that the gateway's bundle protocol agent accepts and for which the expiration time that agent computes, creation time plus lifetime (RFC 9171 Section 5.5), does not overflow.

The gateway SHALL document its no-expiry lifetime and the bundle protocol agent for which it was selected, and SHOULD use the largest value that meets these conditions. For a bundle protocol agent that holds DTN time and expiration time in 64-bit integers, that value is `4294967295000` ms. A bundle protocol agent that holds expiration time as a 32-bit count of seconds cannot represent `4294967295000` ms, which is (2^32 − 1) s, past the creation time: the expiration time wraps into the past and the agent deletes the bundle at once.

RFC 9171 Section 4.3.1 permits the bundle protocol agent of a node to impose a shorter overriding lifetime while the bundle resides at that node. A bundle protocol agent deletes a bundle whose age exceeds its lifetime or an overriding lifetime (RFC 9171 Section 5.5), and the envelope it carries is lost with it. A gateway that receives a bundle whose lifetime has expired discards the envelope (Section 7.3). Neither deletion is TTL expiry (PBS-ENV-01 Section 12.1).

---

### 6.2 Payload Block

Rules:
- The **entire PBS envelope** (44-byte header + payload) SHALL be placed into a single BPv7 Payload Block.
- PBS envelope contents MUST NOT be interpreted or altered by the DTN layer.
- The PBS CRC32 MUST be preserved for end-to-end integrity verification.

---

### 6.3 Priority Handling

RFC 9171 defines no class-of-service field. The BPv7 primary block has none (RFC 9171 Section 4.3.1), and bundle processing control flag bits 7–8, which carry the class-of-service priority in Bundle Protocol version 6 (RFC 5050 Section 4.2), are reserved in BPv7 (RFC 9171 Section 4.2.3) and registered for Bundle Protocol version 6 only (RFC 9171 Section 9.3). A BPv7 deployment that offers class of service or other network treatment provides it through a bundle protocol agent interface or an extension block that RFC 9171 does not define.

Rules:
- No primary block field carries PBS `Priority` (Section 6.1). Priority is carried in the envelope header within the payload block (Section 6.2) and extracted unchanged at the inbound gateway (Section 7.2).
- Gateways MUST NOT set reserved or unassigned bundle processing control flags (RFC 9171 Section 4.2.3), including bits 7 and 8, to convey PBS priority.
- A gateway that requests network treatment for a bundle on the basis of PBS priority SHALL document the mapping in a mapping profile containing the items listed in PBS-DTN-MAP-02 Section 5: the BP QoS mechanism or extension used, queue/scheduling treatment, behavior under congestion, and behavior when the requested treatment is unavailable. The mapping profile SHALL define the treatment requested for each priority class of PBS-PRIO-01 Section 4.
- A gateway that requests treatments other than the DTN classes below SHALL list them in its mapping profile in order from most to least favorable. When all other inputs to the mapping are equal, the gateway SHALL NOT request for a priority class a treatment more favorable than the treatment it requests for any higher-priority class.
- A gateway that requests the Expedited, Normal and Bulk priority classes of the DTN architecture (RFC 4838 Section 3.5) SHALL request, for each PBS priority class, the class in the following table:

| PBS Priority | DTN class |
|-------------|-----------|
| CRITICAL (0) | Expedited |
| HIGH (1) | Expedited |
| NORMAL (2) | Normal |
| LOW (3) | Bulk |
| BULK (4) | Bulk |

The mapping does not modify the envelope. A PBS node that receives the restored envelope recovers all five classes, including CRITICAL and HIGH, and LOW and BULK, which share a DTN class.

Mapping preserves **relative urgency**, not scheduling behavior.

---

### 6.4 Security Handling (Outbound)

Rules:
- PBS CRC32 integrity (PBS-SEC-A-01) MUST be preserved end-to-end.
- DTN security mechanisms (e.g., BPSEC) MAY be applied additionally at the bundle layer.
- DTN security operates at the bundle layer and does not replace PBS header integrity.

PBS envelopes MUST NOT be modified during DTN encapsulation.

---

## 7. BPv7 to PBS Mapping (Inbound)

### 7.1 Bundle Validation

Upon receipt of a BPv7 bundle:

- DTN-layer validation MUST occur first.
- Invalid bundles MUST be discarded before PBS processing.

---

### 7.2 Envelope Restoration

Rules:
- The PBS envelope payload SHALL be extracted verbatim.
- No modification to PBS envelope fields is permitted.
- The envelope SHALL be reintroduced into PBS-native routing.

---

### 7.3 TTL Handling

Rules:
- DTN lifetime expiration, as determined by the bundle protocol agent (RFC 9171 Section 5.5), MUST result in envelope discard.
- PBS `ttl` MUST NOT be modified.
- Within PBS-native hops, an envelope with `ttl` greater than `0` expires when more than `ttl` seconds have elapsed since its PBS `Timestamp` (PBS-ENV-01 Section 12.2). Time spent in the DTN domain counts toward that interval. Section 12.2 does not apply to an envelope with `ttl` `0` (PBS-ENV-01 Section 12.1). Discard on DTN lifetime expiration is not TTL expiry.

---

## 8. Source ID to EID Translation

PBS Source IDs MUST be translated to **DTN Endpoint Identifiers (EIDs)** at gateway boundaries.

Rules:
- Source ID to EID mapping MUST be deterministic within a gateway.
- Gateways SHOULD maintain a mapping table (e.g., "Rover-Alpha" → "ipn:99.1").
- Destination EIDs are configured at the gateway level (not in PBS envelope).

Example mapping:
```
Source ID       →  DTN Source EID
"Rover-Alpha"   →  ipn:99.1
"Drill-01"      →  ipn:99.2
"Habitat-Main"  →  ipn:99.100
```

Exact EID syntax is implementation-defined but MUST be stable within a deployment.

---

## 9. Store-and-Forward Semantics

PBS-DTN-MAP nodes MUST support store-and-forward behavior.

Rules:
- Envelopes MAY be stored until DTN contact is available.
- Storage decisions SHOULD consider PBS priority and TTL.
- DTN custody transfer MAY be used if supported.

DTN storage does not alter PBS routing semantics.

---

## 10. Failure Handling

Rules:
- Failure to forward via DTN MUST NOT invalidate the PBS envelope.
- Envelopes MAY be retried, delayed, or discarded based on policy.
- DTN errors MUST NOT propagate as PBS protocol errors.

---

## 11. Interoperability Expectations

A PBS Core conformant system implementing PBS-DTN-MAP-01 can:

- communicate with NASA DTN infrastructure (e.g., ION)
- interoperate with international and commercial DTN-enabled systems
- preserve PBS semantics across interplanetary links

PBS-DTN-MAP ensures **compatibility without coupling**.

---

## 12. Power and Compute Considerations

PBS-DTN-MAP is designed for constrained environments.

Rules:
- Mapping SHOULD avoid envelope reserialization where possible.
- Cryptographic operations MUST NOT be duplicated unnecessarily.
- Gateways SHOULD minimize buffer copies.

---

## 13. Forward Compatibility

Rules:
- New PBS envelope fields MUST NOT break DTN mapping.
- DTN extensions MUST NOT leak into PBS Core semantics.
- Major DTN version changes MAY require a new mapping document.

---

## 14. Summary

PBS-DTN-MAP-01 defines the gateway mapping between PBS Core envelopes and BPv7 bundles. DTN applies at gateway boundaries only; PBS-native domains do not require DTN wrapping (Section 2).

PBS-DTN-MAP-01 defines a **clean, minimal, and deterministic bridge** between PBS Core and DTN environments.

By treating DTN as a boundary transport rather than an internal dependency, PBS enables commercial, civil, and international systems to interoperate across Earth, lunar, and deep-space domains while preserving performance, security, and architectural independence.