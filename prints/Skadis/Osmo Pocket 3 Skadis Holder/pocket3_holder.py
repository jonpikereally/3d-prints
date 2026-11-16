#!/usr/bin/env python3
"""SKÅDIS holder for a DJI Osmo Pocket 3 that can charge while it's stored: it stands gimbal-up in a
cup on a 3 mm ledge round an open bottom, so a USB-C cable plugged into its underside hangs straight
down through the hole.

Osmo Pocket 3: 139.7 x 42.2 x 33.5 mm, 179 g (DJI). The cup holds the bottom 24 mm with 0.6 mm play
all round; its front wall is cut down to 12 mm so the record button stays in view. Plug the cable in
first, then lower the Pocket 3 in with the cable through the hole. One hook column; to hang: lift
~6.5 mm, push both hooks through, let it drop.

Lean version: above the cup the back plate is only a SPINE_W spine carrying the hooks, so the holder
is no wider than the cup. (Earlier designs: JRJP-OP3-0001, a full 72 x 85 plate and a 30 mm cup, 29 g;
JRJP-OP3-0002, the spine topped by a 68 mm bar for a full-size serial, 20.6 g.)

A serial number (SERIAL below) is engraved low across the cup's rear face, reading from behind, in
SERIAL_CAP capitals (my standard 6 mm is 62 mm long and won't fit the 48 mm face; I chose to shrink
it rather than keep the bar). Change it per copy before exporting ("" = off).

Prints upright on its ledge; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes pocket3_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-OP3-0003"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_W, UNIT_D, UNIT_H = 42.2, 33.5, 139.7    # along the board, out from it, height
UNIT_KG = 0.179
CLEAR = 0.6                        # play per side
RADIUS = 7.0                       # corner radius of the cup, close to the handle's rounded edges
LEDGE, LEDGE_T = 3.0, 3.0          # ledge width round the open bottom, and its thickness
CUP_H, FRONT_H = 24.0, 12.0        # how much of the Pocket 3 the cup holds; front wall height
SPINE_W = 16.0                     # back plate width above the cup (hooks are 4.5 wide)
SERIAL_CAP = 4.0                   # serial capital height: 4 mm fits the cup's 48 mm rear face
PLATE_W = 0.0                      # cup() makes the plate as wide as the cup
INNER_W, INNER_D = UNIT_W + 2 * CLEAR, UNIT_D + 2 * CLEAR


def build(serial=SERIAL):
    part, plate_w, _ = skadis.cup(INNER_W, INNER_D, LEDGE_T + CUP_H, n_cols=1, radius=RADIUS,
                                  floor_t=LEDGE_T, ledge=LEDGE, front_h=LEDGE_T + FRONT_H, plate_w=PLATE_W)
    yc, top = plate_w / 2, LEDGE_T + CUP_H
    side = (plate_w - SPINE_W) / 2
    for y in (side / 2, plate_w - side / 2):              # plate above the cup, either side of the spine
        part -= Pos(skadis.BACK_T / 2, y, (top + skadis.BACK_H) / 2 + 1) * \
            Box(skadis.BACK_T + 0.02, side + 0.02, skadis.BACK_H - top + 2)
    if serial:                                            # 3 mm up from the bottom, reading from behind
        part -= skadis.text_cut(serial, (0, yc, 3 + SERIAL_CAP / 2), (0, -1, 0), (-1, 0, 0), cap=SERIAL_CAP)
    return part


def hook_ys():
    return skadis.cup(INNER_W, INNER_D, LEDGE_T + CUP_H, ledge=LEDGE, plate_w=PLATE_W)[2]


def ghost():
    """The Pocket 3 in place, for previews and the fit check."""
    _, plate_w, _ = skadis.cup(INNER_W, INNER_D, LEDGE_T + CUP_H, ledge=LEDGE, plate_w=PLATE_W)
    return Pos(skadis.BACK_T + CLEAR + UNIT_D / 2, plate_w / 2, LEDGE_T) * \
        extrude(RectangleRounded(UNIT_D, UNIT_W, RADIUS - CLEAR), UNIT_H)


if __name__ == "__main__":
    p = build()
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + INNER_D / 2) + 50 * (skadis.BACK_T + INNER_D + 2.4)
    skadis.report("Osmo Pocket 3 cup", p, hook_ys(), moment)
    print(f"  fit: overlap with the Pocket 3 {(ghost() & p).volume:.3f} mm3; "
          f"cable hole {INNER_D - 2 * LEDGE:.1f} x {INNER_W - 2 * LEDGE:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("pocket3_holder", SERIAL))
