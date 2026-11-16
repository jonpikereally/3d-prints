#!/usr/bin/env python3
"""SKÅDIS holder for four Sennheiser EW-D / EW G4 bodypacks side by side, labelled MIC 1-4 like the
Wireless Caddy and the cable tags; ../MIC 5-8 is its twin. JRJP-EWB-0005 changes 0003 (Earlier designs) as follows:
- Narrower pockets: 29.5 mm across instead of 34 (2026-11-15: about 15% wider than they need to be),
  so the whole holder is 18 mm shorter along the board. Floor windows narrowed to keep 7 mm side ledges.
- Serial engraved low on the back at the right-hand end (reading from behind) instead of underneath, so
  every pocket, MIC 4 included, gets a floor window (less filament).

Pockets 68 x 29.5, 44 deep, each pack standing on its end, edge-on to you, with a flared mouth. Labels (DIN
Alternate Bold 7 mm, like the Wireless Caddy) engraved 1 mm into the front of each pocket. Back plate full
thickness only at the two hook columns, 120 mm apart. 2.4 mm walls, 3 mm floor, three pointed-roof windows
through every divider and end wall (45 deg roofs, no supports). Packs stand on 12 mm ledges front and back.
To hang: lift ~6.5 mm, push all four hooks through, let it drop.

Change SERIAL per copy before exporting ("" = off).
One colour. Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes ewd_bodypack_holder_1-4_<SERIAL>.stl and .3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Plane, Polygon, Pos, RectangleRounded, Text, extrude  # noqa: E402

SERIAL = "JRJP-EWB-0005"          # JRJP- starts every serial; change the number per copy; "" = off
LABELS = ["MIC 1", "MIC 2", "MIC 3", "MIC 4"]  # left to right

PACK_T, PACK_W, PACK_DEPTH = 29.5, 68.0, 44.0   # pocket: along the board (pack + belt clip), out from it, deep
FLOOR_T, WALL = 3.0, 2.4
LABEL_CAP = 7.0                    # the caddy's label size
B = skadis.BACK_T
L = len(LABELS) * PACK_T + (len(LABELS) + 1) * WALL
DEPTH = B + PACK_W + WALL
TOP = FLOOR_T + PACK_DEPTH
HOOK_Y = [L / 2 - 60.0, L / 2 + 60.0]
POCKET_Y = [WALL + PACK_T / 2 + i * (PACK_T + WALL) for i in range(len(LABELS))]
WIN_W, WIN_H, WIN_ROOF, WIN_PITCH = 12.0, 22.0, 6.0, 20.0   # divider windows: width, straight sides, 45 deg roof, spacing
FLOOR_WIN = (44.0, PACK_T - 14.0)  # floor window, front-back x side to side: leaves 12 / 7 mm ledges
SERIAL_Z = 7.0                     # serial's centre height on the back, well below the lower pegs


def windows():
    """Solid to subtract: three pointed-roof windows through each divider and end wall, and floor windows."""
    z0 = FLOOR_T + 6
    cut = None
    for k in (-1, 0, 1):
        c = B + PACK_W / 2 + k * WIN_PITCH
        pts = [(c - WIN_W / 2, z0), (c + WIN_W / 2, z0), (c + WIN_W / 2, z0 + WIN_H),
               (c, z0 + WIN_H + WIN_ROOF), (c - WIN_W / 2, z0 + WIN_H)]
        for i in range(len(LABELS) + 1):
            w = Pos(0, i * (PACK_T + WALL) + WALL / 2, 0) * extrude(Plane.XZ * Polygon(*pts, align=None), WALL / 2 + 1, both=True)
            cut = w if cut is None else cut + w
    for y in POCKET_Y:
        cut += Pos(B + PACK_W / 2, y, -0.5) * extrude(RectangleRounded(*FLOOR_WIN, 4), FLOOR_T + 1)
    return cut


def label_cut():
    return skadis.front_label_cut(list(zip(LABELS, POCKET_Y)), DEPTH, TOP / 2, LABEL_CAP)


def serial_back(serial):
    """Serial low on the back at the right-hand end seen from behind (the low-Y end), reading from behind."""
    fs = 10 * skadis.SERIAL_CAP / Text("MSH", font_size=10, font_path=skadis.SERIAL_FONT).bounding_box().size.Y
    length = Text(serial, font_size=fs, font_path=skadis.SERIAL_FONT).bounding_box().size.X
    return skadis.text_cut(serial, (0, 4 + length / 2, SERIAL_Z), (0, -1, 0), (-1, 0, 0))


def build(serial=SERIAL):
    part = skadis.back_plate(L)
    part -= skadis.back_windows(-20.0, L + 20.0, HOOK_Y, TOP, span=(0, L))
    block = Pos(DEPTH / 2, L / 2, TOP / 2) * Box(DEPTH, L, TOP)
    for y in POCKET_Y:
        slot = RectangleRounded(PACK_W, PACK_T, 3)
        block -= Pos(B + PACK_W / 2, y, FLOOR_T) * extrude(slot, PACK_DEPTH + 1)
        block -= Pos(B + PACK_W / 2, y, TOP - 1) * extrude(slot, 1, taper=-45)            # flared mouth
    part += block                  # pockets cut on their own: flares would otherwise notch the hook plates
    part -= label_cut()
    part -= windows()
    for y in HOOK_Y:
        part += skadis.hooks(y)
    if serial:
        part -= serial_back(serial)
    return part


def ghost():
    """Four bodypacks (63 x 80, ~27 with belt clip) standing in their pockets, for previews and the fit check."""
    g = None
    for y in POCKET_Y:
        pack = Pos(B + 2 + 31.5, y, FLOOR_T + 40) * Box(63, PACK_T - 2.5, 80)
        g = pack if g is None else g + pack
    return g


if __name__ == "__main__":
    p = build()
    moment = len(LABELS) * 0.2 * 9.81 * (B + PACK_W / 2) + 50 * DEPTH     # four ~200 g packs + 50 N lean
    skadis.report("EW-D bodypack holder MIC 1-4", p, HOOK_Y, moment)
    print(f"  fit: overlap with the packs {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm; serial {SERIAL or 'none'}")
    print(f"  volume {p.volume / 1000:.1f} cm3")
    skadis.save(p, HERE, skadis.with_serial("ewd_bodypack_holder_1-4", SERIAL))
