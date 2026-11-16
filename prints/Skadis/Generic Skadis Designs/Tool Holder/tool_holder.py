#!/usr/bin/env python3
"""SKÅDIS ring tool holder, modelled on IKEA's black SKÅDIS tool holder 905.699.45: a short spine on
the board with the hook and peg, and a flat ring right beside it that a screwdriver, scissors, a hammer
handle or a glue gun drops through.

Ring: 44 mm inside, 6 mm wire, 6 mm thick, top edges rounded so tools don't catch; its outside sits
1 mm off the spine, so the holder sticks out only ~61 mm. (JRJP-TLH-0001 used IKEA's listed 11 cm as
the reach, with a 50 mm arm out to the ring; "this shouldnt stick out far from the board". IKEA's
photo has the ring right at the leg. 0001 is in Earlier designs/.)

The ring has to lie flat, so this prints UPRIGHT like the other holders: ring on the bed, spine
standing, and the 3MF carries tree supports (build plate only) for the hook tab. A small 45-degree
gusset joins the spine to the ring's neck, stopping short of the hole. To hang: lift ~6.5 mm, push the
hook and peg through, let it drop.

Serial (SERIAL below) is engraved 3.5 mm tall up the back of the spine, beside the hook column, reading
from behind: the ring leaves no flat underside long enough. "" = off. One file, printed once per holder.

Run with python; writes tool_holder_<SERIAL>.stl/.3mf next to this file, centred on the bed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Box, Cylinder, Pos, fillet  # noqa: E402

SERIAL = "JRJP-TLH-0002"           # JRJP- first; one file, printed as many times as needed; "" = off

SPINE = skadis.SPINE_W             # 16 along the board
HOOK_Y = [0.0]                     # spine centred on y = 0
UPPER_Z = skadis.MIN_UPPER_Z
TOP = skadis.MIN_TOP
NECK = 1.0                         # gap from the spine's front face to the ring's outside
R_IN, WIRE = 22.0, 6.0             # ring: 44 inside, 56 outside (IKEA: 6 cm wide)
THICK = 6.0                        # ring and arm thickness (Z)
ARM_W = 10.0                       # neck width along the board
GUSSET = 7.0                       # 45-degree gusset, this tall and this far out (stops short of the hole)
EDGE_R = 1.5                       # ring and arm top edges
TAB_T = 8.0
SERIAL_CAP = 3.5                   # up the back of the 16 mm spine: no room for 6 mm
SERIAL_Y = 5.25                    # beside the hook column (hooks are 4.5 wide on y = 0)


def build(serial=SERIAL):
    cx = skadis.BACK_T + NECK + R_IN + WIRE             # ring centre: its outside 1 mm off the spine
    ring = Pos(cx, 0, THICK / 2) * (Cylinder(R_IN + WIRE, THICK) - Cylinder(R_IN, THICK))
    a0, a1 = skadis.BACK_T - 0.5, cx - R_IN + 1.0       # sunk into the spine and into the ring
    arm = Pos((a0 + a1) / 2, 0, THICK / 2) * Box(a1 - a0, ARM_W, THICK)
    flat = ring + arm
    tops = flat.edges().filter_by_position(Axis.Z, THICK - 0.01, THICK + 0.01).filter_by(Axis.Y, reverse=True)
    flat = fillet(tops, EDGE_R)
    x0 = skadis.BACK_T - 0.5
    gusset = skadis.profile_solid([(x0, THICK - 1), (x0 + GUSSET, THICK - 1), (x0, THICK + GUSSET)],
                                  ARM_W - 2, -(ARM_W - 2) / 2)
    part = Pos(0, -SPINE / 2, 0) * skadis.back_plate(SPINE, TOP) + flat + gusset
    part += skadis.hooks(HOOK_Y[0], upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        z = (skadis.TONGUE_H + 1 + TOP - 1.5) / 2       # between the peg and the plate top
        part -= skadis.text_cut(serial, (0, SERIAL_Y, z), (0, 0, 1), (-1, 0, 0), cap=SERIAL_CAP)
    return part


if __name__ == "__main__":
    p = build()
    cx = skadis.BACK_T + NECK + R_IN + WIRE
    reach = cx + R_IN + WIRE
    moment = 1.0 * 9.81 * cx + 20 * reach               # 1 kg tool in the ring + a 20 N knock on its rim
    skadis.report("Tool holder", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  {reach:.0f} out x {2 * (R_IN + WIRE):.0f} wide x {TOP:.1f} tall; ring {2 * R_IN:.0f} inside; "
          f"serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("tool_holder", SERIAL), center=True)
