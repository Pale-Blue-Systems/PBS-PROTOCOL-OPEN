#!/usr/bin/env python3
"""
Generate the KiCad reference projects of PBS-HW-LIB from one interconnect model.

  python3 PBS-HW-LIB/kicad/tools/generate.py

Writes three projects next to this folder:

  pbs-scm-core/   PBS-HW-SCM-01 module core board (shared by the SCM-S and SCM-L shells)
  pbs-scm-bay/    PBS-HW-SCM-01 host bay interface board
  pbs-hwid-tag/   PBS-HW-ID-01 master device identity tag

Every block is a generic placeholder named by the common type of chip that goes there,
never by a part number (PBS-HW-SCM-01 Section 1). Pins are the interfaces the design needs.
A builder replaces each placeholder footprint with the footprint of the part they choose;
the nets do not change.

Requires KiCad 9 (the pcbnew Python module). Schematics are written in the KiCad 8 file
format, which KiCad 8 and 9 both open.
"""
from __future__ import annotations

import json
import math
import os
import shutil
import textwrap
import uuid as uuidlib
from dataclasses import dataclass, field

import pcbnew

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATE = "2026-10-08"
REV = "0.2"
COMPANY = "Pale Blue Systems Foundation"
SCH_VERSION = "20231120"   # KiCad 8 schematic format
SYM_VERSION = "20231120"
LIB = "PBS_Generic"

# Deterministic UUIDs so regenerating gives identical files.
NS = uuidlib.UUID("6f1c3a52-9a0e-4d1e-8c55-1b5d6a0e7c11")


def uid(*parts: str) -> str:
    return str(uuidlib.uuid5(NS, "/".join(parts)))


# ───────────────────────────── model ─────────────────────────────

GROUP_COLOURS = {  # 3D body colours (r, g, b)
    "power": (0.80, 0.45, 0.15),
    "control": (0.15, 0.30, 0.65),
    "storage": (0.25, 0.45, 0.75),
    "interface": (0.35, 0.35, 0.38),
    "radio": (0.15, 0.50, 0.30),
    "rf": (0.70, 0.70, 0.72),
    "thermal": (0.70, 0.15, 0.15),
    "mech": (0.55, 0.55, 0.55),
    "ident": (0.45, 0.20, 0.55),
}


@dataclass
class Block:
    ref: str
    kind: str                 # common name of the chip or part type
    group: str
    sheet: str
    left: list[tuple[str, str]]   # (pin name, net)
    right: list[tuple[str, str]]
    size: tuple[float, float]     # footprint body w × h, mm
    height: float = 1.5           # 3D body height, mm
    side: str = "F"
    fit: str = "All"              # which builds fit it
    region: str = ""
    fixed: tuple[float, float] | None = None   # board position if not packed
    footprint: str = "block"      # block | connector | hole | coil | tagpads

    @property
    def pins(self) -> list[tuple[str, str, str]]:
        out = []
        n = 1
        for name, net in self.left:
            out.append((str(n), name, net)); n += 1
        for name, net in self.right:
            out.append((str(n), name, net)); n += 1
        return out

    @property
    def fp_name(self) -> str:
        safe = "".join(c if c.isalnum() else "_" for c in self.kind)
        while "__" in safe:
            safe = safe.replace("__", "_")
        return f"{self.ref}_{safe.strip('_')}"[:80]

    @property
    def sym_name(self) -> str:
        return self.fp_name


@dataclass
class Project:
    name: str
    title: str
    doc: str
    board: tuple[float, float]          # w, h (or diameter twice for round)
    round_board: bool
    sheets: list[tuple[str, str]]       # (sheet id, sheet title)
    blocks: list[Block]
    regions: dict[str, tuple[float, float, float, float]] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)
    drawings: list[tuple[str, tuple[float, float, float, float]]] = field(default_factory=list)


# ───────────────────────────── core board ─────────────────────────────

def efuse(ref: str, rail_in: str, rail_out: str, en: str, what: str) -> Block:
    return Block(ref, f"Current-limited load switch (eFuse), latch-up protection: {what}", "power", "power",
                 [("VIN", rail_in), ("EN", en), ("GND", "GND")], [("VOUT", rail_out), ("FLT_N", "FLT_N")],
                 (3.5, 3.5), 1.0, region="power")


def antport(ref: str, net: str, what: str, region: str) -> Block:
    return Block(ref, f"Coaxial antenna port: {what}", "rf", "radio",
                 [("RF", net)], [("GND", "GND")], (3.5, 3.5), 2.5, region=region)


def core_project() -> Project:
    B: list[Block] = []
    # Host connector, contact order per PBS-HW-SCM-01 REQ-010.
    B.append(Block("J1", "Host connector, blind-mate, shuttered (PBS-HW-SCM-01 Section 5.2)", "interface", "power",
        [("CHASSIS", "CHASSIS"), ("SHIELD", "CHASSIS"), ("VIN+", "VIN_RAW"), ("VIN_RTN", "GND"),
         ("T1_P", "T1_P"), ("T1_N", "T1_N"), ("TX+", "RS422_TX_P"), ("TX-", "RS422_TX_N"), ("RX+", "RS422_RX_P")],
        [("RX-", "RS422_RX_N"), ("ID_3V3", "ID_3V3"), ("ID_GND", "GND"), ("ID_SCL", "ID_SCL"), ("ID_SDA", "ID_SDA"),
         ("DET_A", "DET_A"), ("DET_B", "DET_B"), ("RF_HOST", "RF_HOST")],
        (48, 8), 6.0, fixed=(46, 85.5), footprint="connector"))
    for i, (x, y) in enumerate([(4, 4), (88, 4), (4, 88), (88, 88)], 1):
        B.append(Block(f"MH{i}", "Mounting hole, chassis bonded", "mech", "power", [("MH", "CHASSIS")], [],
                       (6.4, 6.4), 0.0, fixed=(x, y), footprint="hole"))
    # Power path
    B += [
        Block("U1", "Input TVS and EMI filter", "power", "power",
              [("IN", "VIN_RAW"), ("CHASSIS", "CHASSIS")], [("OUT", "VIN_FILT"), ("GND", "GND")], (9, 6), 3.0, region="power"),
        Block("U2", "Hot-swap controller with inrush limit", "power", "power",
              [("VIN", "VIN_FILT"), ("EN", "MATED_EN"), ("GND", "GND")], [("VOUT", "VBUS"), ("PG", "PG")], (6, 5), 1.2, region="power"),
        Block("U3", "Swap-detect conditioning (comparator)", "power", "power",
              [("VIN", "VIN_FILT"), ("SRC", "DET_A"), ("SENSE", "DET_B"), ("GND", "GND")],
              [("EN_OUT", "MATED_EN"), ("DET_N", "DET_N")], (5, 4), 1.0, region="power"),
        Block("U4", "Hold-up controller (ideal diode and supercapacitor charger)", "power", "power",
              [("VBUS", "VBUS"), ("GND", "GND")], [("VSYS", "VSYS"), ("VHOLD", "VHOLD"), ("PFAIL", "PFAIL")], (6, 6), 1.2, region="power"),
        Block("C1", "Supercapacitor bank, at least 10 J usable", "power", "power",
              [("+", "VHOLD")], [("-", "GND")], (22, 11), 8.0, region="power"),
        Block("U5", "Wide-input DC-DC buck converter (VSYS to 5 V)", "power", "power",
              [("VIN", "VSYS"), ("EN", "PG"), ("GND", "GND")], [("VOUT", "V5")], (9, 9), 4.0, region="power"),
        Block("U6", "Point-of-load regulators (3.3 V, 1.8 V, 1.0 V)", "power", "power",
              [("VIN", "V5"), ("GND", "GND")], [("3V3", "V3V3"), ("1V8", "V1V8"), ("1V0", "V1V0")], (9, 9), 2.0, region="power"),
        Block("U7", "Voltage supervisor with watchdog", "control", "power",
              [("VDD", "V3V3"), ("WDI", "WDI"), ("GND", "GND")], [("RST_N", "RST_N")], (3.5, 3.5), 1.0, region="power"),
        efuse("U8", "V5", "VCELL", "EN_CELL", "cellular"),
        efuse("U9", "V3V3", "VMESH", "EN_MESH", "mesh"),
        efuse("U10", "V3V3", "VSDR", "EN_SDR", "S-band and navigation"),
        efuse("U11", "V3V3", "VUWB", "EN_UWB", "ranging"),
        efuse("U12", "V5", "VPA", "EN_PA", "S-band amplifier"),
    ]
    # Control, storage, host data
    B += [
        Block("U13", "Radiation-hardened microcontroller with EDAC (control function)", "control", "control",
              [("VDD", "V3V3"), ("VCORE", "V1V8"), ("RST_N", "RST_N"), ("WDI", "WDI"), ("PG", "PG"), ("PFAIL", "PFAIL"),
               ("DET_N", "DET_N"), ("ETH_MII", "ETH_MII"), ("UART_HOST", "UART_HOST"), ("I2C_SCL", "I2C_SCL"),
               ("I2C_SDA", "I2C_SDA"), ("SPI_FLASH", "SPI_FLASH"), ("MEM_BUS", "MEM_BUS"), ("REF_CLK", "REF_CLK"),
               ("REL_REQ", "REL_REQ"), ("GND", "GND")],
              [("EN_CELL", "EN_CELL"), ("EN_MESH", "EN_MESH"), ("EN_SDR", "EN_SDR"), ("EN_UWB", "EN_UWB"), ("EN_PA", "EN_PA"),
               ("FLT_N", "FLT_N"), ("CELL_IF", "CELL_IF"), ("MESH_IF", "MESH_IF"), ("SDR_IF", "SDR_IF"), ("UWB_IF", "UWB_IF"),
               ("HEAT_PWM", "HEAT_PWM"), ("TEMP1", "TEMP1"), ("TEMP2", "TEMP2"), ("TEMP3", "TEMP3"), ("LED_RDY", "LED_RDY")],
              (20, 20), 3.0, region="control"),
        Block("U14", "Radiation-tolerant NOR flash (two firmware images)", "storage", "control",
              [("VDD", "V3V3"), ("GND", "GND")], [("SPI", "SPI_FLASH")], (6, 8), 1.2, region="control"),
        Block("U15", "Store-and-forward memory, at least 64 MB, EDAC (MRAM or SRAM)", "storage", "control",
              [("VDD", "V3V3"), ("GND", "GND")], [("BUS", "MEM_BUS")], (12, 12), 1.5, region="control"),
        Block("U16", "Single-pair Ethernet PHY (100BASE-T1)", "interface", "control",
              [("VDD", "V3V3"), ("MII", "ETH_MII"), ("GND", "GND")], [("MDI_P", "T1_P"), ("MDI_N", "T1_N")], (6, 6), 1.0, region="control"),
        Block("U17", "RS-422 transceiver", "interface", "control",
              [("VDD", "V3V3"), ("UART", "UART_HOST"), ("GND", "GND")],
              [("Y", "RS422_TX_P"), ("Z", "RS422_TX_N"), ("A", "RS422_RX_P"), ("B", "RS422_RX_N")], (5, 4.5), 1.0, region="control"),
        Block("U18", "Hot-swap I2C bus buffer with tag supply switch", "interface", "control",
              [("VDD", "V3V3"), ("SCL_IN", "I2C_SCL"), ("SDA_IN", "I2C_SDA"), ("GND", "GND")],
              [("SCL_OUT", "ID_SCL"), ("SDA_OUT", "ID_SDA"), ("VTAG", "ID_3V3")], (4.5, 4.5), 1.0, region="control"),
        Block("Y1", "TCXO reference oscillator", "control", "control",
              [("VDD", "V3V3"), ("GND", "GND")], [("OUT", "REF_CLK")], (3.2, 2.5), 1.0, region="control"),
        Block("D1", "Ready indicator LED", "control", "control", [("A", "LED_RDY")], [("K", "GND")], (2.5, 2), 0.8, region="control"),
        Block("SW1", "Release-request switch (latch handle)", "mech", "control",
              [("A", "REL_REQ")], [("B", "GND")], (6, 4), 3.0, region="control"),
    ]
    # Radios
    B += [
        Block("U19", "LTE/NR modem module (3GPP device, B41/n41 and n78)", "radio", "radio",
              [("VCC", "VCELL"), ("HOST_IF", "CELL_IF"), ("SIM", "SIM_IF"), ("GND", "GND")], [("ANT", "RF_CELL")],
              (30, 30), 2.4, fit="Class M only", region="cell"),
        Block("U20", "eSIM (MFF2)", "radio", "radio", [("VDD", "VCELL"), ("GND", "GND")], [("SIM", "SIM_IF")],
              (6, 5), 0.9, fit="Class M only", region="cell"),
        antport("J2", "RF_CELL", "cellular", "cell"),
        Block("U21", "Wi-Fi SoC with 802.11s mesh (2.4 GHz)", "radio", "radio",
              [("VDD", "VMESH"), ("HOST_IF", "MESH_IF"), ("GND", "GND")], [("RF", "RF_MESH_RAW")], (8, 8), 1.0, region="mesh"),
        Block("FL1", "2.4 GHz band-pass filter (2400-2483.5 MHz)", "rf", "radio",
              [("IN", "RF_MESH_RAW"), ("GND", "GND")], [("OUT", "RF_MESH")], (3.5, 2.5), 0.8, region="mesh"),
        antport("J3", "RF_MESH", "2.4 GHz mesh", "mesh"),
        Block("U22", "Wideband SDR transceiver RFIC", "radio", "radio",
              [("VDD", "VSDR"), ("CTRL", "SDR_IF"), ("DATA", "SDR_DATA"), ("REF", "REF_CLK"), ("GND", "GND")],
              [("TX", "RF_SDR_TX"), ("RX1", "RF_SDR_RX"), ("RX2", "RF_NAV")], (12, 12), 1.2, region="sband"),
        Block("U23", "Low-power FPGA (waveform processing)", "radio", "radio",
              [("VDD", "VSDR"), ("VCORE", "V1V0"), ("GND", "GND")], [("DATA", "SDR_DATA"), ("HOST", "SDR_IF")], (10, 10), 1.2, region="sband"),
        Block("U24", "S-band power amplifier, 2 W", "radio", "radio",
              [("IN", "RF_SDR_TX"), ("VDD", "VPA"), ("GND", "GND")], [("OUT", "RF_PA_OUT")], (5, 5), 1.0,
              fit="SCM-L only", region="sband"),
        Block("JP1", "RF bypass link (SCM-S: fitted in place of the amplifier)", "rf", "radio",
              [("A", "RF_SDR_TX")], [("B", "RF_PA_OUT")], (2.5, 1.5), 0.5, fit="SCM-S only", region="sband"),
        Block("U25", "S-band front end: T/R switch and LNA", "rf", "radio",
              [("TX_IN", "RF_PA_OUT"), ("RX_OUT", "RF_SDR_RX"), ("CTRL", "SDR_IF"), ("VDD", "VSDR"), ("GND", "GND")],
              [("ANT", "RF_SBAND")], (5, 5), 1.0, region="sband"),
        Block("FL2", "S-band duplexer (2025-2110 / 2200-2290 MHz)", "rf", "radio",
              [("IN", "RF_SBAND"), ("GND", "GND")], [("OUT", "RF_SBAND_F")], (7, 5), 1.5, region="sband"),
        Block("U26", "RF antenna selector switch (lid antenna or host RF port)", "rf", "radio",
              [("RFC", "RF_SBAND_F"), ("CTRL", "SDR_IF"), ("GND", "GND")], [("P1", "RF_SBAND_LID"), ("P2", "RF_HOST")],
              (4, 4), 0.8, region="sband"),
        antport("J4", "RF_SBAND_LID", "S-band lid patch", "sband"),
        Block("FL3", "Navigation band SAW filter and LNA (2483.5-2500 MHz)", "rf", "radio",
              [("IN", "RF_NAV_ANT"), ("VDD", "VSDR"), ("GND", "GND")], [("OUT", "RF_NAV")], (5, 4), 1.0, region="sband"),
        antport("J5", "RF_NAV_ANT", "navigation patch", "sband"),
        Block("U27", "UWB ranging transceiver (optional, off by default)", "radio", "radio",
              [("VDD", "VUWB"), ("HOST_IF", "UWB_IF"), ("GND", "GND")], [("RF", "RF_UWB")], (6, 6), 1.0,
              fit="Optional", region="mesh"),
        antport("J6", "RF_UWB", "UWB", "mesh"),
    ]
    # Thermal
    B += [
        Block("Q1", "Heater driver, low-side MOSFET", "thermal", "thermal",
              [("G", "HEAT_PWM"), ("S", "GND")], [("D", "HEAT_RTN")], (5, 4), 1.5, region="power"),
        Block("H1", "Polyimide film heater, zone A (radios)", "thermal", "thermal",
              [("+", "VSYS")], [("-", "HEAT_RTN")], (38, 32), 0.3, side="B", fixed=(28, 25)),
        Block("H2", "Polyimide film heater, zone B (power and control)", "thermal", "thermal",
              [("+", "VSYS")], [("-", "HEAT_RTN")], (38, 32), 0.3, side="B", fixed=(68, 62)),
        Block("RT1", "Platinum RTD temperature sensor (radio zone)", "thermal", "thermal",
              [("A", "TEMP1")], [("B", "GND")], (3.2, 1.6), 0.6, region="mesh"),
        Block("RT2", "Platinum RTD temperature sensor (power zone)", "thermal", "thermal",
              [("A", "TEMP2")], [("B", "GND")], (3.2, 1.6), 0.6, region="power"),
        Block("RT3", "Platinum RTD temperature sensor (control zone)", "thermal", "thermal",
              [("A", "TEMP3")], [("B", "GND")], (3.2, 1.6), 0.6, region="control"),
    ]
    return Project(
        "pbs-scm-core", "PBS-HW-SCM-01 Surface Communication Module, core board",
        "PBS-HW-SCM-01", (92.0, 92.0), False,
        [("power", "Host interface and power"), ("control", "Control function, storage, host data"),
         ("radio", "Radios and RF"), ("thermal", "Heaters and temperature sensing")],
        B,
        regions={"cell": (9, 3, 41, 44), "sband": (43, 3, 83, 29), "mesh": (43, 30, 83, 44),
                 "power": (3, 46, 40, 80), "control": (42, 46, 89, 80)},
        notes=[
            "Reference design: every block is a placeholder named by the common type of part that goes there.",
            "Replace each placeholder footprint with the footprint of the chosen part; the nets do not change.",
            "Connector contact groups and mating order: PBS-HW-SCM-01 REQ-010 (pad length = mating order).",
            "Fit: 'Class M only' parts are omitted in Class H; U24 is fitted in SCM-L, JP1 in SCM-S.",
            "Heaters H1 and H2 are film heaters bonded to the back of the board.",
        ],
    )


# ───────────────────────────── bay board ─────────────────────────────

def bay_project() -> Project:
    B = [
        Block("J1", "Module receptacle, blind-mate, shuttered (PBS-HW-SCM-01 Section 5.2)", "interface", "bay",
              [("CHASSIS", "CHASSIS"), ("SHIELD", "CHASSIS"), ("VIN+", "VIN"), ("VIN_RTN", "GND"),
               ("T1_P", "T1_P"), ("T1_N", "T1_N"), ("TX+", "RS422_TX_P"), ("TX-", "RS422_TX_N"), ("RX+", "RS422_RX_P")],
              [("RX-", "RS422_RX_N"), ("ID_3V3", "ID_3V3"), ("ID_GND", "GND"), ("ID_SCL", "ID_SCL"), ("ID_SDA", "ID_SDA"),
               ("DET_A", "DET_LOOP"), ("DET_B", "DET_LOOP"), ("RF_HOST", "RF_HOST")],
              (48, 8), 6.0, fixed=(56, 7.5), footprint="connector"),
        Block("J2", "Host harness connector", "interface", "bay",
              [("VIN", "VIN"), ("GND", "GND"), ("CHASSIS", "CHASSIS"), ("T1_P", "T1_P_H"), ("T1_N", "T1_N_H")],
              [("TX+", "RS422_TX_P_H"), ("TX-", "RS422_TX_N_H"), ("RX+", "RS422_RX_P_H"), ("RX-", "RS422_RX_N_H"), ("SEATED_N", "SEATED_N")],
              (24, 8), 7.0, fixed=(30, 25)),
        Block("U1", "ESD/TVS protection array (data lines)", "interface", "bay",
              [("T1_P", "T1_P_H"), ("T1_N", "T1_N_H"), ("TX+", "RS422_TX_P_H"), ("TX-", "RS422_TX_N_H"),
               ("RX+", "RS422_RX_P_H"), ("RX-", "RS422_RX_N_H"), ("GND", "GND")],
              [("T1_P_M", "T1_P"), ("T1_N_M", "T1_N"), ("TX+_M", "RS422_TX_P"), ("TX-_M", "RS422_TX_N"),
               ("RX+_M", "RS422_RX_P"), ("RX-_M", "RS422_RX_N")],
              (8, 6), 1.0, fixed=(58, 25)),
        Block("J3", "Identity tag pigtail connector, 4 contacts (PBS-HW-ID-01 Section 5.3)", "ident", "bay",
              [("3V3", "ID_3V3"), ("GND", "GND")], [("SCL", "ID_SCL"), ("SDA", "ID_SDA")], (10, 5), 4.0, fixed=(78, 25)),
        Block("J4", "Coaxial host antenna port (SCM-L RF contact)", "rf", "bay",
              [("RF", "RF_HOST")], [("GND", "GND")], (6, 6), 5.0, fixed=(96, 24)),
        Block("SW1", "Module-seated switch (signal to host)", "mech", "bay",
              [("COM", "GND")], [("NO", "SEATED_N")], (6, 4), 3.0, fixed=(12, 24)),
    ]
    for i, (x, y) in enumerate([(4, 4), (108, 4), (4, 28), (108, 28)], 1):
        B.append(Block(f"MH{i}", "Mounting hole, chassis bonded", "mech", "bay", [("MH", "CHASSIS")], [],
                       (6.4, 6.4), 0.0, fixed=(x, y), footprint="hole"))
    return Project(
        "pbs-scm-bay", "PBS-HW-SCM-01 host bay interface board", "PBS-HW-SCM-01", (112.0, 32.0), False,
        [("bay", "Bay interface")], B,
        notes=[
            "Host side of the module connector. DET_A and DET_B are joined here: the swap-detect loop closes only when the module is fully mated.",
            "The identity tag of the host vehicle (PBS-HW-ID-01) connects at J3 and reaches the module on the identity-bus contacts.",
            "J4 is fitted where the host provides an antenna to an SCM-L module.",
        ],
    )


# ───────────────────────────── identity tag ─────────────────────────────

def tag_project() -> Project:
    B = [
        Block("U1", "Secure element (Ed25519, on-chip key generation, I2C)", "ident", "tag",
              [("VDD", "V_SE"), ("SCL", "SCL"), ("SDA", "SDA"), ("GND", "GND")], [("LINK", "SE_LINK")], (3.5, 3.5), 0.8, fixed=(10.2, 13)),
        Block("U2", "ISO/IEC 15693 contactless front end with energy harvest", "ident", "tag",
              [("COIL_A", "COIL_A"), ("COIL_B", "COIL_B"), ("GND", "GND")], [("LINK", "SE_LINK"), ("VHARV", "V_HARV")],
              (3.5, 3.5), 0.8, fixed=(14.8, 13)),
        Block("U3", "Current limiter (latch-up protection)", "power", "tag",
              [("IN", "V_IN"), ("GND", "GND")], [("OUT", "V_PROT")], (2.0, 2.0), 0.6, fixed=(10.5, 9.2)),
        Block("U4", "Power OR-ing (dual ideal diode)", "power", "tag",
              [("A", "V_PROT"), ("B", "V_HARV")], [("OUT", "V_SE"), ("GND", "GND")], (2.0, 2.0), 0.6, fixed=(14.5, 9.2)),
        Block("C1", "Antenna tuning capacitor", "rf", "tag", [("A", "COIL_A")], [("B", "COIL_B")], (1.2, 0.8), 0.5, fixed=(12.5, 16.2)),
        Block("L1", "Contactless antenna coil (copper spiral)", "rf", "tag", [("A", "COIL_A")], [("B", "COIL_B")],
              (24, 24), 0.0, fixed=(12.5, 12.5), footprint="coil"),
        Block("J1", "Wired interface pads: 3.3 V, GND, SCL, SDA (PBS-HW-ID-01 Section 5.3)", "ident", "tag",
              [("3V3", "V_IN"), ("GND", "GND")], [("SCL", "SCL"), ("SDA", "SDA")], (12, 4), 0.0, side="B",
              fixed=(12.5, 12.5), footprint="tagpads"),
    ]
    return Project(
        "pbs-hwid-tag", "PBS-HW-ID-01 master device identity tag", "PBS-HW-ID-01", (25.0, 25.0), True,
        [("tag", "Identity tag")], B,
        notes=[
            "25 mm round tag. Coil on the front copper; electronics inside the coil; wired-interface pads on the back.",
            "The master device ID (hwid:...) and its Data Matrix code are marked on the exposed face (PBS-HW-ID-01 REQ-031).",
            "Unpowered most of its life; the contactless front end powers the secure element from the reader's field.",
        ],
    )


# ───────────────────────────── symbols ─────────────────────────────

G = 2.54


def fmt(v: float) -> str:
    s = f"{v:.4f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def q(s: str) -> str:
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def sym_geom(b: Block):
    n = max(len(b.left), len(b.right), 1)
    ln = max([len(p[0]) for p in b.left] + [0])
    rn = max([len(p[0]) for p in b.right] + [0])
    w = max(15.24, (ln + rn) * 1.27 + 7.62)
    w = math.ceil(w / (2 * G)) * 2 * G
    top = ((n - 1) / 2) * G + G
    return n, w, top


def sym_pins(b: Block):
    """Pin connection points in symbol coordinates (y up)."""
    n, w, top = sym_geom(b)
    pts = []
    num = 1
    for i, (name, net) in enumerate(b.left):
        y = ((n - 1) / 2 - i) * G
        pts.append((str(num), name, net, -w / 2 - G, y, 0)); num += 1
    for i, (name, net) in enumerate(b.right):
        y = ((n - 1) / 2 - i) * G
        pts.append((str(num), name, net, w / 2 + G, y, 180)); num += 1
    return pts


def symbol_def(b: Block, with_lib: bool) -> str:
    n, w, top = sym_geom(b)
    name = f"{LIB}:{b.sym_name}" if with_lib else b.sym_name
    prefix = "".join(c for c in b.ref if c.isalpha())
    lines = [f'(symbol {q(name)} (pin_names (offset 1.016)) (exclude_from_sim no) (in_bom yes) (on_board yes)',
             f'  (property "Reference" {q(prefix)} (at 0 {fmt(top + 1.27)} 0) (effects (font (size 1.27 1.27))))',
             f'  (property "Value" {q(b.kind)} (at 0 {fmt(-top - 1.27)} 0) (effects (font (size 1.27 1.27))))',
             f'  (property "Footprint" {q(LIB + ":" + b.fp_name)} (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
             '  (property "Datasheet" "" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
             f'  (property "Description" {q("Generic placeholder: " + b.kind)} (at 0 0 0) (effects (font (size 1.27 1.27)) hide))',
             f'  (symbol {q(b.sym_name + "_0_1")}',
             f'    (rectangle (start {fmt(-w / 2)} {fmt(top)}) (end {fmt(w / 2)} {fmt(-top)}) (stroke (width 0.254) (type default)) (fill (type background))))',
             f'  (symbol {q(b.sym_name + "_1_1")}']
    for num, pname, _net, x, y, ang in sym_pins(b):
        lines.append(f'    (pin passive line (at {fmt(x)} {fmt(y)} {ang}) (length {fmt(G)})'
                     f' (name {q(pname)} (effects (font (size 1.27 1.27)))) (number {q(num)} (effects (font (size 1.27 1.27)))))')
    lines.append('  ))')
    return "\n".join(lines)


def write_symlib(p: Project, d: str):
    body = "\n".join(symbol_def(b, False) for b in p.blocks)
    with open(os.path.join(d, f"{LIB}.kicad_sym"), "w") as f:
        f.write(f'(kicad_symbol_lib (version {SYM_VERSION}) (generator "pbs_hw_generate") (generator_version "{REV}")\n{body}\n)\n')


# ───────────────────────────── schematics ─────────────────────────────

PAPERS = [("A3", 420, 297), ("A2", 594, 420), ("A1", 841, 594), ("A0", 1189, 841)]


def snap(v: float) -> float:
    return round(v / G) * G


def layout_sheet(blocks: list[Block]):
    """Place symbols in columns; returns positions and paper."""
    items = []
    for b in blocks:
        n, w, top = sym_geom(b)
        lab_l = max([len(net) for _, net in b.left] + [0]) * 1.1 + 4
        lab_r = max([len(net) for _, net in b.right] + [0]) * 1.1 + 4
        width = w + 2 * G + lab_l + lab_r
        height = 2 * top + 8
        items.append((b, width, height, lab_l, w))
    for paper, pw, ph in PAPERS:
        x0, y0 = 25.4, 38.1
        maxy = ph - 45
        pos = {}
        x, y, colw = x0, y0, 0.0
        ok = True
        for b, width, height, lab_l, w in items:
            if y + height > maxy and y > y0:
                x += colw + 10
                y, colw = y0, 0.0
            if x + width > pw - 15:
                ok = False
                break
            cx = snap(x + lab_l + G + w / 2)
            cy = snap(y + height / 2)
            pos[b.ref] = (cx, cy)
            y += height + 2
            colw = max(colw, width)
        if ok:
            return pos, paper
    raise RuntimeError("sheet too large")


def label(net: str, x: float, y: float, ang: int, key: str) -> str:
    just = "right" if ang == 180 else "left"
    return (f'(global_label {q(net)} (shape passive) (at {fmt(x)} {fmt(y)} {ang}) (fields_autoplaced yes)'
            f' (effects (font (size 1.27 1.27)) (justify {just})) (uuid {q(uid(key))}))')


def title_block(p: Project, title: str, n: int) -> str:
    return (f'(title_block (title {q(title)}) (date {q(DATE)}) (rev {q(REV)}) (company {q(COMPANY)})'
            f' (comment 1 {q(p.doc + " open reference design; generic placeholders, no part numbers")})'
            f' (comment 2 {q("Generated by PBS-HW-LIB/kicad/tools/generate.py")}))')


def sheet_file(p: Project, sheet_id: str, sheet_title: str, inst_path: str, root_uuid: str, page: int) -> str:
    blocks = [b for b in p.blocks if b.sheet == sheet_id]
    pos, paper = layout_sheet(blocks)
    out = [f'(kicad_sch (version {SCH_VERSION}) (generator "eeschema") (generator_version "8.0")',
           f'  (uuid {q(uid(p.name, "sheet", sheet_id))})', f'  (paper {q(paper)})',
           '  ' + title_block(p, f"{p.title}: {sheet_title}", page), '  (lib_symbols']
    seen = set()
    for b in blocks:
        if b.sym_name not in seen:
            out.append(textwrap.indent(symbol_def(b, True), "    "))
            seen.add(b.sym_name)
    out.append('  )')
    for b in blocks:
        cx, cy = pos[b.ref]
        n, w, top = sym_geom(b)
        out.append(f'  (symbol (lib_id {q(LIB + ":" + b.sym_name)}) (at {fmt(cx)} {fmt(cy)} 0) (unit 1)'
                   f' (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no) (uuid {q(uid(p.name, "sym", b.ref))})')
        out.append(f'    (property "Reference" {q(b.ref)} (at {fmt(cx)} {fmt(cy - top - 1.27)} 0) (effects (font (size 1.27 1.27))))')
        out.append(f'    (property "Value" {q(b.kind)} (at {fmt(cx)} {fmt(cy + top + 1.27)} 0) (effects (font (size 1.27 1.27))))')
        out.append(f'    (property "Footprint" {q(LIB + ":" + b.fp_name)} (at {fmt(cx)} {fmt(cy)} 0) (effects (font (size 1.27 1.27)) hide))')
        out.append(f'    (property "Datasheet" "" (at {fmt(cx)} {fmt(cy)} 0) (effects (font (size 1.27 1.27)) hide))')
        out.append(f'    (property "Description" {q("Generic placeholder: " + b.kind)} (at {fmt(cx)} {fmt(cy)} 0) (effects (font (size 1.27 1.27)) hide))')
        out.append(f'    (property "Fit" {q(b.fit)} (at {fmt(cx)} {fmt(cy + top + 3.81)} 0) (effects (font (size 1.27 1.27)){"" if b.fit != "All" else " hide"}))')
        for num, *_ in sym_pins(b):
            out.append(f'    (pin {q(num)} (uuid {q(uid(p.name, "pin", b.ref, num))}))')
        out.append(f'    (instances (project {q(p.name)} (path {q(inst_path)} (reference {q(b.ref)}) (unit 1)))))')
        for num, _pname, net, x, y, ang in sym_pins(b):
            out.append('  ' + label(net, cx + x, cy - y, 180 if ang == 0 else 0, f"{p.name}/lab/{b.ref}/{num}"))
    # notes on the first sheet
    if page == 2 or len(p.sheets) == 1:
        ty = 20.32
        for i, note in enumerate(p.notes):
            out.append(f'  (text {q(note)} (exclude_from_sim no) (at 25.4 {fmt(ty + i * 3.81)} 0)'
                       f' (effects (font (size 1.778 1.778)) (justify left bottom)) (uuid {q(uid(p.name, "note", sheet_id, str(i)))}))')
    if len(p.sheets) == 1:
        out.append(f'  (sheet_instances (path "/" (page "1")))')
    out.append(')')
    return "\n".join(out) + "\n"


def root_file(p: Project, root_uuid: str) -> str:
    out = [f'(kicad_sch (version {SCH_VERSION}) (generator "eeschema") (generator_version "8.0")',
           f'  (uuid {q(root_uuid)})', '  (paper "A4")', '  ' + title_block(p, p.title, 1), '  (lib_symbols)']
    for i, note in enumerate(p.notes):
        out.append(f'  (text {q(note)} (exclude_from_sim no) (at 20.32 {fmt(30.48 + i * 5.08)} 0)'
                   f' (effects (font (size 1.778 1.778)) (justify left bottom)) (uuid {q(uid(p.name, "rootnote", str(i)))}))')
    x, y = 25.4, 76.2
    for i, (sid, stitle) in enumerate(p.sheets):
        su = uid(p.name, "sheetsym", sid)
        out.append(f'  (sheet (at {fmt(x)} {fmt(y)}) (size 55.88 17.78) (exclude_from_sim no) (in_bom yes) (on_board yes) (dnp no)'
                   f' (fields_autoplaced yes) (stroke (width 0.1524) (type solid)) (fill (color 0 0 0 0.0000)) (uuid {q(su)})'
                   f' (property "Sheetname" {q(stitle)} (at {fmt(x)} {fmt(y - 0.7116)} 0) (effects (font (size 1.27 1.27)) (justify left bottom)))'
                   f' (property "Sheetfile" {q(sid + ".kicad_sch")} (at {fmt(x)} {fmt(y + 18.3716)} 0) (effects (font (size 1.27 1.27)) (justify left top)))'
                   f' (instances (project {q(p.name)} (path {q("/" + root_uuid)} (page {q(str(i + 2))})))))')
        x += 66.04
        if x > 230:
            x, y = 25.4, y + 30.48
    out.append('  (sheet_instances (path "/" (page "1")))')
    out.append(')')
    return "\n".join(out) + "\n"


def write_schematics(p: Project, d: str):
    root_uuid = uid(p.name, "root")
    if len(p.sheets) == 1:
        sid, stitle = p.sheets[0]
        with open(os.path.join(d, f"{p.name}.kicad_sch"), "w") as f:
            f.write(sheet_file(p, sid, stitle, "/" + uid(p.name, "sheet", sid), root_uuid, 1)
                    .replace(f'(uuid {q(uid(p.name, "sheet", sid))})', f'(uuid {q(uid(p.name, "sheet", sid))})', 1))
        return
    with open(os.path.join(d, f"{p.name}.kicad_sch"), "w") as f:
        f.write(root_file(p, root_uuid))
    for i, (sid, stitle) in enumerate(p.sheets):
        path = f"/{root_uuid}/{uid(p.name, 'sheetsym', sid)}"
        with open(os.path.join(d, f"{sid}.kicad_sch"), "w") as f:
            f.write(sheet_file(p, sid, stitle, path, root_uuid, i + 2))


# ───────────────────────────── board ─────────────────────────────

MM = pcbnew.FromMM


def V(x: float, y: float):
    return pcbnew.VECTOR2I(MM(x), MM(y))


def wrap_label(text: str, w: float, h: float):
    """Fit text in a w × h box: returns (lines, text height)."""
    for th in (1.2, 1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.45, 0.4):
        per = max(4, int((w - 0.8) / (0.86 * th)))
        lines = textwrap.wrap(text, per, break_long_words=False)
        if len(lines) * th * 1.55 + th * 1.8 <= h - 0.4 and all(len(l) * 0.86 * th <= w - 0.6 for l in lines):
            return lines, th
    return textwrap.wrap(text, max(4, int((w - 0.6) / (0.72 * 0.4))))[:3], 0.4


def add_shape(parent, layer, start, end, width=0.1, kind=pcbnew.SHAPE_T_RECT, fill=False):
    s = pcbnew.PCB_SHAPE(parent)
    s.SetShape(kind)
    s.SetStart(V(*start))
    s.SetEnd(V(*end))
    s.SetLayer(layer)
    s.SetWidth(MM(width))
    if fill:
        s.SetFilled(True)
    parent.Add(s)
    return s


def add_text(parent, layer, text, x, y, h, bold=False, mirror=False):
    t = pcbnew.PCB_TEXT(parent)
    t.SetText(text)
    t.SetLayer(layer)
    t.SetPosition(V(x, y))
    t.SetTextSize(V(h, h))
    t.SetTextThickness(MM(max(0.08, h * (0.18 if bold else 0.13))))
    t.SetMirrored(mirror)
    parent.Add(t)
    return t


def vrml_box(path: str, w: float, h: float, z: float, rgb, z0: float = 0.0):
    s = 1 / 2.54   # KiCad VRML unit = 0.1 inch
    hx, hy, hz = w / 2 * s, h / 2 * s, max(z, 0.05) / 2 * s
    cz = (z0 + max(z, 0.05) / 2) * s
    r, g, b = rgb
    with open(path, "w") as f:
        f.write("#VRML V2.0 utf8\n"
                f"Transform {{ translation 0 0 {cz:.5f} children [ Shape {{\n"
                f" appearance Appearance {{ material Material {{ diffuseColor {r} {g} {b} specularColor 0.2 0.2 0.2 shininess 0.3 }} }}\n"
                f" geometry Box {{ size {2 * hx:.5f} {2 * hy:.5f} {2 * hz:.5f} }} }} ] }}\n")


def make_footprint(board, b: Block, nets: dict, model_dir: str):
    fp = pcbnew.FOOTPRINT(board)
    fp.SetFPID(pcbnew.LIB_ID(LIB, b.fp_name))
    fp.SetReference(b.ref)
    fp.SetValue(b.kind)
    fp.SetLibDescription("Generic placeholder: " + b.kind)
    fp.SetKeywords("PBS generic placeholder")
    fp.Reference().SetVisible(False)
    fp.Value().SetVisible(False)
    fp.Value().SetLayer(pcbnew.F_Fab)
    fp.Reference().SetLayer(pcbnew.F_SilkS)
    w, h = b.size
    pins = b.pins

    def pad(num, x, y, sx, sy, shape=pcbnew.PAD_SHAPE_RECT, smd=True, drill=0.0, layers=None):
        pd = pcbnew.PAD(fp)
        pd.SetNumber(num)
        pd.SetShape(shape)
        pd.SetSize(V(sx, sy))
        if smd:
            pd.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
            ls = pcbnew.LSET()
            for l in (layers or [pcbnew.F_Cu, pcbnew.F_Paste, pcbnew.F_Mask]):
                ls.AddLayer(l)
            pd.SetLayerSet(ls)
        else:
            pd.SetAttribute(pcbnew.PAD_ATTRIB_PTH)
            pd.SetDrillSize(V(drill, drill))
            pd.SetLayerSet(pcbnew.PAD.PTHMask())
        pd.SetPosition(V(x, y))
        net = dict((p[0], p[2]) for p in pins).get(num)
        if net:
            pd.SetNet(nets[net])
        fp.Add(pd)
        return pd

    if b.footprint == "hole":
        pad("1", 0, 0, 6.0, 6.0, pcbnew.PAD_SHAPE_CIRCLE, smd=False, drill=3.2)
        add_shape(fp, pcbnew.F_CrtYd, (-3.25, -3.25), (3.25, 3.25), 0.05)
        add_shape(fp, pcbnew.B_CrtYd, (-3.25, -3.25), (3.25, 3.25), 0.05)
        fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_BOM | pcbnew.FP_EXCLUDE_FROM_POS_FILES)
    elif b.footprint == "connector":
        # One row of contacts along the board edge; pad length shows mating order
        # (longer = earlier): chassis 1, power 2, data 3, detect 4 (PBS-HW-SCM-01 REQ-010).
        order = {"CHASSIS": 1, "SHIELD": 1, "VIN+": 2, "VIN_RTN": 2, "DET_A": 4, "DET_B": 4}
        length = {1: 4.0, 2: 3.4, 3: 2.8, 4: 2.2}
        pitch = 2.4
        x0 = -(len(pins) - 1) * pitch / 2
        for i, (num, pname, net) in enumerate(pins):
            o = order.get(pname, 3)
            L = length[o]
            x = x0 + i * pitch
            if pname == "RF_HOST":
                pad(num, x, 1.0, 1.6, 1.6, pcbnew.PAD_SHAPE_CIRCLE)
            else:
                pad(num, x, 3.0 - L / 2, 1.4, L)
            add_text(fp, pcbnew.F_Fab, pname, x, -2.6, 0.45).SetTextAngleDegrees(90)
            add_text(fp, pcbnew.F_SilkS, str(o), x, -1.1 - L / 2 + 0.3 if L > 3 else -0.6, 0.6)
        for gx in (-22.2, 22.2):
            g = pcbnew.PAD(fp)
            g.SetAttribute(pcbnew.PAD_ATTRIB_NPTH)
            g.SetShape(pcbnew.PAD_SHAPE_CIRCLE)
            g.SetSize(V(3.0, 3.0))
            g.SetDrillSize(V(3.0, 3.0))
            g.SetLayerSet(pcbnew.PAD.UnplatedHoleMask())
            g.SetPosition(V(gx, 0))
            fp.Add(g)
        add_shape(fp, pcbnew.F_Fab, (-w / 2, -h / 2), (w / 2, h / 2), 0.1)
        add_shape(fp, pcbnew.F_SilkS, (-w / 2 - 0.2, -h / 2 - 0.2), (w / 2 + 0.2, h / 2 + 0.2), 0.15)
        add_shape(fp, pcbnew.F_CrtYd, (-w / 2 - 0.5, -h / 2 - 0.5), (w / 2 + 0.5, h / 2 + 0.5), 0.05)
        add_text(fp, pcbnew.F_SilkS, f"{b.ref}  HOST CONNECTOR - MATING ORDER 1 CHASSIS / 2 POWER / 3 DATA / 4 DETECT",
                 0, -h / 2 - 1.4, 0.9, bold=True)
    elif b.footprint == "coil":
        # Square spiral on the front copper; the coil is a net tie between COIL_A and COIL_B.
        turns, tw, gap = 4, 0.3, 0.3
        step = tw + gap
        half = 7.9
        r = [half - k * step for k in range(turns + 1)]
        pts = [(-r[0], -r[0])]
        for k in range(turns):
            pts += [(r[k], -r[k]), (r[k], r[k]), (-r[k], r[k]), (-r[k], -r[k + 1])]
        # one copper polygon: the union of the spiral's segments, so a single item joins both pads
        poly = pcbnew.SHAPE_POLY_SET()
        hw = tw / 2
        for a, c in zip(pts, pts[1:]):
            x0, x1 = sorted((a[0], c[0])); y0, y1 = sorted((a[1], c[1]))
            seg = pcbnew.SHAPE_POLY_SET()
            seg.NewOutline()
            for vx, vy in ((x0 - hw, y0 - hw), (x1 + hw, y0 - hw), (x1 + hw, y1 + hw), (x0 - hw, y1 + hw)):
                seg.Append(MM(vx), MM(vy))
            poly.BooleanAdd(seg)
        poly.Simplify()
        coil = pcbnew.PCB_SHAPE(fp)
        coil.SetShape(pcbnew.SHAPE_T_POLY)
        coil.SetPolyShape(poly)
        coil.SetFilled(True)
        coil.SetLayer(pcbnew.F_Cu)
        coil.SetWidth(0)
        fp.Add(coil)
        pad("1", pts[0][0], pts[0][1], 0.4, 0.4)
        pad("2", pts[-1][0], pts[-1][1], 0.4, 0.4)
        fp.AddNetTiePadGroup("1,2")
        add_text(fp, pcbnew.F_Fab, "L1 contactless antenna coil, 4 turns", 0, half + 1.0, 0.6)
        fp.SetAttributes(pcbnew.FP_EXCLUDE_FROM_POS_FILES)
    elif b.footprint == "tagpads":
        for i, (num, pname, net) in enumerate(pins):
            x = -4.5 + i * 3.0
            pad(num, x, 0, 2.2, 3.2)
            add_text(fp, pcbnew.F_SilkS, pname, x, 2.6, 0.7)
        add_shape(fp, pcbnew.F_Fab, (-w / 2, -h / 2), (w / 2, h / 2), 0.1)
        add_shape(fp, pcbnew.F_CrtYd, (-w / 2 - 0.3, -h / 2 - 0.3), (w / 2 + 0.3, h / 2 + 2.2), 0.05)
        add_text(fp, pcbnew.F_SilkS, "WIRED INTERFACE", 0, -2.8, 0.8, bold=True)
    else:
        back = False
        fab, silk, crt, lay = pcbnew.F_Fab, pcbnew.F_SilkS, pcbnew.F_CrtYd, None
        nl = len(b.left)
        nr = len(b.right)
        for side_pins, xs, start in ((pins[:nl], -1, 0), (pins[nl:], 1, nl)):
            n = len(side_pins)
            if not n:
                continue
            pitch = (h - 0.4) / n
            ps = max(0.25, min(0.6, pitch * 0.55, w * 0.18))
            for i, (num, pname, net) in enumerate(side_pins):
                y = -h / 2 + 0.2 + pitch * (i + 0.5)
                pad(num, xs * (w / 2 - ps / 2 - 0.15), y, ps, ps, layers=lay)
        add_shape(fp, fab, (-w / 2, -h / 2), (w / 2, h / 2), 0.1)
        add_shape(fp, silk, (-w / 2 - 0.15, -h / 2 - 0.15), (w / 2 + 0.15, h / 2 + 0.15), 0.12)
        add_shape(fp, crt, (-w / 2 - 0.4, -h / 2 - 0.4), (w / 2 + 0.4, h / 2 + 0.4), 0.05)
        text = b.kind if b.fit == "All" else f"{b.kind} [{b.fit}]"
        lines, th = wrap_label(text, w - 2.0 * (0.75 if w > 6 else 0.4), h)
        if th >= 0.7:
            # large enough to read: reference and part type on the silkscreen and the assembly layer
            for layer in (silk, fab):
                add_text(fp, layer, b.ref, 0, -h / 2 + th * 1.2 + 0.2, th * 1.15, bold=True)
                y = -h / 2 + th * 1.2 + 0.2 + th * 1.7
                for ln in lines:
                    add_text(fp, layer, ln, 0, y, th)
                    y += th * 1.55
        else:
            # small block: reference only; the part type is in the legend beside the board
            rh = max(0.5, min(1.0, w / (len(b.ref) * 0.8 + 0.6), h * 0.55))
            add_text(fp, silk, b.ref, 0, 0, rh, bold=True)
            add_text(fp, fab, b.ref, 0, 0, rh, bold=True)
    if b.height > 0:
        name = f"{b.fp_name}.wrl"
        vrml_box(os.path.join(model_dir, name), w, h, b.height, GROUP_COLOURS[b.group])
        m = pcbnew.FP_3DMODEL()
        m.m_Filename = "${KIPRJMOD}/3d/" + name
        m.m_Show = True
        fp.Models().push_back(m)
    fp.SetPosition(V(0, 0))
    return fp


def pack(blocks: list[Block], region, obstacles, gap=1.6):
    """First-fit placement scanning rows then columns at 0.5 mm steps, largest parts first."""
    x0, y0, x1, y1 = region
    placed = {}

    def hits(cx, cy, w, h):
        for ox, oy, ow, oh in obstacles + list(placed.values()):
            if abs(cx - ox) * 2 < w + ow + 2 * gap and abs(cy - oy) * 2 < h + oh + 2 * gap:
                return True
        return False

    for b in sorted(blocks, key=lambda b: -b.size[0] * b.size[1]):
        w, h = b.size
        done = False
        y = y0
        while not done and y + h <= y1 + 1e-9:
            x = x0
            while x + w <= x1 + 1e-9:
                if not hits(x + w / 2, y + h / 2, w, h):
                    placed[b.ref] = (round(x + w / 2, 2), round(y + h / 2, 2), w, h)
                    done = True
                    break
                x += 0.5
            y += 0.5
        if not done:
            raise RuntimeError(f"region full placing {b.ref} in {region}")
    return placed


def build_board(p: Project, d: str):
    board = pcbnew.CreateEmptyBoard()
    board.SetCopperLayerCount(4 if p.name == "pbs-scm-core" else 2)
    ox, oy = 50.0, 50.0
    nets = {}
    for b in p.blocks:
        for _, _, net in b.pins:
            if net not in nets:
                ni = pcbnew.NETINFO_ITEM(board, net)
                board.Add(ni)
                nets[net] = ni
    model_dir = os.path.join(d, "3d")
    os.makedirs(model_dir, exist_ok=True)
    W, H = p.board
    # outline
    if p.round_board:
        c = pcbnew.PCB_SHAPE(board)
        c.SetShape(pcbnew.SHAPE_T_CIRCLE)
        c.SetCenter(V(ox + W / 2, oy + H / 2))
        c.SetEnd(V(ox + W, oy + H / 2))
        c.SetLayer(pcbnew.Edge_Cuts)
        c.SetWidth(MM(0.1))
        board.Add(c)
    else:
        add_shape(board, pcbnew.Edge_Cuts, (ox, oy), (ox + W, oy + H), 0.1)
    # positions
    pos = {}
    fixed_obs = []
    for b in p.blocks:
        if b.fixed:
            pos[b.ref] = b.fixed
            if b.side == "F" and b.footprint != "coil":
                fixed_obs.append((b.fixed[0], b.fixed[1], b.size[0], b.size[1]))
    for rname, region in p.regions.items():
        rb = [b for b in p.blocks if b.region == rname and not b.fixed]
        placed = pack(rb, region, fixed_obs)
        for ref, (cx, cy, w, h) in placed.items():
            pos[ref] = (cx, cy)
    lib_dir = os.path.join(d, f"{LIB}.pretty")
    os.makedirs(lib_dir, exist_ok=True)
    for b in p.blocks:
        fp = make_footprint(board, b, nets, model_dir)
        pcbnew.PCB_IO_KICAD_SEXPR().FootprintSave(lib_dir, fp)
        board.Add(fp)
        if b.side == "B":
            fp.Flip(fp.GetPosition(), pcbnew.FLIP_DIRECTION_LEFT_RIGHT)
        x, y = pos[b.ref]
        fp.SetPosition(V(ox + x, oy + y))
    # drawings: radio shield-can outlines on the core board
    if p.name == "pbs-scm-core":
        clusters = {"Cellular radio (shield can)": ["U19", "U20", "J2"],
                    "S-band and navigation radio (shield can)": ["U22", "U23", "U24", "JP1", "U25", "FL2", "U26", "J4", "FL3", "J5"],
                    "Mesh and ranging radios (shield can)": ["U21", "FL1", "J3", "U27", "J6"]}
        size = {b.ref: b.size for b in p.blocks}
        for name, refs in clusters.items():
            xs = [pos[r][0] - size[r][0] / 2 for r in refs] + [pos[r][0] + size[r][0] / 2 for r in refs]
            ys = [pos[r][1] - size[r][1] / 2 for r in refs] + [pos[r][1] + size[r][1] / 2 for r in refs]
            a = (ox + min(xs) - 0.8, oy + min(ys) - 0.8)
            e = (ox + max(xs) + 0.8, oy + max(ys) + 0.8)
            add_shape(board, pcbnew.Dwgs_User, a, e, 0.15)
            add_text(board, pcbnew.Dwgs_User, name, (a[0] + e[0]) / 2, a[1] - 0.9, 0.8)
        # keep the S-band lid antenna feed clear of copper pour
        add_text(board, pcbnew.F_SilkS, "PBS-HW-SCM-01 CORE  rev 0.2  OPEN REFERENCE DESIGN", ox + 46, oy + 92 - 1.2, 1.0, bold=True)
        add_text(board, pcbnew.B_SilkS, "BACK: FILM HEATERS H1 / H2  -  PBS-HW-SCM-01", ox + 46, oy + 92 - 1.6, 1.2, bold=True, mirror=True)
    elif p.name == "pbs-scm-bay":
        add_text(board, pcbnew.F_SilkS, "PBS-HW-SCM-01 BAY INTERFACE  rev 0.2", ox + 56, oy + 16.5, 1.0, bold=True)
    elif p.name == "pbs-hwid-tag":
        add_text(board, pcbnew.F_SilkS, "hwid:", ox + 12.5, oy + 5.2, 0.8, bold=True)
        add_text(board, pcbnew.F_SilkS, "PBS-HW-ID-01", ox + 12.5, oy + 19.6, 0.7)
        add_shape(board, pcbnew.F_SilkS, (ox + 7.6, oy + 6.2), (ox + 17.4, oy + 7.4), 0.1)
        add_text(board, pcbnew.F_Fab, "Data Matrix code area (ISO/IEC 16022) and hwid text: marked on the exposed face",
                 ox + 12.5, oy + 26.2, 0.5)
        add_shape(board, pcbnew.B_SilkS, (ox + 9.5, oy + 16.2), (ox + 15.5, oy + 22.2), 0.12)
        add_text(board, pcbnew.B_SilkS, "DATA MATRIX", ox + 12.5, oy + 19.2, 0.6, mirror=True)
    # legend: reference -> part type, beside the board on the drawings layer
    lx, ly = ox + W + 6, oy + 1.5
    add_text(board, pcbnew.Dwgs_User, "PART TYPES (generic placeholders, no part numbers)", lx, ly, 1.2, bold=True).SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
    ly += 2.6
    for b in p.blocks:
        if b.footprint == "hole" and b.ref != "MH1":
            continue
        ref = "MH1-4" if b.ref == "MH1" else b.ref
        fit = "" if b.fit == "All" else f"  [{b.fit}]"
        side = "  (back)" if b.side == "B" else ""
        t = add_text(board, pcbnew.Dwgs_User, f"{ref:<6} {b.kind}{fit}{side}", lx, ly, 1.0)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_LEFT)
        ly += 1.75
    tb = board.GetTitleBlock()
    tb.SetTitle(p.title)
    tb.SetDate(DATE)
    tb.SetRevision(REV)
    tb.SetCompany(COMPANY)
    tb.SetComment(0, p.doc + " open reference design; generic placeholders, no part numbers")
    tb.SetComment(1, "Placeholders are not routed; nets show the required interconnect")
    tb.SetComment(2, "Generated by PBS-HW-LIB/kicad/tools/generate.py")
    path = os.path.join(d, f"{p.name}.kicad_pcb")
    pcbnew.SaveBoard(path, board)
    return pos


# ───────────────────────────── project files ─────────────────────────────

def write_project(p: Project, d: str):
    root_uuid = uid(p.name, "root")
    sheets = [[root_uuid, "Root"]] + ([[uid(p.name, "sheetsym", s), t] for s, t in p.sheets] if len(p.sheets) > 1 else [])
    pro = {
        "meta": {"filename": f"{p.name}.kicad_pro", "version": 1},
        "board": {"design_settings": {"rule_severities": {
            "unconnected_items": "warning",       # placeholders are not routed
            "silk_over_copper": "ignore", "silk_overlap": "ignore", "silk_edge_clearance": "ignore",
            "text_height": "ignore", "text_thickness": "ignore", "lib_footprint_mismatch": "ignore",
            "lib_footprint_issues": "ignore", "footprint_type_mismatch": "ignore", "missing_courtyard": "ignore",
            "courtyards_overlap": "error", "copper_edge_clearance": "error", "clearance": "error",
            "shorting_items": "error", "net_conflict": "error"}}},
        "erc": {"rule_severities": {"global_label_dangling": "warning", "lib_symbol_issues": "ignore",
                                    "lib_symbol_mismatch": "ignore", "footprint_link_issues": "ignore"}},
        "sheets": sheets,
        "text_variables": {},
    }
    path = os.path.join(d, f"{p.name}.kicad_pro")
    if os.path.exists(path):
        with open(path) as f:
            cur = json.load(f)
        cur.setdefault("board", {}).setdefault("design_settings", {}).setdefault("rule_severities", {}).update(
            pro["board"]["design_settings"]["rule_severities"])
        cur.setdefault("erc", {}).setdefault("rule_severities", {}).update(pro["erc"]["rule_severities"])
        cur["sheets"] = pro["sheets"]
        cur["meta"] = pro["meta"]
        pro = cur
    with open(path, "w") as f:
        json.dump(pro, f, indent=2)
    with open(os.path.join(d, "sym-lib-table"), "w") as f:
        f.write(f'(sym_lib_table\n  (version 7)\n  (lib (name "{LIB}")(type "KiCad")(uri "${{KIPRJMOD}}/{LIB}.kicad_sym")(options "")(descr "PBS generic placeholders"))\n)\n')
    with open(os.path.join(d, "fp-lib-table"), "w") as f:
        f.write(f'(fp_lib_table\n  (version 7)\n  (lib (name "{LIB}")(type "KiCad")(uri "${{KIPRJMOD}}/{LIB}.pretty")(options "")(descr "PBS generic placeholders"))\n)\n')


def generate(p: Project):
    d = os.path.join(ROOT, p.name)
    if os.path.isdir(d):
        for sub in ("3d", f"{LIB}.pretty"):
            shutil.rmtree(os.path.join(d, sub), ignore_errors=True)
    os.makedirs(d, exist_ok=True)
    write_symlib(p, d)
    write_schematics(p, d)
    build_board(p, d)          # SaveBoard writes a default project file
    write_project(p, d)        # then merge the reference-design settings into it
    print("wrote", d)


if __name__ == "__main__":
    for proj in (core_project(), bay_project(), tag_project()):
        generate(proj)
