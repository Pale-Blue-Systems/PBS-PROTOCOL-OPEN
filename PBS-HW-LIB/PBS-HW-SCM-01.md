# PBS-HW-SCM-01
## Surface Communication Module: Open Reference Design

**Status:** Draft Reference Design (Informational)
**Version:** 0.3
**Date:** 2026-10-08
**Applies to:** Small and mid-size lunar surface vehicles (rovers, hoppers, remotely driven vehicles), fixed surface infrastructure, and orbital relay nodes that carry PBS traffic
**Related:** PBS-HW-CON-01, PBS-HW-ID-01, PBS-ENV-01, PBS-PRIO-01, PBS-ROUTE-01, PBS-CAPS-01, PBS-SEC-B-01, PBS-DTN-MAP-01, PBS-LNIS-01, PBS-PNT-CTX-01

---

## 1. Purpose

This document defines a swappable communication module for lunar surface vehicles so that anyone can build one, and any module built to it works in any host built to it.

It specifies **what a module must do and how it must interconnect**, not how to build it. It names no components and no manufacturers. A module from one builder and a host bay from another interoperate when both meet this document; how well a module performs above the minimums is the builder's choice.

The design is:

- **Small.** Two shells around one functional core: a half-U shell for vehicles of a few kilograms and a 1U shell for larger vehicles and fixed infrastructure.
- **Hardened where cover is not available.** Mobile units survive radiation by reaching cover; units that cannot move, that are the cover, or that are in orbit operate through it (Section 9).
- **Hot-swappable.** Robot-swappable and glove-swappable in the field for larger units; workshop-swappable without tools for small units (Section 8).
- **Heated when necessary.** Small units survive the lunar night cold and unpowered and warm before use; larger units stay warm (Section 7).

This document is a hardware reference design. It is not part of PBS Core and does not affect any PBS conformance claim (PBS-CONFORMANCE-01).

---

## 2. Scope

In scope: the module's links, its interface to the host, power and thermal behaviour, swap behaviour, radiation classes, identity handling, PBS behaviour and verification.

Out of scope:

- **Component selection.** Any components that meet the requirements may be used.
- **Direct-to-Earth links.** They need an antenna sized and pointed for the host. The 1U shell provides an RF contact for a host-provided antenna (Section 5.3) but no direct-to-Earth function is required in the module.
- **Cellular base stations.** The module is a cellular device; base stations belong to towers, landers and habitats.
- **Vehicle identity.** The permanent identity of a vehicle is defined in PBS-HW-ID-01 and lives on the vehicle, not in the module (Section 10).

---

## 3. Requirement Levels

Every requirement in this document is one of three kinds.

| Kind | Marked | Meaning |
|---|---|---|
| Interoperability | **[I]** | Must be met exactly. Two independent builders who meet these produce a module and a bay that work together |
| Minimum performance | **[P]** | A floor. Exceeding it is allowed and is how builders differentiate |
| Guidance | Informative sections | Explains intent or shows one way to meet a requirement. Not binding |

Normative statements use MUST, SHALL, SHOULD and MAY as in RFC 2119 and RFC 8174. They bind only implementations that claim to follow this document. A claim of conformance to this document MUST state the shell (SCM-S or SCM-L) and the radiation class (M or H).

---

## 4. Terminology

| Term | Meaning |
|---|---|
| Module | One swap unit built to this document |
| Host | The vehicle, structure or spacecraft the module plugs into |
| Bay | The receptacle on the host |
| SCM-S | Half-U shell |
| SCM-L | 1U shell |
| Class M | Radiation class for mobile units that can reach cover (Section 9.2) |
| Class H | Radiation class for units that cannot move, that are cover, or that are in orbit (Section 9.3) |
| Control function | The part of the module that controls power, heat, swap and routing. It may be built any way that meets Section 6 |
| Cover | Terrain or structure that shields a unit from a solar particle event: a crater wall, a shelter, a lander's shadowed side, a garage |

---

## 5. Host Interface

### 5.1 Shell envelopes

PBS-SCM-REQ-001 [I]: An SCM-S module MUST fit within 100 × 100 × 50 mm excluding the connector and latch features, and MUST NOT exceed 0.5 kg.

PBS-SCM-REQ-002 [I]: An SCM-L module MUST fit within 100 × 100 × 100 mm excluding the connector and latch features, and MUST NOT exceed 1.5 kg (Class M) or 2.5 kg (Class H, which carries shielding).

Both shells carry the connector on the same face, centred, so that one bay design accepts either shell when the bay is sized for SCM-L.

### 5.2 Connector contacts

PBS-SCM-REQ-010 [I]: Both shells MUST use the module host connector of PBS-HW-CON-01, which has the following contact groups, mating in the order given on insertion and breaking in reverse order on removal.

| Order | Group | Contacts | Electrical interface |
|---|---|---|---|
| 1 | Chassis | Chassis ground, cable shield | — |
| 2 | Power | Supply positive, supply return | 18–36 V DC, 28 V nominal |
| 3 | Data | Single-pair Ethernet (2 contacts) | IEEE 802.3bw 100BASE-T1 |
| 3 | Fallback | RS-422 transmit pair, receive pair (4 contacts) | TIA-422, 115 200 bit/s, 8N1 |
| 3 | Identity bus | 3.3 V, ground, clock, data (4 contacts) | As PBS-HW-ID-01 Section 5.3 |
| 4 | Detect | Swap-detect pair (2 contacts) | Closed circuit through the bay when fully mated |
| 3 | RF (SCM-L only) | One coaxial contact, 50 Ω | Passes a host antenna to the module |

PBS-HW-CON-01 fixes the contact positions and sizes, the mating heights that set this order, the guide pins and keying, the covers, the forces and the electrical ratings.

### 5.3 Connector mechanics

PBS-SCM-REQ-011 [I]: The connector MUST self-align from a lateral offset of up to ±3 mm and an angular offset of up to ±2°.

PBS-SCM-REQ-012 [P]: Contacts on both the module and the bay MUST be covered except when mated, and the contact faces MUST be cleaned during insertion.

PBS-SCM-REQ-013 [P]: The connector MUST withstand at least 500 mating cycles in lunar regolith simulant with contact resistance remaining within the builder's stated limit.

### 5.4 Host data interface

PBS-SCM-REQ-020 [I]: The module MUST present one network interface to the host over the Ethernet contacts, carrying PBS envelopes (PBS-ENV-01) over UDP/IP. It MAY also carry the host's other IP traffic.

PBS-SCM-REQ-021 [I]: Over the RS-422 fallback the module MUST carry PBS envelopes only, each preceded by a 2-byte big-endian length.

---

## 6. Control Function

The control function is the part of the module that must stay correct when everything else is being reset. This document specifies what it must do, not what it is made of.

PBS-SCM-REQ-030 [P]: The control function MUST continue to control the power of every other active part of the module after any single-event upset, and MUST recover its own state from any single-event upset without loss of buffered traffic.

PBS-SCM-REQ-031 [P]: The control function MUST be able to remove and restore power to each radio function independently.

PBS-SCM-REQ-032 [P]: The control function MUST start only from firmware whose integrity it has verified, and MUST hold a second verified copy to start from if the first fails its check.

PBS-SCM-REQ-033 [P]: After any reset of a radio function, the control function MUST restore that radio's firmware or configuration from a verified copy before the radio transmits.

PBS-SCM-REQ-034 [P]: The module MUST provide at least 64 MB of store-and-forward storage protected against single-event upsets.

Guidance: a radiation-hardened controller with error-correcting memory meets REQ-030 directly; redundant commercial controllers with voting and watchdogs can also meet it if test data shows they do.

---

## 7. Power and Thermal

### 7.1 Supply

PBS-SCM-REQ-040 [I]: The module MUST operate from 18–36 V on the power contacts.

PBS-SCM-REQ-041 [I]: The module MUST limit inrush current on insertion so that the host supply does not fall below 18 V when the host supply source impedance is 0.5 Ω or less.

PBS-SCM-REQ-042 [P]: The module MUST hold enough energy (at least 10 J usable) to complete the shutdown of Section 8.3 after power is lost without warning.

### 7.2 Power limits

These are maximums so that hosts can budget for any conforming module.

PBS-SCM-REQ-043 [I]:

| State | SCM-S maximum | SCM-L maximum |
|---|---|---|
| Asleep, control function only | 0.2 W | 0.2 W |
| Listening (Section 9.2, REQ-091) | 0.5 W | 0.75 W |
| Peak, any combination of transmitters | 6 W | 15 W |
| Heater, warm-up | 6 W | 10 W |

A module MUST report its actual power state to the host through capability advertisement (Section 11.3).

### 7.3 Night survival

PBS-SCM-REQ-050 [P]: An SCM-S module MUST survive repeated unpowered cooling to −100 °C followed by warm-up, for at least twice the number of lunar nights the builder states for it, without loss of function.

PBS-SCM-REQ-051 [P]: A module MUST NOT power any radio function until that function is within its own rated operating temperature, and MUST warm itself to that temperature from the host supply when commanded.

PBS-SCM-REQ-052 [P]: An SCM-S module MUST reach operating temperature from −100 °C within 3 hours at the warm-up power limit of REQ-043.

PBS-SCM-REQ-053 [P]: An SCM-L module MUST be able to maintain operating temperature through a lunar night from host power within the listening power limit of REQ-043 plus 1 W.

PBS-SCM-REQ-054 [I]: An SCM-L module SHOULD provide a mounting interface for a radioisotope heater unit. If it does, the interface MUST accept a heater unit of up to 5 W thermal and up to 0.2 kg.

Guidance: keeping an SCM-S module warm through a night costs roughly 0.5 W. Over a worst-case night of 354 h that is about 180 Wh, more than a small vehicle carries, which is why the half-U shell survives cold instead. The governing failure mode in cold soak is solder-joint fatigue; part, joint and capacitor selection should be qualified for it.

---

## 8. Swap

### 8.1 Service tiers

| Tier | Hosts | Shell | Swap by | Host state |
|---|---|---|---|---|
| Field | Larger rovers, landers, towers, habitats | SCM-L | Robot gripper or gloved crew | Powered |
| Workshop | Small rovers and hoppers brought into a workshop | SCM-S | Technician or robot | Powered or unpowered |

### 8.2 Latch

PBS-SCM-REQ-060 [I]: An SCM-L module MUST be released and secured by one handle operable by a pressurized-suit glove, and the handle MUST carry a grapple feature for a robot gripper. The grapple feature geometry is to be published with version 1.0.

PBS-SCM-REQ-061 [P]: Releasing an SCM-L module MUST require two distinct actions.

PBS-SCM-REQ-062 [P]: An SCM-S module MUST be removable without tools and without loose parts.

### 8.3 Swap behaviour

```text
 INSERTED ──detect closes──► POWER-UP ──identity read, self-test──► OPERATIONAL
     ▲                                                                │
     │                                        release request         │
     │                             (host command or handle action)    ▼
 REMOVED ◄──detect opens── READY-TO-RELEASE ◄──store, close links── DRAINING

 Unannounced removal: detect opens in OPERATIONAL → held energy → DRAINING → REMOVED
```

PBS-SCM-REQ-070 [I]: On a release request the module MUST store pending traffic, close its links, report READY-TO-RELEASE to the host and show a visible ready indication before the latch is released.

PBS-SCM-REQ-071 [P]: On unannounced removal the module MUST complete the same shutdown from held energy (REQ-042).

PBS-SCM-REQ-072 [I]: Stored traffic MUST survive removal and MUST be forwarded or handed to the host after the next insertion, within each envelope's lifetime (PBS-ENV-01).

---

## 9. Radiation Classes

### 9.1 Hazard model

At the lunar surface the accumulated dose is small: the surface baseline measured by Chang'e-4 (13.2 µGy/h) is about 0.12 Gy per year. The hazards that drive the design are single-event effects from galactic cosmic rays and solar energetic particles: bit flips, hung parts, and latch-up that destroys a part unless its power is removed quickly.

The class a host needs depends on whether it can take cover.

### 9.2 Class M: mobile units that can reach cover

Hosts: rovers, hoppers and remotely driven vehicles. The strategy is to reach cover, then wait.

PBS-SCM-REQ-080 [P]: Every part of a Class M module MUST tolerate at least 20 krad(Si) total ionizing dose.

PBS-SCM-REQ-081 [P]: A Class M module MUST detect latch-up in any part and remove that part's power before damage, then restore it (REQ-033). The builder MUST state the detection and removal time and show by test that it prevents damage.

PBS-SCM-REQ-090 [I]: A Class M module MUST provide the cellular, mesh, S-band relay and navigation functions of Section 10.

PBS-SCM-REQ-091 [P]: In every powered state, including asleep, a Class M module MUST keep at least one receive path open (mesh or cellular paging) and MUST signal the host within 5 s of receiving a radiation alert for the host or its deployment scope.

Solar energetic protons can arrive minutes after a flare is seen, and alerts relayed from Earth can arrive after them. On-site and lunar-orbit detectors give the earliest warning, so the wake path listens to the local network.

PBS-SCM-REQ-092 [I]: A Class M module MUST hold a list of cover points distributed by the network and its own position, and MUST give the host the nearest cover point on wake. The cover-point list is carried as an application payload whose format is to be published with version 1.0.

PBS-SCM-REQ-093 [I]: When the host reports that it is under cover, the module MUST stop transmitting except for traffic at CRITICAL priority (PBS-PRIO-01) and MUST store all other traffic until the all-clear.

### 9.3 Class H: units that cannot move, that are cover, or that are in orbit

Hosts: towers, landers, rigs, fixed sensors, habitats and shelters, relay satellites. These units carry the alerts and the crew's traffic during a storm, so they operate through it.

PBS-SCM-REQ-100 [P]: A Class H module MUST continue to provide its mesh, S-band relay and navigation functions throughout the design-reference solar particle event of the deployment's crew-safety plan (surface hosts) or for the mission life in the host orbit (orbital hosts), with a design margin of 2 on dose.

PBS-SCM-REQ-101 [P]: The builder MUST show compliance with REQ-100 by part radiation data and by a shielding dose analysis for the host location.

PBS-SCM-REQ-102 [I]: A Class H module MUST NOT provide a cellular device function. Fixed hosts carry cellular base stations, and orbit has no cellular network.

PBS-SCM-REQ-103 [I]: In storm mode a Class H module MUST stay on and MUST give CRITICAL priority and alert traffic precedence over all other traffic.

PBS-SCM-REQ-104 [I]: Class H is defined for the SCM-L shell only.

---

## 10. Links

### 10.1 Bands

PBS-SCM-REQ-110 [I]: The module MUST provide the following functions in the following bands.

| Function | Band | Class M | Class H |
|---|---|---|---|
| Cellular (3GPP) device | Within 2 503.5–2 655 MHz and within 3 500–3 800 MHz | Required | Not allowed |
| Local mesh | Within 2 400–2 483.5 MHz | Required | Required |
| S-band relay | Return 2 200–2 290 MHz, forward 2 025–2 110 MHz | Required | Required |
| Navigation receive | Lunar navigation signal at 2 492.028 MHz | Required | Required |
| Ranging | See Section 10.4 | Required | Optional |

PBS-SCM-REQ-111 [I]: A module MUST NOT transmit in 2 483.5–2 500 MHz, which is reserved for lunar navigation.

PBS-SCM-REQ-112 [I]: A module MUST NOT transmit below 2 000 MHz. The lunar band plan protects that range for far-side radio astronomy.

Rationale: these bands are in the SFCG lunar band plan and in the candidate set of WRC-27 agenda item 1.15. LTE Band 3, used on the IM-2 mission under a one-time waiver, is excluded.

### 10.2 Link protocols

PBS-SCM-REQ-120 [I]: The cellular function MUST conform to 3GPP LTE or 5G NR user-equipment specifications for the bands of REQ-110.

PBS-SCM-REQ-121 [I]: The mesh function MUST conform to IEEE 802.11 with mesh operation as in IEEE 802.11s, so that modules from different builders form one mesh.

PBS-SCM-REQ-122 [I]: The S-band relay function MUST conform to the LunaNet Interoperability Specification for S-band proximity links.

PBS-SCM-REQ-123 [I]: The navigation function MUST receive the LunaNet Augmented Forward Signal.

### 10.3 Minimum performance

PBS-SCM-REQ-130 [P]:

| Function | Minimum |
|---|---|
| Cellular uplink | 1 Mbit/s at 2 km from a base station in line of sight |
| Mesh | 1 Mbit/s at 300 m line of sight between two modules |
| S-band relay return | 1 kbit/s to a LunaNet relay at 18 000 km slant range and 45° elevation |
| Navigation | Position within 50 m (95 %) when the navigation signal is available |

These floors are set low enough that the smallest module can meet them. For reference, the Nokia coverage study at the Shackleton connecting ridge reported more than 10 Mbit/s to 10 km in open terrain, and 5 W into an omnidirectional antenna closes 10 kbit/s to an LCRNS relay at 17 733 km.

### 10.4 Ranging

Commercial ultra-wideband ranging parts operate near 6.5 GHz and 8 GHz. Neither band is in the WRC-27 candidate list and no lunar regime exists for them.

PBS-SCM-REQ-140 [I]: A module MUST provide two-way ranging to another module over the S-band function, with an accuracy of 10 m or better.

PBS-SCM-REQ-141 [I]: A module MAY also provide ultra-wideband ranging. If it does, the ultra-wideband transmitter MUST be off by default and enabled only by operator command.

---

## 11. Identity and PBS Behaviour

### 11.1 Identity

The module carries no network identity of its own.

PBS-SCM-REQ-150 [I]: On insertion the module MUST read the host's identity from the PBS-HW-ID-01 tag over the identity bus, MUST verify it by challenge and response (PBS-HW-ID-01 Section 7), and MUST operate as that host's node: the same PBS Source ID, node number and operational keys.

PBS-SCM-REQ-151 [I]: The module MUST carry its own component serial number for inventory and fault tracking, and MUST NOT use it as a network identity.

PBS-SCM-REQ-152 [I]: A module MUST erase the host's operational keys on removal.

A swap is invisible to the network apart from a short gap, and a spare or stolen module carries no credentials.

### 11.2 Routing and storage

PBS-SCM-REQ-160 [I]: The module MUST select among available links by a policy the operator configures. The default order is cellular, mesh, S-band relay.

PBS-SCM-REQ-161 [I]: Traffic with no available link MUST be stored and forwarded when a link returns, within each envelope's lifetime.

PBS-SCM-REQ-162 [I]: Over a relay that uses the Bundle Protocol, the module MUST map PBS traffic per PBS-DTN-MAP-01.

### 11.3 Health reporting

PBS-SCM-REQ-170 [I]: The module MUST advertise, by PBS-CAPS-01, its shell, radiation class, the state of each link, its power state, its thermal state, its storm-mode state, and counts of resets and latch-up events since insertion.

Capability advertisements SHOULD be authenticated by PBS-SEC-B-01.

---

## 12. Verification

| Requirements | Verification |
|---|---|
| Envelope, mass (001, 002) | Measurement |
| Connector, alignment, dust (010–013) | Contact-order test; alignment test at the stated offsets; mating cycles in regolith simulant by robot gripper and pressurized glove, with contact resistance logged |
| Host data (020, 021) | Exchange of PBS test envelopes over Ethernet and RS-422 with a reference host |
| Control function (030–034) | Single-event test (beam or fault injection) with traffic running; firmware corruption test |
| Power (040–043) | Supply range, inrush and state-by-state power measurement |
| Thermal (050–054) | Unpowered thermal cycling to −100 °C for the required count; cold start; night keep-warm test for SCM-L |
| Swap (060–072) | Announced and unannounced live extraction under traffic, repeated; no lost stored traffic |
| Class M (080–093) | Total-dose and latch-up data for every part; alert injected in each power state with wake time measured |
| Class H (100–104) | Part radiation data and shielding dose analysis for the host location |
| Links (110–141) | Emission measurement against the bands; interoperation with a second builder's module (mesh, ranging); interoperation with a LunaNet relay simulator; minimum-performance tests |
| Identity and PBS (150–170) | Swap between hosts with node identity following the host; key erasure on removal; PBS routing, store-and-forward and CAPS test vectors |

A builder claiming conformance SHOULD publish its verification results.

---

## 13. Informative: One Way to Build It

This section shows one arrangement that meets the requirements. It is an example, not a requirement, and it names functions, not components.

```text
                 ┌──────────────────────── Module ────────────────────────┐
 Host bay        │                                                        │
 ┌──────────┐    │  ┌───────────────┐  switched rails with latch-up limits│
 │ 18–36 V  ├────┼─►│ inrush limit  ├──►┬────────┬────────┬───────┬──────┐ │
 │ Ethernet ├────┼─►│ + held energy │   ▼        ▼        ▼       ▼      │ │
 │ RS-422   ├────┼─►└───────────────┘ ┌──────┐ ┌──────┐ ┌──────┐ ┌─────┐│ │
 │ detect   ├────┼─►┌───────────────┐ │cell  │ │mesh  │ │S-band│ │UWB  ││ │
 │ ID bus   ├────┼─►│ control       │◄┤device│ │radio │ │+ nav │ │(opt)││ │
 │ RF (L)   ├────┼─┐│ function      │ └──────┘ └──────┘ └──────┘ └─────┘│ │
 └──────────┘    │ ││ router, store │      antennas on the lid           │ │
                 │ ││ heat, swap    │      heaters and sensors           │ │
                 │ │└───────────────┘                    S-band amplifier│ │
                 │ └──────────────────────────────────────►(SCM-L) ──────┘ │
                 └────────────────────────────────────────────────────────┘
```

- A single wideband software-defined radio can serve both the S-band relay and navigation receive, and the ranging of REQ-140, by time-sharing.
- An off-the-shelf cellular device restricted in firmware to the bands of REQ-110 meets REQ-120.
- Antennas face the zenith. At the lunar south pole the elliptical-frozen-orbit relays are at about 46–58° elevation near apolune and towers are near the horizon, so the cellular antenna benefits from a pattern that favours low elevations.

---

## 14. Open Issues

1. **Mechanical drawings.** The grapple feature, the shell rails and the bay dimensions are to be published with version 1.0. The connector is defined in PBS-HW-CON-01.
2. **Cover-point payload format** (REQ-092), to be published with version 1.0.
3. **WRC-27 outcome.** Agenda item 1.15 may narrow the bands of REQ-110.
4. **Ultra-wideband ranging band** (Section 10.4).
5. **Hardware licence.** This document is published under the repository licence. A licence for design files (drawings, schematics) is to be chosen by the Foundation.

---

## 15. References

What vehicle makers publish about their communications, and the sources of figures in this document.

| Topic | Source |
|---|---|
| CADRE: mesh radios between rovers and a lander base station; telecom board with ultra-wideband ranging | JPL, <https://jpl.nasa.gov/missions/cadre>; <https://www-robotics.jpl.nasa.gov/gallery/cadre-telecom-board-testing-2/> |
| MoonFall: four hoppers; communications not published | JPL, <https://www.jpl.nasa.gov/missions/moonfall/> |
| Micro Nova hopper: UHF and 4G/LTE on the surface, S-band to the maker's data network | Intuitive Machines, <https://www.intuitivemachines.com/micro-nova> |
| MAPP rover: S and X band direct-to-Earth, LTE, mesh between rovers | NASASpaceflight, 9 December 2025, <https://www.nasaspaceflight.com/2025/12/lunar-outpost-mapp/> |
| CubeRover: 802.11n at 2.4 GHz to the lander to 200 m; optional 2.25 GHz S-band relay | Astrobotic CubeRover Payload User's Guide v2, <https://www.astrobotic.com/wp-content/uploads/2024/01/Astrobotic_CubeRover-PUG_V2.pdf> |
| MoonRanger: Wi-Fi to the lander, two switched antennas, 160 m tested | Carnegie Mellon, <https://labs.ri.cmu.edu/moonranger/testing-moonrangers-wireless-communication/> |
| Ingenuity: 914 MHz radios, 250 kbit/s to 1 000 m, rover as base station | JPL press kit, <https://www.jpl.nasa.gov/news/press_kits/ingenuity/landing/mission/spacecraft> |
| NASA surface architecture: Wi-Fi about 300 m; 3GPP to about 10 km with the base station on the lander | NASA Glenn, <https://www.nasa.gov/wp-content/uploads/2026/02/lunar-3gpp-gem-paper-rev3-1.pdf>; <https://ntrs.nasa.gov/api/citations/20230013361/downloads/ICSSC-2023_LSR_paper%20rev7k.pdf> |
| Nokia coverage study at the Shackleton connecting ridge; IM-2 Band 3 waiver | Nokia Bell Labs study as summarised in the PBS Shackleton simulation research; MIT Technology Review, <https://www.technologyreview.com/2025/02/18/1111984/nokia-is-putting-the-first-cellular-network-on-the-moon/> |
| S-band proximity bands; Augmented Forward Signal | LunaNet Interoperability Specification v5, <https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf> |
| LCRNS DRM-0 S-band rates | Esper et al., SpaceOps 2025, <https://ntrs.nasa.gov/citations/20250003321> |
| Lunar band plan: 3GPP blocks, navigation band, protection below 2 GHz | SFCG Rec 32-2R5 as presented at the 2025 Cislunar PNT workshop, <https://ioag.org/Cislunar%20PNT%20Workshop/2.%20Lunar%20PNT%20Spectrum/01%20IOAG-ICG%20on%20Lunar%20PNT-Feb2025-SFCG.pdf> |
| WRC-27 agenda item 1.15 candidate bands | Uganda Communications Commission preparatory brief, July 2026, <https://www.ucc.co.ug/wp-content/uploads/2026/07/WRC-27-NPC-preparatory-brief-for-Agenda-Item-1.15-Lunar-Communications.pdf> |
| Lunar surface dose baseline 13.2 µGy/h | Zhang et al. 2020, Science Advances, <https://doi.org/10.1126/sciadv.aaz1334> |
| Worst-case south-pole night of 354 h | NASA Glenn, Lunar Surface Relay terminal (ICSSC 2023), above |
| Relay elevation of 46–58° at the south pole near apolune | PBS Shackleton simulation, computed from the LCRNS reference constellation 3.1 states |
| Radioisotope heater unit (5 W thermal) | World Nuclear News, <https://www.world-nuclear-news.org/articles/blue-ghost-to-carry-nuclear-power-source-to-the-moon> |

---

## 16. Summary

PBS-HW-SCM-01 defines what any communication module for small lunar vehicles must do and how it must connect, so that anyone can build one and any conforming module works in any conforming bay. It fixes the connector, the host interface, the bands and link protocols, the swap behaviour, the identity handling and the PBS behaviour exactly. It sets floors for performance, power, cold survival and radiation tolerance by class, and leaves the choice of components, and how far above the floors to go, to each builder.
