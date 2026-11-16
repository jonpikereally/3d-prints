#!/usr/bin/env python3
"""SKÅDIS stand for storing a Neural DSP Quad Cortex Mini upright: standing on its front edge, the
touchscreen facing you the right way up, rear jacks on top.

QC Mini: 228 x 118 x 50 mm body (118 and 50 measured with calipers for the QC Mini Riser), 65 mm over
the footswitches, 1.5 kg (Neural DSP). The 7" screen fills the middle of the top face and the four
rotary footswitches sit at its corners, so the two that end up at the bottom are only ~5-10 mm above
the edge it stands on; the volume buttons are low on the left side in the front 35 mm (the riser had
to stop its lip short of them). So:
  - it leans back LEAN degrees on a level ledge, resting on its inner bottom edge. That keeps its
    centre of gravity over its base and it would have to tip ~38 degrees forward to fall; its top
    leans to TOP_CLEAR from the board, and the 85 mm back plate stays clear behind it;
  - the front lip reaches only 3.5 mm up its face (4 mm clear of it) and runs under the screen only,
    not in front of the corner footswitches;
  - a 3 mm ridge behind its bottom edge stops it sliding back, and small blocks beside each end, on
    the screen half of the edge (away from the volume buttons), stop it sliding sideways;
  - the end walls brace the back plate from behind the unit, so they never cover its sides.
The back plate is full thickness at the three hook columns (80 mm apart) with a 2 mm web between them,
so the nozzle never crosses open air. Tabs are 8 mm thick (behind the board). To hang: lift ~6.5 mm,
push all six hooks through, let it drop. The flat shelf this replaced is in Earlier designs.

A serial number (SERIAL below) is engraved underneath, along the strip under the unit's bottom edge,
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes qc_mini_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from math import cos, radians, sin, tan
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Cylinder, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-QCM-0001"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_D, UNIT_T = 228.0, 118.0, 50.0   # width (along the board), front to back (its height standing), body
SWITCH_H, SWITCH_D = 15.0, 20.0    # footswitches: height over the top face, cap diameter
UNIT_KG = 1.5
LEAN = 15.0                        # lean back from vertical, degrees
TOP_CLEAR = 2.5                    # its top edge to the board
SIDE_CLEAR = 2.0
LIP_UP, LIP_GAP, LIP_T = 3.5, 4.0, 3.5          # front lip: reach up its face, gap to it, thickness
SWITCH_ZONE = 45.0                 # no lip within this of either end (the corner footswitches)
FLOOR_T, WALL_T, TAB_T = 3.0, 5.0, 8.0
L = UNIT_W + 2 * SIDE_CLEAR + 2 * WALL_T
Y0 = WALL_T + SIDE_CLEAR           # unit's left end
HOOK_Y = [L / 2 - 80.0, L / 2, L / 2 + 80.0]

T = radians(LEAN)
U = (-sin(T), cos(T))              # up its face
V = (cos(T), sin(T))               # out through it, toward the room
PX = TOP_CLEAR + UNIT_D * sin(T)   # its inner bottom edge, on the floor
P = (PX, FLOOR_T)


def at(s_u, s_v):
    """Point s_u up its face and s_v out through it from its inner bottom edge."""
    return (P[0] + s_u * U[0] + s_v * V[0], P[1] + s_u * U[1] + s_v * V[1])


OUTER_EDGE = at(0, UNIT_T)         # outer bottom edge, raised off the level floor
LIP_X = OUTER_EDGE[0] + LIP_GAP
LIP_TOP = OUTER_EDGE[1] + LIP_UP
DEPTH = LIP_X + LIP_T


def build(serial=SERIAL):
    B = skadis.BACK_T
    part = skadis.back_plate(L)
    part -= skadis.back_windows(-20.0, L + 20.0, HOOK_Y, 34.0, span=(0, L))
    part += Pos(DEPTH / 2, L / 2, FLOOR_T / 2) * Box(DEPTH, L, FLOOR_T)
    y1, y2 = Y0 + SWITCH_ZONE, Y0 + UNIT_W - SWITCH_ZONE                                 # lip under the screen only
    part += skadis.profile_solid([(LIP_X, 0), (DEPTH, 0), (DEPTH, LIP_TOP - 1), (DEPTH - 1, LIP_TOP), (LIP_X, LIP_TOP)],
                                 y2 - y1, y1)
    part += Pos(PX - 2.5, L / 2, FLOOR_T + 1.5) * Box(2.0, L, 3.0)       # ridge behind its bottom edge, joins the end walls
    a, b = at(0, 20), at(0, 45)                                                              # side stops, screen half
    for y in (Y0 - 1.5 - 2.0, Y0 + UNIT_W + 1.5 + 2.0):
        part += Pos((a[0] + b[0]) / 2, y, (b[1] + 5) / 2) * Box(b[0] - a[0], 4.0, b[1] + 5)
    # end walls behind the unit: 3 mm behind its bottom face, up to the plate top
    def behind(z):
        return PX - 3 - (z - FLOOR_T) * tan(T)
    wall = [(0, 1), (behind(FLOOR_T), 1), (behind(FLOOR_T), FLOOR_T), (behind(skadis.BACK_H), skadis.BACK_H),
            (0, skadis.BACK_H)]
    part += skadis.profile_solid(wall, WALL_T) + skadis.profile_solid(wall, WALL_T, L - WALL_T)
    for x0, x1 in ((B + 4, PX - 7), (PX + 8, LIP_X - 6)):                                    # floor windows
        part -= Pos((x0 + x1) / 2, L / 2, FLOOR_T / 2) * \
            extrude(RectangleRounded(x1 - x0, L - 2 * (WALL_T + 18), 6), FLOOR_T / 2 + 1, both=True)
    for y in HOOK_Y:
        part += skadis.hooks(y, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, PX + 0.5, L / 2, x_dir=(0, 1, 0))
    return part


def ghost():
    """The QC Mini leaning in place, with its four corner footswitches, for previews and the fit check."""
    cx, cz = at(UNIT_D / 2, UNIT_T / 2)
    g = Pos(cx, Y0 + UNIT_W / 2, cz) * Rot(0, -LEAN, 0) * Box(UNIT_T, UNIT_W, UNIT_D)
    for su in (18.0, UNIT_D - 18.0):
        for y in (Y0 + 15.0, Y0 + UNIT_W - 15.0):
            sx, sz = at(su, UNIT_T + SWITCH_H / 2)
            g += Pos(sx, y, sz) * Rot(0, 90 - LEAN, 0) * Cylinder(SWITCH_D / 2, SWITCH_H)
    return g


if __name__ == "__main__":
    p = build()
    com = at(UNIT_D / 2, UNIT_T / 2)
    moment = UNIT_KG * 9.81 * com[0] + 50 * DEPTH            # its weight + 50 N pressing on the lip
    skadis.report("QC Mini stand", p, HOOK_Y, moment, tab_t=TAB_T)
    g = ghost()
    print(f"  fit: overlap with the QC Mini and its footswitches {(g & p).volume:.3f} mm3; its top edge "
          f"{g.bounding_box().min.X:.1f} mm from the board; sticks out {DEPTH:.1f} mm at the bottom")
    print(f"  centre of gravity {com[0] - PX:.1f} mm in front of its bottom edge, over a {UNIT_T * cos(T):.0f} mm base; "
          f"lip top {LIP_TOP:.1f} above the floor; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("qc_mini_holder", SERIAL))
