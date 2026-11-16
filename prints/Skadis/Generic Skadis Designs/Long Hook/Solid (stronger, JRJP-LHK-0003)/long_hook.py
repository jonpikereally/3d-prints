#!/usr/bin/env python3
"""SKÅDIS long L-hook, modelled on IKEA's SKÅDIS hook 503.356.18 (steel wire, 8 cm tall, 12 cm long):
a leg up the board face with the hook and peg, curving into a straight arm with an upturned tip.

IKEA's is ~6 mm steel wire; PLA needs more, so the leg and arm are 9 mm thick (along the board) and
the arm 10 mm deep, and the 3MF prints it SOLID (PRINT: 100% infill on the object; the profile's 2 walls +
15% left the arm about half as strong: JRJP-LHK-0001, kept as the lighter option in the folder beside this one). Solid, it breaks at
roughly 5 kg hung at the tip (~40 MPa in the arm root, in the plane of the layers); keep everyday
loads to about 1.5 kg at the tip, more nearer the bend, because PLA creeps under a constant load. Sizes are IKEA's listed ones; the bend radii are read off their product photo, not measured.

PRINTS LYING ON ITS SIDE, so the whole outline, hook tab included, lies in the layers: no supports, and
neither the arm nor the tab bends across a layer line (the upright holders' weak spot). The hook and
peg are the standard skadis.hooks() (4.5 mm across the slot), flush with the bed face. To hang: lift
~6.5 mm, push the hook and peg through, let it drop.

One hook per file, printed once per hook you want (2026-11-16: "ill just print twice"; two side
by side were 273 mm, past the 270 mm bed). Its serial (SERIALS below) is engraved underneath the arm,
running out from the board, reading from below, so every copy printed from one file shares it.
"" = off.

Run with python; writes long_hook_<SERIAL>.stl/.3mf per hook next to this file,
each centred on the bed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Box, Pos, Rot, fillet  # noqa: E402

SERIALS = ["JRJP-LHK-0003"]   # one file, printed as many times as needed; JRJP- first; "" = off

W = 9.0                            # thickness along the board (the print height)
LEG_T = 6.0                        # leg, out from the board
HEIGHT = 80.0                      # IKEA: 8 cm
LENGTH = 120.0                     # IKEA: 12 cm
ARM_D = 10.0                       # arm depth (vertical as hung)
TIP_T, TIP_H = 7.0, 14.0           # upturned tip: thickness, height above the arm top
BEND_IN, BEND_OUT = 10.0, 16.0     # leg-to-arm bend radii
UPPER_Z = skadis.UPPER_SLOT_Z      # 75: upper slot centre; peg in the slot 40 below
HOOK_Y = [skadis.HOOK_W / 2]       # hook flush with the y = 0 face, which goes on the bed
SERIAL_CAP = 6.0
PRINT = {"sparse_infill_density": "100%"}   # per-object setting in the 3MF: solid arm


def box(x0, x1, z0, z1):
    return Pos((x0 + x1) / 2, W / 2, (z0 + z1) / 2) * Box(x1 - x0, W, z1 - z0)


def build(serial):
    body = box(0, LEG_T, 0, HEIGHT) + box(0, LENGTH, 0, ARM_D) + box(LENGTH - TIP_T, LENGTH, 0, ARM_D + TIP_H)
    ys = body.edges().filter_by(Axis.Y)
    at = lambda x, z: ys.filter_by_position(Axis.X, x - 0.01, x + 0.01).filter_by_position(Axis.Z, z - 0.01, z + 0.01)
    body = fillet(at(LEG_T, ARM_D), BEND_IN)
    ys = body.edges().filter_by(Axis.Y)
    body = fillet(at(LENGTH - TIP_T, ARM_D), 4.0)
    ys = body.edges().filter_by(Axis.Y)
    body = fillet(at(LENGTH, 0) + at(LENGTH, ARM_D + TIP_H) + at(LENGTH - TIP_T, ARM_D + TIP_H)
                  + at(0, HEIGHT) + at(LEG_T, HEIGHT), 2.5)
    ys = body.edges().filter_by(Axis.Y)
    body = fillet(at(0, 0), BEND_OUT)                     # outer bend: lifts off the board below the leg
    part = body + skadis.hooks(HOOK_Y[0], upper_z=UPPER_Z, tab_t=skadis.TAB_T)
    if serial:
        x = (BEND_OUT + LENGTH - 6) / 2                   # flat underside between the bend and the tip
        part -= skadis.text_cut(serial, (x, W / 2, 0), (1, 0, 0), (0, 0, -1), cap=SERIAL_CAP)
    return part


def print_pose(part):
    """On its side: the y = 0 face (flush with the hooks) on the bed."""
    return Rot(90, 0, 0) * part


if __name__ == "__main__":
    parts = [build(s) for s in SERIALS]
    p = parts[0]
    load = 2.0 * 9.81
    moment = load * (LENGTH - TIP_T / 2)
    skadis.report("Long hook", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=skadis.TAB_T)
    root_mpa = moment / (W * ARM_D ** 2 / 6)
    print(f"  arm root at 2 kg on the tip: {root_mpa:.0f} MPa (in the layers' plane); "
          f"tab stress above is in-plane too, not across layers")
    print(f"  {HEIGHT:.0f} tall x {LENGTH:.0f} out x {W:.0f} thick; serials {', '.join(s or 'none' for s in SERIALS)}")
    for i, (s, q) in enumerate(zip(SERIALS, parts)):
        name = skadis.with_serial("long_hook", s) if s else f"long_hook_{i + 1}"
        skadis.save([(s or f"hook{i + 1}", print_pose(q))], HERE, name, settings=PRINT, center=True)
