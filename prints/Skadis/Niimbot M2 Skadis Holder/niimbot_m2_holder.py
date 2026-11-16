#!/usr/bin/env python3
"""SKÅDIS shelf for storing a Niimbot M2 label printer, lying sideways (its long side along the board).

Niimbot M2: I measured mine at about 107 x 180 mm (retailer listings say 108 x 178 x 74, 0.76 kg).
Sideways it sticks out about 120 mm instead of 190, and its front (label exit) and back face the end
walls, which only matters while it's stored.

Same build as the MC6 Pro shelf, from tools/u1/skadis.py: a pocket 4 mm bigger than the
printer, a 12 mm front lip, end walls that brace it, an open floor frame, and a back plate full height
only at the two hook columns, 160 mm apart. To hang: lift ~6.5 mm, push all four hooks through, let
it drop.

A serial number (SERIAL below) is engraved underneath the right-hand end, running front to back and
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes niimbot_m2_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-NM2-0001"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_L, UNIT_D, UNIT_H = 180.0, 107.0, 74.0   # along the board, out from it, height (~107 x 180)
UNIT_KG = 0.76
SIDE_CLEAR, BACK_GAP, FRONT_CLEAR = 2.0, 2.0, 2.0
WALL_T, STRIP = 4.0, 18.0
TAB_T = 8.0                        # thicker hook tabs (behind the board): 0.76 kg sticking out 131 mm
INNER_L = UNIT_L + 2 * SIDE_CLEAR
INNER_D = BACK_GAP + UNIT_D + FRONT_CLEAR
L = INNER_L + 2 * WALL_T
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]


def build(serial=SERIAL):
    part, length, depth, _ = skadis.shelf(INNER_L, INNER_D, HOOK_Y, wall_t=WALL_T, strip=STRIP, tab_t=TAB_T,
                                          chamfer=BACK_GAP - 0.5)
    if serial:
        part -= skadis.serial_under(serial, depth / 2, length - (WALL_T + STRIP) / 2)
    return part


def ghost():
    """The M2 in place, for previews and the fit check."""
    x0, y0 = skadis.BACK_T + BACK_GAP, WALL_T + SIDE_CLEAR
    return Pos(x0 + UNIT_D / 2, y0 + UNIT_L / 2, 3 + UNIT_H / 2) * Box(UNIT_D, UNIT_L, UNIT_H)


if __name__ == "__main__":
    p = build()
    depth = skadis.BACK_T + INNER_D + 3.5
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + BACK_GAP + UNIT_D / 2) + 50 * depth   # stored + 50 N lean
    skadis.report("Niimbot M2 shelf", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the M2 {(ghost() & p).volume:.3f} mm3; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("niimbot_m2_holder", SERIAL))
