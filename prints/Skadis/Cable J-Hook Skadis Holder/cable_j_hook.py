#!/usr/bin/env python3
"""SKÅDIS J-hook for one or two coiled cables (XLR, power, instrument): a single arm on one hook column.

A smaller sibling of the two-arm Cable Skadis Holder (JRJP-CBL-0001). Hang a coil over the arm; the
15 mm lip at the end stops it sliding off the front, and the arm's top is wide (ARM_W) with R4 top
edges so a heavy coil doesn't fold over a sharp corner. Generic sizes, nothing measured: about 50 mm
of flat arm holds a couple of 10 m XLR coils.

The arm's underside rises at 45 degrees, so it prints without supports. It has no window (the coil
hanger's): the serial needs the whole 44 mm bed strip under the arm. The back is one full-width
plate at the minimum SKÅDIS height (one hook column, tab_t 8 so a single column carries the load). To hang: lift ~6.5 mm, push the hook and peg through, let it drop.

The serial number (SERIAL below) is engraved underneath the arm, running out from the board, reading
from below. 4 mm capitals, not 6: the arm's bed strip is too short for a 6 mm serial. Change it per
copy before exporting ("" = off).

Prints upright; the 3MF carries tree supports (build plate only) for the hook tab.
Run with python; writes cable_j_hook_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Pos, fillet  # noqa: E402

SERIAL = "JRJP-CBJ-0001"           # JRJP- starts every serial; change the number per copy; "" = off

ARM_W = 22.0                       # plate and arm width along the board
HOOK_Y = [ARM_W / 2]
UPPER_Z = skadis.MIN_UPPER_Z
TOP = skadis.MIN_TOP               # arm top level with the plate top
REACH = 80.0                       # out from the board, lip included
TIP_H = 12.0
LIP, LIP_T = 15.0, 6.0
ROUND = 4.0                        # top edges of the arm
SERIAL_CAP = 4.0
TAB_T = 8.0


def build(serial=SERIAL):
    part = skadis.back_plate(ARM_W, TOP)
    arm = skadis.wedge(ARM_W, 0, REACH, TOP, TIP_H, LIP, LIP_T)
    top_edges = arm.edges().filter_by(Axis.X).filter_by_position(Axis.Z, TOP - 0.01, TOP + LIP + 0.01)
    part += fillet(top_edges, ROUND)
    part += skadis.hooks(HOOK_Y[0], upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        bed_end = REACH - (TOP - TIP_H)                     # where the 45-degree underside leaves the bed
        x = bed_end / 2
        part -= skadis.text_cut(serial, (x, ARM_W / 2, 0), (1, 0, 0), (0, 0, -1), cap=SERIAL_CAP)
    return part


if __name__ == "__main__":
    p = build()
    moment = 2.0 * 9.81 * 40 + 30 * REACH                    # 2 kg of coils + a 30 N tug at the lip
    skadis.report("Cable J-hook", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  {ARM_W:.1f} mm wide, sticks out {REACH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("cable_j_hook", SERIAL))
