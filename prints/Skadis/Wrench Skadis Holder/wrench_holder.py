#!/usr/bin/env python3
"""SKÅDIS rack for eight combination wrenches, 8-19 mm (about 5/16-3/4 in), small on the left.

Each wrench goes ring end first through its own slot and hangs by the open end, edge-on to you, so
the set packs tightly. Sizes are generic, from typical proportions, not measured: a ring head is about
1.5 x size + 1.5 across and an open head about 2.2 x size + 5, so each slot is the ring head plus 4 mm,
which passes the ring end and still catches the open end with 5 mm or more to spare. Slots are spaced
and placed by their own wrench, so the small ones sit closer together and nearer the board, and the
plate tapers to match. The back is a low rail with two hook spines at the minimum SKÅDIS height, 80 mm
apart. To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, on the strip behind the slots, reading from
below. Change it per copy before exporting ("" = off).

Prints upright on its plate; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes wrench_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Axis, Box, Polygon, Pos, RectangleRounded, extrude, fillet  # noqa: E402

SERIAL = "JRJP-WRN-0002"           # JRJP- starts every serial; change the number per copy; "" = off

SIZES = [8, 10, 12, 13, 14, 15, 17, 19]   # wrench sizes, mm, left to right
RIB = 4.0                          # plastic between neighbouring slots
END = 5.0                          # plastic from the outer slots to the plate's ends
FRONT = 5.0                        # plastic in front of the slots, at least
HEAD_CLEAR = 8.0                   # back of an open head, out from the board: clears the root fillet
PLATE_T = 6.0
RAIL = 16.0
WALL_T = 2.4
TAB_T = 8.0
SERIAL_X = 6.0                     # across the strip behind the slots; capitals run 3-9
UPPER_Z = skadis.MIN_UPPER_Z


def ring(s):
    return 1.5 * s + 1.5


def open_head(s):
    return 2.2 * s + 5


def slot_len(s):
    return ring(s) + 4


def slot_w(s):
    """Along the board: the ring head's thickness (about 0.55 x size + 2) plus 2 mm."""
    return 0.55 * s + 4


def slot_x(s):
    return open_head(s) / 2 + HEAD_CLEAR


def slot_positions():
    ys = [END + slot_w(SIZES[0]) / 2]
    for a, b in zip(SIZES, SIZES[1:]):
        ys.append(ys[-1] + (slot_w(a) + slot_w(b)) / 2 + RIB)
    return ys


def front_line(ys):
    """Plate depth at y = 0 and y = L: a straight front edge with at least FRONT in front of every slot."""
    fronts = [slot_x(s) + slot_len(s) / 2 + FRONT for s in SIZES]
    slope = (fronts[-1] - fronts[0]) / (ys[-1] - ys[0])
    d0 = max(f - slope * y for f, y in zip(fronts, ys))
    return d0, d0 + slope * L


SLOT_Y = slot_positions()
L = SLOT_Y[-1] + slot_w(SIZES[-1]) / 2 + END
D0, D1 = front_line(SLOT_Y)
HOOK_Y = [L / 2 - 40.0, L / 2 + 40.0]


def build(serial=SERIAL):
    part = skadis.low_back(L, HOOK_Y, RAIL)
    plate = extrude(Polygon((0, 0), (D0, 0), (D1, L), (0, L), align=None), PLATE_T)
    plate = fillet(plate.edges().filter_by(Axis.Z).filter_by_position(Axis.X, 5, 500), 4)
    for s, y in zip(SIZES, SLOT_Y):
        w = slot_w(s)
        plate -= Pos(slot_x(s), y, -1) * extrude(RectangleRounded(slot_len(s), w, min(5, w / 2 - 0.1)), PLATE_T + 2)
    part += plate
    part += skadis.profile_solid([(3.5, PLATE_T - 0.5), (7, PLATE_T - 0.5), (3.5, PLATE_T + 3)], L)     # root fillet
    for y0, reach in ((0, D0 - 8), (L - WALL_T, D1 - 8)):                     # brace the plate's end strips
        part += skadis.profile_solid([(0, 1), (reach, 1), (reach, PLATE_T), (0, RAIL)], WALL_T, y0)
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        part -= serial_cut(serial)
    return part


def serial_cut(serial):
    return skadis.serial_under(serial, SERIAL_X, L / 2, x_dir=(0, 1, 0))


def ghost():
    """Eight wrenches hanging by their open ends, for previews and the fit check."""
    g = None
    for s, y in zip(SIZES, SLOT_Y):
        t = 0.45 * s + 2
        x = slot_x(s)
        w = Pos(x, y, PLATE_T + 11) * Box(open_head(s), t, 22) + \
            Pos(x, y, PLATE_T - 80) * Box(0.7 * ring(s), 0.4 * s + 1, 160) + \
            Pos(x, y, PLATE_T - 160 - ring(s) / 2) * Box(ring(s), 0.55 * s + 2, ring(s))
        g = w if g is None else g + w
    return g


if __name__ == "__main__":
    p = build()
    depth = max(D0, D1)
    moment = sum(0.012 * s * 9.81 * slot_x(s) for s in SIZES) + 50 * depth    # 12 g per mm of size + 50 N lean
    skadis.report("Wrench rack", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    print(f"  fit: overlap with the wrenches {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{D0:.1f}-{D1:.1f} mm; serial {SERIAL or 'none'}")
    print("  slots (len x wide at x): " + ", ".join(f"{s}:{slot_len(s):.1f}x{slot_w(s):.1f} at {slot_x(s):.1f} "
                                                    f"(ring {ring(s):.1f}, open {open_head(s):.1f})" for s in SIZES))
    if SERIAL:
        bb = serial_cut(SERIAL).bounding_box()
        clear = min(slot_x(s) - slot_len(s) / 2 - bb.max.X for s in SIZES)
        print(f"  serial: y {bb.min.Y:.1f}-{bb.max.Y:.1f}, {clear:.1f} mm clear of the slots")
    skadis.save(p, HERE, skadis.with_serial("wrench_holder", SERIAL))
