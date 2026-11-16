#!/usr/bin/env python3
"""Fit test for the Treedix tester storage cup: just the cup's pocket as a low ring, no hooks.

Sizes come from treedix_holder.py, so it always matches the current pocket. Same floor ledges, corners,
walls and clearance as the real cup, only HEIGHT tall. Stand the tester in it on its five-socket edge:
it should drop in with a little play and lift out easily. Fit tests carry no serial.

Run with python; writes treedix_holder_fit_test.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(HERE))
import treedix_holder as h  # noqa: E402
import skadis  # noqa: E402
from build123d import Pos, RectangleRounded, extrude  # noqa: E402

HEIGHT = h.FLOOR_T + 9.0


def build():
    ring = extrude(RectangleRounded(h.D_IN + 2 * h.WALL, h.W_OUT, h.RADIUS + h.WALL), HEIGHT)
    ring -= Pos(0, 0, h.FLOOR_T) * extrude(RectangleRounded(h.D_IN, h.W_IN, h.RADIUS), HEIGHT)
    ring -= Pos(0, 0, -1) * extrude(RectangleRounded(h.D_IN - 2 * h.LEDGE_SIDE, h.W_IN - 2 * h.LEDGE_END, 3.0),
                                    h.FLOOR_T + 2)
    return ring


if __name__ == "__main__":
    p = build()
    bb = p.bounding_box()
    print(f"fit test: pocket {h.D_IN:.1f} x {h.W_IN:.1f}; outside {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f}, "
          f"{p.volume / 1000:.1f} cm3, solids {len(p.solids())}, valid {p.is_valid}")
    skadis.save(p, HERE, "treedix_holder_fit_test", settings={})
