#!/usr/bin/env python3
"""Fit test for the PB205 + CM498 cup: just the two pockets as a low ring, no hooks, no serial.

Sizes come from cm498_holder.py, so it always matches the current pockets. Stand the power bank in
the back pocket and the hub in the front one, on their long edges, and check the play.

Run with python; writes cm498_holder_fit_test.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import cm498_holder as h  # noqa: E402
import skadis  # noqa: E402
from build123d import Pos, RectangleRounded, extrude  # noqa: E402

HEIGHT = h.FLOOR_T + 8.0


def build():
    ring = Pos(h.BX, h.YC, 0) * extrude(RectangleRounded(h.BD + 2 * h.WALL, h.W_OUT, h.RADIUS + h.WALL), HEIGHT)
    ring += Pos(h.HX, h.YC, 0) * extrude(RectangleRounded(h.HD + 2 * h.WALL, h.HW + 2 * h.WALL,
                                                          h.RADIUS + h.WALL), HEIGHT)
    ring -= h.pocket_cut(h.BX, h.BD, h.BW, h.LEDGE_SIDE, h.LEDGE_SIDE)
    ring -= h.pocket_cut(h.HX, h.HD, h.HW, h.LEDGE_SIDE, h.LEDGE_FRONT)
    ring -= h.cable_slots()
    return ring


if __name__ == "__main__":
    p = build()
    bb = p.bounding_box()
    print(f"fit test: outside {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}, "
          f"{p.volume / 1000:.1f} cm3, solids {len(p.solids())}, valid {p.is_valid}")
    skadis.save(p, HERE, "cm498_holder_fit_test", settings={})
