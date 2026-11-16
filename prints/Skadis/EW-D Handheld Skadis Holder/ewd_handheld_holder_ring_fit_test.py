#!/usr/bin/env python3
"""Smallest fit test for the EW-D handheld holder: one hole in a thin ring, to check the hole size alone.

The two-hole fit test (ewd_handheld_holder_fit_test.py) already showed two mics hang side by side; this
only checks the hole size: a thin ring with the holder's chamfer, nothing else. RING_ID is the size
being tried before it goes into the holder: Ø44.5 fitted, then Ø42.5 printed and was "decent"
(2026-11-16, kept in Earlier designs/Ring fit test Ø42.5). Now Ø36.1, 15% smaller: the handle tapers
below Ø40 (the published Ø38.6-41.5 is its widest), so it should wedge on the taper rather than hang by
the head. The ring stays the same 5.75 mm wide round the hole as the Ø42.5 test.
No serial (fit tests carry none).

Run with python; writes ewd_handheld_holder_ring_fit_test.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import ewd_handheld_holder as h  # noqa: E402
import skadis  # noqa: E402
from build123d import Align, Cone, Cylinder, Pos  # noqa: E402

RING_ID = round(42.5 * 0.85, 1)     # 36.1
OD = RING_ID + 2 * 5.75
HEIGHT = 3.0                       # 1.5 mm straight bore under the holder's 1.5 mm chamfer
UP = (Align.CENTER, Align.CENTER, Align.MIN)


def build():
    part = Cylinder(OD / 2, HEIGHT, align=UP)
    part -= Pos(0, 0, -1) * Cylinder(RING_ID / 2, HEIGHT + 2, align=UP)
    part -= Pos(0, 0, HEIGHT - 1.5) * Cone(RING_ID / 2, RING_ID / 2 + 1.6, 1.6, align=UP)
    return part


if __name__ == "__main__":
    p = build()
    bb = p.bounding_box()
    print(f"ring fit test: hole Ø{RING_ID}; Ø{bb.size.X:.1f} x {bb.size.Z:.1f} mm, {p.volume / 1000:.1f} cm3, "
          f"solids {len(p.solids())}, valid {p.is_valid}")
    skadis.save(p, HERE, "ewd_handheld_holder_ring_fit_test", settings={}, center=True)
