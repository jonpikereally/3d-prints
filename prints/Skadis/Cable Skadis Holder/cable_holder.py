#!/usr/bin/env python3
"""SKÅDIS hanger for coiled cables: two arms 80 mm apart, each with a 15 mm lip at the end.

Hang an over-under coil (XLR, power, instrument, USB) over both arms; the lips stop it sliding off
the front, and the arms' top edges are rounded (R3) so a heavy coil doesn't kink on a sharp edge.
Generic sizes, nothing measured: the 74 mm of usable arm takes a bundle of several 10 m XLR coils.
Arm undersides rise at 45 degrees, so they print without supports; a window in each arm saves plastic.
The back is a low rail with two hook spines at the minimum SKÅDIS height. To hang: lift ~6.5 mm,
push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on a foot strip along the back, reading from
below. Change it per copy before exporting ("" = off).

Prints upright; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes cable_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Box, Pos, fillet  # noqa: E402

SERIAL = "JRJP-CBL-0001"           # JRJP- starts every serial; change the number per copy; "" = off

SPINE = skadis.SPINE_W
L = 80.0 + SPINE                   # two hook columns 80 apart
HOOK_Y = [SPINE / 2, L - SPINE / 2]
UPPER_Z = skadis.MIN_UPPER_Z
TOP = skadis.MIN_TOP               # arm tops level with the spine tops
RAIL = 16.0
ARM_W = 14.0                       # wide enough not to bite into a coil
REACH = 95.0                       # out from the board, lip included
TIP_H = 12.0
LIP, LIP_T = 15.0, 6.0
ROUND = 3.0                        # top edges of the arms
WIN = 30.0                         # right-angled window in each arm, legs on the bed and the plate
FOOT_X, FOOT_T = 12.0, 3.0         # serial strip
TAB_T = 8.0


def arm(yc):
    a = skadis.wedge(ARM_W, yc - ARM_W / 2, REACH, TOP, TIP_H, LIP, LIP_T)
    top_edges = a.edges().filter_by(Axis.X).filter_by_position(Axis.Z, TOP - 0.01, TOP + LIP + 0.01)
    a = fillet(top_edges, ROUND)
    x0 = skadis.BACK_T + 4
    win = skadis.profile_solid([(x0, -1), (x0 + WIN + 1, -1), (x0, WIN)], ARM_W + 2, yc - ARM_W / 2 - 1)
    return a - win


def build(serial=SERIAL):
    part = skadis.low_back(L, HOOK_Y, RAIL, top=TOP)
    for y in HOOK_Y:
        part += arm(y)
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    part += Pos(FOOT_X / 2, L / 2, FOOT_T / 2) * Box(FOOT_X, L, FOOT_T)
    if serial:
        part -= skadis.serial_under(serial, FOOT_X / 2, L / 2, x_dir=(0, 1, 0))
    return part


if __name__ == "__main__":
    p = build()
    moment = 3.0 * 9.81 * 50 + 50 * REACH                    # 3 kg of coils + a 50 N tug on an arm end
    skadis.report("Cable hanger", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  {L:.1f} mm wide, sticks out {REACH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("cable_holder", SERIAL))
