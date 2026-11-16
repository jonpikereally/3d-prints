#!/usr/bin/env python3
"""SKÅDIS holder for a DJI Osmo 360: it stands in a cup holding the bottom 22 mm of its body,
touchscreen side facing you, with both fisheye lenses clear of everything.

Osmo 360: 61 x 36.3 x 81 mm body, 183 g (DJI, via retailers; 47 mm thick across the lens domes).
Back-to-back lenses near the top of the two big faces: the touchscreen side has two buttons beneath
the screen, the other side the DJI logo and LED; at the base, DJI's magnetic quick-release with a
1/4" thread. The cup's front wall is only 6 mm tall, below the buttons, and its floor is a LEDGE-wide
ledge round an open bottom.

Lean version: one hook column on a SPINE_W spine only PLATE_H tall, the lowest a SKÅDIS hook + peg
allows (upper slot UPPER_Z up, the peg 0.3 mm off the bed, as on the coin holder), so the spine stays
mostly below the back lens, which faces the board. The camera sits BACK_GAP off the plate line: the
lens, modelled as a flat disc (the worst case), is LENS_ROOM + 2.2 mm from the spine, the extra
LENS_ROOM for my lens protector, which stays on while it's stored. The holder is no wider than the cup.
(Earlier designs: JRJP-O36-0001, a 112 x 85 plate on two columns 80 apart and a 22 mm cup, 52 g;
JRJP-O36-0002, this design with the lens only 2.2 mm off the spine, 18 g;
JRJP-O36-0003, printed: the pocket was sized from DJI's 36.3 mm and was too deep front to back, 3 mm or more;
JRJP-O36-0004, the same 3 mm wrongly taken off the width; JRJP-O36-0005, pocket 34.5 deep;
JRJP-O36-0006, printed: pocket 33 deep and 18 tall, still too deep.)
To hang: lift ~6.5 mm, push both hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, along the strip behind the floor opening,
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tab.
Run with python; writes osmo360_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Cylinder, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-O36-0007"      # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_D, UNIT_H = 61.0, 36.3, 81.0     # along the board, out from it, height (body, not lens domes)
UNIT_KG = 0.183
LENS_D, LENS_OUT, LENS_Z = 30.0, 5.4, 58.0    # lens domes (estimates): diameter, how far each sticks out, centre height
CLEAR, RADIUS = 0.6, 6.0           # play per side; cup corner radius
POCKET_D = 27.0                    # pocket front to back, set by me after printing 0006 (33, too deep); the fit test shares it
BASE_D = POCKET_D - 2 * CLEAR      # the camera's thickness in the cup, for the ghost
LENS_ROOM = 5.0                    # extra room behind the back lens for the lens protector
BACK_GAP = 7.0 + LENS_ROOM         # plate line (x = BACK_T) to the pocket's back wall
FLOOR_T, CUP_H, FRONT_H, WALL = 3.0, 22.0, 6.0, 2.4
LEDGE = 5.0                        # floor ledge round the opening
SPINE_W, TAB_T = 16.0, 8.0         # spine width (hooks are 4.5 wide); hook tab thickness behind the board
UPPER_Z = skadis.SLOT_PITCH + skadis.SLOT_SEAT + 0.3                 # 46.5: lower peg 0.3 off the bed
PLATE_H = UPPER_Z - skadis.SLOT_SEAT + skadis.TONGUE_H + 3.0         # 3 mm above the tongue
W_IN, D_IN = UNIT_W + 2 * CLEAR, POCKET_D
W_OUT = W_IN + 2 * WALL
B = skadis.BACK_T
YC = W_OUT / 2
HOOK_Y = [YC]
CX = B + BACK_GAP + D_IN / 2       # pocket centre
DEPTH = CX + D_IN / 2 + WALL
TOP = FLOOR_T + CUP_H


def build(serial=SERIAL):
    part = Pos(CX, YC, 0) * extrude(RectangleRounded(D_IN + 2 * WALL, W_OUT, RADIUS + WALL), TOP)
    part += Pos(CX / 2, YC, TOP / 2) * Box(CX, W_OUT, TOP)                    # solid back, flat on the board
    part += Pos(0, YC - SPINE_W / 2, 0) * skadis.back_plate(SPINE_W, PLATE_H)
    part -= Pos(CX, YC, FLOOR_T) * extrude(RectangleRounded(D_IN, W_IN, RADIUS), TOP)
    part -= Pos(CX, YC, -1) * extrude(RectangleRounded(D_IN - 2 * LEDGE, W_IN - 2 * LEDGE, RADIUS - LEDGE / 2),
                                      FLOOR_T + 2)                          # open bottom
    span = W_IN - 2 * RADIUS                                                # front wall cut down
    part -= Pos(CX + D_IN / 2 + WALL / 2, YC, FLOOR_T + FRONT_H + 50) * Rot(0, 90, 0) * \
        extrude(RectangleRounded(100, span, 4), WALL, both=True)
    part += skadis.hooks(YC, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:                                                              # strip behind the opening
        part -= skadis.serial_under(serial, (B + BACK_GAP + LEDGE) / 2, YC, x_dir=(0, 1, 0))
    return part


def ghost(lens_drop=0.0):
    """The camera with its lens domes (modelled as flat discs, the worst case), for previews and the
    fit check; lens_drop moves the lenses down to test a wrong estimate."""
    x0 = B + BACK_GAP + CLEAR
    body = Pos(x0 + BASE_D / 2, YC, FLOOR_T) * extrude(RectangleRounded(BASE_D, UNIT_W, RADIUS - CLEAR), CUP_H)
    body += Pos(x0 + UNIT_D / 2, YC, TOP) * extrude(RectangleRounded(UNIT_D, UNIT_W, RADIUS - CLEAR), UNIT_H - CUP_H)
    for x, s in ((x0, -1), (x0 + UNIT_D, 1)):
        body += Pos(x + s * LENS_OUT / 2, YC, FLOOR_T + LENS_Z - lens_drop) * Rot(0, 90, 0) * \
            Cylinder(LENS_D / 2, LENS_OUT)
    return body


if __name__ == "__main__":
    p = build()
    moment = UNIT_KG * 9.81 * CX + 50 * DEPTH                  # stored + 50 N lean on the cup's front
    skadis.report("Osmo 360 cup", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    lens_x = B + BACK_GAP + CLEAR - LENS_OUT
    print(f"  fit: overlap with the camera and lenses {(ghost() & p).volume:.3f} mm3 "
          f"({(ghost(6) & p).volume:.3f} with the lenses 6 mm lower); back lens disc {lens_x - B:.1f} mm "
          f"in front of the spine, its bottom {FLOOR_T + LENS_Z - LENS_D / 2 - PLATE_H:+.1f} mm from the "
          f"spine top; opening {D_IN - 2 * LEDGE:.1f} x {W_IN - 2 * LEDGE:.1f}; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("osmo360_holder", SERIAL))
