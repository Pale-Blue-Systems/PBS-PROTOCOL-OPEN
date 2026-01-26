# Contributing to the Pale Blue Systems Open Standard

Thank you for your interest in contributing to the **Pale Blue Systems (PBS) Open Standard**.

The PBS Foundation maintains this standard to enable reliable, interoperable communication for space, lunar, and extreme environments. We welcome contributions from engineers, researchers, agencies, and commercial developers who share this mission.

To ensure the long-term stability, neutrality, and legal safety of the standard, we ask that all contributors adhere to the following guidelines.

---

## 1. Legal Requirements (The CLA)

**Important:** Before we can merge any Pull Request (PR), you must agree to the **Contributor License Agreement (CLA)**.

* **Why?** This ensures that the Foundation has the necessary legal rights to maintain and defend the standard's openness forever, preventing any single entity from claiming ownership of the core protocol.
* **How?** By submitting a Pull Request, you automatically agree to the terms outlined in [`CLA.md`](CLA.md).
* **Corporate Contributions:** If you are contributing on behalf of a company, please ensure you have authorization to grant these rights.

---

## 2. How to Contribute

### Reporting Issues
* **Bugs/Ambiguities:** If you find a typo, logical error, or ambiguous statement in a specification, please [Open an Issue](https://github.com/pale-blue-systems/pale-blue-systems/issues).
* **Tagging:** Please use tags (e.g., `typo`, `clarification`, `technical-defect`) to help us triage.

### Submitting Changes (Pull Requests)
1.  **Fork** the repository.
2.  **Branch** off `main` (e.g., `fix/pbs-env-typo` or `feat/new-caps-type`).
3.  **Edit** the relevant Markdown files.
4.  **Submit** a Pull Request targeting `main`.

**Note:** For small fixes (typos, formatting), a PR is sufficient. For substantive changes to the protocol logic, please see "The RFC Process" below.

---

## 3. The RFC Process (For Substantive Changes)

Because PBS is a core infrastructure standard, stability is paramount. We cannot accept "breaking changes" or major new features lightly.

If you want to:
* Add a new Frame Type (to MUX, POS, or CAPS)
* Change a mandatory behavior (MUST/MUST NOT)
* Add a new Security Model

**Please follow these steps:**

1.  **Open an Issue First:** Start a discussion titled `RFC Proposal: [Topic]`. Explain the problem you are solving and why existing mechanisms are insufficient.
2.  **Draft:** Once the discussion shows consensus, draft your changes.
    * If adding a feature, ensure it is **Backwards Compatible**.
    * If changing a core behavior, acknowledge that this may require a **Major Version** increment (v2.0).
3.  **Review:** The governance body and community will review your proposal for:
    * **Necessity:** Is this strictly needed?
    * **Simplicity:** Does it add unnecessary complexity?
    * **Neutrality:** Does it favor one vendor over others?

---

## 4. Style Guide

* **Format:** All specifications are written in Markdown.
* **Language:** Use RFC 2119 keywords (**MUST**, **SHOULD**, **MAY**) strictly and correctly.
* **Diagrams:** Use ASCII diagrams or Mermaid.js code blocks where possible to ensure they are version-controllable text.
* **Tone:** Maintain a professional, neutral, and technical tone. Avoid marketing language or vendor-specific terminology.

---

## 5. Community Code of Conduct

We are building infrastructure for humanity's future in space. We expect all contributors to interact with:
* **Professionalism:** Disagreement is fine; disrespect is not.
* **Patience:** Not everyone shares your context or background.
* **Neutrality:** Leave corporate rivalries at the door.

---

## 6. Questions?

If you have questions about governance, trademarks, or the roadmap, please file an issue with the `governance` label or contact the maintainers directly via the repository details.

Thank you for helping build the backbone of the next era of exploration.