# PBS-PNT-CTX-01
## Position, Navigation, and Timing Context

**Status:** Optional Extension
**Version:** 1.4
**Related:** PBS-POS-01, PBS-SVC-01, PBS-LNIS-01

## 1. Purpose

PBS-PNT-CTX-01 defines the context required to interpret position, navigation, and timing information consistently across lunar, cislunar, planetary, terrestrial, and local mission frames.

## 2. Context Model

PNT context consists of spatial reference-frame identifier, time-reference identifier, epoch, measurement or solution uncertainty, provenance, validity interval, and quality flags.

## 3. Encoding

PNT Context is carried as PBS-MUX frame type `0x09`.

The frame value is a deterministic TLV sequence. Each TLV uses `type:u8 | length:u16 | value:length`, network byte order.

| Type | Field | Requirement |
|---:|---|---|
| 0x01 | FRAME_ID | REQUIRED for coordinate-bearing PNT |
| 0x02 | TIME_REF_ID | REQUIRED for time-bearing or epoch-bearing PNT |
| 0x03 | EPOCH | REQUIRED when associated PNT is time-dependent |
| 0x04 | POSITION_UNCERTAINTY | OPTIONAL |
| 0x05 | TIME_UNCERTAINTY | OPTIONAL |
| 0x06 | PROVENANCE | REQUIRED for derived PNT solutions |
| 0x07 | VALID_FROM | OPTIONAL |
| 0x08 | VALID_UNTIL | OPTIONAL |
| 0x09 | QUALITY_FLAGS | OPTIONAL |

## 4. Requirements

- **PBS-PNT-REQ-001:** Coordinate-bearing PNT SHALL identify its spatial reference frame.
- **PBS-PNT-REQ-002:** Time-bearing PNT SHALL identify its time reference.
- **PBS-PNT-REQ-003:** A derived PNT solution SHALL identify provenance.
- **PBS-PNT-REQ-004:** Uncertainty values SHALL identify units and statistical interpretation through the registered field profile.
- **PBS-PNT-REQ-005:** A receiver SHALL evaluate validity interval before using PNT context for time-sensitive mission functions.
- **PBS-PNT-REQ-006:** LunaNet-aligned deployments SHALL support identifiers for the applicable lunar reference system and lunar/LunaNet time reference defined by governing LunaNet documents.
- **PBS-PNT-REQ-007:** Local mission frames SHALL use stable frame IDs and SHALL define an explicit transform path when data crosses into a shared reference frame.

## 5. Relationship to PBS-POS

PBS-POS carries position/presence observations. PBS-PNT-CTX supplies the reference, timing, quality, provenance, and validity context used to interpret those observations. A coordinate-bearing PBS-POS frame used across an interoperability boundary SHALL be accompanied by applicable PBS-PNT-CTX information.

## 6. Traceability

PBS-PNT-CTX-01 implements PBS-NASA-2405-001/002/003 and PBS-LNIS-003.
