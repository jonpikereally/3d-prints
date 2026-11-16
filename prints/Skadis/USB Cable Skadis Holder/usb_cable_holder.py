#!/usr/bin/env python3
"""SKÅDIS comb for USB cables: eight front-open slots; each cable hangs by its plug.

Slide a cable into a slot just below the plug and let go: the cable (up to ~5 mm thick) passes the
5.5 mm slot, and the plug's housing or overmold (USB-A, USB-C, Lightning, micro-B are all wider than
about 6 mm) rests on top. The rest of the cable hangs down in front of the board, so long cables are
best folded in half and hung by both plugs in neighbouring slots. Slots are 16 mm apart so chunky
overmolds still sit side by side. Generic sizes, nothing measured.

The comb's underside rises at 45 degrees, so it prints without supports. The back is a low rail with
two hook spines at the minimum SKÅDIS height, 80 mm apart. To hang: lift ~6.5 mm, push all four hooks
through, let it drop.

A serial number (SERIAL below) is engraved underneath, on a foot strip along the back, reading from
below. Change it per copy before exporting ("" = off).

Prints upright; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes usb_cable_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Cylinder, Plane, Polygon, Pos, extrude  # noqa: E402

SERIAL = "JRJP-USB-0001"           # JRJP- starts every serial; change the number per copy; "" = off

N = 8                              # slots
PITCH = 16.0
END = 12.0                         # plate past the outer slots' centres
L = (N - 1) * PITCH + 2 * END      # 136
HOOK_Y = [L / 2 - 40, L / 2 + 40]
UPPER_Z = skadis.MIN_UPPER_Z
TOP = skadis.MIN_TOP
RAIL = 16.0
REACH = 30.0                       # comb sticks out this far from the board
TIP_H = 8.0
SLOT_W = 5.5                       # cable passes, plug doesn't
SLOT_END = 7.0                     # round end at the back of each slot, a little roomier
SLOT_X = 16.0                      # centre of that round end, out from the board
MOUTH = 1.5                        # chamfer on the slot mouths' top edges
FOOT_X, FOOT_T = 12.0, 3.0         # serial strip
TAB_T = 8.0


def slot_ys():
    return [END + i * PITCH for i in range(N)]


def build(serial=SERIAL):
    part = skadis.low_back(L, HOOK_Y, RAIL, top=TOP)
    part += skadis.wedge(L, 0, REACH, TOP, TIP_H)
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    part += Pos(FOOT_X / 2, L / 2, FOOT_T / 2) * Box(FOOT_X, L, FOOT_T)
    for y in slot_ys():
        part -= Pos(SLOT_X, y, 0) * Cylinder(SLOT_END / 2, TOP + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos((SLOT_X + REACH + 5) / 2, y, TOP / 2 + 1) * Box(REACH + 5 - SLOT_X, SLOT_W, TOP + 2)
        # V lead-in on the slot's top edges, so a cable finds the slot
        h = SLOT_W / 2 + MOUTH
        v = extrude(Plane.YZ * Polygon((y - h - 1, TOP + 1), (y + h + 1, TOP + 1), (y, TOP - h), align=None),
                    REACH + 5, dir=(1, 0, 0))
        part -= Pos(SLOT_X, 0, 0) * v
    if serial:
        part -= skadis.serial_under(serial, FOOT_X / 2, L / 2, x_dir=(0, 1, 0))
    return part


if __name__ == "__main__":
    p = build()
    moment = 1.0 * 9.81 * 25 + 50 * REACH                    # 1 kg of cables + a 50 N tug at the front
    skadis.report("USB cable comb", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  {L:.1f} mm wide, sticks out {REACH:.1f} mm, {N} slots; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("usb_cable_holder", SERIAL))
