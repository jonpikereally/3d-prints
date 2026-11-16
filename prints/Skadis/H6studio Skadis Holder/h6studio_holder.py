#!/usr/bin/env python3
"""SKÅDIS holder for a Zoom H6studio, standing bare with its mic capsule on top, in a cup that holds
the bottom of the body.

H6studio: 83 x 54.5 mm across, 221 mm tall with the capsule, 477 g with batteries (Zoom's spec). The
cup holds the bottom 35 mm with 0.6 mm play all round; its front wall is cut down to 16 mm so the
buttons and screen stay in view. Two hook columns 40 mm apart so it can't twist on the board. To
hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath the cup, running along it and reading from
below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes h6studio_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-H6S-0001"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_D, UNIT_H = 83.0, 54.5, 221.0    # along the board, out from it, height with the capsule
UNIT_KG = 0.477
CLEAR = 0.6                        # play per side
RADIUS = 6.0
FLOOR_T, CUP_H, FRONT_H = 3.0, 35.0, 16.0
INNER_W, INNER_D = UNIT_W + 2 * CLEAR, UNIT_D + 2 * CLEAR


def build(serial=SERIAL):
    part, plate_w, _ = skadis.cup(INNER_W, INNER_D, FLOOR_T + CUP_H, n_cols=2, radius=RADIUS,
                                  floor_t=FLOOR_T, front_h=FLOOR_T + FRONT_H)
    if serial:
        part -= skadis.serial_under(serial, skadis.BACK_T + INNER_D / 2, plate_w / 2, x_dir=(0, 1, 0))
    return part


def hook_ys():
    return skadis.cup(INNER_W, INNER_D, FLOOR_T + CUP_H, n_cols=2)[2]


def ghost():
    """The H6studio in place, for previews and the fit check."""
    _, plate_w, _ = skadis.cup(INNER_W, INNER_D, FLOOR_T + CUP_H, n_cols=2)
    return Pos(skadis.BACK_T + CLEAR + UNIT_D / 2, plate_w / 2, FLOOR_T) * \
        extrude(RectangleRounded(UNIT_D, UNIT_W, RADIUS - CLEAR), UNIT_H)


if __name__ == "__main__":
    p = build()
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + INNER_D / 2) + 50 * (skadis.BACK_T + INNER_D + 2.4)
    skadis.report("H6studio cup", p, hook_ys(), moment)
    print(f"  fit: overlap with the H6studio {(ghost() & p).volume:.3f} mm3; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("h6studio_holder", SERIAL))
