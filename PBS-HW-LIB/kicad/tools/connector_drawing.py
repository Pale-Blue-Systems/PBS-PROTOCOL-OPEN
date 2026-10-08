#!/usr/bin/env python3
"""
Dimensioned drawing of the PBS host connector (PBS-HW-CON-01), from tools/connector.py.

  python3 PBS-HW-LIB/kicad/tools/connector_drawing.py

Writes PBS-HW-LIB/drawings/PBS-HW-CON-01-sheet1.{pdf,png} (contact faces) and
-sheet2.{pdf,png} (mating heights and sequence).
"""
from __future__ import annotations

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

import connector as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.dirname(HERE)), "drawings")
ORDER_COL = {1: "#2e7d32", 2: "#c62828", 3: "#1565c0", 4: "#6a1b9a"}
DIM = "#444444"
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 7})


def dim(ax, p0, p1, text, off=(0, 0), tpos=0.5, rot=None, fs=6.5):
    (x0, y0), (x1, y1) = p0, p1
    ox, oy = off
    a, b = (x0 + ox, y0 + oy), (x1 + ox, y1 + oy)
    ax.annotate("", a, b, arrowprops=dict(arrowstyle="<|-|>", color=DIM, lw=0.6, shrinkA=0, shrinkB=0, mutation_scale=6))
    for (px, py), (qx, qy) in ((p0, a), (p1, b)):
        if (ox, oy) != (0, 0):
            ax.plot([px, qx + 0.6 * (1 if ox > 0 else -1 if ox < 0 else 0)], [py, qy + 0.6 * (1 if oy > 0 else -1 if oy < 0 else 0)],
                    color=DIM, lw=0.35)
    tx, ty = a[0] + (b[0] - a[0]) * tpos, a[1] + (b[1] - a[1]) * tpos
    if rot is None:
        rot = 90 if abs(x1 - x0) < 1e-6 else 0
    ax.text(tx, ty, text, ha="center", va="center", rotation=rot, fontsize=fs, color=DIM,
            bbox=dict(fc="white", ec="none", pad=0.6))


def face(ax, module: bool):
    s = -1 if module else 1                     # module face is seen from outside the module: x mirrored
    fx0, fy0, fx1, fy1 = C.FACE
    ax.add_patch(Rectangle((fx0, fy0), fx1 - fx0, fy1 - fy0, fill=False, ls=(0, (4, 2)), lw=0.6, ec="#777"))
    px0, py0, px1, py1 = C.PLATE
    if module:
        ax.add_patch(Rectangle((s * px1, py0), px1 - px0, py1 - py0, fill=False, ls=(0, (1, 1.5)), lw=0.5, ec="#777"))
        ax.text(s * px0 - 0.5, py1 - 0.9, "bay cover-plate footprint", fontsize=5, color="#777", ha="right")
    else:
        ax.add_patch(Rectangle((px0, py0), px1 - px0, py1 - py0, fc="#f3f1e6", ec="#555", lw=0.8))
        ax.text(px0 + 0.5, py1 - 0.9, "cover plate (moves along z)", fontsize=5, color="#555")
    for name, g in C.GUIDE.items():
        x = s * g["x"]
        if module:
            ax.add_patch(Circle((x, 0), C.BUSHING_ENTRY_DIA / 2, fill=False, lw=0.6, ec="#555"))
            ax.add_patch(Circle((x, 0), g["bore"] / 2, fc="#ddd", ec="#222", lw=0.8))
            ax.text(x, -C.BUSHING_ENTRY_DIA / 2 - 1.6, f"BUSHING {name}\nbore Ø{g['bore']:.2f} +0.03/0\nentry cone 90°, Ø{C.BUSHING_ENTRY_DIA:.1f}",
                    ha="center", va="top", fontsize=5.5)
        else:
            ax.add_patch(Circle((x, 0), g["pin"] / 2, fc="#9ea2a6", ec="#222", lw=0.8))
            ax.add_patch(Circle((x, 0), C.GUIDE_TIP_DIA / 2, fc="#ccc", ec="#222", lw=0.4))
            ax.text(x, -g["pin"] / 2 - 1.6, f"GUIDE PIN {name}\nØ{g['pin']:.2f} 0/−0.02", ha="center", va="top", fontsize=5.5)
    for c in C.CONTACTS:
        x, y = s * c.x, c.y
        col = ORDER_COL[c.order]
        if c.cls == C.RF:
            ax.add_patch(Circle((x, y), C.RF_KEEPOUT_DIA / 2, fill=False, ls=(0, (3, 2)), lw=0.5, ec="#555"))
            ax.add_patch(Circle((x, y), (C.APERTURE_DIA[C.RF] if module else 4.5) / 2, fc="#e5e5e5", ec=col, lw=1.0))
            ax.add_patch(Circle((x, y), 0.45, fc=col, ec="none"))
            ax.text(x, y - 3.0, "17 RF_HOST\n" + ("SMP jack (female)" if module else "SMP plug, smooth bore,\nspring-loaded"),
                    ha="center", va="top", fontsize=5)
            continue
        if module:
            ax.add_patch(Circle((x, y), C.PAD_DIA[c.cls] / 2, fc="#e8c547", ec=col, lw=1.0))
            ax.add_patch(Circle((x, y), C.APERTURE_DIA[c.cls] / 2, fill=False, ec="#333", lw=0.4, ls=(0, (1, 1))))
        else:
            r = C.TIP_DIA[c.cls] / 2
            ax.add_patch(Circle((x, y), r + 0.25, fc="white", ec="#777", lw=0.4))
            ax.add_patch(Circle((x, y), r, fc=col, ec="#222", lw=0.4))
        ax.text(x, y + (2.55 if c.cls == C.POWER else 1.15), f"{c.no}", ha="center", va="bottom", fontsize=6, fontweight="bold")
        ax.text(x, y - (2.35 if c.cls == C.POWER else 1.05), c.name, ha="center", va="top", fontsize=3.9, color=col)
    # origin and axes
    ax.plot([-1.2, 1.2], [0, 0], color="k", lw=0.4)
    ax.plot([0, 0], [-1.2, 1.2], color="k", lw=0.4)
    ax.text(0.5, 0.45, "O", fontsize=6)
    ax.annotate("", (fx0 + 6 * (1 if not module else 1), fy1 + 3.2), (fx0, fy1 + 3.2),
                arrowprops=dict(arrowstyle="-|>", lw=0.7, color="k"))
    ax.text(fx0 + 6.4, fy1 + 3.2, "+x" if not module else "−x", va="center", fontsize=6)
    ax.annotate("", (fx0, fy1 + 9.2), (fx0, fy1 + 3.2), arrowprops=dict(arrowstyle="-|>", lw=0.7, color="k"))
    ax.text(fx0 + 0.6, fy1 + 8.6, "+y  FRONT", fontsize=6)
    # dimensions
    dim(ax, (s * C.GUIDE["A"]["x"], 0), (s * C.GUIDE["B"]["x"], 0), f"{2 * C.GUIDE_X:.2f} ±0.03", off=(0, -13.5))
    dim(ax, (0, 0), (s * C.GUIDE["B"]["x"], 0), f"{C.GUIDE_X:.2f}", off=(0, -10.5))
    p1, p2 = C.by_name("CHASSIS"), C.by_name("VIN_RTN")
    dim(ax, (s * p1.x, p1.y), (s * p2.x, p2.y), "6.00 TYP", off=(0, 4.2))
    q1, q2 = C.by_name("T1_P"), C.by_name("T1_N")
    dim(ax, (s * q1.x, q1.y), (s * q2.x, q2.y), "3.00 TYP", off=(0, -6.3), fs=5.5)
    for yv, lab in ((4.0, "4.00"), (-0.5, "0.50"), (-3.5, "3.50")):
        xe = s * (fx1 if not module else fx0) if False else (fx1 + 1.5)
        dim(ax, (fx1 + 1.5, 0), (fx1 + 1.5, yv), lab, off=(0 + (yv != 4.0) * (1.8 if yv == -0.5 else 3.6), 0), fs=5.5)
    rf = C.by_name("RF_HOST")
    ax.text(s * rf.x, rf.y + 5.0, f"RF at ({rf.x:+.1f}, {rf.y:+.1f})", ha="center", fontsize=5)
    d16 = C.by_name("DET_B")
    ax.text(s * d16.x, d16.y + 2.6, f"({d16.x:+.1f}, {d16.y:+.1f})", ha="center", fontsize=4.6)
    ax.set_xlim(fx0 - 4, fx1 + 9)
    ax.set_ylim(fy0 - 13, fy1 + 11)
    ax.set_aspect("equal")
    ax.axis("off")


def sheet1():
    fig = plt.figure(figsize=(16.54, 11.69))   # A3 landscape
    fig.text(0.04, 0.955, "PBS-HW-CON-01  Module host connector  -  Sheet 1 of 2: contact faces", fontsize=14, fontweight="bold")
    fig.text(0.04, 0.93, "Dimensions in mm. Positions are true position ±0.05 relative to datum A (guide-pin A axis) and datum B "
             "(line A→B), in the frame of Section 4. Open reference design, Pale Blue Systems Foundation, v0.3, 2026-10-08.", fontsize=8)
    ax1 = fig.add_axes([0.02, 0.47, 0.6, 0.43])
    ax1.set_title("BAY HALF - viewed from the module side (looking −z into the bay)", fontsize=9, loc="left")
    face(ax1, False)
    ax2 = fig.add_axes([0.02, 0.03, 0.6, 0.43])
    ax2.set_title("MODULE HALF - viewed from outside the module (looking +z at its connector face); x appears mirrored",
                  fontsize=9, loc="left")
    face(ax2, True)
    # contact table
    ax3 = fig.add_axes([0.64, 0.05, 0.34, 0.86])
    ax3.axis("off")
    rows = [["No.", "Name", "Group", "Order", "x", "y", "Class"]]
    for c in C.CONTACTS:
        rows.append([str(c.no), c.name, c.group, str(c.order), f"{c.x:+.1f}", f"{c.y:+.1f}", c.cls])
    t = ax3.table(cellText=rows, loc="upper left", cellLoc="center", colWidths=[0.07, 0.17, 0.2, 0.1, 0.1, 0.1, 0.12])
    t.auto_set_font_size(False)
    t.set_fontsize(7)
    t.scale(1, 1.35)
    for (r, cidx), cell in t.get_celld().items():
        cell.set_linewidth(0.4)
        if r == 0:
            cell.set_text_props(fontweight="bold")
        elif cidx == 3:
            cell.set_facecolor(ORDER_COL[int(rows[r][3])]); cell.set_text_props(color="white", fontweight="bold")
    lines = [
        "CONTACT CLASSES",
        f"  power:  module pad Ø{C.PAD_DIA[C.POWER]:.2f} flat; bay tip Ø{C.TIP_DIA[C.POWER]:.2f} domed; ≥{C.RATED_A[C.POWER]:.0f} A",
        f"  signal: module pad Ø{C.PAD_DIA[C.SIGNAL]:.2f} flat; bay tip Ø{C.TIP_DIA[C.SIGNAL]:.2f} domed; ≥{C.RATED_A[C.SIGNAL]:.0f} A",
        "  rf:     SMP interface (MIL-STD-348), 50 Ω; SCM-S: aperture only",
        f"  module-face apertures: power Ø{C.APERTURE_DIA[C.POWER]:.2f}, signal Ø{C.APERTURE_DIA[C.SIGNAL]:.2f}, rf Ø{C.APERTURE_DIA[C.RF]:.2f} (min)",
        "",
        "MATING ORDER (colour)",
        "  1 chassis  2 power  3 data, identity bus, RF  4 detect",
        "  Set by bay spring-contact free height; see Sheet 2.",
        "",
        "KEYING",
        "  Guide pin A Ø4.00 and B Ø3.00: a module turned 180° cannot",
        "  enter. DET_A and DET_B sit at opposite corners so a tilted",
        "  module cannot close the detect loop.",
        "",
        "KEEP-OUTS",
        "  Dashed outline: connector face, x −29…+29, y −8…+10.",
        "  Module: nothing protrudes beyond the face in this area.",
        "  Bay: nothing above P except the cover plate and guide pins.",
    ]
    fig.text(0.645, 0.43, "\n".join(lines), fontsize=7.5, va="top", family="DejaVu Sans Mono")
    return fig


def sheet2():
    fig = plt.figure(figsize=(16.54, 11.69))
    fig.text(0.04, 0.955, "PBS-HW-CON-01  Module host connector  -  Sheet 2 of 2: mating heights and sequence", fontsize=14, fontweight="bold")
    fig.text(0.04, 0.93, "Heights along z from the mating plane P (z = 0, where the module face rests when seated). "
             "Positive z points out of the bay towards the module. Dimensions in mm; heights ±0.05 unless stated.", fontsize=8)
    ax = fig.add_axes([0.02, 0.42, 0.96, 0.5])
    ax.axhline(0, color="k", lw=1.0)
    ax.text(-1.5, 0.15, "P  (mating plane, z = 0)", fontsize=7, ha="right", va="bottom")
    # guide pin
    gx = 0
    g = C.GUIDE["A"]
    r = g["pin"] / 2
    L, N = C.GUIDE_LENGTH, C.GUIDE_NOSE
    ax.add_patch(Polygon([(gx - r, -3), (gx - r, L - N), (gx - C.GUIDE_TIP_DIA / 2, L), (gx + C.GUIDE_TIP_DIA / 2, L), (gx + r, L - N), (gx + r, -3)],
                         fc="#9ea2a6", ec="#222", lw=0.6))
    ax.text(gx, -4.0, "guide pin", ha="center", va="top", fontsize=7)
    dim(ax, (gx + 3, 0), (gx + 3, L), f"{L:.1f}", fs=6.5)
    dim(ax, (gx - 3.2, L - N), (gx - 3.2, L), f"nose {N:.1f}", fs=5.5)
    # spring contacts
    xs = {1: 9, 2: 17, 3: 25, 4: 33}
    for o, x in xs.items():
        h = C.FREE_HEIGHT[o]
        w = 1.4 if o <= 2 else 0.8
        ax.add_patch(Rectangle((x - w * 0.9, -3), w * 1.8, 3 + h - 1.2, fc="#bbb", ec="#333", lw=0.5))
        ax.add_patch(Rectangle((x - w / 2, h - 1.4), w, 1.2, fc=ORDER_COL[o], ec="#222", lw=0.5))
        ax.add_patch(Circle((x, h - 0.2), w / 2, fc=ORDER_COL[o], ec="#222", lw=0.5))
        ax.text(x, -4.0, f"order {o}\n" + C.ORDER_NAMES[o].replace(", RF", ",\nRF"), ha="center", va="top", fontsize=6.5, color=ORDER_COL[o])
        dim(ax, (x + 2.1, 0), (x + 2.1, h), f"{h:.2f}", fs=6)
    # cover plate
    ax.add_patch(Rectangle((6.0, C.PLATE_FREE - C.PLATE_THICK), 30.0, C.PLATE_THICK, fc="#f3f1e6", ec="#555", lw=0.6, alpha=0.6))
    ax.text(21.0, C.PLATE_FREE + 0.3, f"bay cover plate, unmated: front face at +{C.PLATE_FREE:.1f}, travel {C.PLATE_FREE:.1f}, "
            f"≤{C.PLATE_FORCE_MAX:.0f} N at seat", ha="center", fontsize=6.5)
    # module-side reference planes (module seated), with staggered labels
    X0, X1, TX = 42, 54, 56
    planes = [(0.0, "#1565c0", "-", 2.0, "module face (datum M) = P when seated", -0.8),
              (C.PAD_RECESS, "#e8c547", "-", 3.0, f"module pad surface, {C.PAD_RECESS:.2f} behind the module face", 0.0),
              (C.RF_MODULE_REF, "#888", "--", 0.8, f"module SMP jack reference plane, {C.RF_MODULE_REF:.2f} behind the face", 0.6),
              (C.RF_BAY_REF_FREE, "#888", ":", 0.8, f"bay SMP plug reference plane, unmated, +{C.RF_BAY_REF_FREE:.2f} "
               f"(float ≥{C.RF_BAY_FLOAT_AXIAL:.1f} axial, ±{C.RF_BAY_FLOAT_RADIAL:.2f} radial)", 1.5),
              (C.BUSHING_DEPTH, "#888", "-", 0.8, f"module bushing bore depth ≥{C.BUSHING_DEPTH:.1f} from the module face", 0.0)]
    for z, col, ls, lw, text, dy in planes:
        ax.plot([X0, X1], [z, z], color=col, lw=lw, ls=ls)
        ax.plot([X1, TX - 0.3], [z, z + dy], color="#aaa", lw=0.4)
        ax.text(TX, z + dy, text, fontsize=7, va="center", color="#333")
    dim(ax, (X0 + 2, 0), (X0 + 2, C.PAD_RECESS), f"{C.PAD_RECESS:.2f}", fs=6)
    ax.text((X0 + X1) / 2, -2.0, "module side (seated)", ha="center", fontsize=7)
    ax.set_xlim(-16, 100)
    ax.set_ylim(-8, 19)
    ax.set_aspect("equal")
    ax.axis("off")
    # sequence table
    ax2 = fig.add_axes([0.04, 0.05, 0.5, 0.33])
    ax2.axis("off")
    rows = [["Event on insertion", "Module face above P", "Compression at seat"],
            ["Guide pins enter bushings", f"{C.GUIDE_LENGTH:.1f}", "-"],
            ["Module face meets cover plate", f"{C.PLATE_FREE:.1f}", "-"]]
    for o in (1, 2, 3, 4):
        rows.append([f"Order {o} makes ({C.ORDER_NAMES[o].lower()})", f"{C.MAKE_AT[o]:.1f}", f"{C.COMPRESSION[o]:.1f}"])
    rows.append(["Seated (latch holds face ≤0.2 above P)", "0.0", "-"])
    t = ax2.table(cellText=rows, loc="upper left", cellLoc="center", colWidths=[0.52, 0.24, 0.24])
    t.auto_set_font_size(False)
    t.set_fontsize(7.5)
    t.scale(1, 1.6)
    for (r, cidx), cell in t.get_celld().items():
        cell.set_linewidth(0.4)
        if r == 0:
            cell.set_text_props(fontweight="bold")
        if 3 <= r <= 6 and cidx == 0:
            cell.set_text_props(color=ORDER_COL[r - 2], fontweight="bold")
    notes = [
        "Removal breaks in reverse order: detect first, chassis last.",
        f"Groups are {C.FREE_HEIGHT[1] - C.FREE_HEIGHT[2]:.1f} apart: at the maximum insertion",
        "speed of 100 mm/s each group leads the next by ≥6 ms.",
        f"Bay spring contacts: working stroke ≥{C.MIN_STROKE:.1f}.",
        "",
        "Contact force at seat: power 1.5-3.0 N, signal 0.5-1.2 N.",
        "Insertion force ≤60 N; separating force at seat ≤60 N.",
        "",
        "Module SMP jack is fixed; bay SMP plug floats ±0.25 radial",
        f"and ≥{C.RF_BAY_FLOAT_AXIAL:.1f} axial, compressed 0.5 ±0.3 at seat.",
    ]
    fig.text(0.58, 0.37, "\n".join(notes), fontsize=8, va="top", family="DejaVu Sans Mono")
    return fig


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for n, f in ((1, sheet1()), (2, sheet2())):
        base = os.path.join(OUT, f"PBS-HW-CON-01-sheet{n}")
        f.savefig(base + ".pdf")
        f.savefig(base + ".png", dpi=110)
        print("wrote", base + ".pdf/.png")
