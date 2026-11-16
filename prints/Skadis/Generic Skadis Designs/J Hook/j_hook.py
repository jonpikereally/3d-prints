#!/usr/bin/env python3
"""SKÅDIS J-hook, modelled on IKEA's black SKÅDIS hook 505.699.33 (sold as a 3-pack; this is ONE hook,
print it once per hook you want): a tall leg up the board with the hook and peg, curling at the bottom
into a small J that sticks out about 2.5 cm.

IKEA lists 10 cm long x 2 cm; the curl's size is read off their product photo, not measured. Their
wire is ~5 mm; this is 6 mm (out from the board) x 9 mm (along it), in the long hook's style.

PRINTS LYING ON ITS SIDE, like the Long Hook: the whole outline, hook tab included, lies in the layers,
so no supports, and nothing bends across a layer line. The 6 mm section is nearly solid even with the
profile's 2 walls + 15% infill, so it prints with standard settings: ~2 MPa in the leg at 1 kg in the J.
The hook and peg are the standard skadis.hooks(), flush with the bed face. To hang: lift ~6.5 mm, push
the hook and peg through, let it drop.

Serial (SERIAL below) is engraved 4 mm tall up the side of the leg, on the face that's on top while
printing: the back (against the board) is taken by the hook and peg, and the J has no flat underside.
"" = off.

Run with python; writes j_hook_<SERIAL>.stl/.3mf next to this file, centred on the bed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Box, Cylinder, Pos, Rot, fillet  # noqa: E402

SERIAL = "JRJP-JHK-0001"           # JRJP- first; one file, printed as many times as needed; "" = off

W = 9.0                            # thickness along the board (the print height)
T = 6.0                            # wire thickness in the outline
HEIGHT = 100.0                     # IKEA: 10 cm
R_IN = 7.0                         # inside radius of the J's curl
TIP_Z = 36.0                       # top of the J's front tip above the hook's bottom
UPPER_Z = HEIGHT - 2.0             # upper slot centre: leg top 3.2 mm above the tongue
HOOK_Y = [skadis.HOOK_W / 2]       # hook flush with the y = 0 face, which goes on the bed
SERIAL_CAP = 4.0


def build(serial=SERIAL):
    cx = cz = T + R_IN                                  # curl centre; its outside touches x = 0 and z = 0
    leg = Pos(T / 2, W / 2, (cz + HEIGHT) / 2) * Box(T, W, HEIGHT - cz)
    ring = Pos(cx, W / 2, cz) * Rot(90, 0, 0) * (Cylinder(R_IN + T, W) - Cylinder(R_IN, W))
    ring &= Pos(cx, W / 2, cz / 2) * Box(2 * (R_IN + T) + 2, W, cz)        # lower half
    x_tip = cx + R_IN + T / 2
    tip = Pos(x_tip, W / 2, (cz + TIP_Z) / 2) * Box(T, W, TIP_Z - cz)
    body = leg + ring + tip
    ys = body.edges().filter_by(Axis.Y)
    ends = ys.filter_by_position(Axis.Z, HEIGHT - 0.01, HEIGHT + 0.01) + ys.filter_by_position(Axis.Z, TIP_Z - 0.01, TIP_Z + 0.01)
    body = fillet(ends, T / 2 - 0.2)                    # round ends on the leg top and the J's tip
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
    load = 1.0 * 9.81
    moment = load * (T + R_IN)                          # 1 kg in the bottom of the J
    skadis.report("J hook", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=skadis.TAB_T)
    print(f"  leg at 1 kg in the J: {moment / (W * T ** 2 / 6):.1f} MPa (in the layers' plane)")
    print(f"  {HEIGHT:.0f} tall x {p.bounding_box().max.X:.0f} out x {W:.0f} thick; serial {SERIAL or 'none'}")
    skadis.save([(SERIAL or "j_hook", print_pose(p))], HERE, skadis.with_serial("j_hook", SERIAL),
                settings={}, center=True)
