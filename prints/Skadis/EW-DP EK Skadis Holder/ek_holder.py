#!/usr/bin/env python3
"""SKÅDIS shelf for a Sennheiser EW-DP EK receiver: it sits flat as on a camera, display facing you,
its two rod antennas standing up from the back corners.

EW-DP EK: 86 x 67 x 28 mm, 140 g (the Evolve Receiver Table's numbers), OLED display front and
centre, MIC OUT / headphone / USB-C on the left end, a cold-shoe foot underneath. So the lip and end
walls are only 6 mm tall (clear of the display), the floor is an open frame the foot drops into, and
the back plate is full thickness only at the single hook column in the middle, 24 mm clear of each
antenna. To hang: lift ~6.5 mm, push both hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath the right-hand end, running front to back and
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes ek_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-EKH-0001"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_L, UNIT_D, UNIT_H = 86.0, 67.0, 28.0     # along the board, out from it, height (antennas extra)
UNIT_KG = 0.14
SIDE_CLEAR, BACK_GAP, FRONT_CLEAR = 1.0, 2.0, 1.0
WALL_T, STRIP, LIP_H = 4.0, 15.0, 6.0
TAB_T = 8.0                        # thicker hook tabs (behind the board): it hangs on one column
INNER_L = UNIT_L + 2 * SIDE_CLEAR
INNER_D = BACK_GAP + UNIT_D + FRONT_CLEAR
L = INNER_L + 2 * WALL_T
HOOK_Y = [L / 2]


def build(serial=SERIAL):
    part, length, depth, _ = skadis.shelf(INNER_L, INNER_D, HOOK_Y, lip_h=LIP_H, wall_t=WALL_T, wall_top=0,
                                          rail_h=20.0, strip=STRIP, tab_t=TAB_T, chamfer=BACK_GAP - 0.5)
    if serial:
        part -= skadis.serial_under(serial, depth / 2, length - (WALL_T + STRIP) / 2)
    return part


def ghost():
    """The EK and its antennas in place, for previews and the fit check."""
    x0, y0 = skadis.BACK_T + BACK_GAP, WALL_T + SIDE_CLEAR
    body = Pos(x0 + UNIT_D / 2, y0 + UNIT_L / 2, 3 + UNIT_H / 2) * Box(UNIT_D, UNIT_L, UNIT_H)
    for y in (y0 + 5, y0 + UNIT_L - 5):
        body += Pos(x0 + 5, y, 3 + UNIT_H + 60) * Box(5, 5, 120)
    return body


if __name__ == "__main__":
    p = build()
    depth = skadis.BACK_T + INNER_D + 3.5
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + BACK_GAP + UNIT_D / 2) + 50 * depth   # stored + 50 N lean
    skadis.report("EW-DP EK shelf", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the EK and antennas {(ghost() & p).volume:.3f} mm3; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("ek_holder", SERIAL))
