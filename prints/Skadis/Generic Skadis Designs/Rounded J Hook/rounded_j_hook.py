#!/usr/bin/env python3
"""SKÅDIS rounded J-hook, modelled on IKEA's white plastic SKÅDIS hook 203.208.02 (sold as a 5-pack;
this is ONE hook, print it once per hook you want): the chunkier, soft-edged cousin of the J Hook
(IKEA's black wire one), for keys, headphones, bags and cables.

Sizes are read off IKEA's product photo, not measured (the page lists 8 x 1 x 12 cm, the same as the
long wire hook, so it isn't this hook's size): 100 mm tall, an 8 mm body (out from the board) x 9 mm
(along it), a 7 mm inside curl reaching 30 mm out, and its tip 40 mm up.

PRINTS LYING ON ITS SIDE like the other wire-style hooks: no supports, nothing bends across a layer
line. The top face's edges are rounded R1.5 for the soft look; the bed face only gets a 0.5 mm
chamfer so it keeps full contact. Standard settings; the 8 x 9 section is nearly solid anyway.

Serial (SERIAL below) is engraved 4 mm tall up the side of the leg, on the face that's on top while
printing (the back carries the hook and peg; the J has no flat underside). "" = off.

Run with python; writes rounded_j_hook_<SERIAL>.stl/.3mf next to this file, centred on the bed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Box, Cylinder, Pos, Rot, chamfer, fillet  # noqa: E402

SERIAL = "JRJP-RJH-0001"           # JRJP- first; one file, printed as many times as needed; "" = off

W = 9.0                            # thickness along the board (the print height)
T = 8.0                            # body thickness in the outline
HEIGHT = 100.0
R_IN = 7.0                         # inside radius of the curl
TIP_Z = 40.0                       # top of the tip above the hook's bottom
UPPER_Z = HEIGHT - 2.0             # upper slot centre: leg top 3.2 mm above the tongue
HOOK_Y = [skadis.HOOK_W / 2]       # hook flush with the y = 0 face, which goes on the bed
TOP_R, BED_CH = 1.5, 0.5           # top-face edge round, bed-face edge chamfer
SERIAL_CAP = 4.0


def build(serial=SERIAL):
    cx = cz = T + R_IN                                  # curl centre; its outside touches x = 0 and z = 0
    leg = Pos(T / 2, W / 2, (cz + HEIGHT) / 2) * Box(T, W, HEIGHT - cz)
    ring = Pos(cx, W / 2, cz) * Rot(90, 0, 0) * (Cylinder(R_IN + T, W) - Cylinder(R_IN, W))
    ring &= Pos(cx, W / 2, cz / 2) * Box(2 * (R_IN + T) + 2, W, cz)        # lower half
    tip = Pos(cx + R_IN + T / 2, W / 2, (cz + TIP_Z) / 2) * Box(T, W, TIP_Z - cz)
    body = leg + ring + tip
    ys = body.edges().filter_by(Axis.Y)
    ends = ys.filter_by_position(Axis.Z, HEIGHT - 0.01, HEIGHT + 0.01) + ys.filter_by_position(Axis.Z, TIP_Z - 0.01, TIP_Z + 0.01)
    body = fillet(ends, T / 2 - 0.2)                    # round ends on the leg top and the tip
    body = fillet(body.edges().filter_by_position(Axis.Y, W - 0.01, W + 0.01), TOP_R)
    body = chamfer(body.edges().filter_by_position(Axis.Y, -0.01, 0.01), BED_CH)
    part = body + skadis.hooks(HOOK_Y[0], upper_z=UPPER_Z, tab_t=skadis.TAB_T)
    if serial:
        z = (cz + UPPER_Z - skadis.SLOT_SEAT - 3) / 2   # up the leg, below the tongue
        part -= skadis.text_cut(serial, (T / 2, W, z), (0, 0, 1), (0, 1, 0), cap=SERIAL_CAP)
    return part


def print_pose(part):
    """On its side: the y = 0 face (flush with the hooks) on the bed."""
    return Rot(90, 0, 0) * part


if __name__ == "__main__":
    p = build()
    moment = 1.0 * 9.81 * (T + R_IN)                    # 1 kg in the bottom of the J
    skadis.report("Rounded J hook", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=skadis.TAB_T)
    print(f"  leg at 1 kg in the J: {moment / (W * T ** 2 / 6):.1f} MPa (in the layers' plane)")
    print(f"  {HEIGHT:.0f} tall x {2 * T + 2 * R_IN:.0f} out x {W:.0f} thick; serial {SERIAL or 'none'}")
    skadis.save([(SERIAL or "rounded_j_hook", print_pose(p))], HERE, skadis.with_serial("rounded_j_hook", SERIAL),
                settings={}, center=True)
