#!/usr/bin/env python3
"""SKÅDIS rack for seven bare 10-hole diatonic harmonicas, one per key: each stands on its end in a
pocket, mouthpiece facing you, with its key inlaid in black filament on the pocket's front.

Harmonicas: about 102 x 29 x 25 mm (Hohner Special 20 / Marine Band: ~100 long, 29 front to back,
17-25 thick with covers), so the pockets are 30.5 x 26.5 with 0.75 mm play per side and hold the
bottom 38 mm. Each front wall is cut down to 22 mm so more of the holes show, and carries the key
label (DIN Alternate Bold, like the MIC labels). A vent hole in each floor lets a played harmonica
dry. Back plate full thickness only at the two hook columns, 160 mm apart. To hang: lift ~6.5 mm, push
all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, along the front strip, reading from below.
Change it per copy before exporting ("" = off).

Two colours: body on toolhead 1, labels on toolhead 2 (load black there). Prints upright on its floor;
the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes harmonica_holder_<SERIAL>.3mf next to this file and body and label
STLs in parts/. Slice with ARRANGE=0 and two filaments ("A;B").
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Cylinder, Pos, RectangleRounded, Rot, extrude  # noqa: E402

SERIAL = "JRJP-HRM-0002"          # JRJP- starts every serial; change the number per copy; "" = off
KEYS = ["G", "A", "Bb", "C", "D", "E", "F"]   # left to right; one pocket per key

HARP_L, HARP_D, HARP_T = 102.0, 29.0, 25.0    # length (stands up), mouthpiece to back, thickness
CLEAR = 0.75                       # play per side
WALL, FLOOR_T = 3.0, 3.0
SIDE_H, FRONT_H = 38.0, 22.0       # pocket depth above the floor; front wall height
VENT_D = 12.0                      # vent hole in each pocket floor
LABEL_CAP = 8.0
P_D, P_W = HARP_D + 2 * CLEAR, HARP_T + 2 * CLEAR             # pocket: out from the board, along it
B = skadis.BACK_T
L = len(KEYS) * P_W + (len(KEYS) + 1) * WALL
DEPTH = B + P_D + WALL
TOP = FLOOR_T + SIDE_H
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]
POCKET_Y = [WALL + P_W / 2 + i * (P_W + WALL) for i in range(len(KEYS))]
PX = B + P_D / 2                   # pocket centre, out from the board


def label_cut():
    return skadis.front_label_cut(list(zip(KEYS, POCKET_Y)), DEPTH, FLOOR_T + FRONT_H / 2, LABEL_CAP)


def build(serial=SERIAL):
    part = skadis.back_plate(L)
    part -= skadis.back_windows(-20.0, L + 20.0, HOOK_Y, TOP, span=(0, L))
    block = Pos(DEPTH / 2, L / 2, TOP / 2) * Box(DEPTH, L, TOP)
    for y in POCKET_Y:
        slot = RectangleRounded(P_D, P_W, 2)    # tight corners: square-edged harps still fit
        block -= Pos(PX, y, FLOOR_T) * extrude(slot, SIDE_H + 1)
        block -= Pos(PX, y, TOP - 1) * extrude(slot, 1, taper=-45)                    # flared mouth
        block -= Pos(B + P_D + WALL / 2, y, FLOOR_T + FRONT_H + 50) * Rot(0, 90, 0) * \
            extrude(RectangleRounded(100, P_W - 6, 4), WALL, both=True)               # front wall cut down
        block -= Pos(PX, y, -1) * Cylinder(VENT_D / 2, FLOOR_T + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part += block                  # pockets cut on their own: flares would otherwise notch the hook plates
    part -= label_cut()
    for y in HOOK_Y:
        part += skadis.hooks(y)
    if serial:
        part -= skadis.serial_under(serial, (PX + VENT_D / 2 + DEPTH) / 2, L / 2, x_dir=(0, 1, 0))
    return part


def ghost():
    """Seven harmonicas standing in their pockets, for previews and the fit check."""
    g = None
    for y in POCKET_Y:
        h = Pos(PX, y, FLOOR_T + HARP_L / 2) * Box(HARP_D, HARP_T, HARP_L)
        g = h if g is None else g + h
    return g


if __name__ == "__main__":
    p = build()
    moment = len(KEYS) * 0.065 * 9.81 * PX + 50 * DEPTH          # seven ~65 g harps + 50 N lean on the front
    skadis.report("Harmonica rack", p, HOOK_Y, moment)
    print(f"  fit: overlap with the harmonicas {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm; serial {SERIAL or 'none'}")
    ink = skadis.flush_inlay(label_cut(), DEPTH)
    print(f"  black inlay: {ink.volume:.1f} mm3, {len(ink.solids())} solids, overlap with the body {(ink & p).volume:.3f} mm3")
    skadis.save_inlaid(p, ink, HERE, skadis.with_serial("harmonica_holder", SERIAL))
