#!/usr/bin/env python3
"""Fit test for the Osmo 360 holder: just the cup's pocket as a low ring, no hooks, no back block.

Sizes come from osmo360_holder.py, so it always matches the current pocket. Same floor ledge, corner
radius, walls and clearance as the real cup, and as tall as its front wall (FLOOR_T + FRONT_H). Stand
the camera in it from the top, as in the holder. Fit tests carry no serial.

Run with python; writes osmo360_holder_fit_test.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import osmo360_holder as h  # noqa: E402
import skadis  # noqa: E402
from build123d import Pos, RectangleRounded, extrude  # noqa: E402

HEIGHT = h.FLOOR_T + h.FRONT_H


def build():
    ring = extrude(RectangleRounded(h.D_IN + 2 * h.WALL, h.W_OUT, h.RADIUS + h.WALL), HEIGHT)
    ring -= Pos(0, 0, h.FLOOR_T) * extrude(RectangleRounded(h.D_IN, h.W_IN, h.RADIUS), HEIGHT)
    ring -= Pos(0, 0, -1) * extrude(RectangleRounded(h.D_IN - 2 * h.LEDGE, h.W_IN - 2 * h.LEDGE,
                                                     h.RADIUS - h.LEDGE / 2), h.FLOOR_T + 2)
    return ring


if __name__ == "__main__":
    p = build()
    bb = p.bounding_box()
    print(f"fit test: pocket {h.D_IN:.1f} x {h.W_IN:.1f}; outside {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}, "
          f"{p.volume / 1000:.1f} cm3, solids {len(p.solids())}, valid {p.is_valid}")
    skadis.save(p, HERE, "osmo360_holder_fit_test", settings={})
