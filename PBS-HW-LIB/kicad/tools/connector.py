"""
Geometry of the PBS host connector (PBS-HW-CON-01): the single source for the KiCad
footprints, the 3D models and the dimensioned drawing.

Frame (PBS-HW-CON-01 Section 4): origin O on the mating plane P, midway between the
guide-pin axes; z along the insertion axis, positive out of the bay towards the module;
x along the guide-pin line, positive towards guide pin B; y = z x x, positive towards
the front of the module and bay. All values in millimetres.
"""
from __future__ import annotations

from dataclasses import dataclass

# ── contact classes ──
POWER = "power"
SIGNAL = "signal"
RF = "rf"

PAD_DIA = {POWER: 4.00, SIGNAL: 1.80}          # module contact pad, flat
TIP_DIA = {POWER: 2.00, SIGNAL: 0.90}          # bay spring-contact plunger tip, domed
APERTURE_DIA = {POWER: 3.00, SIGNAL: 1.40, RF: 6.00}   # clear opening in the module face
RATED_A = {POWER: 5.0, SIGNAL: 1.0}

# ── mating order: free tip height of the bay spring contact above P ──
FREE_HEIGHT = {1: 4.50, 2: 3.90, 3: 3.30, 4: 2.70}
PAD_RECESS = 1.50                              # module pad surface behind the module face
MAKE_AT = {o: round(h - PAD_RECESS, 2) for o, h in FREE_HEIGHT.items()}   # module-face distance at make
COMPRESSION = MAKE_AT                          # compression when seated (face on P)
MIN_STROKE = 3.50


@dataclass(frozen=True)
class Contact:
    no: int
    name: str
    group: str
    order: int
    x: float
    y: float
    cls: str
    note: str


CONTACTS = [
    Contact(1, "CHASSIS", "Chassis", 1, -15.0, 4.0, POWER, "Chassis ground"),
    Contact(2, "VIN_RTN", "Power", 2, -9.0, 4.0, POWER, "Supply return"),
    Contact(3, "VIN+", "Power", 2, -3.0, 4.0, POWER, "Supply positive, 18-36 V"),
    Contact(4, "SHIELD", "Chassis", 1, 3.0, 4.0, POWER, "Host cable shield"),
    Contact(5, "T1_P", "Data", 3, -15.0, -0.5, SIGNAL, "100BASE-T1 +"),
    Contact(6, "T1_N", "Data", 3, -12.0, -0.5, SIGNAL, "100BASE-T1 -"),
    Contact(7, "ID_3V3", "Identity bus", 3, -9.0, -0.5, SIGNAL, "Tag supply, from module"),
    Contact(8, "ID_SCL", "Identity bus", 3, -6.0, -0.5, SIGNAL, "Tag clock"),
    Contact(9, "ID_SDA", "Identity bus", 3, -3.0, -0.5, SIGNAL, "Tag data"),
    Contact(10, "ID_GND", "Identity bus", 3, 0.0, -0.5, SIGNAL, "Tag ground"),
    Contact(11, "DET_A", "Detect", 4, -15.0, -3.5, SIGNAL, "Swap detect, module drives"),
    Contact(12, "TX+", "Fallback", 3, -12.0, -3.5, SIGNAL, "RS-422 module transmit +"),
    Contact(13, "TX-", "Fallback", 3, -9.0, -3.5, SIGNAL, "RS-422 module transmit -"),
    Contact(14, "RX+", "Fallback", 3, -6.0, -3.5, SIGNAL, "RS-422 module receive +"),
    Contact(15, "RX-", "Fallback", 3, -3.0, -3.5, SIGNAL, "RS-422 module receive -"),
    Contact(16, "DET_B", "Detect", 4, 15.5, 4.0, SIGNAL, "Swap detect, module senses"),
    Contact(17, "RF_HOST", "RF", 3, 10.0, -1.0, RF, "50 ohm coaxial, SCM-L only"),
]

# ── guide pins (bay) and bushings (module) ──
GUIDE_X = 23.0                                 # A at -23, B at +23
GUIDE = {"A": {"x": -GUIDE_X, "pin": 4.00, "bore": 4.10},
         "B": {"x": +GUIDE_X, "pin": 3.00, "bore": 3.10}}
GUIDE_LENGTH = 16.0                            # pin tip above P
GUIDE_NOSE = 4.0                               # length of the bullet nose
GUIDE_TIP_DIA = 1.5
BUSHING_ENTRY_DIA = 10.0                       # 90-degree entry cone at the module face
BUSHING_DEPTH = 18.0
BUSHING_OD = 8.0                               # reference design only

# ── bay cover plate (moves along z; pushed by the module face) ──
PLATE = (-19.0, -6.0, 19.0, 8.0)               # x0, y0, x1, y1
PLATE_FREE = 6.0                               # front face above P when unmated
PLATE_THICK = 4.0
PLATE_FORCE_MAX = 20.0                         # N, at seat

# ── module connector face: flat, nothing below the face (module) / above P (bay, except plate and pins) ──
FACE = (-29.0, -8.0, 29.0, 10.0)

# ── RF contact ──
RF_KEEPOUT_DIA = 8.0
RF_MODULE_REF = 2.50                           # module SMP jack reference plane behind the face
RF_BAY_REF_FREE = 3.00                         # bay SMP plug reference plane above P, unmated
RF_BAY_FLOAT_AXIAL = 1.0
RF_BAY_FLOAT_RADIAL = 0.25

# ── bay reference build: height of P above the bay board ──
BAY_P_ABOVE_BOARD = 8.0

ORDER_NAMES = {1: "Chassis", 2: "Power", 3: "Data, identity bus, RF", 4: "Detect"}


def by_name(name: str) -> Contact:
    return next(c for c in CONTACTS if c.name == name)


if __name__ == "__main__":
    for c in CONTACTS:
        print(f"{c.no:>2} {c.name:<8} {c.group:<13} order {c.order}  ({c.x:+6.1f}, {c.y:+5.1f})  {c.cls}")
    print("make at module-face distance:", MAKE_AT)
