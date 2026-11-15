# PBS-PROX-01
## Proximity Sessions: Discovery, Authentication and Envelope Handover

**Status:** Draft (proposed Optional Extension; not part of any PBS release)
**Version:** 0.1
**Applies to:** PBS nodes that meet over short-range or opportunistic links, in space or on Earth
**Related:** PBS-ENV-01, PBS-PRIO-01, PBS-CAPS-01, PBS-POS-01, PBS-ROUTE-01, PBS-SEC-B-01, PBS-HW-ID-01, PBS-CLP-01, PBS-TIME-01

---

## 1. Purpose

PBS-ROUTE-01 assumes store-and-forward operation and PBS-CAPS-01 lets a node advertise what it can do, but no PBS specification says how two nodes that come into range find each other, prove who they are, agree on a link and hand over stored envelopes. PBS-CAPS-01 Section 6.5 places negotiation out of scope.

PBS-PROX-01 defines that procedure once, for any radio. A scheduled contact in a DTN contact plan and an unplanned meeting between two ground devices use the same session. The session supplies what a contact plan supplies where contacts are scheduled: the neighbor, the link and the expected duration.

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
| 0 | Sub-GHz chirp spread spectrum (LoRa) |
| 1 | Bluetooth Low Energy |
| 2 | Wi-Fi Aware (Neighbor Awareness Networking) |
| 3 | IEEE 802.11ah (Wi-Fi HaLow) |
| 4 | IP over any infrastructure network |
| 5 | ISO/IEC 15693 contactless (PBS-HW-ID-01 passive interface) |
| 6 | CCSDS Proximity-1 |
| 7 | LunaNet proximity link (PBS-LNIS-01) |
| 8 | Wired (PBS-HW-CON-01 or Ethernet) |
| 9–15 | Reserved for PBSF assignment |

Discovery MAY happen on one link and transfer on another: two nodes can hail on a low-rate link and move bulk transfer to a faster one both support.

---

## 4. BEACON

A beacon is 19 bytes, small enough for the service data of a BLE legacy advertisement. Its time on air on a sub-GHz link depends on the regional settings in use.

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

## 11. Relationship to Other Specifications

- **PBS-CAPS-01 and PBS-POS-01** remain the way to describe a node in detail. They travel as envelopes after the session is up.
- **CCSDS Proximity-1** provides hailing and link establishment for its own links. Where it is in use, PBS-PROX-01 starts at HAIL over the established link.
- **Wi-Fi Aware, BLE** provide their own discovery. BEACON content MAY be carried in their service-discovery payloads.
- **BPv7:** a PBS-PROX-01 session can serve as a convergence-layer contact between two bundle nodes; that binding is future work.

---

## 12. Security and Privacy Considerations

- A beacon reveals a stable Short ID to any listener. Deployments where units must not be trackable use the rotating ID flag.
- AUTH resists replay and reflection because each proof covers both fresh nonces and a role byte. It does not stop a relay attack in which an adversary forwards messages between two real units; link-specific ranging or time-of-flight limits are out of scope.
- The tag signs any challenge a reader presents (PBS-HW-ID-01). The `PBS-PROX-v1` prefix inside the hashed challenge keeps session proofs distinct from other uses of `SIGN_CHALLENGE`.
- HAIL flooding consumes signature operations. A node SHOULD limit concurrent unauthenticated sessions.

---

## 13. Open Issues

1. Per-frame link protection (Section 9) is unspecified.
2. Signing with the tag requires the tag to be powered and reachable by the host during AUTH. Whether a host-held session key certified by the tag should be allowed needs a decision.
3. Channel plans and beacon intervals per link type are not defined.
4. Group sessions (one sender, several receivers) are not defined.
5. The BPv7 convergence-layer binding (Section 11) is not defined.
