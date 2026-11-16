#!/usr/bin/env python3
"""SKÅDIS tray for one tape measure: it stands in an open-floored tray with its belt clip toward the board.

Generic sizes, nothing measured: the 115 x 62 pocket takes 16-33 ft tapes up to about 105 mm long and
60 mm thick including the clip, leaving room at the end for the hook. The front wall is notched so you
can grip the tape. Two hook spines at the minimum SKÅDIS height, 80 mm apart, rise above the tray. To
hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on the floor frame's back strip, reading from
below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes tape_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-TPM-0002"           # JRJP- starts every serial; change the number per copy; "" = off

INNER_W, INNER_D = 115.0, 62.0     # along the board, out from the plate
WALL, FLOOR_T = 2.4, 2.4
HEIGHT = 24.0
LEDGE = 10.0                       # floor frame round the open middle
FRONT_H, NOTCH_W = 14.0, 70.0      # front wall notch
TAB_T = 8.0
UPPER_Z = skadis.MIN_UPPER_Z

B = skadis.BACK_T
L = INNER_W + 2 * WALL
YC = L / 2
CX = B + INNER_D / 2
DEPTH = B + INNER_D + WALL
HOOK_Y = [YC - 40.0, YC + 40.0]


def build(serial=SERIAL):
    part = skadis.low_back(L, HOOK_Y, HEIGHT)
    part += Pos(CX, YC, 0) * extrude(RectangleRounded(INNER_D + 2 * WALL, L, 8.4), HEIGHT)
    part -= Pos(CX, YC, FLOOR_T) * extrude(RectangleRounded(INNER_D, INNER_W, 6), HEIGHT)
    part -= Pos(CX, YC, -1) * extrude(RectangleRounded(INNER_D - 2 * LEDGE, INNER_W - 2 * LEDGE, 5), FLOOR_T + 2)
    part -= Pos(B + INNER_D + WALL / 2, YC, FRONT_H + 50) * Rot(0, 90, 0) * \
        extrude(RectangleRounded(100, NOTCH_W, 5), WALL, both=True)
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, B + LEDGE / 2, YC, x_dir=(0, 1, 0))
    return part


def ghost():
    """A 25 ft tape standing in the tray, for previews and the fit check."""
    return Pos(CX, YC, FLOOR_T + 45) * Box(56, 100, 90)


if __name__ == "__main__":
    p = build()
    moment = 0.5 * 9.81 * CX + 50 * DEPTH                      # 500 g tape + 50 N lean on the front
    skadis.report("Tape measure tray", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the tape {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("tape_holder", SERIAL))
