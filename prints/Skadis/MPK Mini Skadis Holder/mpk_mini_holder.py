#!/usr/bin/env python3
"""SKÅDIS brackets for storing an Akai MPK Mini MK4 upright: standing on its back (USB) edge, keys
pointing up, playing surface facing the room. A left and a right bracket each hold one end of it,
each printed on its own (together on one plate, the nozzle strings across the gap between them).

MPK Mini MK4: 347.5 x 192 x 45.7 mm, 1.05 kg (Akai's spec). Pads, knobs and the pitch / mod wheels
fill the back half of the top face from end to end, starting about 8-10 mm from the back edge, so
nothing can sit in front of them. Instead it leans back LEAN degrees against a back rest: that puts
its centre of gravity behind its bottom edge, so it rests on the back rest under its own weight and
would have to be rotated about 28 degrees to tip forward. A lip on the ledge only reaches 3.5 mm up
its face (4 mm clear of it, for rubber feet that push it out) and stops the bottom sliding forward.
The ledge is level, so the edge with the USB-C, sustain and MIDI sockets mostly stays off it. Its top
leans to within ~2 mm of the board.

Each bracket: hook plate, floor, back rest (80 mm up the keyboard), lip, an end wall that locates the
keyboard and ties the back rest to the plate, and a gusset behind the back rest at the inner end. The end walls' inner faces are 351.5 mm apart (2 mm
play each end) when the brackets hang with their outer hook columns 320 mm apart (16 columns), which
keeps all four columns on same-height slots. Tabs are 8 mm thick (behind the board).

Serial numbers (SERIAL below, with L / R) are engraved underneath each bracket's end-wall strip,
running front to back and reading from below. Change the number per copy ("" = off).

Prints upright on their floors; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes mpk_mini_holder_L_<L serial>.stl/.3mf and mpk_mini_holder_R_<R serial>.stl/.3mf.
"""
import sys
from math import cos, radians, sin
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Plane, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-MPK-{}-0001"        # JRJP- starts every serial; {} = L / R; change the number per copy; "" = off

UNIT_L, UNIT_D, UNIT_T = 347.5, 192.0, 45.7   # length, front to back edge (its height standing up), thickness
UNIT_KG = 1.05
SIDE_CLEAR = 2.0                   # play at each end
LEAN = 15.0                        # lean back from vertical, degrees
REST_H = 80.0                      # back rest height, measured up the keyboard
TOP_CLEAR = 2.0                    # keyboard's top edge to the board
LIP_UP, LIP_GAP, LIP_T = 3.5, 4.0, 3.5         # lip: reach up the face, gap to the face, thickness
FLOOR_T, REST_T, WALL_T, GUSSET_T, TAB_T = 3.0, 4.0, 5.0, 3.0, 8.0
SPAN = UNIT_L + 2 * SIDE_CLEAR                 # end walls' inner faces apart
OUTER = 320.0                                  # outer hook columns apart: a multiple of 40
C1 = (SPAN - OUTER) / 2                        # outer hook column in from its end wall's inner face
INNER_L = C1 + skadis.COLUMN_STEP + skadis.HOOK_ZONE / 2       # each bracket's share of the keyboard
L = WALL_T + INNER_L
HOOK_Y = [WALL_T + C1, WALL_T + C1 + skadis.COLUMN_STEP]      # left bracket

T = radians(LEAN)
U = (-sin(T), cos(T))              # up the keyboard's face
V = (cos(T), sin(T))               # out through it, toward the room
PX = TOP_CLEAR + UNIT_D * sin(T)   # keyboard's inner bottom edge, on the floor
P = (PX, FLOOR_T)


def at(s_u, s_v):
    """Point s_u up the keyboard and s_v out through it from its inner bottom edge."""
    return (P[0] + s_u * U[0] + s_v * V[0], P[1] + s_u * U[1] + s_v * V[1])


OUTER_EDGE = at(0, UNIT_T)                     # outer bottom edge, raised off the level floor
LIP_X = OUTER_EDGE[0] + LIP_GAP
LIP_TOP = OUTER_EDGE[1] + LIP_UP
DEPTH = LIP_X + LIP_T


def bracket():
    """Left bracket, its end wall at Y = 0..WALL_T."""
    part = skadis.back_plate(L)
    part += Pos(DEPTH / 2, L / 2, FLOOR_T / 2) * Box(DEPTH, L, FLOOR_T)
    rest_top, rest_back_top, rest_back = at(REST_H, 0), at(REST_H, -REST_T), at(0, -REST_T)
    part += skadis.profile_solid([(rest_back[0], 0), (P[0], 0), P, rest_top, rest_back_top, rest_back], L)
    part += skadis.profile_solid([(LIP_X, 0), (DEPTH, 0), (DEPTH, LIP_TOP - 1), (DEPTH - 1, LIP_TOP), (LIP_X, LIP_TOP)], L)
    part += skadis.profile_solid([(0, 0), (DEPTH, 0), (DEPTH, LIP_TOP), rest_top, (skadis.BACK_T, skadis.BACK_H),
                                  (0, skadis.BACK_H)], WALL_T)
    # inner gusset behind the back rest: ties its free edge to the plate (Orca supported it otherwise)
    part += skadis.profile_solid([(0, 0), (rest_back[0], 0), rest_back, rest_back_top, (skadis.BACK_T, skadis.BACK_H),
                                  (0, skadis.BACK_H)], GUSSET_T, L - GUSSET_T)
    # floor windows behind the back rest and in front of the keyboard's bottom edge
    y0, y1 = WALL_T + 12, L - 12
    for x0, x1 in ((skadis.BACK_T + 6, rest_back[0] - 6), (PX + 12, LIP_X - 6)):
        part -= Pos((x0 + x1) / 2, (y0 + y1) / 2, FLOOR_T / 2) * \
            extrude(RectangleRounded(x1 - x0, y1 - y0, 6), FLOOR_T / 2 + 1, both=True)
    for y in HOOK_Y:
        part += skadis.hooks(y, tab_t=TAB_T)
    return part


def build(serial=SERIAL):
    """[(name, left bracket), (name, right bracket)]; the right one is the left mirrored, end wall at Y = -WALL_T..0."""
    left = bracket()
    out = []
    for side in ("L", "R"):
        p = left if side == "L" else left.mirror(Plane.XZ)
        if serial:
            y = (WALL_T + 12) / 2 if side == "L" else -(WALL_T + 12) / 2
            p -= skadis.serial_under(serial.format(side), DEPTH / 2, y)
        out.append((f"mpk_bracket_{side}", p))
    return out


def ghost(length=120.0):
    """The keyboard's left end (length mm of it) leaning on the left bracket, for previews and the fit check."""
    cx, cz = at(UNIT_D / 2, UNIT_T / 2)
    return Pos(cx, WALL_T + SIDE_CLEAR + length / 2, cz) * Rot(0, -LEAN, 0) * Box(UNIT_T, length, UNIT_D)


if __name__ == "__main__":
    brackets = build()
    (_, left), (_, right) = brackets
    com_x = at(UNIT_D / 2, UNIT_T / 2)[0]
    moment = UNIT_KG / 2 * 9.81 * com_x + 50 * DEPTH        # half its weight + 50 N pressing on the lip
    skadis.report("MPK left bracket", left, HOOK_Y, moment, tab_t=TAB_T)
    skadis.report("MPK right bracket", right, [-y for y in HOOK_Y], moment, tab_t=TAB_T, sim=False)
    g = ghost()
    print(f"  fit: overlap with the keyboard {(g & left).volume:.3f} mm3; its top edge {g.bounding_box().min.X:.1f} mm "
          f"from the board; sticks out {DEPTH:.1f} mm at the bottom; lip top {LIP_TOP:.1f} above the floor")
    print(f"  centre of gravity {PX - com_x:.1f} mm behind its bottom edge (leans on the back rest); "
          f"end walls {SPAN} apart, outer hooks {OUTER:.0f} apart")
    # one file per bracket: printed together, the nozzle strings across the gap between them every layer
    for side, (_, part) in zip("LR", brackets):
        skadis.save(part, HERE, skadis.with_serial(f"mpk_mini_holder_{side}", SERIAL.format(side) if SERIAL else ""))
