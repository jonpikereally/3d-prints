#!/usr/bin/env python3
"""Fit test for the EW-D handheld holder: two neighbouring holes, to check two mics hang side by side.

A slice of the holder through MIC 1 and MIC 2: the same floor plate, collars, chamfers, hole size and
6 mm head gap, with the back wall and front lip at full height so the heads' clearance to both shows
too. No hooks, no labels, no serial (fit tests carry none). Sizes come from ewd_handheld_holder.py, so
it always matches the current design, except RING_ID below, which is being tried here before it goes
into the holder (Ø44.5 fitted, 2026-11-16; now Ø42.5 for less wobble). Hold it level (or lay it across two books) and drop both mics in.

Run with python; writes ewd_handheld_holder_fit_test.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import ewd_handheld_holder as h  # noqa: E402
import skadis  # noqa: E402
from build123d import Align, Box, Cone, Cylinder, Pos  # noqa: E402

RINGS = h.RING_Y[:2]
RING_ID = 42.5      # trying a tighter hole than the holder's Ø44.5: still passes the thickest handle (Ø41.5)
L = RINGS[-1] + h.HEAD_D / 2 + 4          # same 4 mm end margin as the holder


def build():
    part = Pos(h.B / 2, L / 2, h.RAIL_H / 2) * Box(h.B, L, h.RAIL_H)                      # back wall stub
    part += Pos(h.DEPTH / 2, L / 2, h.PLATE_T / 2) * Box(h.DEPTH, L, h.PLATE_T)           # floor plate
    part += skadis.profile_solid([(h.DEPTH - h.LIP_T, 0), (h.DEPTH, 0), (h.DEPTH, h.PLATE_T + h.LIP_H - 1),
                                  (h.DEPTH - 1, h.PLATE_T + h.LIP_H), (h.DEPTH - h.LIP_T, h.PLATE_T + h.LIP_H)], L)
    for y in RINGS:
        part += Pos(h.RING_X, y, h.PLATE_T) * Cylinder(h.COLLAR_OD / 2, h.COLLAR_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos(h.RING_X, y, -1) * Cylinder(RING_ID / 2, h.PLATE_T + h.COLLAR_H + 2,
                                                align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos(h.RING_X, y, h.PLATE_T + h.COLLAR_H - 1.5) * Cone(RING_ID / 2, RING_ID / 2 + 1.6, 1.6,
                                                                     align=(Align.CENTER, Align.CENTER, Align.MIN))
    return part


if __name__ == "__main__":
    p = build()
    bb = p.bounding_box()
    ghost = h.ghost()
    print(f"fit test: holes Ø{RING_ID} at {RINGS[1] - RINGS[0]:.1f} mm centres ({h.HEAD_GAP} mm between heads); "
          f"{bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}, {p.volume / 1000:.1f} cm3, "
          f"solids {len(p.solids())}, valid {p.is_valid}, overlap with mics {(ghost & p).volume:.3f} mm3")
    skadis.save(p, HERE, "ewd_handheld_holder_fit_test", settings={}, center=True)
