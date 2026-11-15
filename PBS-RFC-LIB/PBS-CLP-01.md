# PBS-CLP-01
## Constrained Link Profile: Link Dispatch, Header Compression and Segmentation

**Status:** Draft (proposed Optional Extension; not part of any PBS release)
**Version:** 0.1
**Applies to:** PBS nodes exchanging envelopes over links whose frame size is smaller than a typical envelope (for example LoRa, BLE, ISO/IEC 15693)
**Related:** PBS-ENV-01, PBS-SEC-A-01, PBS-ROUTE-01, PBS-DTN-MAP-02, PBS-PROX-01, PBS-TIME-01

---

## 1. Purpose

PBS-ENV-01 fixes a 44-byte header and requires relays to forward it byte for byte (PBS-ENV-01 Section 15). A PBS-SEC-B-01 protected envelope with Service Intent carries 160 bytes of overhead around its application data (Section 7). Many low-power radios carry less than that in one frame.

PBS-CLP-01 defines, for one hop between two adjacent nodes:

- a one-byte link dispatch that tells envelope, compressed envelope, segment and PBS-PROX-01 message apart;
- a lossless compression of the PBS-ENV-01 header that restores the identical 44 bytes;
- segmentation and reassembly of a datagram larger than the link frame.

PBS-CLP-01 does not change the PBS-ENV-01 wire format. An envelope leaving a PBS-CLP-01 hop is byte-identical to the envelope that entered it. PBS-DTN-MAP-02 Section 2 refers to a registered segmentation profile; Section 5 of this document is proposed as that profile for link-level use.

---

## 2. Terms

- **Link frame:** one unit of data delivered whole by the link, of at most `MTU` bytes.
- **Datagram:** one envelope (compressed or not) or one PBS-PROX-01 message.
- **Context:** state two adjacent nodes share for one session: a table of context IDs to 16-byte Source IDs, and a 64-bit time base in Unix epoch microseconds. PBS-PROX-01 Section 7 establishes it.

All multi-byte fields are in network byte order (big-endian).

---

## 3. Link Dispatch

The first byte of every link frame is the dispatch byte.

| First byte | Meaning |
|---|---|
| `0x10` | Uncompressed PBS envelope (the PBS-ENV-01 Magic) |
| `0x11`–`0x1F` | Reserved for future PBS-ENV Magic values |
| `0x20`–`0x2F` | PBS-PROX-01 and PBS-TIME-01 messages |
| `0x40`–`0x7F` | Segment (Section 5) |
| `0x80`–`0xFF` | Compressed PBS envelope (Section 4) |
| all other values | Reserved |

- **PBS-CLP-REQ-001:** A receiver SHALL discard a link frame whose dispatch byte is reserved.
- **PBS-CLP-REQ-002:** A node SHALL be able to receive an uncompressed envelope on any link on which it accepts compressed envelopes.

---

## 4. Header Compression

### 4.1 Compressed form

| Field | Size | Content |
|---|---:|---|
| CTL | 1 | Bit 7 = `1`. Bits 6–4 = Priority (0–4). Bit 3 = ACK_REQ. Bits 2–1 = TTL form. Bit 0 = Timestamp form. |
| SID | 1 or 17 | `0x00`–`0xFE`: context ID. `0xFF`: the 16 Source ID bytes follow. |
| Sequence | 2 | As in the header |
| Timestamp | 5 or 8 | Form 0: `Timestamp − time base` as a 40-bit unsigned integer. Form 1: the 8 header bytes. |
| TTL | 0, 1, 2 or 4 | Form 0: TTL is `0`, no bytes. Forms 1, 2, 3: TTL in 1, 2 or 4 bytes. |
| CRC32 | 4 | The originator's CRC32, bytes 0x28–0x2B of the header |
| Payload | Size | The envelope payload, unchanged |

Magic, both reserved fields and Size are not carried. Size equals the number of payload bytes in the datagram.

### 4.2 Sender rules

- **PBS-CLP-REQ-010:** A sender SHALL verify the header CRC32 (PBS-ENV-01 Section 13.1) before compressing.
- **PBS-CLP-REQ-011:** A sender SHALL compress a header only if Magic is `0x10`, Priority is 0–4, Flags is `0x00` or `0x01`, and both reserved fields are zero. Any other envelope SHALL be sent uncompressed.
- **PBS-CLP-REQ-012:** A sender SHALL use Timestamp form 0 only when `0 <= Timestamp − time base < 2^40`, and SHALL use the shortest TTL form that represents the TTL.
- **PBS-CLP-REQ-013:** A sender SHALL use a context ID only for a Source ID the peer has acknowledged in the current session.

### 4.3 Receiver rules

- **PBS-CLP-REQ-020:** A receiver SHALL rebuild the 44 header bytes from the compressed form and its context, insert the carried CRC32 unchanged, and apply the PBS-ENV-01 Section 13.1 receiver procedure.
- **PBS-CLP-REQ-021:** If that verification fails, the receiver SHALL discard the datagram and SHALL count a context error. It SHALL NOT recompute the CRC32.
- **PBS-CLP-REQ-022:** After three consecutive context errors from one peer, a receiver SHOULD request uncompressed envelopes for the rest of the session (PBS-PROX-01 Section 7).

Carrying the originator's CRC32 keeps its end-to-end property (PBS-SEC-A-01 Section 5.1) across the compressed hop and detects a wrong context ID or time base.

### 4.4 Test vectors

Context: ID `0x01` = `"Rover-A"`; time base = `1767225597500000` (2.5 s before the PBS-ENV-01 Section 13.2 Timestamp).

The PBS-ENV-01 Section 13.2 header (TTL `30`, CRC32 `0x588721ED`), 44 bytes, compresses to 14 bytes:

```
8a 01 00 01 00 00 26 25 a0 1e 58 87 21 ed
```

The PBS-ENV-01 Section 12.5 header (TTL `0`, CRC32 `0x8757080E`) compresses to 13 bytes:

```
88 01 00 01 00 00 26 25 a0 87 57 08 0e
```

Each decompresses to the original 44 bytes. A header with an inline Source ID, an absolute Timestamp and a 4-byte TTL takes 36 bytes. Decompressing the first vector with context ID `0x01` bound to `"Rover-B"`, or with a time base one microsecond off, fails CRC32 verification.

---

## 5. Segmentation and Reassembly

A datagram longer than the link MTU is sent as 2 to 256 segments.

| Field | Size | Content |
|---|---:|---|
| Dispatch | 1 | `0x40` + datagram tag (6 bits) |
| Index | 1 | Segment number, from 0 |
| Last | 1 | Number of segments minus 1 |
| Data | up to MTU − 3 | The next bytes of the datagram |

- **PBS-CLP-REQ-030:** Every segment except the last SHALL carry exactly `MTU − 3` data bytes. Segment 0 carries the start of the datagram, including its dispatch byte.
- **PBS-CLP-REQ-031:** A sender SHALL NOT reuse a datagram tag toward a peer until the previous datagram with that tag is acknowledged or its reassembly timeout has passed.
- **PBS-CLP-REQ-032:** A receiver SHALL key reassembly by peer and tag, SHALL discard an incomplete datagram after the reassembly timeout (default 60 s), and SHALL discard it earlier if segment 0 shows the envelope has expired (PBS-ENV-01 Section 12.2).
- **PBS-CLP-REQ-033:** A receiver SHALL NOT deliver or forward a partly reassembled datagram.
- **PBS-CLP-REQ-034:** A sender SHALL NOT segment a datagram that needs more than 256 segments. It holds the envelope for a link with a larger MTU.

Lost segments are recovered by the PBS-PROX-01 XFER-ACK bitmap (PBS-PROX-01 Section 8). At an MTU of 51 bytes the largest datagram is 12,288 bytes.

---

## 6. Relays

A relay decompresses and reassembles on receipt, applies PBS-ENV-01 Section 15 to the restored envelope, and compresses again for the next hop with that hop's context. Compression state never crosses a node.

- **PBS-CLP-REQ-040:** A gateway SHALL restore the full envelope before PBS-DTN-MAP-01 or PBS-DTN-MAP-02 encapsulation.

---

## 7. Sizes (Informative)

A PBS-SEC-B-01 envelope carrying a MUX container (2 bytes), a Service Intent frame (23), one 40-byte application frame and an Ed25519 Security frame with an 8-byte `key_id` (91) is 200 bytes, of which 160 are overhead. Compressed it is 170 bytes.

| Link MTU | Link frames |
|---:|---:|
| 51 | 4 |
| 115 | 2 |
| 222 | 1 |

A Security frame with an 8-byte `key_id` is 91 bytes for Ed25519, 59 for HMAC-SHA-256 and 43 for the 128-bit truncated tag proposed in PBS-SUITE-01.

---

## 8. Security Considerations

Compression and segmentation add no authentication. A forged segment can spoil a reassembly; link protection (PBS-PROX-01 Section 9) or PBS-SEC-B-01 limits the effect to loss. Reassembly buffers are bounded by the 256-segment limit and the timeout; a receiver SHOULD also cap concurrent reassemblies per peer.

---

## 9. Open Issues

1. MTU values per radio and data rate belong in an informative annex once measured on reference hardware.
2. Whether to add payload compression (for example a registered dictionary for MUX frame headers).
3. Whether segmentation should also be registered for end-to-end use under PBS-DTN-MAP-02 Section 2, or stay hop-by-hop only.
