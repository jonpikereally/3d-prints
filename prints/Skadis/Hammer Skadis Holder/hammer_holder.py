#!/usr/bin/env python3
"""SKÅDIS fork for a hammer: the handle goes in the front-open slot and the head rests across the tines.

Generic sizes, nothing measured: the 42 mm slot passes claw-hammer and mallet handles up to about 38 mm
wide, and the head just has to be longer than the 66 mm fork. An 8 mm lip on each tine stops the head
walking off the front; lift it over the lips to take it down. Tine undersides rise at 45 degrees, so
they print without supports. Hooks 40 mm apart. Allow about 40 mm of clear board above the fork for
the head and 350 mm below for the handle. To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on a foot strip along the back plate, reading
from below. Change it per copy before exporting ("" = off).

Prints upright; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes hammer_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-HAM-0001"           # JRJP- starts every serial; change the number per copy; "" = off

L = 72.0
YC = L / 2
HOOK_Y = [YC - 20.0, YC + 20.0]
SLOT_W, TINE_W = 42.0, 12.0
SLOT_X = 43.0                      # back of the slot's round end is 22 mm out from the board
REACH = 74.0
TOP = 72.0
TIP_H = 10.0
LIP = 8.0
FOOT_X, FOOT_T = 12.0, 3.0         # serial strip
TAB_T = 8.0


def build(serial=SERIAL):
    part = skadis.back_plate(L)
    part += skadis.fork(YC, SLOT_W, TINE_W, SLOT_X, REACH, TOP, TIP_H, LIP)
    part += Pos(FOOT_X / 2, YC, FOOT_T / 2) * Box(FOOT_X, L, FOOT_T)
    for y in HOOK_Y:
        part += skadis.hooks(y, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, FOOT_X / 2, YC, x_dir=(0, 1, 0))
    return part


def ghost():
    """A 20 oz claw hammer hanging in place, for previews and the fit check."""
    head = Pos(SLOT_X, YC, TOP + 16) * Box(30, 130, 32)
    handle = Pos(SLOT_X, YC, TOP + 16 - 165) * Box(24, 34, 330)
    return head + handle


if __name__ == "__main__":
    p = build()
    moment = 0.9 * 9.81 * SLOT_X + 50 * REACH                  # 900 g hammer + 50 N lean on a tine end
    skadis.report("Hammer fork", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the hammer {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{REACH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("hammer_holder", SERIAL))
