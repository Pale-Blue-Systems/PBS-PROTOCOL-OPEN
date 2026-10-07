# Why Now — Context for PBS Open Protocols

The PBS Open Protocols repository exists to address a foreseeable challenge in the future of space communications: **interoperability across multiple independent authorities operating beyond Earth**.

This work does not respond to a present operational deficiency.  
It anticipates an environment that has been repeatedly described in long-range space architecture planning but has not yet fully materialized.

This document states why the specifications are published now.

---

## The Future Operating Context

Space systems are evolving toward an environment that includes:

- multiple national space agencies operating concurrently,
- commercial operators with independent technical stacks,
- scientific, industrial, and tourism activities,
- shared relays, shared spectrum, and shared physical infrastructure,
- missions and systems that persist beyond individual programs.

In such an environment, **no single organization can reasonably assume global authority**, even when cooperation exists.

---

## The Operating Context

Lunar communications are moving from single-agency, point-to-point links to networks built and operated by several parties:

- LunaNet Interoperability Specification Version 5 (LNIS V005, 29 January 2025) was written and approved by NASA, ESA and JAXA. It describes LunaNet as a network of cooperating networks and states that user needs are expected to be met by a combination of interoperable LunaNet Service Providers rather than by a single provider (Preface, Section 1).
- NASA's LCRNS project procures commercially owned and operated lunar relay services. Intuitive Machines was selected in 2024 as the first commercial LCRNS service provider, and NASA is expected to be one of many users of LCRNS services. LCRNS, ESA's Moonlight and JAXA's Lunar Navigation Satellite System providers are expected to interoperate (Esper et al., SpaceOps 2025, Section 2).
- NASA's *FY26 Civil Space Shortfall Prioritization* (May 2026) lists need statements for advanced networking for multi-spacecraft responsive operations (13.09), scalable lunar surface-to-surface communications usable by all participating elements (15.01), secure command and control over high-latency, bandwidth-limited networks (15.03) and a scalable lunar PNT architecture (24.05).

In this environment no single organization holds authority over every system that exchanges a given message.

---

## The Architectural Risk

Interoperability defined after systems are deployed is limited to what those systems already share. Mars relay services were built across multiple missions and organizations over time, with interoperability mostly at the physical or basic link layer; LCRNS requirements extend interoperability to the network layer and standardize the store-and-forward networking capability and its interfaces (Verville and Eddy, 2025 IEEE Aerospace Conference, Section 3).

PBS applies the same reasoning one layer higher. If application semantics such as priority, freshness, authority and PNT reference are not specified before deployment:

- each mission defines them differently,
- authority boundaries remain implicit in configuration rather than explicit in the data,
- later participants inherit conventions they did not define.

---

## Why Open Specifications Matter Early

Open, inspectable specifications allow:

- conflicting assumptions to be found before deployment,
- review by organizations that will implement them,
- collaborative refinement before deployment pressure exists,
- experimentation without commitment,
- coexistence of diverse implementations under shared semantics.

Publishing protocol concepts early enables discussion **before interoperability becomes a constraint rather than a choice**.

---

## Purpose of Publishing Now

This repository exists to:

1. Make future interoperability concerns explicit and discussable. The interoperability requirements for mission semantics are stated with identifiers and verification methods (PBS-TRACE-NASA-FY26-01, PBS-CONFORMANCE-02).
2. Provide a neutral foundation for collaboration across organizations: a vendor-neutral specification set under the governance of PBS-GOV-01.
3. Allow protocol ideas to evolve in the open before they are required, through the RFC process of PBS-GOV-01 Section 5.

---

## Summary

PBS Open Protocols are published now because future space operations are expected to be **multi-authority by default**.

Early clarity in protocol design helps ensure that future systems remain interoperable, adaptable, and resilient as participation expands.

---

## Sources

- NASA, ESA, and JAXA. *LunaNet Interoperability Specification Document*, Version 5 (LNIS V005), Baseline, 29 January 2025. <https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf>
- Esper, J., G. Heckler, J. Verville, and G. Ryden. “NASA’s Lunar Communications Relay and Navigation Systems (LCRNS).” SpaceOps 2025. <https://ntrs.nasa.gov/citations/20250003321>
- NASA Space Technology Mission Directorate. *FY26 Civil Space Shortfall Prioritization*. May 2026. <https://www.nasa.gov/wp-content/uploads/2026/05/fy26-civil-space-shortfall-prioritization.pdf>
- Verville, J., and W. Eddy. “Onboard Processing for LunaNet Data Services.” *2025 IEEE Aerospace Conference*, doi:10.1109/AERO63441.2025.11068727.
