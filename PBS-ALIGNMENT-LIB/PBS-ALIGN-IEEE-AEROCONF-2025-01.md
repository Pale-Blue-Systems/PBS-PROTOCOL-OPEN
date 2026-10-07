# PBS Alignment  
## High-Performance DTN Convergence Layers (IEEE Aerospace Conference 2025)

**Alignment Identifier:** `PBS-ALIGN-IEEE-AEROCONF-2025-01`

---

## Aligned Work

Templin, Fred, Rachel Dudukovich, Scott Burleigh, William Pohlchuck, Brian Tomko, Bhargava Raman Sai Prakash, Tom Herbert, and Daniel Raible.  
“High Performance DTN Using Larger Packets and Kernel Resident Convergence Layers.”  
*2025 IEEE Aerospace Conference*, Big Sky, MT, USA, 1–8 March 2025, pp. 1–12.  
doi:10.1109/AERO63441.2025.11068517.  
Author manuscript: NASA Technical Reports Server 20240015952, <https://ntrs.nasa.gov/citations/20240015952>.

**Source identification.** Earlier revisions of this document identified the source only by the file name `IEEE_Aeroconf_2025 final.pdf` and described a mission-architecture paper. NTRS record 20240015952 publishes the paper above under that file name. The paper does not contain the mission-architecture content the earlier text attributed to it; this revision is written from the paper.

---

## Alignment Overview

Templin et al. (Boeing, NASA Glenn Research Center, Kiisel Burleigh Corporation, SiPanda) measure the throughput of Bundle Protocol (RFC 9171) transfer over the Licklider Transmission Protocol (LTP, RFC 5326) convergence layer in two DTN implementations: JPL's Interplanetary Overlay Network (ION) and NASA Glenn's High-rate DTN (HDTN). LTP divides each bundle into blocks and segments and sends each segment in an IP packet; segments larger than the path MTU invoke IP fragmentation (Section I).

Findings:

- Larger LTP segments raise throughput even when IP fragmentation is invoked. HDTN on 100 Gbps NICs gained a factor of 2 to 3 depending on path MTU (1,500, 4,500 and 9,702 bytes); ION gained a factor of 10 or more independently of path MTU (Sections V, VI, X).
- Replacing `sendmsg`/`recvmsg` with `sendmmsg`/`recvmmsg`, or adding GSO/GRO, had little effect on ION LTP throughput (Section V).
- Segmentation offload and a kernel-resident LTP segmentation function are projected to give HDTN a factor of 4 over the LTP base case (Section X).
- On the International Space Station, BP runs over TCP, LTP, UDP and STCP convergence layers selected per link (Section IV).

The IEEE Aerospace Conference 2025 paper presents a mission-oriented space systems architecture emphasizing distributed assets, heterogeneous communications, and coordinated operations across independently operated systems. The architecture assumes intermittent connectivity, variable latency, and mixed relay and direct communication paths as baseline operating conditions. It further separates mission logic and data workflows from underlying transport and relay mechanisms to support extensibility and reuse across future missions.

---

## Alignment Dimensions

### PBS Is Independent of the Convergence Layer

The paper's gains come from changes below the Bundle Protocol: LTP segment size, path MTU and kernel or hardware segmentation offload.

**PBS alignment:**  
PBS-DTN-MAP-02 places the PBS envelope in the BPv7 payload and the convergence-layer adapter below BPv7 (Section 2), and assigns convergence-layer selection to the DTN network service (Section 8). Convergence-layer changes of the kind the paper measures therefore apply beneath PBS without a change to PBS.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-CLA-01`

---

### Envelope-to-Bundle Granularity

The paper notes that bundles are often 100 KB, 1 MB or larger, in contrast to IP packets (Section I), and shows that LTP throughput rises with segment size.

**PBS alignment:**  
PBS-DTN-MAP-01 Section 5.1 maps each PBS envelope to exactly one bundle and prohibits fragmenting an envelope across bundles; PBS-DTN-MAP-02 Section 2 specifies that one PBS protocol data unit SHOULD map to one BP application data unit unless a registered segmentation profile defines segmentation and reassembly. Under PBS-DTN-MAP-01 the BPv7 payload block therefore carries exactly one envelope: the 44-byte PBS-ENV-01 header plus the payload, whose maximum is implementation-defined (PBS-ENV-01 Section 16.3). The bundle adds the primary block and any extension blocks (RFC 9171 Sections 4.1 and 4.3).

**Alignment Reference:** `PBS-ALIGN-AEROCONF-SIZE-02`

---

### Integrity Scope

Section IX observes that a 32-bit frame check sequence loses effectiveness for data sets larger than 9 KB and proposes IP parcels, which protect headers plus an integrity block so that intact segments are delivered when others are corrupted.

**PBS alignment:**  
The PBS-ENV-01 CRC32 covers only the fixed 44-byte header (PBS-ENV-01 Sections 13 and 16.2). Payload integrity is the application's responsibility (PBS-ENV-01 Section 16.2); PBS-SEC-B-01 authenticates the application payload when that profile applies (PBS-SEC-B-01 Section 5). PBS-DTN-MAP-01 Section 6.4 permits BPSec at the bundle layer in addition to the PBS header CRC32.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-INTEG-03`

---

## Planned Architecture (in development)

Pale Blue Systems (PBS) is building a governance-aware interoperability and coordination layer capable of operating across heterogeneous, intermittently connected mission, relay, and ground networks. PBS complements mission architectures by enabling policy-consistent data exchange and coordination without imposing centralized control or constraining internal system designs.

### Mission-Centric, Federated Architecture

PBS is designed to operate in federated, mission-centric environments, enabling interoperable data exchange across autonomous systems while preserving mission ownership, operational independence, and organizational boundaries.

### Heterogeneous and Intermittent Communications

PBS is delay-tolerant by design and assumes heterogeneous, disruption-prone links as the baseline. Its interoperability mechanisms support coordinated operations across inconsistent connectivity without requiring continuous end-to-end links.

### Separation of Mission Logic from Transport Infrastructure

PBS operates above transport and relay layers, reinforcing this separation by allowing missions to evolve communications technologies without refactoring mission logic or cross-system coordination mechanisms.

### Multi-Authority and Multi-Stakeholder Operations

PBS is explicitly designed for multi-authority interoperability. It provides policy-aware mediation between independently governed systems, enabling coordination without requiring shared control planes or internal disclosure.

### Forward Extensibility and Reuse

The paper positions its architecture as reusable across future missions and adaptable to expanding operational domains, including cislunar and deeper-space environments.

**PBS alignment:**  
PBS is mission-agnostic and orbit-agnostic, designed to persist across mission eras and domains. Its architecture supports progressive expansion without requiring architectural reset as mission scope evolves.

---

## Alignment Summary

Templin et al. show that DTN throughput over LTP depends on segment size, path MTU and where segmentation is performed. PBS sits above that layer: PBS-DTN-MAP-01 maps one envelope to one bundle, PBS-DTN-MAP-02 leaves convergence-layer selection to the DTN network service, and the PBS header CRC32 covers 44 bytes.

---

## Citation (MLA)

Templin, Fred, et al. “High Performance DTN Using Larger Packets and Kernel Resident Convergence Layers.” *2025 IEEE Aerospace Conference*, IEEE, 2025, pp. 1–12, doi:10.1109/AERO63441.2025.11068517.
