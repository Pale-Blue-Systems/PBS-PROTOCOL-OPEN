# PBS Protocol Changelog

All notable changes to PBS Protocol specifications are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [1.4.1] - 2026-10-06

Errata and documentation release of PBS v1.4. No wire-format change.

### Errata (normative text corrected; wire format unchanged)

Each corrected document carries an **Errata** line under its Version line (Baseline Date for the matrix). Version values are unchanged.

- **PBS-ENV-01** — Section 4: the CRC32 row said "header bytes 0x00–0x27". It now states the Section 13 rule: IEEE 802.3 CRC-32 over bytes 0x00–0x2B with the CRC32 field (0x28–0x2B) set to zero, stored big-endian at 0x28. Section 12.2: `timestamp` is in microseconds, as the expiry formula already assumed. Section 13.2: test vector added (CRC32 `0x588721ED`; the 0x00–0x27 rule yields `0x019507AC`).
- **PBS-SEC-A-01** — Sections 4.1 and 5.1 computed CRC32 over bytes 0x00–0x27. Both now use bytes 0x00–0x2B with the CRC32 field zeroed, and Section 4.1 lists the PBS-ENV-01 Section 13.1 receiver procedure. Section 11 references PBS-SEC-B-01.
- **PBS-CONFORMANCE-01** — Sections 4.3 and 5.1 required CRC32 over bytes 0x00–0x27 ("40 bytes"). Both now require bytes 0x00–0x2B with the CRC32 field zeroed. Section 3 cites PBS-PRIO-01 v1.4 (MUST requirements unchanged from v1.3) and lists PBS-ADDR-01 and PBS-MUX-01 as optional, as recorded in [1.3.0]; it refers implementations claiming the v1.4 alignment profile to PBS-CONFORMANCE-02.
- **PBS-PRIO-01** — Section 10 required "priority bits" to be covered by envelope authentication (v1.0 text). Priority is the u8 at offset 0x01, covered by the header CRC32 (PBS-SEC-A-01) and authenticated when PBS-SEC-B-01 applies (PBS-SECB-REQ-004).
- **PBS-ROUTE-01** — Section 4: forwarding eligibility requires header CRC32 verification, not authentication, and the destination is determined per Section 6 (the v1.3 header has no destination field). Section 12: relays preserve the Priority byte and all header fields except TTL and CRC32.
- **PBS-ADDR-01** — Section 3 located the authority context in an envelope `scope` field that v1.3 removed. Section 4.1 applied TLV addressing to all PBS implementations; it applies to implementations of this optional extension.
- **PBS-MUX-01** — Section 3 required every envelope payload to be a MUX container; the requirement applies only when PBS-MUX-01 is used. Section 6 permitted explicit frame-level priority, contradicting PBS-PRIO-01 Section 9; frames inherit the envelope priority.
- **PBS-CAPS-01**, **PBS-POS-01** — stated that payload frames inherit envelope authentication from PBS-SEC-A-01. The SEC-A-01 CRC32 does not cover the payload; CAPS and POS frames are authenticated when PBS-SEC-B-01 applies.
- **PBS-SEC-B-01** — Section 9 cited LNIS requirement 008 by an identifier that matches no definition; it cites PBS-LNIS-REQ-008.
- **PBS-TRACE-NASA-FY26-01** — the Allocation column used short names (DTN, CONFORMANCE) and omitted specifications that state they implement a row. It lists specification identifiers and matches the specification Traceability sections. PBS-NASA-1309-003 was cited by no specification; PBS-CAPS-01 Section 15 cites it. Traceability sections added or completed in PBS-ENV-01 (Section 21), PBS-PRIO-01 (Section 15), PBS-CAPS-01 (Section 15), PBS-SVC-01 (Section 13) and PBS-CONFORMANCE-02 (Section 6).

### Documentation

- **PBS-ENV-01** Section 19, **PBS-CONFORMANCE-01** Section 11.1 — link the PBS_LINK reference SDK (<https://github.com/Pale-Blue-Systems/PBS_LINK>, version 0.1.1) and name its import package, `PBS_LINK`. The Section 19 Python function was executed: its output parses with `PBS_LINK.parse_envelope` and is byte-identical to `PBS_LINK.build_envelope` output for the same timestamp.
- **PBS-ALIGN-IEEE-AEROCONF-2025-01**, **PBS-ALIGN-ASSIGNMENT-NASA-FY26-01** — files renamed to their declared identifiers (were `PBS-ALIGN-IEEE-AEROCONF-2025.md` and `PBS-ALIGNMENT-ASSIGNMENT-NASA-FY26.md`); PBS-ALIGN-INDEX-01 links updated.
- **PBS-ALIGN-INDEX-01** — lists all alignment documents under their own IDs, including PBS-ALIGN-NASA-LCRNS-02 and the FY26 traceability matrix; citations corrected against their DOIs.
- **PBS-ALIGN-NASA-LCRNS-02** — declares its own identifier; it declared PBS-ALIGN-NASA-LCRNS-01.
- **PBS-ALIGN-TF-GOVERNANCE-2024-01** — placeholder title and publisher-as-author replaced with the published citation.
- **PBS-ALIGN-CARBONARA-TNTN-01**, **PBS-ALIGN-NTONTIN-6G-01** — author name, volume and page numbers corrected.
- **PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01** — given its `.md` extension.
- **PBS-ALIGN-SPJ-LEO-2022-01** (was PBS-ALIGN-SPJ-AUTONOMY-2022-01) — rewritten against the paper its DOI (doi:10.34133/2022/9865174) identifies: Zhang et al., "LEO Mega Constellations: Review of Development, Impact, Surveillance, and Governance", *Space: Science & Technology*, 2022. The previous text described a paper on autonomy that the DOI does not resolve to.
- **README** — Status names PBS v1.4.1; alignment table and repository structure match the repository.

---

## [1.4.0] - 2026-09-22

### NASA FY26 / LunaNet Alignment

PBS v1.4 establishes the mission-semantic interoperability profile for lunar, cislunar, and deep-space applications operating across heterogeneous network services and independently operated providers.

### Added
- **PBS-SVC-01** — Mission Service Intent
- **PBS-AUTH-01** — Authority and Scope Context
- **PBS-SEC-B-01** — Authenticated Mission Messaging
- **PBS-PNT-CTX-01** — Position, Navigation, and Timing Context
- **PBS-LNIS-01** — LunaNet Application Alignment Profile
- **PBS-DTN-MAP-02** — BPv7 Mapping
- **PBS-QOS-MAP-01** — Mission Intent to Network Treatment Mapping
- **PBS-CONFORMANCE-02** — NASA/LunaNet Alignment Conformance and Verification Profile
- **PBS-ALIGNMENT-ASSIGNMENT-NASA-FY26** — controlled alignment assignment
- **PBS-TRACE-NASA-FY26-01** — requirements traceability baseline
- **PBS-ALIGN-NASA-LCRNS-02** — NASA LCRNS/LunaNet/FY26 architecture mapping

### Updated
- **PBS-MUX-01 v1.4** — registered frame types for Service Intent, Authority Context, PNT Context, and authenticated mission messaging.
- **PBS-POS-01 v1.4** — explicit reference-frame and time-context binding through PBS-PNT-CTX-01.
- **PBS-PRIO-01 v1.4** — priority defined as transport-independent mission urgency and policy input.
- **README** — mission-semantic interoperability architecture and LunaNet network-service allocation.

### Engineering Basis
The release aligns PBS requirements with NASA FY26 Civil Space Shortfall needs 15.01, 13.09, 15.03, and 24.05; LunaNet Interoperability Specification V005; NASA LCRNS multi-provider service architecture; and current BPv7 network-service semantics.

---

## [1.3.0] - 2026-01-28

### Changed

#### PBS-ENV-01 (Major Revision)
- **Complete rewrite to fixed 44-byte binary header format**
  - Replaces abstract variable-length envelope with concrete binary specification
  - Optimized for embedded systems (ARM Cortex-M, RISC-V)
  - 4-byte aligned for efficient memory access
  - Fixed fields: Magic, Priority, Flags, Sequence, Source ID, Timestamp, Size, TTL, CRC32
- **Added Sequence field** (u16 at offset 0x04) for packet-loss detection and gap reporting
- **Added CRC32 field** (u32 at offset 0x28) for header integrity verification
- **Source ID** now fixed 16-byte null-padded UTF-8 string (replaces variable TLV addressing)
- **Timestamp** now Unix microseconds (u64 at offset 0x18)
- **Removed** variable-length addressing (PBS-ADDR-01 now optional extension)
- **Removed** mandatory MUX container (PBS-MUX-01 now optional extension)
- **Removed** mandatory HMAC authentication (CRC32 provides baseline integrity)

#### PBS-PRIO-01 (Updated)
- Priority now encoded as dedicated byte field at offset 0x01 (previously bits 5-7 of flags)
- Clarified 5-level priority system (0=Critical through 4=Bulk)
- Retained NASA DSN compatibility section from v1.0.1

#### PBS-SEC-A-01 (Major Revision)
- **Renamed** from "Envelope Authentication" to "Integrity Verification and Security Boundaries"
- **CRC32** now mandatory baseline (replaces HMAC-SHA-256 as mandatory-to-implement)
- HMAC-SHA-256 and Ed25519 documented as optional cryptographic extensions
- Added threat model documenting what CRC32 does/does not protect against
- Clarified CRC32 recalculation requirements for TTL modification

#### PBS-CONFORMANCE-01 (Updated)
- Mandatory specifications reduced to: PBS-ENV-01, PBS-PRIO-01, PBS-SEC-A-01
- PBS-ADDR-01, PBS-MUX-01 moved to optional specifications
- CRC32 now mandatory baseline (replaces HMAC-SHA-256)
- Added reference to PBS-LINK SDK as conformance reference implementation

### Added
- **PBS-LINK SDK** (v0.1.1) — Official Python reference implementation
  - Implements PBS-ENV-01 v1.3 44-byte header
  - Includes test vectors for conformance validation
  - Apache 2.0 licensed

### Purpose
This major revision simplifies PBS Core for embedded systems deployment while maintaining semantic compatibility. The fixed 44-byte header enables efficient implementation on resource-constrained devices (512KB RAM target). Variable-length features (TLV addressing, MUX containers, cryptographic authentication) remain available as optional extensions for applications requiring them.

---

## [1.0.1] - 2026-01-28

### Added

#### PBS-PRIO-01
- **Section 14: NASA DSN Compatibility** — Documents the relationship between PBS 5-level priority classes and NASA Deep Space Network 7-level scheduling system.
  - Section 14.1: Scope Differentiation (packet-layer vs. ground scheduling)
  - Section 14.2: Informative priority mapping table
  - Section 14.3: Interoperability notes for DSN-serviced missions

### Purpose
This addition clarifies that PBS operates as complementary packet-layer scheduling within DSN-allocated antenna time, enabling commercial operators to implement NASA-compatible prioritization without modifying DSN infrastructure.

---

## [1.0.0] - Initial Release

### Added
- PBS-ENV-01: Core Message Envelope
- PBS-ADDR-01: Addressing and Identification
- PBS-MUX-01: Payload Multiplexing
- PBS-PRIO-01: Priority Classification
- PBS-SEC-A-01: Security Model A
- PBS-POS-01: Position and Presence Signaling
- PBS-CAPS-01: Capability Advertisement
- PBS-ROUTE-01: Routing and Forwarding Semantics
- PBS-DTN-MAP-01: DTN Mapping
- PBS-CONFORMANCE-01: Conformance Requirements
- PBS-GOV-01: Governance and Stewardship
