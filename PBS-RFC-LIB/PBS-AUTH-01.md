# PBS-AUTH-01
## Authority and Scope Context

**Status:** Optional Extension; Required by PBS-SEC-B command profile
**Version:** 1.4
**Related:** PBS-ADDR-01, PBS-SVC-01, PBS-SEC-B-01

## 1. Purpose

PBS-AUTH-01 defines explicit authority and administrative-scope context for multi-operator mission environments.

Authority context identifies the administrative domain asserting a PBS identity and the role under which a protected mission message is issued. It supports deterministic authorization at civil, commercial, international, and mission boundaries.

## 2. Encoding

Authority context is carried as PBS-MUX frame type `0x08`.

| Field | Size | Meaning |
|---|---:|---|
| version | 1 | `0x01` |
| authority_id_type | 1 | Identifier namespace |
| authority_id_len | 1 | Authority identifier length |
| role_len | 1 | Role identifier length |
| policy_epoch | 4 | Authority policy epoch/version |
| authority_id | variable | Authority identifier |
| role | variable | Role asserted by sender |

The complete AUTH frame SHALL be covered by PBS-SEC-B authentication when used for protected operations.

## 3. Requirements

- **PBS-AUTH-REQ-001:** Authority identifiers SHALL be unique within their declared identifier namespace.
- **PBS-AUTH-REQ-002:** A protected command SHALL carry authenticated authority context.
- **PBS-AUTH-REQ-003:** A receiver SHALL evaluate authenticated source, authority, role, operation, and current policy before command acceptance.
- **PBS-AUTH-REQ-004:** Authority translation across administrative domains SHALL be explicit and policy-controlled.
- **PBS-AUTH-REQ-005:** `policy_epoch` SHALL identify the policy generation used for authorization evaluation when mission policy uses versioned authority state.
- **PBS-AUTH-REQ-006:** Authorization failure SHALL produce deterministic rejection and auditable status.

## 4. Identifier Namespaces

Initial values:
- `0` - deployment-defined
- `1` - URI
- `2` - registered organization identifier
- `3` - mission authority identifier

Additional namespaces are assigned through PBS governance.

## 5. Authorization Model

Authorization is evaluated locally using authenticated assertions and mission policy. Policy may constrain command classes, target assets, operational phase, time interval, safety state, delegated roles, and permitted priority classes.

## 6. Traceability

PBS-AUTH-01 implements PBS-NASA-1503-003 and supports PBS-LNIS-002.
