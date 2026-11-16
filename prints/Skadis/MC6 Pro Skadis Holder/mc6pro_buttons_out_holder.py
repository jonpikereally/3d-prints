#!/usr/bin/env python3
"""SKÅDIS stand for storing the Morningstar MC6 PRO with its footswitches facing out into the room:
standing on its front edge, leaning well back, the face the right way up, rear jacks on top. The flat
shelf (mc6pro_holder.py, JRJP-MSH-0002) is the other way of storing it.

History: JRJP-MSH-0003 (Earlier designs, printed 2026-11-10) stood it on a LEVEL floor behind a lip.
A box on a flat edge on a level floor just stands upright, so it never leaned onto the plate: it stood
straight, slid front to back, and its bottom switches landed on the lip. I then leaned it back by hand
(photo in that folder) until its underside rested on the top of the back plate, about 25 degrees, and
asked for that.

So it now stands on a SEAT tilted LEAN degrees, square to its face: four ribs whose tops slope down
toward the board. Gravity slides it back down the seat until its underside rests on the top of the back
plate, so it's located from its back and its unmeasured front-edge thickness doesn't matter. FEET
leaves room for stick-on feet; without them it slides 3 mm further back and sits the same way.
Nothing stands in front of it: no lip, so nothing near the footswitches. At 25 degrees it would have to be
tipped over 50 degrees forward to fall. Low blocks beside each end stop it sliding sideways; the end
walls brace the plate from behind it, so its sides (MIDI jacks on the left end) stay open.

MC6 PRO: I measured 180 x 92 mm (length x front to back); the 50 mm thickness, 70 mm over the
switches and 0.6 kg are published figures. The back plate is full thickness at the two hook columns
(160 mm apart) with a 2 mm web between. Tabs are 8 mm thick (behind the board). To hang: lift ~6.5 mm,
push all four hooks through, let it drop. Same hooks as the flat shelf, so mc6pro_holder_fit_test checks
these too.

A serial number (SERIAL below) is engraved underneath at the right-hand end, along the front strip,
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes mc6pro_buttons_out_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from math import atan2, cos, degrees, radians, sin, tan
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Cylinder, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-MSH-0004"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_D, UNIT_T = 180.0, 92.0, 50.0    # width (along the board), its height standing, body thickness (max)
SWITCH_H, COLLAR_R = 20.0, 11.0    # footswitches: height over the face, radius of the nut round each
SWITCH_ACROSS, SWITCH_ROWS = 75.0, 70.0       # published spacing across, and between the two rows
JACKS = 10.0                       # how far the rear jacks stick up past the body
UNIT_KG = 0.6
LEAN = 25.0                        # lean back from vertical, degrees (my photo)
FEET = 3.0                         # room for feet between its underside and the top of the plate
SIDE_CLEAR = 2.0
SEAT_UP = 3.0                      # its inner bottom edge sits this far above the floor's top
SEAT_BACK, SEAT_OUT = 6.0, UNIT_T + 4.0       # seat runs this far behind and out from its inner bottom edge
RIB_Y_OFF, RIB_W = (-70.0, -25.0, 25.0, 70.0), 6.0   # seat ribs, from the centre
FLOOR_T, WALL_T, TAB_T = 3.0, 5.0, 8.0
L = UNIT_W + 2 * SIDE_CLEAR + 2 * WALL_T
Y0 = WALL_T + SIDE_CLEAR           # unit's left end
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]
SWITCH_Y = [L / 2 - SWITCH_ACROSS, L / 2, L / 2 + SWITCH_ACROSS]

T = radians(LEAN)
U = (-sin(T), cos(T))              # up its face
V = (cos(T), sin(T))               # out through it, toward the room
PLATE_Z = skadis.BACK_H - 1.5      # top of the plate's front face, where its underside leans
PZ = FLOOR_T + SEAT_UP
PX = skadis.BACK_T + (PLATE_Z - PZ) * tan(T) + FEET / cos(T)   # its inner bottom edge, on the seat
P = (PX, PZ)


def at(s_u, s_v):
    """Point s_u up its face and s_v out through it from its inner bottom edge."""
    return (P[0] + s_u * U[0] + s_v * V[0], P[1] + s_u * U[1] + s_v * V[1])


SEAT_A, SEAT_B = at(0, -SEAT_BACK), at(0, SEAT_OUT)
DEPTH = SEAT_B[0] + 2.0
ROW_U = ((UNIT_D - SWITCH_ROWS) / 2, (UNIT_D + SWITCH_ROWS) / 2)    # the two switch rows, up its face


def build(serial=SERIAL):
    B = skadis.BACK_T
    part = skadis.back_plate(L)
    part -= skadis.back_windows(-20.0, L + 20.0, HOOK_Y, 34.0, span=(0, L))
    floor = Pos(DEPTH / 2, L / 2, FLOOR_T / 2) * Box(DEPTH, L, FLOOR_T)
    floor -= Pos((B + 4 + DEPTH - 12) / 2, L / 2, FLOOR_T / 2) * \
        extrude(RectangleRounded(DEPTH - 12 - (B + 4), L - 2 * (WALL_T + 18), 6), FLOOR_T / 2 + 1, both=True)
    part += floor
    rib = [(SEAT_A[0], 0), (SEAT_B[0], 0), (SEAT_B[0], SEAT_B[1] - 1.5), at(0, SEAT_OUT - 2.0), SEAT_A]   # top on the seat line
    for dy in RIB_Y_OFF:
        part += skadis.profile_solid(rib, RIB_W, L / 2 + dy - RIB_W / 2)
    a, b = at(0, 15), at(0, 40)                                                              # side stops
    for y in (Y0 - 1.5 - 2.0, Y0 + UNIT_W + 1.5 + 2.0):
        part += Pos((a[0] + b[0]) / 2, y, (b[1] + 10) / 2) * Box(b[0] - a[0], 4.0, b[1] + 10)

    def behind(z):                                                                           # 3 mm behind its underside
        return PX - 3 - (z - PZ) * tan(T)
    top = max(behind(skadis.BACK_H), 1.0)
    wall = [(0, 1), (behind(1), 1), (top, skadis.BACK_H), (0, skadis.BACK_H)]
    part += skadis.profile_solid(wall, WALL_T) + skadis.profile_solid(wall, WALL_T, L - WALL_T)
    for y in HOOK_Y:
        part += skadis.hooks(y, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, DEPTH - 6, L - WALL_T - 2 - 34, x_dir=(0, 1, 0))
    return part


def ghost(thick=UNIT_T, feet=FEET):
    """The MC6 PRO leaning in place, with switches and jacks, for the fit check. feet=0 slides it back down
    the seat by the feet allowance."""
    s = feet - FEET                # along the seat: without feet it sits FEET further back
    cx, cz = at(UNIT_D / 2, s + thick / 2)
    g = Pos(cx, Y0 + UNIT_W / 2, cz) * Rot(0, -LEAN, 0) * Box(thick, UNIT_W, UNIT_D)
    for su in ROW_U:
        for y in SWITCH_Y:
            sx, sz = at(su, s + thick + SWITCH_H / 2)
            g += Pos(sx, y, sz) * Rot(0, 90 - LEAN, 0) * Cylinder(COLLAR_R, SWITCH_H)
    jx, jz = at(UNIT_D + JACKS / 2, s + thick / 2)
    return g + Pos(jx, Y0 + UNIT_W / 2, jz) * Rot(0, -LEAN, 0) * Box(30.0, UNIT_W - 20, JACKS)


if __name__ == "__main__":
    p = build()
    com = at(UNIT_D / 2, UNIT_T / 2)
    outer = at(0, UNIT_T)
    moment = UNIT_KG * 9.81 * com[0] + 50 * DEPTH            # its weight + 50 N pressing on the front
    skadis.report("MC6 PRO buttons-out stand", p, HOOK_Y, moment, tab_t=TAB_T)
    g = ghost()
    tip = degrees(atan2(outer[0] - com[0], com[1] - outer[1]))
    print(f"  fit: overlap with the MC6 (50 mm, on feet) {(g & p).volume:.3f} mm3, without feet "
          f"{(ghost(feet=0) & p).volume:.3f}, 40 mm thick {(ghost(40) & p).volume:.3f}; nearest point to the board "
          f"{g.bounding_box().min.X:.1f} mm")
    print(f"  sticks out {DEPTH:.1f} mm at the bottom, {L:.0f} wide; seat front {SEAT_B[1]:.1f} tall; "
          f"{tip:.0f} degrees to tip forward; top of unit {g.bounding_box().max.Z:.1f}; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("mc6pro_buttons_out_holder", SERIAL))
