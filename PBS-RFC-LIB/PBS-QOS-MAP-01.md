# PBS-QOS-MAP-01
## Mission Intent to Network Treatment Mapping

**Status:** Optional Adapter Profile
**Version:** 1.4
**Related:** PBS-PRIO-01, PBS-SVC-01, PBS-DTN-MAP-02, PBS-LNIS-01

## 1. Purpose

PBS-QOS-MAP-01 defines how an implementation converts PBS mission semantics into authorized network-treatment requests while preserving provider independence.

## 2. Inputs

A policy adapter evaluates:
- PBS priority;
- Service Intent;
- remaining freshness and deadline;
- data class;
- security profile;
- network/service capabilities;
- contact and path state;
- mission resource policy.

## 3. Requirements

- **PBS-QOS-REQ-001:** Network-treatment mapping SHALL be deterministic for a given policy version and input state.
- **PBS-QOS-REQ-002:** The adapter SHALL preserve PBS priority and Service Intent fields unchanged.
- **PBS-QOS-REQ-003:** The adapter SHALL use only network-treatment mechanisms authorized by the active network/service profile.
- **PBS-QOS-REQ-004:** The adapter SHALL provide an observable disposition when a requested treatment is unavailable.
- **PBS-QOS-REQ-005:** Mission policy SHALL define resource-allocation rules for contention among equal and unequal PBS priorities.
- **PBS-QOS-REQ-006:** A network-treatment mapping SHALL identify its policy version for verification and audit.

## 4. Mapping Outputs

Outputs may include queue selection, scheduling weight, link/service class, BP QoS extension parameters, IP QoS parameters, store-and-forward retention, replication authorization, or provider service selection.

## 5. Degraded Operation

When available service capacity changes, the adapter applies the Service Intent degradation policy and current mission resource policy. Authorized degradation profiles remain application-defined and versioned.

## 6. Verification

Verification SHALL exercise nominal capacity, constrained capacity, service transition, contact loss, restored contact, expired deadline, and equal-priority contention.

## 7. Traceability

PBS-QOS-MAP-01 implements PBS-NASA-1309-001/002 and PBS-BPV7-001.
