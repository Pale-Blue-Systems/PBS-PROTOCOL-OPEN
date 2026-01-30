# PBS-ENV-01
## Core Message Envelope

**Status:** Core
**Version:** 1.3
**Applies to:** All PBS Core Messages
**Related:** PBS-PRIO-01, PBS-SEC-A-01, PBS-CONFORMANCE-01

---

## 1. Purpose

This document defines the **Pale Blue Systems (PBS) Core Message Envelope**.

The envelope provides a fixed, binary, transport-agnostic container for all PBS messages. It defines source identification, lifetime, sequencing, priority, and integrity verification required for reliable operation across embedded systems and delay-tolerant environments.

---

## 2. Envelope Overview

Every PBS message SHALL be transmitted within a PBS envelope.

The envelope:
- identifies the originating device
- defines message lifetime and priority
- provides sequence tracking for gap detection
- includes integrity verification via CRC32 checksum

The envelope does not define transport, routing, or physical-layer behavior. Gateway devices handle encapsulation into higher-level protocols (e.g., CCSDS BPv7) for deep-space transmission.

---

## 3. Design Principles

The PBS-ENV-01 v1.3 header is designed for:

- **Aligned Access:** All 4-byte integers start on 4-byte boundaries (offsets 0x20, 0x24, 0x28), preventing alignment faults on strict embedded processors (ARM Cortex-M, RISC-V).
- **Safety:** CRC32 allows receivers to validate header integrity before processing payload data.
- **Traceability:** Sequence numbers enable detection of lost packets and gap reporting.
- **Simplicity:** Fixed 44-byte header with no variable-length fields enables efficient parsing on resource-constrained devices.

---

## 4. Envelope Structure

A PBS envelope consists of a fixed 44-byte header followed by a variable-length payload.

**Total Header Size:** 44 Bytes
**Byte Order:** Big-Endian (Network Standard)
**Alignment:** 4-Byte Aligned

| Offset | Field | Size | Type | Description |
|--------|-------|------|------|-------------|
| 0x00 | Magic | 1 | u8 | Fixed `0x10` (Protocol ID v1.x) |
| 0x01 | Priority | 1 | u8 | `0`=Critical, `1`=High, `2`=Normal, `3`=Low, `4`=Bulk |
| 0x02 | Flags | 1 | u8 | `0x01`=ACK Requested, `0x00`=None |
| 0x03 | Reserved | 1 | u8 | Padding (MUST be `0x00`) |
| 0x04 | Sequence | 2 | u16 | Rolling counter (0–65535) for gap detection |
| 0x06 | Reserved | 2 | u16 | Padding (MUST be `0x0000`) |
| 0x08 | Source ID | 16 | char[16] | Device name (e.g., "Rover-A"), null-padded UTF-8 |
| 0x18 | Timestamp | 8 | u64 | Unix epoch in microseconds |
| 0x20 | Size | 4 | u32 | Size of payload in bytes |
| 0x24 | TTL | 4 | u32 | Time-to-live in seconds (`0` = never expires) |
| 0x28 | CRC32 | 4 | u32 | Checksum of header bytes 0x00–0x27 |

**Total: 44 Bytes**

---

## 5. Magic Number

The `Magic` field identifies the PBS protocol version family.

Rules:
- PBS Core v1.x implementations MUST set `Magic = 0x10`.
- Receivers MUST reject envelopes with unrecognized magic values.
- Future major versions MAY define new magic values.

---

## 6. Priority

The `Priority` field specifies the scheduling class for the message.

Defined values:

| Value | Name | Description |
|-------|------|-------------|
| 0 | CRITICAL | Immediate life- or safety-critical data |
| 1 | HIGH | Mission-critical operational data |
| 2 | NORMAL | Routine mission data |
| 3 | LOW | Opportunistic or deferrable data |
| 4 | BULK | Non-urgent, high-volume data (best-effort) |

Rules:
- Values 5–255 are reserved and MUST NOT be used.
- Receivers MUST discard envelopes with reserved priority values.
- Priority handling semantics are defined in PBS-PRIO-01.

---

## 7. Flags

The `Flags` field provides envelope-level control information.

Defined bits:

| Bit | Name | Meaning |
|----:|------|---------|
| 0 | ACK_REQ | Acknowledgement requested from recipient |
| 1–7 | RESERVED | Reserved for future use (MUST be `0`) |

Rules:
- Senders requesting acknowledgement MUST set bit 0 (`Flags = 0x01`).
- Reserved bits MUST be set to zero by senders.
- Receivers MUST ignore reserved bits.

---

## 8. Sequence Number

The `Sequence` field provides monotonic sequencing for messages from a given source.

Rules:
- Sequence numbers MUST increase monotonically per source device.
- Sequence numbers roll over from 65535 to 0.
- Receivers SHOULD track sequence numbers to detect lost packets.
- Gap detection enables reporting: "Packets #502–#505 were lost."

---

## 9. Source Identification

The `Source ID` field identifies the originating device.

Rules:
- Source ID is a 16-byte UTF-8 string, null-padded if shorter.
- Source IDs SHOULD be human-readable (e.g., "Rover-Alpha", "Drill-01").
- Source IDs MUST be unique within a deployment scope.
- Bytes beyond the null terminator MUST be `0x00`.

---

## 10. Timestamp

The `Timestamp` field records when the message was created.

Rules:
- Timestamp is Unix epoch time in **microseconds** (not seconds).
- Timestamps enable latency measurement and temporal ordering.
- Receivers MAY use timestamps to detect clock drift or stale data.

---

## 11. Payload Size

The `Size` field specifies the length of the payload in bytes.

Rules:
- Size indicates bytes immediately following the 44-byte header.
- Size of 0 indicates a header-only message (valid for heartbeats, ACKs).
- Maximum payload size is implementation-defined but SHOULD NOT exceed transport MTU.

---

## 12. Time-to-Live (TTL)

The `TTL` field defines the maximum lifetime of the envelope.

### 12.1 Basic Rules

- TTL is specified in **seconds**.
- TTL of `0` indicates the message never expires ("keep trying forever").
- Gateways MUST discard envelopes whose TTL has expired.

### 12.2 TTL Expiration Check

An envelope is expired if:
```
current_time - (timestamp / 1_000_000) > TTL
```

Where `current_time` and `timestamp` are both Unix epoch seconds.

Receivers MUST check TTL expiration:
- On receipt, before processing
- Before forwarding stored messages
- Periodically for stored messages awaiting transmission

### 12.3 TTL Decrement (Store-and-Forward)

When a relay or gateway stores and later forwards an envelope:

1. Calculate storage duration: `storage_seconds = forward_time - receive_time`
2. Calculate new TTL: `new_ttl = original_ttl - storage_seconds`
3. If `new_ttl <= 0`, discard the envelope
4. Otherwise, update TTL field and recalculate CRC32

Implementations MAY use either method:
- **Timestamp-based** (RECOMMENDED): Check `current_time - timestamp > TTL` without modifying TTL
- **Decrement-based**: Reduce TTL value at each hop (requires CRC32 recalculation)

The timestamp-based method is preferred as it avoids CRC32 recalculation overhead.

### 12.4 Typical Values

| Use Case | TTL | Rationale |
|----------|-----|-----------|
| Critical alerts | `0` | Never expire - life safety |
| Commands | `30` | Stale commands may be dangerous |
| Telemetry | `60` | 1 minute freshness |
| Science data | `3600` | 1 hour - can tolerate delay |
| Bulk transfers | `86400` | 24 hours - best effort |

---

## 13. CRC32 Checksum

The `CRC32` field provides header integrity verification.

Rules:
- CRC32 is computed over header bytes 0x00–0x2B (44 bytes) with the CRC32 field set to zero.
- CRC32 uses the standard IEEE 802.3 polynomial (0xEDB88320, reflected).
- Receivers MUST verify CRC32 before processing the envelope.
- Envelopes failing CRC32 verification MUST be discarded.

### 13.1 CRC32 Calculation Procedure

**Sender:**
1. Construct header with CRC32 field (bytes 0x28–0x2B) set to `0x00000000`
2. Compute CRC32 over all 44 bytes
3. Write computed CRC32 value into bytes 0x28–0x2B (big-endian)

**Receiver:**
1. Extract CRC32 value from bytes 0x28–0x2B
2. Set bytes 0x28–0x2B to `0x00000000`
3. Compute CRC32 over all 44 bytes
4. Compare computed value with extracted value
5. Discard envelope if values do not match

The CRC32 checksum:
- Detects transmission errors and bit-flips (radiation, noise)
- Validates header integrity before trusting routing instructions
- Does NOT provide cryptographic authentication (see PBS-SEC-A-01 for security extensions)

---

## 14. Processing Order

Receivers MUST process envelopes in the following order:

1. Magic validation (reject if not `0x10`)
2. CRC32 verification (discard if invalid)
3. Priority validation (discard if reserved value 5–255)
4. TTL validation (discard if expired)
5. Payload extraction (read `Size` bytes following header)

Failure at any step MUST result in envelope discard.

---

## 15. Relay and Gateway Behavior

Gateways and relay nodes:
- MUST verify CRC32 before forwarding
- MUST decrement TTL appropriately
- MUST discard expired envelopes
- MUST preserve all header fields except TTL
- MUST recalculate CRC32 after TTL modification
- MAY encapsulate envelopes into higher-level protocols (e.g., CCSDS BPv7)

---

## 16. Payload

The payload immediately follows the 44-byte header.

### 16.1 Basic Rules

- Payload length is specified by the `Size` field.
- Payload content is application-defined (telemetry, commands, alerts, binary data).
- Payload encoding is not mandated by this specification.
- Implementations MAY define payload schemas for specific use cases.

### 16.2 Payload Integrity

The PBS header CRC32 covers only the 44-byte header, **not the payload**.

**Rationale:** This design allows gateways to make routing decisions based on header fields without processing potentially large payloads. It also enables efficient store-and-forward where payloads may be stored separately from headers.

**Application Responsibility:** Applications requiring payload integrity SHOULD implement one of:

| Method | Overhead | Use Case |
|--------|----------|----------|
| Trailing CRC32 | 4 bytes | Simple integrity check |
| HMAC-SHA256 | 32 bytes | Authenticated integrity |
| AES-GCM | 16+ bytes | Authenticated encryption |

**Example: Application-Level CRC32**
```
Payload structure: [application_data] [crc32_of_application_data]
```

Applications MUST NOT rely on transport-layer integrity alone for safety-critical payloads. Radiation-induced bit-flips can corrupt payload data between PBS nodes.

### 16.3 Maximum Payload Size

Maximum payload size is implementation-defined.

Recommendations:
- Embedded devices: 1–4 KB (memory constrained)
- General purpose: 64 KB (reasonable default)
- Bulk transfers: Segment into multiple envelopes

The `Size` field (u32) supports up to 4 GB, but implementations SHOULD enforce reasonable limits to prevent resource exhaustion.

---

## 17. Error Handling

Implementations MUST:
- Discard envelopes with invalid magic number
- Discard envelopes failing CRC32 verification
- Discard envelopes with reserved priority values
- Discard envelopes with expired TTL
- Continue processing subsequent messages

Envelope-level errors MUST NOT cause persistent failure states.

---

## 18. Forward Compatibility

Rules:
- Unknown flag bits MUST be ignored.
- Reserved fields MUST be set to zero by senders.
- Reserved fields MUST be ignored by receivers.
- The 44-byte header structure SHALL remain stable for PBS Core v1.x.

---

## 19. Reference Implementation

A reference implementation is available in the PBS-LINK SDK:

```python
import struct
import time
import zlib

# Layout: Magic(B), Prio(B), Flags(B), Pad(x), Seq(H), Pad(xx), Src(16s), Time(Q), Size(I), TTL(I), CRC(I)
HEADER_FORMAT = '>B B B x H xx 16s Q I I I'
HEADER_SIZE = 44  # bytes

def build_envelope(source_id, priority, payload, ttl=0, sequence=0, require_ack=False):
    if not (0 <= priority <= 4):
        raise ValueError("Priority must be 0-4")

    src = source_id.encode('utf-8')[:16].ljust(16, b'\0')
    timestamp = int(time.time() * 1_000_000)
    flags = 0x01 if require_ack else 0x00
    payload_bytes = payload.encode('utf-8') if isinstance(payload, str) else payload

    # Build header with CRC32 field set to zero
    pre_header = struct.pack(
        HEADER_FORMAT,
        0x10, priority, flags, sequence,
        src, timestamp, len(payload_bytes), ttl, 0  # CRC32 = 0
    )

    # Calculate CRC32 over all 44 bytes (with CRC32 field zeroed)
    crc = zlib.crc32(pre_header) & 0xFFFFFFFF

    # Rebuild with computed CRC32
    header = struct.pack(
        HEADER_FORMAT,
        0x10, priority, flags, sequence,
        src, timestamp, len(payload_bytes), ttl, crc
    )

    return header + payload_bytes
```

---

## 20. Summary

PBS-ENV-01 v1.3 defines a fixed 44-byte binary envelope optimized for embedded systems and delay-tolerant networks.

Key features:
- 4-byte aligned for efficient processing on ARM/RISC-V
- CRC32 integrity verification
- Sequence tracking for gap detection
- 5-level priority classification
- TTL-based lifetime management
- 16-byte human-readable source identification

This envelope provides a stable, efficient foundation for reliable communication across lunar surface networks, commercial space infrastructure, and deep-space relay systems.
