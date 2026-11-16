#!/usr/bin/env python3
"""SKÅDIS shelf for storing a Sonic Research TurboTuner ST-300 (full size) as it sits on a pedalboard:
footswitch up and toward you, display readable from the front.

ST-300: 4.4 x 2.4 x 1.4 in = 112 x 61 x 34 mm (owner's manual, via Tone Start), about 0.25 kg. Its
input and output jacks are on the long sides, which face the end walls (it's unplugged in storage).

Same build as the MC6 Pro shelf, from tools/u1/skadis.py: a pocket 4 mm bigger than the
pedal, a 12 mm front lip, end walls that brace it, an open floor frame, and two hook columns 40 mm
apart (it sticks out 124 mm, so one column would be too weak). Tabs are 8 mm thick (behind the
board). To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath the right-hand end, running front to back and
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes turbotuner_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-TT3-0001"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_L, UNIT_D, UNIT_H = 61.0, 112.0, 34.0    # width along the board, length out from it, height
UNIT_KG = 0.25
SIDE_CLEAR, BACK_GAP, FRONT_CLEAR = 2.0, 2.0, 2.0
WALL_T, STRIP, TAB_T = 4.0, 15.0, 8.0
INNER_L = UNIT_L + 2 * SIDE_CLEAR
INNER_D = BACK_GAP + UNIT_D + FRONT_CLEAR
L = INNER_L + 2 * WALL_T
HOOK_Y = [L / 2 - 20.0, L / 2 + 20.0]


def build(serial=SERIAL):
    part, length, depth, _ = skadis.shelf(INNER_L, INNER_D, HOOK_Y, wall_t=WALL_T, strip=STRIP, tab_t=TAB_T,
                                          chamfer=BACK_GAP - 0.5)
    if serial:
        part -= skadis.serial_under(serial, depth / 2, length - (WALL_T + STRIP) / 2)
    return part


def ghost():
    """The pedal in place (plus its footswitch), for previews and the fit check."""
    x0, y0 = skadis.BACK_T + BACK_GAP, WALL_T + SIDE_CLEAR
    box = Pos(x0 + UNIT_D / 2, y0 + UNIT_L / 2, 3 + UNIT_H / 2) * Box(UNIT_D, UNIT_L, UNIT_H)
    return box + Pos(x0 + UNIT_D - 20, y0 + UNIT_L / 2, 3 + UNIT_H + 9) * Box(12, 12, 18)


if __name__ == "__main__":
    p = build()
    depth = skadis.BACK_T + INNER_D + 3.5
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + BACK_GAP + UNIT_D / 2) + 50 * depth   # stored + 50 N lean
    skadis.report("TurboTuner ST-300 shelf", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the pedal {(ghost() & p).volume:.3f} mm3; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("turbotuner_holder", SERIAL))
