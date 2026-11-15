# PBS-TIME-01
## Open Clock Network: Time Distribution, Quality and Holdover

**Status:** Draft (proposed Optional Extension; not part of any PBS release)
**Version:** 0.1
**Applies to:** PBS relays, gateways and endpoints that evaluate envelope expiry
**Related:** PBS-ENV-01, PBS-SVC-01, PBS-PNT-CTX-01, PBS-PROX-01, PBS-CLP-01, PBS-HW-ID-01

---

## 1. Purpose

PBS-ENV-01 Section 15 requires every relay and gateway to keep a clock synchronized to Unix epoch time and defines no age field for a node without one. It does not say where that time comes from or how good it must be.

PBS-TIME-01 defines an open clock network that PBS nodes operate themselves: time is passed from node to node over the same radios and sessions that carry envelopes, each node states how uncertain its clock is, and a node that cannot bound its uncertainty stops making expiry decisions until it can.

The design goal is modest. Envelope lifetimes are in whole seconds (PBS-ENV-01 Section 12), so the network needs agreement within about a second, not nanoseconds. That is achievable with low-cost oscillators and occasional contact.

PBS-TIME-01 does not replace a positioning or precision-timing service and is not a source of legal or traceable time.

---

## 2. Roles

| Class | Role | Requirement |
|---:|---|---|
| 3 | Reference | Disciplined by at least two independent sources (Section 7) |
| 2 | Holdover | Synchronized from a reference or holdover node; oscillator drift bound of 2 ppm or better |
| 1 | Follower | Synchronized from any valid node; any oscillator with a stated drift bound |
| 0 | Unsynchronized | No valid time |

A node's class is what it is doing now, not what it was built as. A reference node that loses its sources becomes a holdover node.

---

## 3. Uncertainty

Every node tracks `U`, an upper bound on the error of its clock.

```text
U(t) = U_sync + rho × (t − t_sync)
```

`U_sync` is the uncertainty right after the last synchronization (Section 5.2), `t_sync` its time, and `rho` the node's stated worst-case drift rate.

- **PBS-TIME-REQ-001:** A node SHALL state `rho` for its oscillator over its operating temperature range and SHALL compute `U` as above.
- **PBS-TIME-REQ-002:** A node that restarts without a clock that kept running SHALL set its class to 0.

Informative holdover, for a budget of `U <= 1 s` after a synchronization with `U_sync = 50 ms`:

| Oscillator | Drift | Stays within 1 s for |
|---|---:|---:|
| 20 ppm crystal | 1.73 s/day | 13 hours |
| 2 ppm TCXO | 0.17 s/day | 5.5 days |
| 0.1 ppm OCXO | 0.009 s/day | 110 days |

---

## 4. Time Quality Byte

One byte summarizes a node's time. It is carried in the PBS-PROX-01 BEACON and in TIME-RESP.

- Bits 7–5: class (Section 2).
- Bits 4–0: exponent `e`. The node's `U` is at most `2^e` milliseconds. `e = 31` means unbounded.

Examples: `e = 5` means `U <= 32 ms`; `e = 10` means `U <= 1.024 s`.

---

## 5. Time Validity and Expiry Decisions

### 5.1 Valid time

A node has valid time when its class is 1 or higher and `U <= U_max`. The default `U_max` is 2 s; a deployment MAY set a smaller value.

- **PBS-TIME-REQ-010:** A node without valid time SHALL NOT discard an envelope as TTL-expired and SHALL NOT forward an envelope with `TTL > 0`. It holds such envelopes, subject to storage policy (PBS-PRIO-01 Section 7), until it has valid time.
- **PBS-TIME-REQ-011:** A node without valid time MAY forward an envelope with TTL `0` (PBS-ENV-01 Section 12.1).
- **PBS-TIME-REQ-012:** A node with valid time applies the PBS-ENV-01 Section 12.2 check with its clock, unchanged.

These rules define what "synchronized" means for PBS-ENV-01 Section 15. They add no field and change no PBS-ENV-01 behavior.

### 5.2 Guard band for commands

- **PBS-TIME-REQ-013:** A receiver delivering an envelope whose Service Intent data class is COMMAND or SERVICE_CONTROL (PBS-SVC-01 Section 4) SHOULD treat it as expired when `now + U` is later than its expiry instant.

A late command is the hazardous case (PBS-ENV-01 Section 12.4), so a receiver resolves doubt toward rejection.

---

## 6. Time Exchange

### 6.1 TIME-REQ and TIME-RESP

Used inside a PBS-PROX-01 session after AUTH. Times are Unix epoch microseconds.

| TIME-REQ field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x25` |
| Nonce | 8 | Random |
| T1 | 8 | Requester's clock at transmission |

| TIME-RESP field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x26` |
| Nonce | 8 | Copied from TIME-REQ |
| T2 | 8 | Responder's clock when TIME-REQ arrived |
| T3 | 8 | Responder's clock at transmission |
| Uncertainty | 4 | Responder's `U` in microseconds; `0xFFFFFFFF` unbounded |
| Quality | 1 | Section 4 |
| Hops | 1 | `0` for a reference node; otherwise the responder's source's hops plus 1 |
| Sources | 1 | Bitmap of Section 7 sources currently disciplining the path's reference |
| Holdover | 4 | Seconds since the responder last synchronized; `0` for a disciplined reference |
| Time scale | 1 | `0` = Unix epoch time (UTC-based). Other values reserved for PBSF assignment. |

TIME-REQ is 17 bytes and TIME-RESP 37 bytes; each fits one frame at the smallest MTU listed in PBS-CLP-01 Section 7.

With `T4` the requester's clock when TIME-RESP arrived:

```text
offset     = ((T2 − T1) + (T3 − T4)) / 2
round_trip = (T4 − T1) − (T3 − T2)
U_sync     = U_responder + round_trip / 2
```

Example: `T1 = 1000.000`, `T2 = 1000.340`, `T3 = 1000.350`, `T4 = 1000.700` s gives an offset of −0.005 s, a round trip of 0.690 s and a path term of 0.345 s. On slow links the path term dominates; a node SHOULD timestamp at the radio, and MAY subtract the known time on air of each frame from the round trip when both frames used the same settings.

- **PBS-TIME-REQ-020:** A requester SHALL discard a TIME-RESP whose nonce does not match an outstanding request.
- **PBS-TIME-REQ-021:** A requester SHALL NOT adopt time from a responder whose resulting `U_sync` is larger than the requester's current `U`.
- **PBS-TIME-REQ-022:** A node SHALL NOT answer TIME-REQ when its class is 0.
- **PBS-TIME-REQ-023:** A node SHALL NOT synchronize from a peer whose time was derived from the node itself. A node records the master device ID of its current source and SHALL NOT answer a TIME-REQ from that source. A `Hops` value above 15 is treated as unbounded uncertainty.

### 6.2 Broadcast TIME-STATEMENT

A reference or holdover node MAY broadcast a signed statement so that listeners can cross-check without a session: dispatch `0x29`, time (8), uncertainty (4), quality (1), sources (1), `key_id` length (1), `key_id`, Ed25519 signature (64) by a time-service key the deployment trusts. A statement gives a one-way bound only: the listener's clock is not earlier than the stated time minus the stated uncertainty.

### 6.3 Beacon time

The Epoch and Time quality fields of a PBS-PROX-01 BEACON are hints. A node uses them to decide whom to hail, not to set its clock (PBS-PROX-REQ-001).

---

## 7. Reference Sources

| Bit | Source |
|---:|---|
| 0 | GNSS, one constellation |
| 1 | GNSS, a second independent constellation |
| 2 | Terrestrial broadcast time signal |
| 3 | Authenticated network time (for example NTS, RFC 8915) |
| 4 | Another PBS-TIME-01 reference node over an authenticated session |
| 5 | Local atomic or oven-controlled oscillator in holdover from a prior discipline |
| 6 | LunaNet time service (PBS-PNT-CTX-01 REQ-006) |
| 7 | Reserved |

- **PBS-TIME-REQ-030:** A reference node SHALL discipline its clock only while at least two sources from different rows agree within the sum of their uncertainties. Two GNSS constellations received through one antenna and receiver count as one source for this rule when the threat includes jamming or spoofing.
- **PBS-TIME-REQ-031:** When sources disagree, a reference node SHALL stop disciplining, continue in holdover as class 2, and record the event.
- **PBS-TIME-REQ-032:** A node SHALL NOT step its clock by more than its current `U` plus the new source's `U_sync` on the word of a single source. A larger correction needs two sources that agree, or operator action.

---

## 8. Deployment (Informative)

The clock network is deployed with the communication hardware, not beside it.

- **No extra transmissions for discovery.** Time rides in five bytes of every beacon and in a 17/37-byte exchange at the start of a session that is happening anyway.
- **Reference nodes go where power and backhaul already are:** gateways, relay masts, access points, and on the lunar surface the powered relay and habitat nodes. A reference node needs its sources, an oscillator of holdover grade, and a clock that keeps running through a power interruption.
- **Battery nodes are followers.** With a 20 ppm crystal a node stays within a 1 s budget for about 13 hours after a contact; with a 2 ppm TCXO, about 5.5 days. Contact frequency and oscillator grade are traded against each other at design time.
- **A real-time clock with backup energy** lets a node keep class 1 or 2 through sleep or a power swap and avoid restarting at class 0 (PBS-TIME-REQ-002). Reference designs in PBS-HW-LIB SHOULD state the oscillator drift bound and backup duration.
- **Sparse networks.** A mobile node that visits a reference node carries time outward to nodes that never see one, at the cost of one hop of added uncertainty each time.

---

## 9. Security Considerations

- Time is safety-relevant: a clock that runs late keeps stale commands alive, and a clock that runs early discards live traffic. Sections 5.2 and 7 bound both.
- TIME-RESP is trusted only as far as the PBS-PROX-01 session is authenticated. Authentication identifies the responder; it does not make the responder's clock right. PBS-TIME-REQ-021 and PBS-TIME-REQ-032 limit what one wrong or malicious peer can do.
- A delayed TIME-RESP enlarges `round_trip` and therefore `U_sync`; it cannot make the requester more confident than the path allows.
- GNSS interference is the expected failure of bit 0 and bit 1 sources. PBS-TIME-REQ-030 exists so that it degrades a reference node to holdover instead of misleading the network.

---

## 10. Open Issues

1. Whether a relay with valid time may forward an envelope that is expired by less than `U` and leave the decision to the receiver. That would change PBS-ENV-01 Section 12.2 behavior and needs the PBS-GOV-01 Section 5 process.
2. Recording and exchanging evidence of a misbehaving time source.
3. Leap seconds: Unix epoch time repeats or skips a second; the effect is within `U_max` but should be stated.
4. Mapping between Unix epoch time and a lunar time scale for PBS-ENV-01 Timestamp on the Moon (PBS-PNT-CTX-01 REQ-006).
5. Whether TIME-STATEMENT needs a nonce-based variant for listeners that can transmit.
