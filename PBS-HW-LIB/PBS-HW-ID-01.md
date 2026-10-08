# PBS-HW-ID-01
## Master Device Identity Tag: Open Reference Design

**Status:** Draft Reference Design (Informational)
**Version:** 0.1
**Date:** 2026-10-08
**Applies to:** Any vehicle, structure or spacecraft that carries PBS traffic, including units built before PBS and fitted afterwards
**Related:** PBS-HW-SCM-01, PBS-ENV-01, PBS-ADDR-01, PBS-SEC-B-01, PBS-AUTH-01, PBS-CAPS-01

---

## 1. Purpose

This document defines a master hardware identity for physical units and a small tag that carries it. The tag can be fitted to a unit at manufacture or added afterwards.

The identity answers one question that no operational identifier answers: **which physical unit is this?** Network names, node numbers, operators and owners change during a unit's life. The physical unit does not.

This document is a hardware reference design. It is not part of PBS Core and does not affect any PBS conformance claim. Its normative statements (MUST, SHALL, SHOULD, MAY per RFC 2119 and RFC 8174) bind only implementations that claim to follow it.

---

## 2. Three Layers of Identity

| Layer | Identifies | Lifetime | Where it lives |
|---|---|---|---|
| Master device ID | The physical unit | Life of the unit; never reused | The tag of this document, fixed to the unit |
| Operational identity | The unit's role in a deployment: PBS Source ID (PBS-ENV-01), node number, operator | Until reassigned | A binding certificate signed by the operator (Section 5) |
| Component serial | A replaceable part: a communication module, a battery, a payload | Life of the part | The part |

PBS-HWID-REQ-001: An operational identity MUST be bound to exactly one master device ID at a time.

PBS-HWID-REQ-002: A component serial MUST NOT be used as a master device ID or as an operational identity.

This separation follows PBS-ADDR-01: identity is not location, and moving never changes an address. It extends the same rule to hardware: replacing a part never changes the unit.

---

## 3. The Master Device ID

### 3.1 Generation

PBS-HWID-REQ-010: Each tag MUST generate an Ed25519 key pair (RFC 8032) inside its secure element at manufacture. The private key MUST NOT leave the secure element.

PBS-HWID-REQ-011: The master device ID MUST be the first 16 bytes of SHA-256 over the ASCII string `PBS-HWID-v1` followed by the 32-byte Ed25519 public key.

The ID is therefore self-certifying: anyone holding the public key can check the ID, and anyone holding the ID can check a signature from the tag. No registry is needed for the ID to work.

### 3.2 Text form

The text form is `hwid:` followed by the 16 bytes as 32 lowercase hexadecimal digits, grouped 8-4-4-4-12 with hyphens (for example `hwid:3f9a1c20-7b44-1e0d-9a2b-55c0e1f4a7d3`).

### 3.3 Optional registration

A manufacturer MAY register with the Pale Blue Systems Foundation.

- The Foundation signs a manufacturer certificate binding the manufacturer's name to the manufacturer's signing key.
- The manufacturer signs a device certificate for each tag it fits, binding the master device ID to the manufacturer, model and serial number.

PBS-HWID-REQ-020: Registration MUST NOT be required for a tag to operate. A unit with an unregistered tag MUST be usable by any operator who accepts it.

PBS-HWID-REQ-021: Registered manufacturers and the Foundation MUST publish revocation lists of master device IDs. Revocation lists MUST be signed and SHOULD be distributable as PBS traffic so that units off Earth can hold current copies.

---

## 4. The Tag

### 4.1 Form

| Property | Value |
|---|---|
| Size | About 25 mm diameter, 5 mm thick [A] |
| Mounting | Bolted or bonded to primary structure; tamper-evident seal over the mounting |
| Marking | The master device ID in text form and as a 2-D code, laser-marked on the lid |
| Wired interface | Four contacts: 3.3 V, ground, two-wire serial bus (I²C class) |
| Passive interface | Near-field contactless readout (ISO/IEC 14443 or ISO/IEC 15693 class) |
| Storage | Fuses and non-volatile memory; no battery |

### 4.2 Retrofit

The tag is designed to be added to a unit after the fact.

PBS-HWID-REQ-030: A tag MUST be readable through either its wired interface or its passive interface, so that a unit with no spare data line can still carry one.

PBS-HWID-REQ-031: For units fitted with a PBS-HW-SCM-01 bay, the bay MUST route the tag's wired interface to the module connector's identity bus.

PBS-HWID-REQ-032: For other units, the wired interface MAY be connected by a pigtail to any host controller with a two-wire serial bus, or left unconnected and read only through the passive interface.

### 4.3 Environment

PBS-HWID-REQ-040: The tag MUST survive repeated unpowered soaks to −150 °C [A] with its identity intact.

PBS-HWID-REQ-041: The tag MUST operate (wired and passive readout, signing) from −40 °C to +85 °C. A colder tag is read after warming.

PBS-HWID-REQ-042: The secure element MUST tolerate at least 20 krad(Si) total ionizing dose, and its supply MUST be current-limited so that a latch-up does not destroy it. Spot shielding SHOULD cover the secure element.

The tag is unpowered most of its life, which limits radiation exposure to dose and to upsets during reads.

---

## 5. Binding Certificate

The operational identity is a signed statement by the operator.

PBS-HWID-REQ-050: A binding certificate MUST be a COSE_Sign1 structure (RFC 9052) signed with Ed25519, whose payload is a deterministically encoded CBOR map (RFC 8949 Section 4.2) with these fields:

| Key | Field | Type |
|---|---|---|
| 1 | Master device ID | bstr, 16 bytes |
| 2 | PBS Source ID (PBS-ENV-01) | tstr, at most 16 bytes UTF-8 |
| 3 | Node number (ipn allocator and node) | array of two unsigned integers |
| 4 | Operator code | tstr |
| 5 | Valid from | unsigned integer, seconds since 1970-01-01 UTC |
| 6 | Valid until | unsigned integer, seconds since 1970-01-01 UTC |
| 7 | Sequence | unsigned integer, increased on each reissue |

PBS-HWID-REQ-051: A node MUST accept a binding certificate only if its signature verifies against a key the node trusts for that operator, its validity period includes the current time, and its sequence is greater than or equal to any binding it holds for the same master device ID.

PBS-HWID-REQ-052: Reassignment (sale, lease, redeployment) MUST be done by issuing a new binding certificate. It MUST NOT require changing the tag.

---

## 6. Proving Identity

PBS-HWID-REQ-060: A reader proves a unit's identity by sending a challenge of at least 16 random bytes. The tag returns its public key and an Ed25519 signature over `PBS-HWID-v1-CHALLENGE` followed by the challenge. The reader MUST check that the public key derives the claimed master device ID (Section 3.1) and that the signature verifies.

A copied serial number or a copied 2-D code therefore cannot impersonate the unit.

PBS-HWID-REQ-061: Operational keys used by the unit's PBS traffic (for example PBS-SEC-B-01 keys) SHOULD be issued to the unit under its binding certificate and SHOULD be stored on the unit's controller, not in a swappable part (PBS-HW-SCM-01 Section 9).

---

## 7. Lifecycle

| Event | Action |
|---|---|
| Manufacture | Tag generates its key; optional device certificate from the manufacturer |
| Commissioning | Operator issues a binding certificate |
| Part swap | Nothing changes; the unit keeps its master device ID and binding |
| Reassignment | New binding certificate with a higher sequence |
| Tag damaged or lost | A new tag is fitted; the operator issues a binding to the new master device ID; the old ID is added to the revocation list with a reference to the new one |
| Decommissioning | The master device ID is added to the revocation list as retired. It is never reused |

---

## 8. Verification

| Requirement area | Verification |
|---|---|
| Generation (REQ-010, 011) | Key generation inside the secure element; ID derivation checked against test vectors |
| Readout (REQ-030 to 032) | Wired and passive readout on a host with a bay and on a retrofit host without one |
| Environment (REQ-040 to 042) | Unpowered cold soak to −150 °C; operating test at −40 °C and +85 °C; dose and latch-up data for the secure element |
| Binding (REQ-050 to 052) | Certificate encoding against test vectors; acceptance rules for validity, sequence and signature |
| Proof (REQ-060) | Challenge-response with a genuine tag and with a copied ID |
| Lifecycle (Section 7) | Revocation list handling and tag replacement |

Test vectors for the ID derivation, the challenge-response and a binding certificate are to be published with version 1.0 of this document.

---

## 9. Open Issues

1. **Passive readout at low temperature.** Readout below −40 °C is not required by this version.
2. **Foundation registry operation.** The procedures, fees (if any) and publication schedule of manufacturer registration are to be defined by Foundation policy.
3. **Hardware licence.** As in PBS-HW-SCM-01 Section 12.

---

## 10. Summary

PBS-HW-ID-01 gives every physical unit a permanent, self-certifying identity in a small tag that can be fitted at any point in the unit's life. Operational names are bound to it by certificates that operators reissue as roles change. Parts carry their own serials and never become the unit's identity. Registration with the Foundation adds traceability and revocation, but nothing depends on it.
