#!/usr/bin/env python3
"""SKÅDIS fork for a cordless drill or driver, hanging nose down with the handle pointing out at you.

Generic sizes, nothing measured: the 54 mm slot passes the chuck, and whatever part of the body is
wider than the slot (motor housing or clutch ring) rests on the tines. An 8 mm lip on each tine stops
it walking off the front; lift it over the lips to take it down. Tine undersides rise at 45 degrees, so
they print without supports. Hooks 80 mm apart with 8 mm tabs. Leave about 150 mm of clear board below
for the chuck and bit, and 200 mm above for the body and battery. To hang: lift ~6.5 mm, push all four
hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on a foot strip along the back plate, reading
from below. Change it per copy before exporting ("" = off).

Prints upright; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes drill_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Cylinder, Pos  # noqa: E402

SERIAL = "JRJP-DRL-0001"           # JRJP- starts every serial; change the number per copy; "" = off

L = 112.0
YC = L / 2
HOOK_Y = [YC - 40.0, YC + 40.0]
SLOT_W, TINE_W = 54.0, 16.0
SLOT_X = 48.0                      # back of the slot's round end is 21 mm out: a Ø62 motor clears the board
REACH = 98.0
TOP = 80.0
TIP_H = 14.0
LIP = 8.0
RAIL = 20.0
FOOT_X, FOOT_T = 12.0, 3.0         # serial strip
TAB_T = 8.0
UP = (Align.CENTER, Align.CENTER, Align.MIN)


def build(serial=SERIAL):
    part = skadis.back_plate(L)
    win = skadis.back_windows(-20.0, L + 20.0, HOOK_Y, RAIL, span=(0, L))
    if win is not None:
        part -= win
    part += skadis.fork(YC, SLOT_W, TINE_W, SLOT_X, REACH, TOP, TIP_H, LIP)
    part += Pos(FOOT_X / 2, YC, FOOT_T / 2) * Box(FOOT_X, L, FOOT_T)
    for y in HOOK_Y:
        part += skadis.hooks(y, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, FOOT_X / 2, YC, x_dir=(0, 1, 0))
    return part


def ghost():
    """An 18 V drill hanging nose down, for previews and the fit check."""
    chuck = Pos(SLOT_X, YC, TOP - 70) * Cylinder(23, 70, align=UP)
    bit = Pos(SLOT_X, YC, TOP - 130) * Cylinder(4, 60, align=UP)
    body = Pos(SLOT_X, YC, TOP) * Cylinder(31, 130, align=UP)
    grip = Pos(SLOT_X + 31 + 55, YC, TOP + 60) * Box(120, 34, 46)
    battery = Pos(SLOT_X + 31 + 130, YC, TOP + 60) * Box(50, 76, 110)
    return chuck + bit + body + grip + battery


if __name__ == "__main__":
    p = build()
    moment = 2.2 * 9.81 * 90 + 50 * REACH                      # 2.2 kg drill, weight ~90 mm out, + 50 N lean
    skadis.report("Drill fork", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the drill {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{REACH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("drill_holder", SERIAL))
