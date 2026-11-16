#!/usr/bin/env python3
"""SKÅDIS rack for ten screwdrivers: they drop through holes in a flat plate and hang by their handles.

Generic sizes, nothing measured. The back row has Ø13 holes for regular drivers (blades up to about
12 mm across) and the front row Ø9 for small ones. The rows are staggered, so handles up to about Ø38
(back) and Ø28 (front) sit side by side; the end handles overhang the plate's ends a little. The back
is a low rail with two hook spines at the minimum SKÅDIS height, 160 mm apart, and a thin web between
them. To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on the strip behind the back row, reading from
below. Change it per copy before exporting ("" = off).

Prints upright on its plate; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes screwdriver_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Cone, Cylinder, Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-SDR-0002"           # JRJP- starts every serial; change the number per copy; "" = off

N_PER_ROW = 5
PITCH = 40.0                       # along a row; the rows are offset by half of this
REAR_D, FRONT_D = 13.0, 9.0        # hole diameters
REAR_X, FRONT_X = 26.0, 54.0       # hole centres, out from the board: a Ø38 and a Ø28 handle just clear
EDGE = 6.0                         # plastic from a hole to the plate's ends and front
PLATE_T = 6.0
RAIL = 14.0                        # back plate stays full thickness below this
TAB_T = 8.0
UPPER_Z = skadis.MIN_UPPER_Z

REAR_Y = [REAR_D / 2 + EDGE + i * PITCH for i in range(N_PER_ROW)]
FRONT_Y = [y + PITCH / 2 for y in REAR_Y]
L = FRONT_Y[-1] + FRONT_D / 2 + EDGE
DEPTH = FRONT_X + FRONT_D / 2 + EDGE
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]
UP = (Align.CENTER, Align.CENTER, Align.MIN)


def build(serial=SERIAL):
    part = skadis.low_back(L, HOOK_Y, RAIL)
    plate = Pos(DEPTH / 2, L / 2, 0) * extrude(RectangleRounded(DEPTH, L, 6), PLATE_T)
    for x, ys, d in ((REAR_X, REAR_Y, REAR_D), (FRONT_X, FRONT_Y, FRONT_D)):
        for y in ys:
            plate -= Pos(x, y, -1) * Cylinder(d / 2, PLATE_T + 2, align=UP)
            plate -= Pos(x, y, PLATE_T - 1.2) * Cone(d / 2, d / 2 + 1.3, 1.3, align=UP)     # lead-in
    part += plate
    part += skadis.profile_solid([(3.5, PLATE_T - 0.5), (7, PLATE_T - 0.5), (3.5, PLATE_T + 3)], L)     # root fillet
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, 11.5, L - 48.0, x_dir=(0, 1, 0))
    return part


def ghost():
    """Ten screwdrivers hanging in place, for previews and the fit check."""
    g = None
    for x, ys, handle, shaft in ((REAR_X, REAR_Y, 38.0, 8.0), (FRONT_X, FRONT_Y, 28.0, 5.0)):
        for y in ys:
            s = Pos(x, y, PLATE_T) * Cylinder(handle / 2, 100, align=UP) + \
                Pos(x, y, PLATE_T - 140) * Cylinder(shaft / 2, 140, align=UP)
            g = s if g is None else g + s
    return g


if __name__ == "__main__":
    p = build()
    moment = 10 * 0.15 * 9.81 * (REAR_X + FRONT_X) / 2 + 50 * DEPTH        # ten 150 g drivers + 50 N lean on the front
    skadis.report("Screwdriver rack", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the drivers {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("screwdriver_holder", SERIAL))
