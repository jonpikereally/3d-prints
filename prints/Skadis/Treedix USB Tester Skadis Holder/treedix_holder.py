#!/usr/bin/env python3
"""SKÅDIS storage cup for a Treedix TRX5-0816 USB cable tester (2.4-inch colour screen).

Storage only: lift the tester out to use it. It stands on its bottom edge (the five-socket Port A
edge), screen facing out and reading the right way up, in a low cup that holds the bottom part of it.
The back plate is the lowest a SKÅDIS hook + peg allows. A floor opening inside small ledges saves
plastic and lets dust fall through.

Size is from retailer listings (76 x 65 x 15 mm), NOT measured: run the fit test first.
Two hook columns 40 mm apart; tabs 8 mm thick (behind the board). To hang: lift ~6.5 mm, push all four
hooks through, let it drop.
(Earlier designs: JRJP-UCT-0001, an open frame for testing cables while it hangs.)

A serial number (SERIAL below) is engraved low on the back at the right-hand end, reading from behind.
Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes treedix_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos, RectangleRounded, Text, extrude  # noqa: E402

SERIAL = "JRJP-UCT-0002"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_T, UNIT_H = 76.0, 15.0, 65.0     # along the board; out from it; standing height (retailer listing)
UNIT_KG = 0.09
CLEAR, RADIUS = 0.75, 2.0          # play per side; pocket corner radius
FLOOR_T, WALL, TAB_T = 3.0, 2.4, 8.0
CUP_H = 22.0                       # top of the cup above the bed
LEDGE_END, LEDGE_SIDE = 6.0, 3.0   # floor left under the tester: at each end, and along the two long edges
UPPER_Z = skadis.SLOT_PITCH + skadis.SLOT_SEAT + 0.3                 # 46.5: lower peg 0.3 off the bed
PLATE_H = UPPER_Z - skadis.SLOT_SEAT + skadis.TONGUE_H + 3.0         # 48.3: 3 mm above the tongue
W_IN, D_IN = UNIT_W + 2 * CLEAR, UNIT_T + 2 * CLEAR
W_OUT = W_IN + 2 * WALL
B = skadis.BACK_T
YC = W_OUT / 2
HOOK_Y = [YC - 20.0, YC + 20.0]
CX = B + D_IN / 2                  # pocket centre; its back wall is the plate
DEPTH = CX + D_IN / 2 + WALL


def build(serial=SERIAL):
    part = skadis.back_plate(W_OUT, PLATE_H)
    part += Pos(CX, YC, 0) * extrude(RectangleRounded(D_IN + 2 * WALL, W_OUT, RADIUS + WALL), CUP_H)
    part += Pos(CX / 2, YC, CUP_H / 2) * Box(CX, W_OUT, CUP_H)                # square back, flat on the board
    part -= Pos(CX, YC, FLOOR_T) * extrude(RectangleRounded(D_IN, W_IN, RADIUS), PLATE_H)
    part -= Pos(CX, YC, -1) * extrude(RectangleRounded(D_IN - 2 * LEDGE_SIDE, W_IN - 2 * LEDGE_END, 3.0),
                                      FLOOR_T + 2)
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:                                                                # above the lower pegs
        fs = 10 * skadis.SERIAL_CAP / Text("MSH", font_size=10, font_path=skadis.SERIAL_FONT).bounding_box().size.Y
        length = Text(serial, font_size=fs, font_path=skadis.SERIAL_FONT).bounding_box().size.X
        part -= skadis.text_cut(serial, (0, 4 + length / 2, 11.0), (0, -1, 0), (-1, 0, 0))
    return part


def ghost():
    """The tester standing in place, for previews and the fit check."""
    return Pos(CX, YC, FLOOR_T + UNIT_H / 2) * Box(UNIT_T, UNIT_W, UNIT_H)


if __name__ == "__main__":
    p = build()
    moment = UNIT_KG * 9.81 * CX + 50 * DEPTH                  # stored + 50 N lean on the cup's front
    skadis.report("Treedix tester storage cup", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the tester {(ghost() & p).volume:.3f} mm3; pocket {D_IN:.1f} x {W_IN:.1f}; "
          f"cup holds the bottom {CUP_H - FLOOR_T:.1f} of {UNIT_H:.0f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("treedix_holder", SERIAL))
