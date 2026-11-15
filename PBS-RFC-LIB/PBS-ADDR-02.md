# PBS-ADDR-02
## Address Frame for PBS-MUX Containers

**Status:** Draft (proposed Optional Extension; not part of any PBS release)
**Version:** 0.1
**Applies to:** Implementations that use both PBS-ADDR-01 and PBS-MUX-01
**Related:** PBS-ADDR-01, PBS-MUX-01, PBS-ROUTE-01, PBS-SEC-B-01, PBS-HW-ID-01, PBS-DTN-MAP-01

---

## 1. Purpose

PBS-ADDR-01 Section 3.1 places address TLVs in the first bytes of the payload. PBS-MUX-01 Section 3 makes the payload a MUX container that begins with `mux_version` and `frame_count`. Neither document refers to the other, and PBS-MUX-01 Section 5 assigns no frame type to addresses. An implementation using both cannot tell from the specifications where an address goes.

PBS-ADDR-02 defines an Address frame so that addresses travel inside the container like every other semantic unit, and states what the address value is.

---

## 2. Address Frame

Requested MUX frame type: `0x0B` (assignment through PBS-GOV-01 Section 5).

The frame value is:

| Field | Size | Content |
|---|---:|---|
| role | 1 | `0x01` destination, `0x02` reply-to, `0x03` on-behalf-of |
| form | 1 | Section 3 |
| address | variable | One PBS-ADDR-01 Section 4.1 TLV (`type`, `length`, `value`) |

- **PBS-ADDR2-REQ-001:** When an envelope payload is a PBS-MUX-01 container, addresses SHALL be carried in Address frames and SHALL NOT precede the container.
- **PBS-ADDR2-REQ-002:** Address frames SHOULD be the first frames in the container so that a gateway can resolve the destination without parsing the rest.
- **PBS-ADDR2-REQ-003:** A container SHALL carry at most one frame with role `0x01` and a unicast or service address type. Additional destination frames are permitted only with group or broadcast types.
- **PBS-ADDR2-REQ-004:** A node that does not implement this document skips the frame by its length (PBS-MUX-01 Section 4.2) and routes as PBS-ROUTE-01 Section 6 describes.

---

## 3. Address Forms

PBS-ADDR-01 leaves the TLV `value` type-specific. This document registers four forms.

| form | Value | Use |
|---:|---|---|
| `0x00` | Scope-defined | As agreed within the authority scope |
| `0x01` | PBS Source ID, 1–16 bytes UTF-8, without padding | Addressing a unit by its operational name |
| `0x02` | Master device ID, 16 bytes (PBS-HW-ID-01 REQ-011) | Addressing a physical unit regardless of its current role |
| `0x03` | Allocator Identifier and Node Number, two unsigned 32-bit integers (RFC 9758 Sections 3.2 and 3.3) | Direct mapping to an `ipn` node (PBS-DTN-MAP-01 Section 8) |

- **PBS-ADDR2-REQ-010:** Form `0x01` identifies an endpoint only within an authority scope (PBS-ADDR-01 Section 3). Across scopes, an envelope SHALL also carry a PBS-AUTH-01 Authority Context frame, or SHALL use form `0x02`.

Form `0x02` gives a destination that is unique without a registry and does not change when a unit is renamed or reassigned.

---

## 4. Security

An Address frame is part of the payload. The PBS-ENV-01 CRC32 does not cover it; PBS-SEC-B-01 authenticates it with the rest of the container (PBS-SUITE-01 Section 4). A relay MUST NOT modify it (PBS-ROUTE-01 Section 12).

---

## 5. Proposed Erratum to PBS-ADDR-01

Section 3.1, first bullet, to read: "When PBS-MUX-01 is not used, extension TLVs SHALL appear as the first bytes of the payload or within a payload schema explicitly defined by the application layer. When PBS-MUX-01 is used, they are carried as PBS-ADDR-02 Address frames."

This is proposed as a corrective change under PBS-GOV-01 Section 5.2, on the reading that it resolves a conflict between PBS-ADDR-01 and PBS-MUX-01 without changing either wire format. That classification is for the governance body to decide.

---

## 6. Open Issues

1. Whether the on-behalf-of role belongs here or in PBS-AUTH-01.
2. A text form for addresses (for logs and configuration), parallel to the `hwid:` form.
3. No implementation of the Address frame exists. PBS_LINK 0.1.3 implements the PBS-ENV-01 envelope and was not examined for PBS-ADDR-01 or PBS-MUX-01 support.

## 7. References

- RFC 9758, *Updates to the 'ipn' URI Scheme*.
