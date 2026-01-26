# PBS-SEC-A-01  
## Envelope Authentication and Security Boundaries (Model A)

**Status:** Core  
**Version:** 1.0  
**Applies to:** All PBS Core Messages  
**Related:** PBS-ENV-01, PBS-ADDR-01, PBS-MUX-01, PBS-PRIO-01

---

## 1. Purpose

This document defines **Security Model A** for the Pale Blue Systems (PBS) Open Standard.

Security Model A specifies how PBS envelopes are authenticated, how trust boundaries are enforced, and how message integrity is preserved across multi-hop, multi-authority, and delay-tolerant environments.

This model is intentionally minimal and deterministic, designed to provide **strong integrity and authenticity guarantees** while allowing normal relay behavior in store-and-forward networks.

---

## 2. Security Objectives

PBS Security Model A is designed to achieve the following objectives:

- **Envelope integrity:** Detect unauthorized modification of immutable envelope contents.
- **Source authenticity:** Allow receivers to verify the claimed sender.
- **Replay resistance:** Enable detection of replayed envelopes.
- **Relay transparency:** Allow intermediate relays to forward messages without re-signing.
- **Low computational overhead:** Support constrained and low-power systems.

Confidentiality (encryption) is outside the scope of Model A and MAY be layered above or below PBS Core.

---

## 3. Security Scope

Security Model A applies to the **PBS envelope boundary**, with explicit distinction between immutable and mutable fields.

Rules:
- Immutable fields are authenticated end-to-end.
- Mutable fields MAY be modified during transit without invalidating authentication.
- Relays MUST NOT modify authenticated (immutable) fields.

---

## 4. Trust Model

PBS uses a **scope-based trust model**.

Rules:
- Trust is evaluated within the authority context defined by the `scope` field (PBS-ENV-01).
- Each scope defines its own trust anchors and key management policies.
- Cross-scope trust requires explicit agreement and translation.

Key distribution and trust anchor management are outside the scope of this specification.

---

## 5. Authentication Mechanism

PBS Security Model A uses a **Message Authentication Code (MAC)** to authenticate envelope contents.

### 5.1 Auth Tag Field

The `auth_tag` field in the PBS envelope carries the authentication data.

Rules:
- The `auth_tag` is computed over all authenticated envelope fields (Section 5.2).
- The MAC algorithm MUST be cryptographically strong and collision-resistant.
- The specific MAC algorithm is implementation-defined but MUST be consistent within a scope.

---

### 5.2 Authenticated (Immutable) Fields

The following envelope fields MUST be authenticated:

- `version`
- `scope`
- `src`
- `dst`
- `counter`
- `flags`
- `payload_len`
- `payload`

Any modification to the authenticated fields MUST result in authentication failure.

#### Mutable Field Exclusion

The following field is **explicitly excluded** from authentication:

- `ttl`

The `ttl` field is mutable by design and is expected to change as an envelope traverses the network.

---

## 6. Replay Protection

Replay protection is achieved through the combined use of:

- monotonic counters (`counter`)
- authority context (`scope`)
- source address (`src`)

Rules:
- Receivers SHOULD track recent counters per (`scope`, `src`).
- Envelopes with counters lower than or equal to previously accepted values SHOULD be rejected.
- Counter rollover handling is implementation-defined but MUST preserve monotonicity guarantees.

---

## 7. Authentication Processing

Receivers MUST process authentication as follows:

1. Validate envelope structure.
2. Verify the `auth_tag` against immutable fields.
3. Validate counter monotonicity.
4. Process payload only after successful authentication.

Failure at any step MUST result in envelope discard.

---

## 8. Relay Behavior

Relays operate within the authenticated envelope boundary.

Rules:
- Relays MUST decrement `ttl` as required (PBS-ENV-01).
- Relays MUST NOT modify any authenticated (immutable) field.
- Relays MUST NOT recompute or regenerate authentication tags.
- Relays MAY discard envelopes based on local policy or expired TTL.

TTL modification does not invalidate authentication.

---

## 9. Priority and Security Interaction

Priority bits (PBS-PRIO-01) are part of the authenticated envelope.

Rules:
- Unauthorized priority modification MUST be detected via authentication failure.
- Relays MUST preserve priority values end-to-end.
- Priority handling MUST NOT bypass authentication checks.

---

## 10. Addressing and Security Interaction

Source and destination addresses are authenticated.

Rules:
- Address spoofing MUST be detectable via authentication failure.
- Address resolution MUST occur only after successful authentication.
- Scope-based trust boundaries apply to address interpretation.

---

## 11. Failure Handling

Implementations MUST:
- discard envelopes failing authentication
- avoid emitting error responses that leak security state
- continue processing subsequent envelopes

Authentication failure MUST NOT cause persistent failure modes.

---

## 12. Forward Compatibility

Rules:
- Security Model A semantics SHALL remain stable for PBS Core v1.
- Additional security models MAY be defined in future specifications.
- Implementations MUST NOT assume stronger guarantees than those defined here.

---

## 13. Summary

PBS-SEC-A-01 defines **Security Model A**, an envelope-level authentication model that correctly distinguishes between immutable and mutable fields.

By authenticating identity, intent, and payload while allowing controlled in-transit mutation of TTL, PBS Security Model A enables secure, interoperable operation across multi-hop and delay-tolerant environments.
