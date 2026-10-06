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

## Alignment Summary

Carbonara et al. catalogue the tools for building integrated T/NTN testbeds and report that experimental work on specific T/NTN functions is still limited. PBS sits above the 3GPP links those testbeds emulate, and PBS-CONFORMANCE-02 requires the emulator and link-impairment configuration of any PBS verification run to be recorded.

---

## Citation (MLA)

Carbonara, Salvatore, et al. “Hands-On Solutions for Testing Integrated Terrestrial and Non-Terrestrial Networks: A Comprehensive Survey.” *IEEE Open Journal of the Communications Society*, vol. 6, 2025, pp. 10729–10760, doi:10.1109/OJCOMS.2025.3646364.
