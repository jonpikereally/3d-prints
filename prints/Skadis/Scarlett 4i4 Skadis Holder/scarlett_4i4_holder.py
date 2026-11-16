#!/usr/bin/env python3
"""SKÅDIS holder for a Focusrite Scarlett 4i4 (4th Gen) standing on its rear panel, knobs facing up.

Tipped back from its normal position: front panel up and reading the right way round from in front,
top face to the board, underside (rubber feet) facing out. It stands in a cup PLATE_H tall, the lowest a
SKÅDIS hook + peg allows, resting on two end ledges. Between them the floor is open, so the rear jacks
(USB, outputs, MIDI, which point down here) touch nothing and cables can stay plugged in and drop through.

Scarlett 4i4 4th Gen: 180 x 129-130 x 59-60 mm, 0.81 kg (retailer listings, NOT measured; run the fit test).

One continuous wall per layer, with the back wall doubling as the plate, so the nozzle has no gap to
string across. Two hook columns 160 apart; tabs 8 mm thick (behind the board). To hang: lift ~6.5 mm,
push all four hooks through, let it drop.
(Earlier designs: JRJP-4I4-0001, a flat shelf with the front panel facing you, 100 g.)

A serial number (SERIAL below) is engraved underneath, along the right-hand end ledge, reading from
below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes scarlett_4i4_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-4I4-0002"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_T, UNIT_H = 180.0, 60.0, 130.0   # along the board; out from it (top face to feet); standing height
UNIT_KG = 0.81
CLEAR, RADIUS = 0.75, 2.0          # play per side; pocket corner radius (R2 clears a square-cornered box)
FLOOR_T, WALL, TAB_T = 3.0, 3.0, 8.0
LEDGE_END, LEDGE_SIDE = 8.0, 3.0   # floor left under the unit: at each end, and along the two long edges
UPPER_Z = skadis.SLOT_PITCH + skadis.SLOT_SEAT + 0.3                 # 46.5: lower peg 0.3 off the bed
PLATE_H = UPPER_Z - skadis.SLOT_SEAT + skadis.TONGUE_H + 3.0         # 48.3: 3 mm above the tongue, the cup's height too
W_IN, D_IN = UNIT_W + 2 * CLEAR, UNIT_T + 2 * CLEAR
W_OUT = W_IN + 2 * WALL
B = skadis.BACK_T
YC = W_OUT / 2
HOOK_Y = [YC - 80.0, YC + 80.0]
CX = B + D_IN / 2                  # pocket centre; its back wall is the plate
DEPTH = CX + D_IN / 2 + WALL


def build(serial=SERIAL):
    part = Pos(CX, YC, 0) * extrude(RectangleRounded(D_IN + 2 * WALL, W_OUT, RADIUS + WALL), PLATE_H)
    part += Pos(CX / 2, YC, PLATE_H / 2) * Box(CX, W_OUT, PLATE_H)            # square back, flat on the board
    part -= Pos(CX, YC, FLOOR_T) * extrude(RectangleRounded(D_IN, W_IN, RADIUS), PLATE_H)
    part -= Pos(CX, YC, -1) * extrude(RectangleRounded(D_IN - 2 * LEDGE_SIDE, W_IN - 2 * LEDGE_END, 3.0),
                                      FLOOR_T + 2)                            # open under the jacks
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:                                                                # right-hand end ledge
        part -= skadis.serial_under(serial, DEPTH / 2, W_OUT - (WALL + LEDGE_END) / 2)
    return part


def ghost():
    """The 4i4 standing in place, for previews and the fit check."""
    return Pos(CX, YC, FLOOR_T + UNIT_H / 2) * Box(UNIT_T, UNIT_W, UNIT_H)


if __name__ == "__main__":
    p = build()
    moment = UNIT_KG * 9.81 * CX + 50 * DEPTH                  # stored + 50 N lean on the cup's front
    skadis.report("Scarlett 4i4 knobs-up cup", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the 4i4 {(ghost() & p).volume:.3f} mm3; pocket {D_IN:.1f} x {W_IN:.1f}; "
          f"cup holds the bottom {PLATE_H - FLOOR_T:.1f} of {UNIT_H:.0f} mm; "
          f"floor opening {D_IN - 2 * LEDGE_SIDE:.1f} x {W_IN - 2 * LEDGE_END:.1f}; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("scarlett_4i4_holder", SERIAL))
