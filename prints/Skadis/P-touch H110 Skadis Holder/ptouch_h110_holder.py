#!/usr/bin/env python3
"""SKÅDIS stand for the Brother P-touch PT-H110 label maker, lying on its side (a long edge down) with
the keyboard and display facing out into the room.

Same idea as the MC6 PRO buttons-out stand (JRJP-MSH-0004): a box on its edge on a LEVEL ledge just
stands upright and slides (the printed JRJP-MSH-0003 did that), so the PT-H110 stands on a SEAT tilted
LEAN degrees, square to its face: four ribs whose tops slope down toward the board. Gravity slides it
back down the seat until its back rests on the top of the back plate, so it's located from its back and
its rounded, tapering body doesn't matter. JRJP-PTH-0002 ("more secure", against tipping out
forward) leans 30 degrees instead of 25 and adds a 3 mm lip 8 mm up its face along the whole bottom
edge, 1.5 mm off the face at Brother's 58 mm thickness: to fall it now has to lift over the lip. The lip
stands on a front wall with pointed (45 degree) windows between the ribs, so nothing prints over air.
Lift it up over the lip to take it out. Low blocks beside
each end stop it sliding sideways; the end walls brace the plate from behind it, so its ends (tape exit,
cutter) stay open.

PT-H110: Brother's figures 111 x 204 x 58 mm, 0.4 kg (not measured). It lies 204 along the board,
111 up its face. Its back rests on the top of a 101 mm plate (taller than the usual 85, else its
top edge would lean into the board), on the full-thickness hook zones. The back plate is full thickness at the two hook columns (160 apart) with a 2 mm web
between. Tabs are 8 mm thick (behind the board). To hang: lift ~6.5 mm, push all four hooks through,
let it drop.

A serial number (SERIAL below) is engraved underneath at the right-hand end, along the front strip,
reading from below. Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes ptouch_h110_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from math import atan2, cos, degrees, radians, sin, tan
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Plane, Polygon, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-PTH-0002"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_D, UNIT_T = 204.0, 111.0, 58.0   # length (along the board), its height on its side, thickness (max)
UNIT_KG = 0.4
LEAN = 30.0                        # lean back from vertical, degrees (0001 was 25)
FEET = 2.0                         # room for rubber feet on its back; without them it slides back and sits the same
SIDE_CLEAR = 2.0
SEAT_UP = 3.0                      # its inner bottom edge sits this far above the floor's top
LIP_UP, LIP_GAP, LIP_T = 8.0, 1.5, 3.0         # front lip: reaches this far up its face, gap to the face, thickness
SEAT_BACK, SEAT_OUT = 6.0, UNIT_T + LIP_GAP + LIP_T   # seat runs this far behind and out from its inner bottom edge
RIB_Y_OFF, RIB_W = (-85.0, -30.0, 30.0, 85.0), 6.0   # seat ribs, from the centre
FLOOR_T, WALL_T, TAB_T = 3.0, 5.0, 8.0
L = UNIT_W + 2 * SIDE_CLEAR + 2 * WALL_T
Y0 = WALL_T + SIDE_CLEAR           # unit's left end
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]

T = radians(LEAN)
U = (-sin(T), cos(T))              # up its face
V = (cos(T), sin(T))               # out through it, toward the room
PZ = FLOOR_T + SEAT_UP
TOP_REST = 8.0                     # its back rests on the plate this far below its top edge
PLATE_H = round(PZ + (UNIT_D - TOP_REST) * cos(T) + 1.5, 1)   # taller than the usual 85: it is 111 tall
PLATE_Z = PLATE_H - 1.5            # top of the plate's front face, where its back leans
PX = skadis.BACK_T + (PLATE_Z - PZ) * tan(T) + FEET / cos(T)   # its inner bottom edge, on the seat
P = (PX, PZ)


def at(s_u, s_v):
    """Point s_u up its face and s_v out through it from its inner bottom edge."""
    return (P[0] + s_u * U[0] + s_v * V[0], P[1] + s_u * U[1] + s_v * V[1])


SEAT_A, SEAT_B = at(0, -SEAT_BACK), at(0, SEAT_OUT)
DEPTH = SEAT_B[0] + 2.0


def build(serial=SERIAL):
    B = skadis.BACK_T
    part = skadis.back_plate(L, PLATE_H)
    part -= skadis.back_windows(-20.0, L + 20.0, HOOK_Y, 34.0, span=(0, L))
    floor = Pos(DEPTH / 2, L / 2, FLOOR_T / 2) * Box(DEPTH, L, FLOOR_T)
    floor -= Pos((B + 4 + DEPTH - 12) / 2, L / 2, FLOOR_T / 2) * \
        extrude(RectangleRounded(DEPTH - 12 - (B + 4), L - 2 * (WALL_T + 18), 6), FLOOR_T / 2 + 1, both=True)
    part += floor
    rib = [(SEAT_A[0], 0), (SEAT_B[0], 0), (SEAT_B[0], SEAT_B[1] - 1.5), at(0, SEAT_OUT - 2.0), SEAT_A]   # top on the seat line
    for dy in RIB_Y_OFF:
        part += skadis.profile_solid(rib, RIB_W, L / 2 + dy - RIB_W / 2)
    f = UNIT_T + LIP_GAP                                                                     # front lip, full length,
    si, so = at(0, f), at(0, f + LIP_T)                                                      # on a wall standing on the
    lip = [(si[0], 0), (so[0], 0), so, at(LIP_UP - 1.0, f + LIP_T), at(LIP_UP, f + LIP_T - 1.0),   # floor's front strip
           at(LIP_UP, f), si]
    wall_f = skadis.profile_solid(lip, L - 2 * WALL_T, WALL_T)
    ribs = sorted(L / 2 + dy for dy in RIB_Y_OFF)
    for y0, y1 in zip([WALL_T] + ribs, ribs + [L - WALL_T]):                                # pointed windows, 45 degree
        lo, hi = y0 + (RIB_W / 2 if y0 in ribs else 0) + 4, y1 - (RIB_W / 2 if y1 in ribs else 0) - 4   # roofs
        apex, half = si[1] - 4.0, (hi - lo) / 2
        if half < 8 or apex - half < FLOOR_T + 3:
            continue
        win = [(lo, FLOOR_T + 1), (hi, FLOOR_T + 1), (hi, apex - half), ((lo + hi) / 2, apex), (lo, apex - half)]
        wall_f -= extrude(Plane.YZ.offset(si[0] - 5) * Polygon(*win, align=None), 20)
    part += wall_f
    a, b = at(0, 15), at(0, 40)                                                              # side stops
    for y in (Y0 - 1.5 - 2.0, Y0 + UNIT_W + 1.5 + 2.0):
        part += Pos((a[0] + b[0]) / 2, y, (b[1] + 10) / 2) * Box(b[0] - a[0], 4.0, b[1] + 10)

    def behind(z):                                                                           # 3 mm behind its back
        return PX - 3 - (z - PZ) * tan(T)
    top = max(behind(PLATE_H), 1.0)
    wall = [(0, 1), (behind(1), 1), (top, PLATE_H), (0, PLATE_H)]
    part += skadis.profile_solid(wall, WALL_T) + skadis.profile_solid(wall, WALL_T, L - WALL_T)
    for y in HOOK_Y:
        part += skadis.hooks(y, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, DEPTH - 6, L - WALL_T - 2 - 40, x_dir=(0, 1, 0))
    return part


def ghost(thick=UNIT_T, feet=FEET):
    """The PT-H110 leaning in place, as a box, for the fit check. feet=0 slides it back down the seat."""
    s = feet - FEET
    cx, cz = at(UNIT_D / 2, s + thick / 2)
    return Pos(cx, Y0 + UNIT_W / 2, cz) * Rot(0, -LEAN, 0) * Box(thick, UNIT_W, UNIT_D)


if __name__ == "__main__":
    p = build()
    com = at(UNIT_D / 2, UNIT_T / 2)
    outer = at(0, UNIT_T)
    moment = UNIT_KG * 9.81 * com[0] + 50 * DEPTH            # its weight + 50 N pressing on the front
    skadis.report("PT-H110 stand", p, HOOK_Y, moment, tab_t=TAB_T)
    g = ghost()
    tip = degrees(atan2(outer[0] - com[0], com[1] - outer[1]))
    lt = at(LIP_UP, UNIT_T)                                  # with the lip it has to pivot over the lip's top
    tip_lip = degrees(atan2(lt[0] - com[0], com[1] - lt[1]))
    print(f"  fit: overlap {(g & p).volume:.3f} mm3, without feet {(ghost(feet=0) & p).volume:.3f}, "
          f"45 mm thick {(ghost(45) & p).volume:.3f}; nearest point to the board {g.bounding_box().min.X:.1f} mm")
    print(f"  sticks out {DEPTH:.1f} mm at the bottom, {L:.0f} wide; seat front {SEAT_B[1]:.1f} tall; "
          f"{tip:.0f} degrees to tip about its bottom edge, {tip_lip:.0f} over the lip; top of unit {g.bounding_box().max.Z:.1f}; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("ptouch_h110_holder", SERIAL))
    from build123d import export_stl
    (HERE / "parts").mkdir(exist_ok=True)
    export_stl(g, str(HERE / "parts" / "ptouch_ghost.stl"))
