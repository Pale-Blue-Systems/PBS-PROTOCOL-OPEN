# PBS-HW-SCM-01
## Surface Communication Module: Open Reference Design

**Status:** Draft Reference Design (Informational)
**Version:** 0.1
**Date:** 2026-10-08
**Applies to:** Small and mid-size lunar surface vehicles (rovers, hoppers, remotely driven vehicles), fixed surface infrastructure, and orbital relay nodes that carry PBS traffic
**Related:** PBS-HW-ID-01, PBS-ENV-01, PBS-ROUTE-01, PBS-CAPS-01, PBS-SEC-B-01, PBS-DTN-MAP-01, PBS-LNIS-01, PBS-PNT-CTX-01

---

## 1. Purpose

This document defines an open reference design for a swappable communication module that carries PBS traffic for lunar surface vehicles.

Vendors of small lunar vehicles publish the architecture of their communication systems but rarely their radios, bands, rates, power or thermal design (Section 13 lists what is published). PBS-HW-SCM-01 fills that gap with a design anyone may build, inspect and improve.

The design is:

- **Small.** Two shells around one electronics core: a half-U shell for vehicles of a few kilograms and a 1U shell for larger vehicles and fixed infrastructure.
- **Hardened where cover is not available.** Mobile units survive radiation by reaching cover; units that cannot move, that are the cover, or that are in orbit carry hardened parts (Section 8).
- **Hot-swappable.** Robot-swappable and glove-swappable in the field for larger units; workshop-swappable with no tools for small units (Section 7).
- **Heated when necessary.** Small units survive the lunar night cold and unpowered and are warmed before use; larger units stay warm (Section 6).

This document is a hardware reference design. It is not part of PBS Core and does not affect any PBS conformance claim (PBS-CONFORMANCE-01). Its normative statements (MUST, SHALL, SHOULD, MAY per RFC 2119 and RFC 8174) bind only implementations that claim to follow this reference design.

---

## 2. Scope

In scope: the module's links, electronics architecture, power, thermal design, swap interface, radiation classes, fault handling, PBS behaviour and verification.

Out of scope:

- Direct-to-Earth links. They need an antenna sized and pointed for the host vehicle. The 1U shell provides an RF port for a host-provided direct-to-Earth antenna (Section 7.2) but contains no direct-to-Earth radio.
- Cellular base stations. The module is a cellular device (user equipment); base stations belong to towers, landers and habitats.
- Vehicle identity. The permanent hardware identity of a vehicle is defined in PBS-HW-ID-01 and lives on the vehicle, not in the module (Section 9).

Figures marked **[A]** are design assumptions of this document, to be replaced by measured values during development. Other figures cite the source in Section 13.

---

## 3. Terminology

| Term | Meaning |
|---|---|
| Module | One swap unit of this design: core plus shell |
| Core | The electronics common to both shells (Section 5) |
| SCM-S | Half-U shell, about 10 × 10 × 5 cm |
| SCM-L | 1U shell, about 10 × 10 × 10 cm |
| Class M | Radiation class for mobile units that can reach cover (Section 8.2) |
| Class H | Radiation class for units that cannot move, that are cover, or that are in orbit (Section 8.3) |
| Bay | The receptacle on the host vehicle that the module plugs into |
| Supervisor | The radiation-hardened controller that owns power, heat, swap and routing |
| Cover | Terrain or structure that shields a unit from a solar particle event: a crater wall, a shelter, a lander's shadowed side, a garage |

---

## 4. Links

### 4.1 Link set

| Link | Purpose | Band | Class M | Class H |
|---|---|---|---|---|
| Cellular (3GPP) device | Surface link to a tower, lander or habitat cell to about 10 km | LTE B41 / NR n41 within 2 503.5–2 655 MHz; NR n78 within 3 500–3 800 MHz | Yes | No (Section 8.3) |
| Local mesh | Vehicle-to-vehicle and vehicle-to-lander links to about 300 m | 2 400–2 483.5 MHz | Yes | Yes |
| S-band relay | Low-rate always-available path through lunar relay satellites | Return 2 200–2 290 MHz, forward 2 025–2 110 MHz | Yes | Yes |
| Navigation receive | Lunar navigation signal (Augmented Forward Signal) | 2 492.028 MHz centre, 2 483.5–2 500 MHz band | Yes | Yes |
| Ranging | Vehicle-to-vehicle distance | Ultra-wideband; see Section 4.3 | Yes | Optional |

PBS-SCM-REQ-001: A module MUST NOT transmit in 2 483.5–2 500 MHz, which is reserved for lunar navigation.

PBS-SCM-REQ-002: Cellular carriers MUST lie within the lunar 3GPP blocks of the SFCG lunar band plan (2 503.5–2 655 MHz and 3 500–3 800 MHz). LTE Band 3, used on the IM-2 mission under a one-time waiver, MUST NOT be used.

PBS-SCM-REQ-003: The local mesh MUST stay within 2 400–2 483.5 MHz.

Rationale: these bands are inside the candidate set of WRC-27 agenda item 1.15 and the SFCG lunar band plan, and they keep the module clear of the navigation band. Below 2 GHz is avoided because the band plan protects it for far-side radio astronomy.

### 4.2 Expected performance

| Link | SCM-S | SCM-L | Basis |
|---|---|---|---|
| Cellular | > 10 Mbit/s uplink to 10 km in open terrain, about 1 km where terrain blocks | Same | Nokia coverage study at the Shackleton connecting ridge, UE 23 dBm, 2 m antenna |
| Local mesh | ≥ 1 Mbit/s at 300 m line of sight [A] | Same | NASA surface Wi-Fi range of about 300 m; a CC3200-based rover radio reached 160 m |
| S-band relay return | 1–10 kbit/s at 0.5 W RF into a 5 dBi patch | 10–30 kbit/s at 2 W RF | Scaled from the LCRNS DRM-0 S-band case: 5 W into 0 dBi closes 10 kbit/s with 8.2 dB margin at 17 733 km |
| Navigation | Signal-in-space error per provider (10–20 m class) | Same | Moonlight (≤ 10 m, 95 %) and JAXA (20 m, 2σ initial) requirements |

The S-band relay link is the path of last resort for commands, alerts, telemetry and capability advertisements. Bulk data uses the cellular or mesh links.

### 4.3 Ranging band (open issue)

Commercial ultra-wideband ranging parts operate near 6.5 GHz and 8 GHz. Neither is in the WRC-27 candidate list. Ultra-wideband transmitters on Earth operate as low-power-density underlays without a band allocation; no lunar regime exists.

PBS-SCM-REQ-004: A module MUST be able to range by two-way time transfer on the S-band software-defined radio when ultra-wideband ranging is disabled. The ultra-wideband part MUST be switchable off by command.

This issue is listed in Section 12.

---

## 5. Electronics Architecture

### 5.1 Block diagram

```text
                 ┌──────────────────────── Module ────────────────────────┐
 Host bay        │                                                        │
 ┌──────────┐    │  ┌──────────────┐   rails with latch-up limiters      │
 │ 28 V     ├────┼─►│ Hot-swap ctl  ├──►┬────────┬────────┬──────┬──────┐ │
 │ 100B-T1  ├────┼─►│ + supercap    │   │        │        │      │      │ │
 │ RS-422   ├────┼─►└──────────────┘   ▼        ▼        ▼      ▼      ▼ │
 │ detect   ├────┼─►┌──────────────┐ ┌──────┐ ┌──────┐ ┌─────┐ ┌────┐   │
 │ ID bus   ├────┼─►│  Supervisor   │ │ Cell │ │ Mesh │ │ SDR │ │UWB │   │
 │ RF (L)   ├────┼─┐│ rad-hard MCU  │◄┤modem │ │radio │ │S+nav│ │    │   │
 └──────────┘    │ ││ EDAC memory   │ └──┬───┘ └──┬───┘ └──┬──┘ └─┬──┘   │
                 │ ││ PBS router    │    │        │        │      │      │
                 │ ││ heater loop   │  antennas on lid (patch, helix)    │
                 │ ││ swap logic    │                         │          │
                 │ │└──────────────┘    heaters + sensors     PA (L only)│
                 │ └───────────────────────────────────────────►RF port  │
                 └────────────────────────────────────────────────────────┘
```

### 5.2 Supervisor

The supervisor is the only part trusted to remain correct after a single-event upset. It is a radiation-hardened microcontroller with error-correcting memory (class of the Vorago VA41630 or Microchip SAMRH71).

PBS-SCM-REQ-010: The supervisor MUST control the power rail of every other active part and MUST be able to cut and restore each rail independently.

PBS-SCM-REQ-011: The supervisor MUST hold two firmware images for itself, each with an integrity check, and MUST boot from an image whose check passes.

PBS-SCM-REQ-012: The supervisor MUST hold verified firmware for each radio and MUST reload a radio's firmware after every reset of that radio.

The supervisor runs:

- the PBS router (Section 10);
- a store-and-forward buffer, at least 64 MB in error-corrected memory [A];
- the heater control loop (Section 6);
- the swap state machine (Section 7.4);
- health monitoring and capability advertisement (Section 10.3).

### 5.3 Radios

| Function | Part class | Notes |
|---|---|---|
| Cellular device | Industrial LTE/NR module supporting B41/n41 and n78 | Class M only. Band-locked by firmware to the blocks of PBS-SCM-REQ-002 |
| Local mesh | Low-power 2.4 GHz IEEE 802.11 radio with mesh support (IEEE 802.11s class) | Duty-cycled listen for wake-on-alert (Section 8.2) |
| S-band relay and navigation | One wideband low-power software-defined radio (class of the Analog Devices ADRV9002), time-shared between S-band return/forward and navigation receive | Class H uses a space-grade equivalent |
| Ranging | Ultra-wideband transceiver (class of the Qorvo DW3000) | Optional in Class H; see Section 4.3 |
| Power amplifier | S-band, 2 W RF | SCM-L only |

Part classes name an example of the required function and grade. They are not endorsements; any part meeting the requirements MAY be used.

### 5.4 Antennas

- SCM-S: lid-mounted S-band patch (about 5 dBi at zenith [A]), 2.4 GHz patch, 2.5/3.5 GHz dual-band patch, ultra-wideband patch.
- SCM-L: the same lid set, plus the RF port of Section 7.2 for a host antenna.

Patches face the zenith. At the lunar south pole the elliptical-frozen-orbit relays are at 46–58° elevation near apolune and the towers are near the horizon, so the cellular patch SHOULD have a pattern that favours low elevations [A].

---

## 6. Power and Thermal Design

### 6.1 Supply

PBS-SCM-REQ-020: The module MUST accept 18–36 V from the host, 28 V nominal.

PBS-SCM-REQ-021: The module MUST limit inrush current on insertion so that the host bus voltage does not fall below 18 V when the host bus source impedance is 0.5 Ω or less [A].

PBS-SCM-REQ-022: The module MUST carry hold-up energy of at least 10 J usable (for example about 2 F at 5 V) to complete the shutdown of Section 7.4 after power is lost without warning.

SCM-S carries no battery: lithium cells cannot be charged below 0 °C, and a battery would set the thermal design of the whole module. SCM-L MAY carry a small heated battery.

### 6.2 Power by state

All values [A], to be replaced by measurement.

| State | SCM-S | SCM-L |
|---|---|---|
| Off (cold soak) | 0 | 0 |
| Asleep, supervisor only | 0.15 W | 0.15 W |
| Listening: cellular in power-saving mode, mesh duty-cycled | < 0.5 W | < 0.6 W |
| Cellular transmitting at 23 dBm | about 3 W | about 3 W |
| S-band transmitting | about 2 W (0.5 W RF) | about 8 W (2 W RF) |
| Heater, warm-up | 5 W | 8 W |
| Heater, keep-warm at −30 °C | not used | about 0.65 W |

### 6.3 Night survival

Keeping a module warm through the night costs energy a small vehicle does not have. For SCM-S at −30 °C behind multilayer insulation with an effective emittance of 0.03 [A], radiation over the 0.04 m² surface is about 0.24 W, and conduction through low-conductance mounts and the harness adds about 0.25 W [A], about 0.5 W in total. Over the worst-case night of 354 h this is about 180 Wh.

The design therefore defines two thermal modes.

**Cold-soak survival (SCM-S).** The module powers fully off and is allowed to cool unpowered.

PBS-SCM-REQ-030: SCM-S MUST survive repeated unpowered soaks to −100 °C followed by warm-up, for at least the number of lunar nights in the host's mission plus a factor of 2 [A].

PBS-SCM-REQ-031: Parts, solder joints, connectors and the supercapacitor MUST be selected and qualified for the cold-soak range. Solder-joint fatigue under thermal cycling is the governing failure mode.

**Warm-up when necessary (both shells).**

PBS-SCM-REQ-032: The supervisor MUST NOT enable power to any radio until that radio's board temperature is at or above −20 °C, and MUST NOT enable the S-band power amplifier or the cellular transmitter until its temperature is at or above its rated minimum.

Warm-up energy for SCM-S from −100 °C to −20 °C is about 0.5 kg × 850 J/(kg·K) × 80 K ≈ 34 kJ (9.4 Wh) [A]. With a 5 W heater, warm-up takes about 2 hours.

**Keep-warm (SCM-L).** Larger hosts have power to keep the module at or above −30 °C through the night (about 230 Wh over 354 h [A]), giving immediate service.

PBS-SCM-REQ-033: SCM-L SHOULD provide a mounting interface for a radioisotope heater unit (5 W-thermal americium-241 class) so that keep-warm needs no electrical power.

---

## 7. Swap Interface

### 7.1 Service tiers

| Tier | Hosts | Shell | Swap by | Latch |
|---|---|---|---|---|
| Field | Larger rovers, landers, towers, habitats | SCM-L | Robot gripper or gloved crew, host powered | T-handle with grapple fitting |
| Workshop | Small rovers and hoppers brought into a workshop | SCM-S | Workshop technician or robot, host powered or not | Retaining bracket with two captive thumbscrews |

Both tiers use the same connector and the same core, so one spares stock of cores serves every host.

### 7.2 Connector

PBS-SCM-REQ-040: Both shells MUST use one connector face with these contacts:

| Contact group | Contents | Mating order on insertion |
|---|---|---|
| Chassis | Chassis ground, shield | 1 |
| Power | 28 V and return, through the hot-swap controller | 2 |
| Data | Single-pair Ethernet 100BASE-T1 (IEEE 802.3bw); RS-422 fallback; identity bus to PBS-HW-ID-01 | 3 |
| Detect | Swap-detect contact | 4 (last) |
| RF (SCM-L) | One blind-mate coaxial contact for a host antenna | With data |

Removal breaks the contacts in reverse order, so swap-detect opens before power.

PBS-SCM-REQ-041: The connector MUST self-align from a lateral offset of ±3 mm and an angular offset of ±2° by two conical guide pins.

PBS-SCM-REQ-042: Contacts on both the module and the bay MUST be covered by spring-loaded shutters except when mated, and a wiper MUST clean the contact face during insertion.

PBS-SCM-REQ-043: The connector MUST be rated for at least 500 mating cycles in lunar regolith simulant with contact resistance within the qualified limit [A].

### 7.3 Latch

PBS-SCM-REQ-050: The SCM-L latch MUST be operable by a pressurized-suit glove and by a robot gripper through one T-handle with a quarter-turn lock and a grapple fitting.

PBS-SCM-REQ-051: Releasing the SCM-L latch MUST require two distinct actions.

PBS-SCM-REQ-052: The SCM-S bracket MUST be removable without tools and without loose parts.

### 7.4 Swap state machine

```text
 INSERTED ──detect closes──► POWER-UP ──ID read, self-test──► OPERATIONAL
     ▲                                                          │
     │                                    release request       │
     │                         (command or handle press)        ▼
 REMOVED ◄──detect opens── READY-TO-RELEASE ◄──flush, close links─ DRAINING

 Unannounced removal: detect opens in OPERATIONAL → hold-up energy → DRAINING → REMOVED
```

PBS-SCM-REQ-060: On a release request the module MUST store pending traffic, close its links, report its state and light a ready indicator before the latch is released.

PBS-SCM-REQ-061: On unannounced removal the module MUST complete the same shutdown from hold-up energy (PBS-SCM-REQ-022).

PBS-SCM-REQ-062: Buffered traffic MUST survive removal in non-volatile memory and MUST be handed to the host or forwarded on the next insertion.

---

## 8. Radiation Classes

### 8.1 Hazard model

At the lunar surface, accumulated dose is small: the surface baseline measured by Chang'e-4 (13.2 µGy/h) is about 0.12 Gy per year. The hazards that drive the design are single-event effects from galactic cosmic rays and solar energetic particles: bit flips, hung parts, and latch-up that destroys a part unless its power is cut within milliseconds.

The design response depends on whether a unit can take cover.

### 8.2 Class M: mobile units that can reach cover

Hosts: rovers, hoppers and remotely driven vehicles.

Strategy: reach cover, then wait. Commercial radios behind latch-up protection are sufficient.

PBS-SCM-REQ-070: Every commercial part MUST tolerate at least 20 krad(Si) total ionizing dose and MUST have latch-up test data from the supplier or from testing to this design.

PBS-SCM-REQ-071: Each commercial part's rail MUST have a current limit that detects latch-up and cuts power within 1 ms [A], after which the supervisor restores power and reloads firmware.

PBS-SCM-REQ-072: In every powered state, including asleep, the module MUST keep one receive path open (mesh listen or cellular paging) and MUST wake the host within 5 s [A] of receiving a radiation alert addressed to it or to its deployment scope.

Solar energetic protons can arrive minutes after a flare is seen, and alerts relayed from Earth can arrive after them. On-site detectors and lunar-orbit detectors give the earliest warning, so the wake path listens to the local network.

PBS-SCM-REQ-073: The module MUST hold a list of nearby cover points supplied by the network, with the module's own position from the navigation receiver and ranging, and MUST give the host the nearest reachable cover point on wake.

PBS-SCM-REQ-074: Under cover, the module MUST stop transmitting except for traffic at CRITICAL priority (PBS-PRIO-01) and MUST store all other traffic until the all-clear.

Spot shielding over the memory and the cellular modem SHOULD be used.

### 8.3 Class H: units that cannot move, that are cover, or that are in orbit

Hosts: towers, landers, rigs, fixed sensors, habitats and shelters, relay satellites.

These units carry the alerts and the crew's traffic during a storm, so they operate through it.

PBS-SCM-REQ-080: Class H modules MUST use space-grade, radiation-tolerant parts for the software-defined radio and its processing (a radiation-tolerant FPGA where the waveform needs one), in addition to the radiation-hardened supervisor.

PBS-SCM-REQ-081: Class H modules MUST NOT contain a commercial cellular device. Fixed hosts carry cellular base stations, and orbit has no cellular network.

PBS-SCM-REQ-082: Class H shielding MUST be sized by analysis for the host location:

- surface hosts: the design-reference solar particle event used by the deployment's crew-safety plan, with the module operating throughout;
- orbital hosts: the accumulated dose over the mission life in the host orbit, using a solar particle fluence model (for example ESP/PSYCHIC) and a shielding dose-depth calculation (for example SHIELDOSE-2), with a design margin of 2.

PBS-SCM-REQ-083: In storm mode a Class H module MUST stay on and MUST give CRITICAL and alert traffic precedence over all other traffic.

Class H is offered in the SCM-L shell, which has the volume for shielding.

---

## 9. Identity

The module carries no network identity.

PBS-SCM-REQ-090: On insertion the module MUST read the host's identity from the PBS-HW-ID-01 tag on the identity bus, MUST verify it by challenge and response, and MUST operate as that host's node: same PBS Source ID, same node number, same keys.

PBS-SCM-REQ-091: The module MUST hold its own component serial number for inventory and fault tracking. The component serial MUST NOT be used as a network identity.

PBS-SCM-REQ-092: A module removed from a host MUST NOT retain the host's operational keys.

A swap is therefore invisible to the network apart from a short gap, and a spare or stolen module carries no credentials.

---

## 10. PBS Behaviour

### 10.1 Host interface

The host sees one network interface over single-pair Ethernet, carrying PBS envelopes (PBS-ENV-01) and, where the host uses them, IP packets. The RS-422 fallback carries PBS envelopes only.

### 10.2 Routing and storage

PBS-SCM-REQ-100: The supervisor MUST select among available links by a policy configured by the operator; the default order is cellular, mesh, S-band relay.

PBS-SCM-REQ-101: Traffic with no available link MUST be stored and forwarded when a link returns, within the lifetime of each envelope (PBS-ENV-01).

PBS-SCM-REQ-102: Over the relay path the module MUST map PBS traffic to the Bundle Protocol per PBS-DTN-MAP-01 when the relay provider uses the Bundle Protocol.

### 10.3 Health reporting

PBS-SCM-REQ-110: The module MUST advertise, by PBS-CAPS-01, the state of each link, its thermal mode, its radiation class, its storm-mode state, and counts of resets and latch-up events since insertion.

Capability advertisements SHOULD be authenticated by PBS-SEC-B-01.

---

## 11. Verification

| Requirement area | Verification |
|---|---|
| Bands (REQ-001 to 004) | Conducted and radiated emission measurement of each transmitter against its band |
| Cold soak (REQ-030, 031) | Thermal cycling to −100 °C and back, unpowered, for the required cycle count; solder-joint inspection by X-ray and cross-section of a test article |
| Warm-up (REQ-032) | Cold start from −100 °C; radios confirmed unpowered until −20 °C |
| Swap in dust (REQ-040 to 052) | Mating cycles in regolith simulant by robot gripper and by a pressurized-glove operator; contact resistance logged |
| Unannounced removal (REQ-022, 061, 062) | Live extraction under load, repeated; no lost buffered traffic; host bus voltage recorded |
| Class M radiation (REQ-070, 071) | Proton and heavy-ion beam tests of each commercial part; every latch-up detected and cleared |
| Wake on alert (REQ-072 to 074) | Alert injected in each power state; wake time measured; cover-point output checked |
| Class H radiation (REQ-080 to 083) | Space-grade part data; shielding dose analysis for surface and orbit cases |
| Identity (REQ-090 to 092) | Swap between hosts; node identity follows the host; removed module holds no host keys |
| PBS behaviour (REQ-100 to 110) | PBS envelope, routing, store-and-forward and CAPS test vectors |

---

## 12. Open Issues

1. **Ranging band.** No lunar band covers commercial ultra-wideband ranging (Section 4.3).
2. **WRC-27 outcome.** Agenda item 1.15 may narrow the cellular or mesh bands. Cellular is a modem swap; the mesh and S-band are re-tunable in firmware.
3. **Hardware licence.** This document is published under the repository licence. A hardware licence for design files (schematics, layouts, mechanical drawings) is to be chosen by the Foundation.
4. **Measured values.** Every [A] figure is replaced by measurement on a development unit.

---

## 13. References

What vehicle makers publish, and the sources of figures in this document.

| Topic | Source |
|---|---|
| CADRE: mesh radios between rovers and a lander base station; telecom board with ultra-wideband ranging | JPL, <https://jpl.nasa.gov/missions/cadre>; <https://www-robotics.jpl.nasa.gov/gallery/cadre-telecom-board-testing-2/> |
| MoonFall: four hoppers, communications not published | JPL, <https://www.jpl.nasa.gov/missions/moonfall/> |
| Micro Nova hopper: UHF and 4G/LTE on the surface, S-band to the maker's data network | Intuitive Machines, <https://www.intuitivemachines.com/micro-nova> |
| MAPP rover: S and X band direct-to-Earth, LTE, mesh between rovers | NASASpaceflight, 9 December 2025, <https://www.nasaspaceflight.com/2025/12/lunar-outpost-mapp/> |
| CubeRover: 802.11n at 2.4 GHz to the lander to 200 m, optional 2.25 GHz S-band relay, about 10 kbit/s per kg | Astrobotic CubeRover Payload User's Guide v2, <https://www.astrobotic.com/wp-content/uploads/2024/01/Astrobotic_CubeRover-PUG_V2.pdf> |
| MoonRanger: CC3200 Wi-Fi board, two switched omni antennas, 160 m tested | Carnegie Mellon, <https://labs.ri.cmu.edu/moonranger/testing-moonrangers-wireless-communication/> |
| Ingenuity: 914 MHz Zigbee radios, 250 kbit/s to 1 000 m, rover as base station | JPL press kit, <https://www.jpl.nasa.gov/news/press_kits/ingenuity/landing/mission/spacecraft> |
| NASA surface architecture: Wi-Fi about 300 m from Artemis III; 3GPP to about 10 km, base station on the lander; 23 dBm UE, 2 m UE antenna | NASA Glenn, <https://www.nasa.gov/wp-content/uploads/2026/02/lunar-3gpp-gem-paper-rev3-1.pdf>; <https://ntrs.nasa.gov/api/citations/20230013361/downloads/ICSSC-2023_LSR_paper%20rev7k.pdf> |
| Nokia coverage study at the Shackleton connecting ridge; IM-2 Band 3 waiver | Nokia Bell Labs study as summarised in the PBS Shackleton simulation research (nokia-lte-5g fact sheet); MIT Technology Review, <https://www.technologyreview.com/2025/02/18/1111984/nokia-is-putting-the-first-cellular-network-on-the-moon/> |
| Lunar S-band proximity bands; navigation signal | LunaNet Interoperability Specification v5, <https://www.nasa.gov/wp-content/uploads/2025/02/lunanet-interoperability-specification-v5-baseline.pdf> |
| LCRNS DRM-0 S-band rates (50 bit/s–100 kbit/s) | Esper et al., SpaceOps 2025, <https://ntrs.nasa.gov/citations/20250003321> |
| Lunar band plan: 3GPP blocks, navigation band, far-side protection below 2 GHz | SFCG Rec 32-2R5 as presented at the 2025 Cislunar PNT workshop, <https://ioag.org/Cislunar%20PNT%20Workshop/2.%20Lunar%20PNT%20Spectrum/01%20IOAG-ICG%20on%20Lunar%20PNT-Feb2025-SFCG.pdf> |
| WRC-27 agenda item 1.15 candidate bands | Uganda Communications Commission preparatory brief, July 2026, <https://www.ucc.co.ug/wp-content/uploads/2026/07/WRC-27-NPC-preparatory-brief-for-Agenda-Item-1.15-Lunar-Communications.pdf> |
| Moonlight navigation requirements | ESA and Telespazio, <https://ioag.org/Cislunar2026/Tuesday/02%20Lunar/1110%20Moonlight%20Programme%20Development%20Status_ESA%20TPZ_final.pdf> |
| Lunar surface dose baseline 13.2 µGy/h | Zhang et al. 2020, Science Advances, Chang'e-4 LND, <https://doi.org/10.1126/sciadv.aaz1334> |
| Relay elevation of 46–58° at the south pole near apolune | PBS Shackleton simulation, ELFO geometry computed from the LCRNS reference constellation 3.1 states |
| Worst-case south-pole night of 354 h | NASA Glenn, Lunar Surface Relay terminal (ICSSC 2023), above |
| Radioisotope heater unit (5 W-thermal, americium-241) | World Nuclear News, <https://www.world-nuclear-news.org/articles/blue-ghost-to-carry-nuclear-power-source-to-the-moon> |

---

## 14. Summary

PBS-HW-SCM-01 defines one communication core in two shells. It carries cellular, mesh, S-band relay, navigation and ranging links in bands chosen for the lunar band plan. It survives the night cold or stays warm according to the host's power. It swaps by robot, glove or workshop hand through one dust-tolerant connector. It hardens where cover is not available and helps mobile units reach cover where it is. The vehicle's identity stays with the vehicle (PBS-HW-ID-01), so a swap never changes who a node is.
