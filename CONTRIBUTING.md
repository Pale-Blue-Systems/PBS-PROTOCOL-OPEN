# Contributing to the Pale Blue Systems Open Standard

This document describes how to report defects in and propose changes to the **Pale Blue Systems (PBS) Open Standard**.

The Pale Blue Systems Foundation (PBSF) maintains this standard for communication in space, lunar, and other delay- and disruption-prone environments. Contributions from engineers, researchers, agencies, and commercial developers follow the rules below.

---

## 1. Legal Requirements (The CLA)

**Important:** Before we can merge any Pull Request (PR), you must agree to the **Contributor License Agreement (CLA)**.

* **Why?** The CLA grants the Foundation the copyright and patent licenses of CLA Sections 3 and 4 for every contribution.
* **How?** By submitting a Pull Request, you automatically agree to the terms outlined in [`CLA.md`](CLA.md).
* **Corporate Contributions:** If you are contributing on behalf of a company, please ensure you have authorization to grant these rights.

---

## 2. How to Contribute

### Reporting Issues
* **Defects and ambiguities:** Report a typo, logical error, or ambiguous statement in a specification by opening an issue at <https://github.com/Pale-Blue-Systems/PBS-PROTOCOL-OPEN/issues>. Name the specification ID and section in the title (for example, `PBS-ENV-01 s13.1: CRC32 procedure`).
* **Labels:** Suggest a label in the issue body (`typo`, `clarification`, `technical-defect`) to help triage.

### Submitting Changes (Pull Requests)
1.  **Fork** the repository.
2.  **Branch** off `main` (e.g., `fix/pbs-env-typo` or `feat/new-caps-type`).
3.  **Edit** the relevant Markdown files.
4.  **Submit** a Pull Request targeting `main`.

Small fixes (typos, formatting) need only a PR. Substantive changes to protocol behavior follow the RFC process in Section 3.

---

## 3. The RFC Process (For Substantive Changes)

PBS Core semantics and the 44-byte PBS-ENV-01 header are stable for all v1.x releases (PBS-CONFORMANCE-01 Section 12). Changes that affect them follow the PBS-GOV-01 Section 5 lifecycle.

The RFC process applies when you want to:
* Add a new Frame Type (to MUX, POS, or CAPS)
* Change a mandatory behavior (MUST/SHALL or MUST NOT/SHALL NOT)
* Add a new security profile

**Steps:**

1.  **Open an issue first:** Title it `RFC Proposal: [Topic]`. State the problem and why existing mechanisms do not solve it.
2.  **Draft:** Once the discussion reaches consensus, draft the change.
    * A new feature in v1.x is an additive change and remains backward compatible (PBS-GOV-01 Section 5.2).
    * A corrective change resolves a conflict between clauses, or with a referenced standard, without changing the wire format. It ships in a patch release when another clause already states the rule and otherwise in a minor release, with migration guidance for any behavior it makes non-conformant (PBS-GOV-01 Sections 5.2 and 6).
    * A backward-incompatible change requires a new major version (PBS-GOV-01 Section 6; PBS-CONFORMANCE-01 Section 12).
3.  **Review:** The governance body and community review the proposal for:
    * **Necessity:** Is the change required?
    * **Simplicity:** Does it add complexity the problem does not require?
    * **Neutrality:** Does it favor one vendor over others?

---

## 4. Style Guide

* **Format:** All specifications are written in Markdown.
* **Language:** Use the requirement keywords of RFC 2119 and RFC 8174 (MUST/SHALL, MUST NOT/SHALL NOT, SHOULD, MAY) in uppercase only where a statement is normative.
* **Identifiers:** Give each new normative requirement a unique identifier `PBS-<ABBR>-REQ-<nnn>`, where `<ABBR>` is the abbreviation the specification already uses (for example, `PBS-SECB-REQ-001` in PBS-SEC-B-01). Traceability-matrix rows use the matrix's own scheme (for example, `PBS-NASA-1501-001`). Reference specifications by their declared IDs.
* **Diagrams:** Use ASCII diagrams or Mermaid.js code blocks so diagrams remain version-controlled text.
* **Tone:** Write declaratively and technically. No marketing language or vendor-specific terminology.

---

## 5. Community Code of Conduct

Contributors are expected to interact with:
* **Professionalism:** Disagreement is fine; disrespect is not.
* **Patience:** Not everyone shares your context or background.
* **Neutrality:** Leave corporate rivalries at the door.

---

## 6. Questions

File questions about governance, trademarks, or the roadmap as an issue and suggest the `governance` label.
