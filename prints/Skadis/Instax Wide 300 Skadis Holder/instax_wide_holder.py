#!/usr/bin/env python3
"""SKÅDIS shelf for storing a Fujifilm Instax Wide 300, sitting on its base with the lens facing out.

Instax Wide 300: 167.8 x 94.7 x 120.9 mm "not including protrusions" (Fujifilm; read as width x
height x depth), 612 g without batteries, strap and film, so about 0.8 kg loaded. The lens sticks out
past that, so the pocket allows LENS_MARGIN extra depth (I chose spec + margin over measuring): if
it sits loose front to back, push it against the back plate. The 8 mm front lip stops it sliding off
whether it reaches the body or the lens first.

Same build as the MC6 Pro shelf, from tools/u1/skadis.py: a pocket bigger than the camera,
end walls that brace it, an open floor frame, and a back plate full thickness only at the two hook
columns, 120 mm apart. Tabs are 8 mm thick (behind the board). To hang: lift ~6.5 mm, push all four
hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath the right-hand end, running front to back and
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes instax_wide_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-IW3-0001"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_L, UNIT_D, UNIT_H = 167.8, 120.9, 94.7   # width along the board, depth out from it, height (spec)
UNIT_KG = 0.8
LENS_MARGIN = 20.0                 # extra depth for the lens past the spec's "not including protrusions"
SIDE_CLEAR, BACK_GAP, FRONT_CLEAR = 2.0, 2.0, 2.0
WALL_T, STRIP, LIP_H, TAB_T = 4.0, 18.0, 8.0, 8.0
INNER_L = UNIT_L + 2 * SIDE_CLEAR
INNER_D = BACK_GAP + UNIT_D + LENS_MARGIN + FRONT_CLEAR
L = INNER_L + 2 * WALL_T
HOOK_Y = [L / 2 - 60.0, L / 2 + 60.0]


def build(serial=SERIAL):
    part, length, depth, _ = skadis.shelf(INNER_L, INNER_D, HOOK_Y, lip_h=LIP_H, wall_t=WALL_T, strip=STRIP,
                                          tab_t=TAB_T, chamfer=BACK_GAP - 0.5)
    if serial:
        part -= skadis.serial_under(serial, depth / 2, length - (WALL_T + STRIP) / 2)
    return part


def ghost():
    """The camera (spec box, lens margin in front of it) pushed against the back plate, for previews and the fit check."""
    x0, y0 = skadis.BACK_T + BACK_GAP, WALL_T + SIDE_CLEAR
    return Pos(x0 + UNIT_D / 2, y0 + UNIT_L / 2, 3 + UNIT_H / 2) * Box(UNIT_D, UNIT_L, UNIT_H)


if __name__ == "__main__":
    p = build()
    depth = skadis.BACK_T + INNER_D + 3.5
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + BACK_GAP + UNIT_D / 2) + 50 * depth   # stored + 50 N lean
    skadis.report("Instax Wide 300 shelf", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the camera {(ghost() & p).volume:.3f} mm3; pocket {INNER_L:.1f} x {INNER_D:.1f}; "
          f"serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("instax_wide_holder", SERIAL))
