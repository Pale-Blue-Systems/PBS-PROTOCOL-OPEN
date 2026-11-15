# PBS-PROX-01
## Proximity Sessions: Discovery, Authentication and Envelope Handover

**Status:** Draft (proposed Optional Extension; not part of any PBS release)
**Version:** 0.1
**Applies to:** PBS nodes that meet over short-range or opportunistic links, in space or on Earth
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-CAPS-01, PBS-POS-01, PBS-ROUTE-01, PBS-SEC-B-01, PBS-HW-ID-01, PBS-CLP-01, PBS-TIME-01

---

## 1. Purpose

PBS-ROUTE-01 assumes store-and-forward operation and PBS-CAPS-01 lets a node advertise what it can do, but no PBS specification says how two nodes that come into range find each other, prove who they are, agree on a link and hand over stored envelopes. PBS-CAPS-01 Section 6.5 places negotiation of security capabilities out of scope, and no PBS specification defines session establishment.

PBS-PROX-01 proposes one procedure intended to work over any link. The intent is that a scheduled contact and an unplanned meeting use the same session, and that the session gives a node, for an unplanned meeting, what a contact plan gives for a scheduled one: the neighbor, the link and the expected duration. None of this has been implemented or tested (Section 14).

PBS-PROX-01 messages are link-level. They are not PBS envelopes, are never forwarded, and do not change PBS-ENV-01.

---

## 2. Session Overview

```text
Initiator                                   Responder
    |  <------------- BEACON -------------      |   discovery (unauthenticated hint)
    |  -------------- HAIL --------------->     |
    |  <------------ HAIL-ACK -------------     |
    |  -------------- AUTH --------------->     |   mutual proof of master device ID
    |  <------------- AUTH ----------------     |
    |  <----------- PARAMS (both) -------->     |   link, context, queue summary
    |  <------ TIME-REQ / TIME-RESP ------>     |   PBS-TIME-01, before any transfer
    |  <== envelopes, highest priority first => |   PBS-CLP-01 datagrams
    |  <------------ XFER-ACK ------------>     |
    |  -------------- CLOSE -------------->     |
```

All messages use the PBS-CLP-01 Section 3 dispatch byte and MAY be segmented (PBS-CLP-01 Section 5). Multi-byte fields are big-endian.

| Dispatch | Message |
|---|---|
| `0x20` | BEACON |
| `0x21` | HAIL |
| `0x22` | HAIL-ACK |
| `0x23` | AUTH |
| `0x24` | PARAMS |
| `0x25` | TIME-REQ (PBS-TIME-01) |
| `0x26` | TIME-RESP (PBS-TIME-01) |
| `0x27` | XFER-ACK |
| `0x28` | CLOSE |
| `0x29` | TIME-STATEMENT (PBS-TIME-01) |

---

## 3. Link Types

A 16-bit bitmap names the links a node can use in a session.

| Bit | Link |
|---:|---|
| 0 | Sub-GHz chirp spread spectrum (LoRa physical layer used directly; not LoRaWAN, see Section 11) |
| 1 | Bluetooth Low Energy |
| 2 | Wi-Fi Aware (Neighbor Awareness Networking) |
| 3 | IEEE 802.11ah (Wi-Fi HaLow) |
| 4 | IP over any infrastructure network |
| 5 | ISO/IEC 15693 contactless (PBS-HW-ID-01 passive interface) |
| 6 | CCSDS Proximity-1 |
| 7 | LunaNet proximity interface (LNIS V005 Section 4.1, LNSP-User Proximity Interfaces) |
| 8 | Wired serial or Ethernet |
| 9 | Ultra-wideband ranging radio (IEEE 802.15.4z) |
| 10 | Optical (coded light or display read by a camera) |
| 11–15 | Reserved for PBSF assignment |

Discovery MAY happen on one link and transfer on another: two nodes can hail on a low-rate link and move bulk transfer to a faster one both support.

---

## 4. BEACON

A beacon is 19 bytes. A Bluetooth LE legacy advertisement carries at most 31 bytes of advertising data, so a beacon fits in one together with the structure headers it needs; Section 11 states what else that requires. On a sub-GHz link, whether a 19-byte frame is permitted at a given data rate depends on the region (PBS-CLP-01 Section 7).

| Field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x20` |
| Version and flags | 1 | Bits 7–4: version `1`. Bit 3: accepts HAIL. Bit 2: has traffic to send. Bit 1: relay. Bit 0: rotating ID. |
| Short ID | 8 | First 8 bytes of the master device ID (PBS-HW-ID-01 REQ-011), or 8 random bytes when the rotating ID flag is set |
| Link bitmap | 2 | Section 3 |
| Time quality | 1 | PBS-TIME-01 Section 4 |
| Epoch | 4 | Sender's Unix time in seconds at transmission |
| Queue | 1 | Bits 7–4: highest priority class waiting (0–4), `0xF` if none. Bits 3–0: floor(log2(envelopes waiting + 1)), capped at 15. |
| Link hint | 1 | Link-specific (for example a data-rate index); `0` if unused |

- **PBS-PROX-REQ-001:** A beacon is unauthenticated. A receiver SHALL treat every beacon field as a hint and SHALL NOT set its clock from a beacon alone (PBS-TIME-01 Section 6).
- **PBS-PROX-REQ-002:** A node SHALL rate-limit beacons and SHALL comply with the duty-cycle and channel rules of the band and region in which it transmits.
- **PBS-PROX-REQ-003:** A node that sets the rotating ID flag SHALL change the random Short ID at least once per hour.

Beacons MAY be omitted where contacts are scheduled; the initiator then sends HAIL at the planned time.

---

## 5. HAIL and HAIL-ACK

| Field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x21` HAIL, `0x22` HAIL-ACK |
| Version and flags | 1 | Bits 7–4: version `1`. Bit 0: ephemeral key present. |
| Master device ID | 16 | Sender's ID (PBS-HW-ID-01 REQ-011) |
| Nonce | 16 | Random, new for every session |
| Link bitmap | 2 | Links the sender offers for this session |
| MTU | 2 | Largest link frame the sender accepts on the current link |
| Ephemeral key | 0 or 32 | X25519 public key (RFC 7748), when the flag is set |

HAIL and HAIL-ACK are 38 bytes, or 70 with an ephemeral key.

- **PBS-PROX-REQ-010:** A nonce SHALL come from a cryptographically secure source and SHALL NOT be reused.
- **PBS-PROX-REQ-011:** An initiator that receives no HAIL-ACK SHALL back off exponentially with random jitter before the next HAIL.

---

## 6. AUTH

Each side proves possession of the private key behind its master device ID, using the PBS-HW-ID-01 Section 5.5 `SIGN_CHALLENGE` command unchanged.

```text
C_role = SHA-256( "PBS-PROX-v1" || role ||
                  ID_initiator || ID_responder ||
                  Nonce_initiator || Nonce_responder ||
                  LinkBitmap_i || MTU_i || LinkBitmap_r || MTU_r ||
                  EphemeralKey_i || EphemeralKey_r )
```

`role` is the ASCII byte `I` for the initiator's proof and `R` for the responder's. Absent ephemeral keys contribute no bytes. `C_role` is 32 bytes, within the 16–64 byte challenge range of `SIGN_CHALLENGE`; the tag signs `PBS-HWID-v1-CHALLENGE || C_role`.

| Field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x23` |
| Public key | 32 | Sender's Ed25519 public key (`GET_INFO`) |
| Signature | 64 | Signature over the sender's `C_role` |
| Certificate length | 2 | `0` if none |
| Binding certificate | variable | PBS-HW-ID-01 Section 6 COSE_Sign1 |

- **PBS-PROX-REQ-020:** A receiver SHALL check that the public key derives the master device ID sent in HAIL or HAIL-ACK (PBS-HW-ID-01 REQ-011) and that the signature verifies over the peer's `C_role`. On failure it SHALL send CLOSE and end the session.
- **PBS-PROX-REQ-021:** A receiver SHALL accept a binding certificate only under PBS-HW-ID-01 REQ-081. An accepted certificate binds the peer's Source ID to its master device ID for this session.
- **PBS-PROX-REQ-022:** A node SHALL NOT send or accept envelopes in a session before both AUTH messages verify, except where deployment policy explicitly allows unauthenticated transfer of envelopes that carry PBS-SEC-B-01 protection.
- **PBS-PROX-REQ-023:** Authentication proves which unit is present. It does not grant authority. Command acceptance remains governed by PBS-AUTH-01 and PBS-SEC-B-01.

---

## 7. PARAMS

Each side sends one PARAMS after AUTH.

| Field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x24` |
| Selected link | 1 | Bit number from Section 3; the initiator's choice prevails if the two differ and both support it |
| Flags | 1 | Bit 0: compression accepted (PBS-CLP-01). Bit 1: uncompressed only. Bit 2: time offered (PBS-TIME-01). Bit 3: time requested. |
| Contact estimate | 2 | Expected remaining contact in seconds; `0xFFFF` unknown |
| Time base | 8 | PBS-CLP-01 time base in Unix epoch microseconds for envelopes this side will send |
| Queue summary | 10 | Five 16-bit counts of envelopes waiting, priority class 0 to 4 |
| Context count | 1 | Number of context entries that follow |
| Context entries | 17 each | Context ID (1) and Source ID (16) this side will use when sending |

- **PBS-PROX-REQ-030:** A context entry takes effect for the sender once the peer's next XFER-ACK or PARAMS acknowledges it. Until then the sender uses the inline Source ID form.

---

## 8. Transfer and XFER-ACK

- **PBS-PROX-REQ-040:** Before transfer, a node whose clock is not valid under PBS-TIME-01 Section 5 SHALL obtain time from the peer if the peer offers it.
- **PBS-PROX-REQ-041:** A sender SHALL apply the PBS-ENV-01 Section 12.2 check before sending each envelope and SHALL send in priority order (PBS-PRIO-01 Section 6), highest class first.
- **PBS-PROX-REQ-042:** Both sides MAY send. When the link is half-duplex, the side holding the higher-priority traffic sends first; ties go to the initiator.

| Field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x27` |
| Tag | 1 | Datagram tag (PBS-CLP-01 Section 5), or Sequence low byte for an unsegmented envelope |
| Status | 1 | `0` received and stored; `1` segments missing; `2` rejected (invalid); `3` rejected (storage full); `4` rejected (policy) |
| Bitmap length | 1 | Bytes of bitmap that follow |
| Missing bitmap | variable | One bit per segment, set if missing (status `1`) |

- **PBS-PROX-REQ-043:** XFER-ACK status `0` means the receiver holds the envelope. It is not acceptance by the destination and does not satisfy an ACK_REQ flag (PBS-ENV-01 Section 7).
- **PBS-PROX-REQ-044:** After status `0`, the sender handles its own copy under the envelope's persistence policy (PBS-SVC-01 Section 7) and local policy. PBS-PROX-01 defines no custody transfer.

---

## 9. Link Protection (Optional)

When both sides sent ephemeral keys, they share `K = HKDF-SHA-256(X25519 secret, salt = C_I || C_R, info = "PBS-PROX-v1 link")`. Because both ephemeral keys are inside the signed challenges, `K` is bound to the authenticated units. A later revision of this document will define per-frame integrity using `K`. Until then, PBS-SEC-B-01 remains the protection for envelope content.

---

## 10. CLOSE and Timers

CLOSE is `0x28` followed by one reason byte: `0` complete, `1` authentication failed, `2` contact ending, `3` policy, `4` error.

- **PBS-PROX-REQ-050:** A session with no valid frame for 30 s (default, configurable per link) is closed without CLOSE. State from that session, including PBS-CLP-01 context, is discarded.

---

## 11. Relationship to Existing Protocols

This section states what the named protocols provide and what has and has not been examined. PBS-PROX-01 is not derived from any of them and does not interoperate with any of them.

- **PBS-CAPS-01 and PBS-POS-01** remain the way to describe a node in detail. They travel as envelopes after the session is up.
- **CCSDS Proximity-1.** Its Data Link Layer defines the procedures for establishing and terminating a session between a caller and a responder (CCSDS 211.0-B-5, adopted as ISO 22663:2015). Its Physical Layer defines a hailing channel and, in the edition adopted as ISO 21460:2015, operation at UHF for the Mars environment only. Where a Proximity-1 link is in use, the intent is that PBS-PROX-01 begins at HAIL over the established link. That arrangement has not been designed in detail.
- **Bluetooth LE.** A legacy advertisement carries at most 31 bytes of advertising data, organized as structures with a one-byte length and one-byte type. Carrying a BEACON as Service Data or Manufacturer Specific Data requires a 16-bit UUID or a company identifier assigned by the Bluetooth SIG. PBSF holds neither.
- **Wi-Fi Aware** provides its own discovery and pairing. Carriage of BEACON content in its service discovery has not been examined.
- **LoRa and LoRaWAN.** LoRaWAN defines communication between end devices and network gateways; it is not a device-to-device protocol. Link bit 0 therefore means the LoRa physical layer used directly. A node doing so is itself responsible for the duty-cycle and dwell-time rules of its region.
- **BPv7.** A PBS-PROX-01 session could serve as a contact between two bundle nodes. No convergence-layer binding is defined, and none has been proposed to the IETF DTN working group.

## 12. Security and Privacy Considerations

- A beacon reveals a stable Short ID to any listener. Deployments where units must not be trackable use the rotating ID flag.
- AUTH resists replay and reflection because each proof covers both fresh nonces and a role byte. It does not stop a relay attack in which an adversary forwards messages between two real units; link-specific ranging or time-of-flight limits are out of scope.
- The tag signs any challenge a reader presents (PBS-HW-ID-01). The `PBS-PROX-v1` prefix inside the hashed challenge keeps session proofs distinct from other uses of `SIGN_CHALLENGE`.
- HAIL flooding consumes signature operations. A node SHOULD limit concurrent unauthenticated sessions.

---

## 13. Open Issues

1. Per-frame link protection (Section 9) is unspecified.
1a. Measured proximity. AUTH proves identity, not distance. A session on a ranging-capable link (Section 3, bits 9 and 10) should be able to carry a distance or line-of-sight measurement bound to the session challenge, and report it with the result, so that a receiver can require presence and not only identity.
1b. Disagreement reporting. A node that hears conflicting time or identity on different links has no message in which to record and publish it.
2. Signing with the tag requires the tag to be powered and reachable by the host during AUTH. Whether a host-held session key certified by the tag should be allowed needs a decision.
3. Channel plans and beacon intervals per link type are not defined.
4. Group sessions (one sender, several receivers) are not defined.
5. The BPv7 convergence-layer binding (Section 11) is not defined.

---

## 14. Basis and Limits

- **Checked by computation:** the message sizes in Sections 4 to 8, and that an Ed25519 signature over the initiator's Section 6 challenge does not verify as the responder's.
- **Taken from other PBS documents:** the `SIGN_CHALLENGE` command, its 16 to 64 byte challenge and its signing prefix (PBS-HW-ID-01 Section 5.5), the master device ID derivation (REQ-011) and the binding certificate (Section 6).
- **Not done:** no implementation exists. No message has been sent over any radio. Timers, back-off and the 30 s session timeout are estimates. The design has had no security review, and Section 12 lists a relay attack it does not prevent.
- **Prior work not yet reviewed:** neighbor discovery proposals from the DTN research community, and the discovery and ranging procedures of IEEE 802.15.4z. Either may supersede parts of this draft.

## 15. References

- CCSDS 211.0-B-5, *Proximity-1 Space Link Protocol: Data Link Layer*, December 2013 (ISO 22663:2015).
- ISO 21460:2015, *Space data and information transfer systems: Proximity-1 space link protocol: Physical layer*.
- NASA, ESA and JAXA, *LunaNet Interoperability Specification*, Version 5, 29 January 2025.
- RFC 7748, *Elliptic Curves for Security*. RFC 8032, *Edwards-Curve Digital Signature Algorithm (EdDSA)*. RFC 5869, *HMAC-based Extract-and-Expand Key Derivation Function (HKDF)*.
- Bluetooth SIG, *Bluetooth Core Specification*, advertising data format. Figures here were taken from vendor documentation of that format, not from the specification text.
