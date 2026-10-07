# PBS Alignment  
## Integrated Terrestrial and Non-Terrestrial Network Testbeds

**Alignment Identifier:** `PBS-ALIGN-CARBONARA-TNTN-01`

---

## Aligned Work

Carbonara, Salvatore, Marco Olivieri, Arcangela Rago, Vincenzo Sciancalepore, Giuseppe Piro, Gennaro Boggia, and Luigi Alfredo Grieco.  
“Hands-On Solutions for Testing Integrated Terrestrial and Non-Terrestrial Networks: A Comprehensive Survey.”  
*IEEE Open Journal of the Communications Society*, vol. 6, 2025, pp. 10729–10760.  
doi:10.1109/OJCOMS.2025.3646364. Open access (CC BY 4.0).

---

## Alignment Overview

Carbonara et al. (Politecnico di Bari, CNIT, NEC Laboratories Europe) survey the hardware and software used to build experimental testbeds for integrated Terrestrial and Non-Terrestrial Networks (T/NTNs), which combine terrestrial 5G/6G access with UAVs, high-altitude platforms and multi-orbit satellite constellations. The survey covers:

- reference T/NTN architectures with transparent and regenerative payloads (Section II);
- hardware: software-defined radios, channel emulators and commercial off-the-shelf user equipment (Section III);
- software emulating the core and radio access network, such as OpenAirInterface, srsRAN, Open5GS and OpenSAND (Section IV);
- remotely accessible experimental platforms (Section V);
- other beyond-5G/6G enablers (Section VI);
- published testbeds, lessons learned and research directions (Section VII).

The authors report that, at the time of writing, very few contributions had explored specific T/NTN functions through experimental tests (Section VII).

The study emphasizes the necessity of experimental platforms, hardware-in-the-loop systems, emulation environments, and cross-domain testbeds to move space communications research from theory into deployable, scalable systems.

The work situates integrated T/NTNs as a foundational architectural condition for 6G and beyond, highlighting heterogeneity, multi-segment integration, and real-world validation as essential requirements.

The survey concerns 3GPP radio access and core networks. It does not address delay-tolerant networking, application-layer protocols or governance.

---

## Alignment Dimensions

### 3GPP Non-Terrestrial Links as a Carrier for PBS

The surveyed testbeds carry IP traffic between user equipment and a 5G core over UAV relays and transparent or regenerative satellite payloads in LEO and GEO (Sections II and VII-A).

**PBS alignment:**  
PBS envelopes are application data and do not depend on the access technology. PBS-LNIS-01 Section 5 lists 3GPP among the links over which a PBS gateway preserves the PBS semantic contract, and PBS-LNIS-REQ-004 requires surface access technology to remain transparent to PBS application semantics.

**Alignment Reference:** `PBS-ALIGN-CARBONARA-3GPP-01`

---

### Emulated Channels in Verification

The testbeds pair SDRs with channel emulators (for example Keysight PROPSIM and IZT C5040) or packet-level emulators (OpenSAND) to reproduce satellite delay, Doppler and loss, with hardware and software in the loop (Sections III, IV and VII-A, Table 8).

**PBS alignment:**  
PBS-CONFORMANCE-02 Section 4 requires each PBS verification record to identify the transport/network emulators and the link impairment model used, and requires disruption tests for complete outage, delayed contact, asymmetric link availability, constrained throughput and service restoration. Testbeds of the surveyed kind provide those emulated conditions. No PBS-CONFORMANCE-02 results on such testbeds are published.

**Alignment Reference:** `PBS-ALIGN-CARBONARA-EMU-02`

---

### Lunar NTN Experimentation

One reviewed testbed, the 5G Space Communications Lab of the University of Luxembourg (Kodheli et al.), is used for both Earth and lunar NTN communications (Section VII-A).

**PBS alignment:**  
PBS-LNIS-01 Section 5 covers 3GPP surface links in LunaNet-aligned deployments. A lunar 3GPP link of this kind is a PBS bearer under PBS-LNIS-REQ-004.

**Alignment Reference:** `PBS-ALIGN-CARBONARA-LUNAR-03`

---

## Planned Architecture (in development)

Pale Blue Systems is building PBS to the following architecture for integrated terrestrial and non-terrestrial environments.

### Integrated Terrestrial and Non-Terrestrial Networking

PBS is designed for interoperability across terrestrial, aerial, orbital, lunar, and deep-space networks. Its architecture treats integrated T/NTNs as the default operating environment rather than a special case, enabling coordinated data exchange across these domains while preserving segment-specific constraints.

### Heterogeneity Across Network Segments

PBS is architected with heterogeneity as a first-order design assumption. Its interoperability layer operates above diverse physical and network implementations, allowing independently designed systems to interconnect without requiring uniform technologies or configurations.

### Experimental Validation and Testbeds as Core Infrastructure

PBS aligns with this emphasis by providing an architectural layer that can be exercised across heterogeneous testbeds and experimental environments. Its design enables interoperability and coordination among independently operated platforms, supporting end-to-end validation across the types of systems surveyed in the study.

### Layered Architectural Separation

PBS is positioned above these layers as an interoperability and governance mechanism. It remains agnostic to specific radio, access, and core network implementations, enabling lower-layer innovation without disrupting inter-system coordination.

### Multi-Actor and Multi-Authority Participation

PBS is designed to support interoperability in multi-actor, multi-authority environments. Its architecture enables independently governed systems to exchange data and coordinate through policy-aware interfaces without requiring centralized ownership or unified control.

### Scalability from Testbeds to Operational Systems

PBS supports this progression by providing a consistent interoperability framework that can be applied across experimental, pilot, and operational deployments, enabling continuity as systems scale in size, scope, and complexity.

---

## Alignment Summary

Carbonara et al. catalogue the tools for building integrated T/NTN testbeds and report that experimental work on specific T/NTN functions is still limited. PBS sits above the 3GPP links those testbeds emulate, and PBS-CONFORMANCE-02 requires the emulator and link-impairment configuration of any PBS verification run to be recorded.

**Planned architecture (in development):** Pale Blue Systems aligns with this work by providing an architectural interoperability and governance layer capable of operating across the diverse testbeds, platforms, and network segments surveyed in the study, supporting scalable coordination in 6G-and-beyond environments.

---

## Citation (MLA)

Carbonara, Salvatore, et al. “Hands-On Solutions for Testing Integrated Terrestrial and Non-Terrestrial Networks: A Comprehensive Survey.” *IEEE Open Journal of the Communications Society*, vol. 6, 2025, pp. 10729–10760, doi:10.1109/OJCOMS.2025.3646364.
