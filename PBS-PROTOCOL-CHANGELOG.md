# PBS Protocol Changelog

All notable changes to PBS Protocol specifications are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

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
