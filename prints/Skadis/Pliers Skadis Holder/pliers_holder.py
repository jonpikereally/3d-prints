#!/usr/bin/env python3
"""SKÅDIS rack for pliers and cutters: three thin fins, each carrying two tools.

Generic, so nothing is sized to one tool: open the handles a little and drape them over a fin, the
pivot resting on its top edge, jaws up and handles hanging either side. Any size works. A lip at the
fin's end stops tools sliding off. The fins' undersides rise at 45 degrees, so they print without
supports. Fins are 80 mm apart to leave room for spread handles, each straight in front of its own
hook spine at the minimum SKÅDIS height. Allow about 70 mm of clear board above the fins for the jaws.
To hang: lift ~6.5 mm, push all six hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on a foot strip between the first two fins,
reading from below. Change it per copy before exporting ("" = off).

Prints upright; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes pliers_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-PLR-0002"           # JRJP- starts every serial; change the number per copy; "" = off

FIN_Y = [8.0, 88.0, 168.0]         # fin centres; multiples of 40 apart, like the hook columns
HOOK_Y = FIN_Y
L = FIN_Y[-1] + FIN_Y[0]
FIN_W = 6.0                        # thin enough for handles that barely open
REACH = 54.0                       # fin end, out from the board
TOP = skadis.MIN_TOP               # fin top, level with the spines
TIP_H = 6.0
LIP = 6.0
RAIL = 14.0
FOOT_X, FOOT_T = 10.0, 3.0         # serial strip, clear of handles hanging at the back of a fin
TAB_T = 8.0
UPPER_Z = skadis.MIN_UPPER_Z


def build(serial=SERIAL):
    part = skadis.low_back(L, FIN_Y, RAIL)
    for y in FIN_Y:
        part += skadis.wedge(FIN_W, y - FIN_W / 2, REACH, TOP, TIP_H, LIP)
    foot_y = (FIN_Y[0] + FIN_Y[1]) / 2
    part += Pos(FOOT_X / 2, foot_y, FOOT_T / 2) * Box(FOOT_X, FIN_Y[1] - FIN_Y[0] - FIN_W, FOOT_T)
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, FOOT_X / 2, foot_y, x_dir=(0, 1, 0))
    return part


def ghost():
    """Two pairs of 200 mm pliers on each fin, for previews and the fit check."""
    g = None
    for y in FIN_Y:
        for x in (17.0, 35.0):
            head = Pos(x, y, TOP + 32) * Box(13, 42, 64)
            sides = sum((Pos(x, y + s * (FIN_W / 2 + 9), TOP - 66) * Box(13, 18, 132) for s in (-1, 1)), start=head)
            g = sides if g is None else g + sides
    return g


if __name__ == "__main__":
    p = build()
    moment = 6 * 0.35 * 9.81 * 26 + 50 * REACH                 # six 350 g pliers + 50 N lean on a fin end
    skadis.report("Pliers rack", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the pliers {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{REACH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("pliers_holder", SERIAL))
