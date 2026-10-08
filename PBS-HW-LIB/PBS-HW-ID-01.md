# PBS-HW-ID-01
## Master Device Identity Tag: Open Reference Design

**Status:** Draft Reference Design (Informational)
**Version:** 0.2
**Date:** 2026-10-08
**Applies to:** Any vehicle, structure or spacecraft that carries PBS traffic, including units built before PBS and fitted afterwards
**Related:** PBS-HW-SCM-01, PBS-ENV-01, PBS-ADDR-01, PBS-SEC-B-01, PBS-AUTH-01, PBS-CAPS-01

---

## 1. Purpose

This document defines a master hardware identity for physical units and a small tag that carries it, so that anyone can build a tag and any reader built to this document can read any tag. The tag can be fitted at manufacture or added to a unit afterwards.

The identity answers one question no operational identifier answers: **which physical unit is this?** Network names, node numbers, operators and owners change during a unit's life. The physical unit does not.

This document specifies formats, interfaces and minimum performance. It names no components and no manufacturers. It is a hardware reference design, not part of PBS Core, and does not affect any PBS conformance claim.

---

## 2. Requirement Levels

As in PBS-HW-SCM-01 Section 3: **[I]** interoperability requirements must be met exactly; **[P]** minimum-performance requirements are floors; informative text is not binding. Normative statements use MUST, SHALL, SHOULD and MAY as in RFC 2119 and RFC 8174 and bind only implementations that claim to follow this document.

---

## 3. Three Layers of Identity

| Layer | Identifies | Lifetime | Where it lives |
|---|---|---|---|
| Master device ID | The physical unit | Life of the unit; never reused | The tag of this document, fixed to the unit |
| Operational identity | The unit's role in a deployment: PBS Source ID (PBS-ENV-01), node number, operator | Until reassigned | A binding certificate signed by the operator (Section 6), stored in the tag |
| Component serial | A replaceable part: a communication module, a battery, a payload | Life of the part | The part |

PBS-HWID-REQ-001 [I]: An operational identity MUST be bound to exactly one master device ID at a time.

PBS-HWID-REQ-002 [I]: A component serial MUST NOT be used as a master device ID or as an operational identity.

This separation follows PBS-ADDR-01, under which identity is not location and moving never changes an address, and extends it to hardware: replacing a part never changes the unit.

---

## 4. The Master Device ID

### 4.1 Derivation

PBS-HWID-REQ-010 [I]: Each tag MUST generate an Ed25519 key pair (RFC 8032) inside the tag. The private key MUST NOT be readable from the tag by any interface.

PBS-HWID-REQ-011 [I]: The master device ID MUST be the first 16 bytes of SHA-256 over the 11 ASCII bytes `PBS-HWID-v1` followed by the 32-byte Ed25519 public key.

The ID is self-certifying: anyone holding the public key can check the ID, and anyone holding the ID can check a signature from the tag. No registry is needed for the ID to work.

### 4.2 Text form

PBS-HWID-REQ-012 [I]: The text form of a master device ID MUST be `hwid:` followed by the 16 bytes as 32 lowercase hexadecimal digits, grouped 8-4-4-4-12 with hyphens (for example `hwid:3f9a1c20-7b44-1e0d-9a2b-55c0e1f4a7d3`).

### 4.3 Optional registration

A manufacturer MAY register with the Pale Blue Systems Foundation.

- The Foundation signs a manufacturer certificate binding the manufacturer's name to the manufacturer's signing key.
- The manufacturer signs a device certificate for each tag it fits, binding the master device ID to the manufacturer, model and serial number.

PBS-HWID-REQ-020 [I]: Registration MUST NOT be required for a tag to operate. A unit with an unregistered tag MUST be usable by any operator who accepts it.

PBS-HWID-REQ-021 [I]: Registered manufacturers and the Foundation MUST publish signed revocation lists of master device IDs. Revocation lists SHOULD be distributable as PBS traffic so that units off Earth can hold current copies.

---

## 5. The Tag

### 5.1 Form

PBS-HWID-REQ-030 [I]: A tag MUST fit within a cylinder 30 mm in diameter and 6 mm high, excluding a wired pigtail.

PBS-HWID-REQ-031 [I]: A tag MUST carry its master device ID in text form and as a Data Matrix code (ISO/IEC 16022) on its exposed face, marked so that it survives the tag's environment.

PBS-HWID-REQ-032 [P]: A tag MUST be fixed to primary structure so that removal leaves visible evidence.

PBS-HWID-REQ-033 [I]: A tag MUST contain no battery.

### 5.2 Retrofit

The tag is designed to be added to a unit after the fact.

PBS-HWID-REQ-040 [I]: A tag MUST provide both the wired interface (Section 5.3) and the passive interface (Section 5.4), so that a unit with no spare data line can still carry one.

PBS-HWID-REQ-041 [I]: A host fitted with a PBS-HW-SCM-01 bay MUST connect the tag's wired interface to the bay's identity-bus contacts.

For other units, the wired interface may be connected by a pigtail to any controller with a two-wire bus, or left unconnected and read only through the passive interface.

### 5.3 Wired interface

PBS-HWID-REQ-050 [I]: The wired interface MUST be a two-wire bus electrically and logically compatible with the NXP I²C-bus specification (UM10204) in Fast-mode (400 kHz), at 3.3 V, with four contacts: 3.3 V, ground, clock, data. The tag MUST respond at the 7-bit address 0x5B.

PBS-HWID-REQ-051 [I]: Every exchange MUST be a request written to the tag followed by a response read from the tag, framed as:

| Field | Size | Content |
|---|---|---|
| Command (request) or status (response) | 1 byte | See Section 5.5 |
| Length | 2 bytes, big-endian | Length of the body |
| Body | Length bytes | Command-specific |
| CRC | 2 bytes, big-endian | CRC-16/CCITT-FALSE over the preceding fields |

A tag that is still working on a request MUST answer reads with status 0x01 (busy) until the response is ready.

### 5.4 Passive interface

PBS-HWID-REQ-052 [I]: The passive interface MUST be a vicinity contactless interface conforming to ISO/IEC 15693, powered by the reader's field. It MUST carry the same commands and responses as Section 5.5, framed as in REQ-051, within ISO/IEC 15693 custom commands. The custom-command code and the manufacturer code are to be published with version 1.0.

### 5.5 Commands

PBS-HWID-REQ-060 [I]: A tag MUST implement these commands.

| Code | Command | Request body | Response body (status 0x00) |
|---|---|---|---|
| 0x10 | GET_INFO | none | Format version (1 byte, 0x01), master device ID (16 bytes), Ed25519 public key (32 bytes) |
| 0x11 | SIGN_CHALLENGE | Challenge, 16–64 bytes | Ed25519 signature (64 bytes) over `PBS-HWID-v1-CHALLENGE` followed by the challenge |
| 0x12 | READ_BINDING | none | The stored binding certificate (Section 6), or an empty body if none |
| 0x13 | WRITE_BINDING | A binding certificate, up to 512 bytes | none |
| 0x14 | READ_DEVICE_CERT | none | The manufacturer's device certificate (Section 4.3), or an empty body if none |

Response status codes: 0x00 success, 0x01 busy, 0x02 unknown command, 0x03 bad length, 0x04 CRC error, 0x05 storage error.

PBS-HWID-REQ-061 [I]: A tag MUST store at least 512 bytes for the binding certificate and at least 512 bytes for the device certificate, in non-volatile memory.

PBS-HWID-REQ-062 [I]: WRITE_BINDING MUST replace the stored binding certificate atomically. The tag does not validate certificates; readers validate them (REQ-081).

Guidance: storing the binding in the tag lets a freshly inserted communication module, or a workshop reader with a dead host, learn the unit's operational identity from the tag alone.

### 5.6 Environment

PBS-HWID-REQ-070 [P]: A tag MUST retain its key, ID and stored certificates through repeated unpowered cooling to −150 °C.

PBS-HWID-REQ-071 [P]: A tag MUST operate both interfaces from −40 °C to +85 °C. A colder tag is read after warming.

PBS-HWID-REQ-072 [P]: A tag MUST tolerate at least 20 krad(Si) total ionizing dose, and MUST survive a latch-up event on its wired supply without loss of its key, ID or stored certificates.

The tag is unpowered most of its life, which limits its radiation exposure to dose and to upsets during reads.

---

## 6. Binding Certificate

The operational identity is a signed statement by the operator.

PBS-HWID-REQ-080 [I]: A binding certificate MUST be a COSE_Sign1 structure (RFC 9052) signed with Ed25519, whose payload is a CBOR map in deterministic encoding (RFC 8949 Section 4.2.1) with these entries:

| Key | Field | Type |
|---|---|---|
| 1 | Master device ID | bstr, 16 bytes |
| 2 | PBS Source ID (PBS-ENV-01) | tstr, at most 16 bytes UTF-8 |
| 3 | Node number (ipn allocator and node) | array of two unsigned integers |
| 4 | Operator code | tstr |
| 5 | Valid from | unsigned integer, seconds since 1970-01-01 UTC |
| 6 | Valid until | unsigned integer, seconds since 1970-01-01 UTC |
| 7 | Sequence | unsigned integer, increased on each reissue |

PBS-HWID-REQ-081 [I]: A reader MUST accept a binding certificate only if its signature verifies against a key the reader trusts for that operator, its validity period includes the current time, its master device ID equals the tag's, and its sequence is greater than or equal to any binding the reader holds for the same master device ID.

PBS-HWID-REQ-082 [I]: Reassignment (sale, lease, redeployment) MUST be done by issuing and writing a new binding certificate. It MUST NOT require changing the tag.

---

## 7. Proving Identity

PBS-HWID-REQ-090 [I]: A reader proves a unit's identity by sending SIGN_CHALLENGE with at least 16 random bytes and reading GET_INFO. The reader MUST check that the public key derives the claimed master device ID (REQ-011) and that the signature verifies.

A copied serial number or a copied Data Matrix code therefore cannot impersonate the unit.

PBS-HWID-REQ-091 [I]: Operational keys used for the unit's PBS traffic (for example PBS-SEC-B-01 keys) MUST NOT be stored in a swappable part between uses (PBS-HW-SCM-01 REQ-152).

---

## 8. Lifecycle

| Event | Action |
|---|---|
| Manufacture | The tag generates its key; optional device certificate from the manufacturer |
| Commissioning | The operator writes a binding certificate |
| Part swap | Nothing changes; the unit keeps its master device ID and binding |
| Reassignment | A new binding certificate with a higher sequence |
| Tag damaged or lost | A new tag is fitted; the operator writes a binding for the new master device ID; the old ID is revoked with a reference to the new one |
| Decommissioning | The master device ID is revoked as retired and never reused |

---

## 9. Verification

| Requirements | Verification |
|---|---|
| Derivation and text form (010–012) | ID derived from the public key and checked against test vectors |
| Form and marking (030–033) | Measurement; marking legibility after environmental test |
| Interfaces and commands (040–062) | Every command over the wired and the passive interface, against test vectors, with a reader from a different builder |
| Environment (070–072) | Unpowered cold soak to −150 °C; operation at −40 °C and +85 °C; dose and latch-up data |
| Binding (080–082) | Certificate encoding against test vectors; acceptance rules for signature, validity, ID and sequence |
| Proof (090, 091) | Challenge-response with a genuine tag and with a copied ID |

Test vectors for the ID derivation, the command frames, the challenge-response and a binding certificate are to be published with version 1.0.

---

## 10. Open Issues

1. **Passive-interface codes** (REQ-052), to be published with version 1.0.
2. **Passive readout below −40 °C** is not required by this version.
3. **Foundation registry operation.** Procedures and publication schedule for manufacturer registration are to be set by Foundation policy.
4. **Hardware licence.** As in PBS-HW-SCM-01 Section 14.

---

## 11. Summary

PBS-HW-ID-01 gives every physical unit a permanent, self-certifying identity in a small tag that any builder can make and any conforming reader can read, through a fixed wired or contactless command set. Operational names are bound to it by certificates that operators reissue as roles change, stored in the tag itself. Parts carry their own serials and never become the unit's identity. Registration with the Foundation adds traceability and revocation, but nothing depends on it.
