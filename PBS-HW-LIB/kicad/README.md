# PBS Hardware Reference Library: KiCad Projects

KiCad projects for the open reference designs of this library. Every part on these boards is a generic placeholder named by the **common type of part that goes there** (for example "Radiation-hardened microcontroller with EDAC", "LTE/NR modem module", "Secure element"). No part numbers and no manufacturers appear. A builder replaces each placeholder footprint with the footprint of the part they choose; the nets, which carry the interconnect the specifications require, do not change.

| Project | Document | Board |
|---|---|---|
| [`pbs-scm-core/`](pbs-scm-core/) | PBS-HW-SCM-01 | Module core board, 92 × 92 mm, shared by the SCM-S and SCM-L shells, with the module half of the host connector on the back. Four schematic sheets: host interface and power; control function, storage, host data; radios and RF; heaters and temperature sensing |
| [`pbs-scm-bay/`](pbs-scm-bay/) | PBS-HW-SCM-01 | Host bay interface board, 112 × 32 mm: the host side of the module connector, the swap-detect loop and the identity-tag connection |
| [`pbs-hwid-tag/`](pbs-hwid-tag/) | PBS-HW-ID-01 | Identity tag, 25 mm round: secure element, contactless front end, antenna coil in copper, wired-interface pads on the back |

## What each project contains

- `<project>.kicad_pro`, `.kicad_sch` (and sub-sheets), `.kicad_pcb`: open in KiCad 8 or 9.
- `PBS_Generic.kicad_sym` and `PBS_Generic.pretty/`: the project's placeholder symbols and footprints, registered in the project's library tables.
- `3d/`: placeholder 3D bodies, coloured by function.
- `output/`:
  - `-schematic.pdf`: the schematics;
  - `-assembly-top.pdf`, `-assembly-bottom.pdf`: board outline, part outlines and a legend of reference to part type;
  - `-labelled-top.png`: top view with part types on the silkscreen;
  - `-3d-top.png`, `-3d-bottom.png`, `-3d-iso.png`: renders with placeholder bodies;
  - `.step`, `.wrl`: 3D models of the board;
  - `-erc.rpt`, `-drc.rpt`: the KiCad electrical and design rule check reports.

## Conventions

| Colour of 3D body | Function |
|---|---|
| Orange | Power path |
| Dark blue | Control function |
| Light blue | Storage |
| Grey | Host and data interfaces |
| Green | Radios |
| Light grey | RF filters, switches and antenna ports |
| Red | Heaters and temperature sensors |
| Purple | Identity |

- **Host connector (core J1, bay J1).** Both halves of the connector of PBS-HW-CON-01, at its true contact positions. Core J1 is the module half on the back of the core board, centred, drawn in the module-face view: hard-gold pads and the two guide-bushing holes. Bay J1 is the bay half: plated holes for the spring contacts and the RF plug, and the two guide-pin holes (A Ø4.00, B Ø3.00). Pad numbers are the contact numbers. The bay 3D model shows the spring contacts at their free heights, coloured by mating order (green 1 chassis, red 2 power, blue 3 data and identity bus, purple 4 detect), the guide pins, and the cover plate (translucent) in its unmated position. In both board views the top edge of the drawing is the module front (+y).
- **Connector geometry.** `tools/connector.py` holds every connector dimension. The footprints, the 3D models and the drawings in [`../drawings/`](../drawings/) are generated from it.
- **Fit.** Parts marked "Class M only" are omitted from Class H modules. U24 (S-band amplifier) is fitted in SCM-L; JP1 (RF bypass) in SCM-S. U27 (ultra-wideband) is optional and off by default.
- **Not routed.** The placeholders are not routed. The design rule check reports unrouted nets as warnings and passes with no errors; the schematic check passes with no errors or warnings.
- **Antenna coil (tag L1).** Drawn as one copper polygon in a net-tie footprint between COIL_A and COIL_B.

## Regenerating

The projects are generated from one interconnect model:

```sh
sh PBS-HW-LIB/kicad/tools/export.sh
```

This runs `tools/generate.py` (requires KiCad 9 and its Python module), the KiCad checks, every export above, and `tools/connector_drawing.py` (requires matplotlib), which draws the connector sheets. Editing the projects in KiCad directly is also fine; regenerating overwrites them.
