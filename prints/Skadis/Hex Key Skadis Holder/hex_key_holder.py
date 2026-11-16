#!/usr/bin/env python3
"""Compact SKÅDIS strip for a metric L-key set, 1.5-10 mm, sizes inlaid on the front in black filament.

Each key goes long arm down through its own hole and hangs by the short arm. Holes are the key's
across-corners size plus 0.7 mm so printed holes still pass it. Imperial keys fit the next metric size
up, a little looser. The strip hangs from one hook column on a 16 mm spine at the minimum SKÅDIS height
(the Osmo 360 pattern, printed and confirmed), since a key set only weighs about 250 g. Holes are
spaced by their own size, so the small keys sit close together. To hang: lift ~6.5 mm, push both hooks
through, let it drop.

A serial number (SERIAL below) is engraved underneath, on the strip behind the small holes, reading
from below. Change it per copy before exporting ("" = off).

Two colours: body on toolhead 1, labels on toolhead 2 (load black there). The numerals' strokes are only
0.56-0.87 mm wide, so the inlay is LABEL_DEPTH deep, not the usual 0.6, to give the slicer room to fill it.

Prints upright on its strip; the 3MF carries tree supports (build plate only) for the hook tab.
Run with python; writes hex_key_holder_<SERIAL>.3mf next to this file and body and label
STLs in parts/. Slice with ARRANGE=0 and two filaments ("A;B").
"""
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Cone, Cylinder, Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-HEX-0003"           # JRJP- starts every serial; change the number per copy; "" = off

SIZES = [1.5, 2, 2.5, 3, 4, 5, 6, 8, 10]   # across flats, mm, left to right
MIN_PITCH = 9.0                    # the labels need this much
HOLE_GAP = 3.0                     # plastic between neighbouring holes, and round the outer ones
LEFT_END = 6.0                     # strip end to first hole
HOLE_X = 13.0                      # hole centres, out from the board
STRIP_T = 8.0
LABEL_CAP = 4.0
LABEL_DEPTH = 1.0                  # black inlay, into the front face
UPPER_Z = 46.5                     # minimum hook height: the lower peg sits 0.3 above the bottom
TOP = 48.3                         # spine top, 3 mm above the tongue
SPINE_W = 16.0
TAB_T = 8.0
UP = (Align.CENTER, Align.CENTER, Align.MIN)


def hole_d(af):
    return af / math.cos(math.radians(30)) + 0.7


def hole_positions():
    ys = [LEFT_END]
    for a, b in zip(SIZES, SIZES[1:]):
        ys.append(ys[-1] + max(MIN_PITCH, (hole_d(a) + hole_d(b)) / 2 + HOLE_GAP))
    return ys


HOLE_Y = hole_positions()
R_MAX = hole_d(SIZES[-1]) / 2
L = HOLE_Y[-1] + R_MAX + HOLE_GAP
DEPTH = HOLE_X + R_MAX + HOLE_GAP
HOOK_Y = [L / 2]
SERIAL_X = 4.5                     # across the strip; capitals run 1.5-7.5


def serial_cut(serial):
    span = skadis.serial_under(serial, SERIAL_X, 0.0, x_dir=(0, 1, 0)).bounding_box().size.Y
    return skadis.serial_under(serial, SERIAL_X, 2.5 + span / 2, x_dir=(0, 1, 0))


def label_cut():
    """The size numerals, standing a little proud of the front face so they cut it cleanly."""
    cut = None
    for af, y in zip(SIZES, HOLE_Y):
        c = skadis.text_cut(f"{af:g}", (DEPTH, y, STRIP_T / 2), (0, 1, 0), (1, 0, 0), cap=LABEL_CAP,
                            depth=LABEL_DEPTH, font=skadis.LABEL_FONT)
        cut = c if cut is None else cut + c
    return cut


def labels():
    """The black inlay: the numerals trimmed flush with the front face."""
    return label_cut() & (Pos(DEPTH - LABEL_DEPTH / 2, L / 2, STRIP_T / 2) * Box(LABEL_DEPTH, L, STRIP_T))


def build(serial=SERIAL):
    """The body, with recesses for the labels."""
    part = Pos(DEPTH / 2, L / 2, 0) * extrude(RectangleRounded(DEPTH, L, 4), STRIP_T)
    for af, y in zip(SIZES, HOLE_Y):
        d = hole_d(af)
        part -= Pos(HOLE_X, y, -1) * Cylinder(d / 2, STRIP_T + 2, align=UP)
        part -= Pos(HOLE_X, y, STRIP_T - 0.8) * Cone(d / 2, d / 2 + 0.9, 0.9, align=UP)     # lead-in
    part -= label_cut()
    y0 = L / 2 - SPINE_W / 2
    part += Pos(0, y0, 0) * skadis.back_plate(SPINE_W, TOP)
    part += skadis.profile_solid([(3.5, STRIP_T - 0.5), (7, STRIP_T - 0.5), (3.5, STRIP_T + 3)], SPINE_W, y0)   # root fillet
    part += skadis.hooks(L / 2, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        part -= serial_cut(serial)
    return part


def ghost():
    """Nine keys hanging in place, for previews and the fit check (round bars at the across-flats size)."""
    g = None
    for af, y in zip(SIZES, HOLE_Y):
        long_arm = 30 + 10 * af
        k = Pos(HOLE_X, y, STRIP_T - long_arm) * Cylinder(af / 2, long_arm + af, align=UP) + \
            Pos(HOLE_X + 8 + 2 * af, y, STRIP_T + af / 2 + 0.1) * Box(16 + 4 * af, af, af)
        g = k if g is None else g + k
    return g


if __name__ == "__main__":
    p = build()
    moment = 0.25 * 9.81 * HOLE_X + 50 * DEPTH                 # 250 g of keys + 50 N lean on the front
    skadis.report("Hex key strip", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the keys {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm, {TOP:.1f} tall; serial {SERIAL or 'none'}")
    print("  holes (y:dia): " + ", ".join(f"{a:g} at {y:.1f}:{hole_d(a):.1f}" for a, y in zip(SIZES, HOLE_Y)))
    widths = [skadis.text_cut(f"{a:g}", (DEPTH, y, 4), (0, 1, 0), (1, 0, 0), cap=LABEL_CAP,
                              font=skadis.LABEL_FONT).bounding_box().size.Y for a, y in zip(SIZES, HOLE_Y)]
    gaps = [b - a - (wa + wb) / 2 for a, b, wa, wb in zip(HOLE_Y, HOLE_Y[1:], widths, widths[1:])]
    print(f"  labels: narrowest gap between neighbours {min(gaps):.1f} mm")
    if SERIAL:
        bb = serial_cut(SERIAL).bounding_box()
        clear = min(HOLE_X - hole_d(a) / 2 - bb.max.X for a, y in zip(SIZES, HOLE_Y) if y - hole_d(a) / 2 < bb.max.Y)
        print(f"  serial: y {bb.min.Y:.1f}-{bb.max.Y:.1f}, x {bb.min.X:.1f}-{bb.max.X:.1f}, {clear:.1f} mm clear of the holes")
    ink = labels()
    bb = ink.bounding_box()
    print(f"  black inlay: {ink.volume:.1f} mm3, {len(ink.solids())} solids, overlap with the body "
          f"{(ink & p).volume:.3f} mm3, front face at x {bb.max.X:.2f} (strip front {DEPTH:.2f})")
    skadis.save_inlaid(p, ink, HERE, skadis.with_serial("hex_key_holder", SERIAL))
