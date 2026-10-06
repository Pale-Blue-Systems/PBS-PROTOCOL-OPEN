# PBS Alignment  
## Onboard Processing for LunaNet Data Services (IEEE Aerospace Conference 2025)

**Alignment Identifier:** `PBS-ALIGN-IEEE-AEROCONF-ONBOARD-2025-01`

---

## Aligned Work

Verville, Jonathan, and Wesley Eddy.  
“Onboard Processing for LunaNet Data Services.”  
*2025 IEEE Aerospace Conference*, Big Sky, MT, USA, 1–8 March 2025, pp. 1–12.  
doi:10.1109/AERO63441.2025.11068727.  
Author manuscript: NASA Technical Reports Server 20240012437, <https://ntrs.nasa.gov/citations/20240012437>.

**Source identification.** Earlier revisions of this document identified the source only by the file name `2025-AeroConf-OnboardProcessing-FinalAfterComments.pdf` and the title “Onboard Processing for Future Space Missions”. NTRS record 20240012437 publishes the paper above under that file name. This revision is written from that paper.

---

## Alignment Overview

Verville (NASA GSFC, LCRNS Data Systems lead) and Eddy (MTI Systems) describe the onboard processing that the Lunar Communications Relay and Navigation Systems (LCRNS) project requires of commercial lunar relay satellites operated by LunaNet Service Providers (LNSPs). The relays provide three LunaNet data services (Section 1):

1. a real-time frame service relaying CCSDS AOS frames;
2. a real-time network service relaying IP packets;
3. a store-and-forward network service using the DTN Bundle Protocol and onboard storage.

Unlike TDRSS bent-pipe relays, LCRNS relays demodulate user signals, process link-layer and higher-layer protocols, and route on the contents of frames, packets or bundles (Section 3). The LCRNS requirements imply throughput in the 100 Mbps range per node (Section 1) and Ka-band rates up to 50 Mbps (Section 5).

PBS does not run on the relays. PBS is user application data carried over the LunaNet IP and BPv7 network services the paper describes (PBS-LNIS-01 Section 2). The dimensions below identify where the paper's service model sets requirements on the user data that PBS carries.

---

## Alignment Dimensions

### User Services Over Generic Packet and Bundle Transfer

LunaNet network services provide generic packet and bundle transfer, so users implement their own services over that connectivity without further coordination with the network architecture (Section 3, design pattern 4).

**PBS alignment:**  
PBS is such a user-layer protocol. PBS envelopes are user-application protocol data over LunaNet IP or BPv7 services (PBS-LNIS-01 Section 2). PBS-LNIS-REQ-002 requires a BPv7 binding when the mission profile requires disruption-tolerant service; PBS-LNIS-REQ-003 permits IP bindings for contemporaneous connectivity.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-ONBOARD-SVC-01`

---

### Real-Time and Store-and-Forward Service Selection

Missions select the type of service (real-time or store-and-forward) and the interface options appropriate to their needs (Section 3, design pattern 4). Data flows on a relay may mix real-time and store-and-forward traffic (Section 3).

**PBS alignment:**  
PBS-SVC-01 Section 9 carries the application's disruption policy (`CONTINUOUS_PATH`, `STORE_FORWARD`, `EITHER`) with the data. PBS-LNIS-01 Section 4 makes BPv7 the eligible binding for `STORE_FORWARD` and `EITHER`, and an IP or real-time LunaNet service eligible for `CONTINUOUS_PATH`.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-ONBOARD-MODE-02`

---

### Traffic Prioritization and Agreed QoS Treatment

The paper states that relays should prioritize user traffic while routing it, distinguishing traffic types (science data return versus critical or emergency traffic) and service interfaces (Section 3). QoS treatment, including any priority scheme for forward data flows, is agreed between the user mission and the LNSP (Section 4).

**PBS alignment:**  
PBS carries the mission's own classification end to end: the Priority byte at header offset 0x01 (PBS-PRIO-01 Section 4: 0 CRITICAL to 4 BULK) and the Service Intent `data_class` (PBS-SVC-01 Section 4: COMMAND, ALERT, SCIENCE and others). PBS-QOS-MAP-01 converts these into network-treatment requests, preserves the PBS fields unchanged (PBS-QOS-REQ-002) and uses only treatment mechanisms authorized by the active network/service profile (PBS-QOS-REQ-003). PBS does not define relay queueing.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-ONBOARD-PRIO-03`

---

### Endpoint Identifier Coordination

Information coordinated between a user mission and an LNSP includes IP addresses and prefixes, DTN endpoint IDs, convergence-layer configuration, bundle storage policy, QoS treatment and packet or bundle size limits (Section 4).

**PBS alignment:**  
PBS-DTN-MAP-02 Section 3 maps PBS endpoint addressing deterministically to BP Endpoint Identifiers at the binding boundary and requires the mapping to remain stable for the mission transaction. PBS-DTN-MAP-01 Section 8 defines a gateway Source ID to EID mapping table.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-ONBOARD-EID-04`

---

### Shared Security Responsibility

LNSPs secure their ground systems and spacecraft. Mission end users are responsible for the security of their data across terrestrial and space networks and should use strong encryption and appropriate authentication. Systems using LunaNet should not assume a closed network (Section 4).

**PBS alignment:**  
PBS-SEC-B-01 provides end-to-end source authentication, payload integrity, replay detection and optional authenticated encryption for PBS mission data (Sections 2 and 6), independent of bundle-layer BPSec (Section 8). PBS-LNIS-REQ-008 requires security processing to satisfy both the mission security profile and the network security profile. The PBS-SEC-A-01 baseline is a header CRC32 and provides no authentication.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-ONBOARD-SEC-05`

---

### Multi-Hop Surface Access

Surface base stations relay packets or bundles between surface nodes that support only Wi-Fi or 3GPP and the orbital relays, adding a hop (Section 5).

**PBS alignment:**  
PBS-LNIS-REQ-004 requires surface access technology to remain transparent to PBS application semantics. PBS-LNIS-01 Section 5 requires a gateway to preserve the PBS semantic contract while adapting link framing and network encapsulation across 3GPP, Wi-Fi, S-band, Ka-band and other links.

**Alignment Reference:** `PBS-ALIGN-AEROCONF-ONBOARD-SURF-06`

---

## Scope Boundary

The paper's subject is relay-internal: onboard hardware and software, trunk-link multiplexing (Table 1 compares CCSDS virtual channels, frame encapsulation, ITU GFP-F, VLAN tagging, IP/UDP, IPsec, MPLS and Bundle Protocol encapsulation) and LNSP routing coordination. PBS defines none of these functions.

---

## Alignment Summary

Verville and Eddy define the LunaNet data services that LCRNS relays provide and the coordination they require of user missions: service-type selection, traffic prioritization, endpoint identifiers, QoS agreements and end-user data security. PBS carries the corresponding user-side information with the data (disruption policy, priority, data class, endpoint mapping, authenticated content) above those services.

---

## Citation (MLA)

Verville, Jonathan, and Wesley Eddy. “Onboard Processing for LunaNet Data Services.” *2025 IEEE Aerospace Conference*, IEEE, 2025, pp. 1–12, doi:10.1109/AERO63441.2025.11068727.
