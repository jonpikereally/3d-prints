#!/usr/bin/env python3
"""SKÅDIS change holder: one upright tube per circulating Canadian coin (5¢ 10¢ 25¢ $1 $2, left to
right), coins stacked flat on top of one another.

Coin sizes are the Royal Canadian Mint's (diameter x thickness). Each bore is the coin plus CLEAR
(the 11-sided loonie gets a little more) and is 20% taller than the SKÅDIS minimum (the
hook and peg need two slots 40 apart, 48.3 mm): 58 mm tall, each tube about two thirds of a roll.
Getting coins out:
  - bottom: a window across the full bore at the front, two coins high, and a fingertip notch in the
    floor. Press a fingertip up on the bottom coin through the notch and drag it out forward; the
    coins above stay put behind the wall.
  - anywhere: a front slot up the tube (half the bore wide, so coins can't fall out) shows how many
    are left and lets you push the stack up from the floor notch to pick coins off the top.
Fill from the top through the flared mouth. Each tube's flat collar carries its label (DIN Alternate
Bold, like the other SKÅDIS labels, inlaid in black filament). Hook columns 80 apart.
To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, along the back strip, reading from below.
Change it per copy before exporting ("" = off).

Two colours: body on toolhead 1, labels on toolhead 2 (load black there). Prints upright on its floor;
the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes coin_holder_<SERIAL>.3mf next to this file and body and label STLs
in parts/. Slice with ARRANGE=0 and two filaments ("A;B").
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Circle, Cylinder, Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-CHG-0004"          # JRJP- starts every serial; new number per copy AND per design change; "" = off
# label, diameter, thickness, mass (g), extra clearance; left to right. Add ("50¢", 27.13, 1.95, 6.9, 0)
# or ("1¢", 19.05, 1.45, 2.35, 0) here for a half-dollar or penny tube.
COINS = [("5¢", 21.20, 1.76, 3.95, 0.0),
         ("10¢", 18.03, 1.22, 1.75, 0.0),
         ("25¢", 23.88, 1.58, 4.40, 0.0),
         ("$1", 26.50, 1.95, 6.27, 0.4),     # 11-sided: corners stick out a little past 26.5
         ("$2", 28.00, 1.80, 6.92, 0.0)]

CLEAR = 1.2                        # bore over coin diameter
WALL, FLOOR_T = 2.0, 2.5           # walls between and in front of the bores; floor
BACK_GAP = 1.0                     # wall between the biggest bore and the back plate
UPPER_Z = skadis.SLOT_PITCH + skadis.SLOT_SEAT + 0.3   # lowest upper slot that keeps the peg above the bottom
COLLAR_H = 10.0                    # solid band round the top that carries the label
WINDOW_COINS = 2                   # bottom window height, in coins
LABEL_CAP = 6.0
LABEL_DEPTH = 0.8                  # black inlay: the front wall is only 2 mm where it crosses a bore
B = skadis.BACK_T
BORES = [d + CLEAR + extra for _, d, _, _, extra in COINS]
L = sum(BORES) + (len(COINS) + 1) * WALL
DEPTH = B + BACK_GAP + max(BORES) + WALL
MIN_TOP = UPPER_Z - skadis.SLOT_SEAT + skadis.TONGUE_H + 3.0   # 3 mm of plate above the tongue
TOP = 1.2 * MIN_TOP
INNER_H = TOP - FLOOR_T
HOOK_Y = [L / 2 - 40.0, L / 2 + 40.0]
CENTRE_Y = [WALL + sum(BORES[:i]) + i * WALL + BORES[i] / 2 for i in range(len(COINS))]
CENTRE_X = [DEPTH - WALL - b / 2 for b in BORES]       # bores flush with the front: same front wall everywhere


def label_cut():
    return skadis.front_label_cut([(c[0], y) for c, y in zip(COINS, CENTRE_Y)], DEPTH, TOP - COLLAR_H / 2, LABEL_CAP,
                                  depth=LABEL_DEPTH)


def build(serial=SERIAL):
    part = skadis.back_plate(L, TOP)
    block = Pos(DEPTH / 2, L / 2, 0) * extrude(RectangleRounded(DEPTH, L, 4), TOP)
    for (label, d, t, _, _), bore, x, y in zip(COINS, BORES, CENTRE_X, CENTRE_Y):
        r = bore / 2
        block -= Pos(x, y, FLOOR_T) * Cylinder(r, INNER_H + 1, align=(Align.CENTER, Align.CENTER, Align.MIN))
        block -= Pos(x, y, TOP - 1.5) * extrude(Circle(r), 2, taper=-45)                         # flared mouth
        win_h = WINDOW_COINS * t + 0.6
        block -= Pos(x + DEPTH / 2, y, FLOOR_T + win_h / 2) * Box(DEPTH, bore, win_h)             # bottom window
        slot_w = max(10.0, bore / 2)
        block -= Pos(x + DEPTH / 2, y, (FLOOR_T + TOP - COLLAR_H) / 2) * \
            Box(DEPTH, slot_w, TOP - COLLAR_H - FLOOR_T)                                         # front slot
        notch_w = max(11.0, bore / 2)
        block -= Pos(x + DEPTH / 2, y, FLOOR_T / 2) * Box(DEPTH, notch_w, FLOOR_T + 2)          # floor notch
        block -= Pos(x, y, -1) * Cylinder(notch_w / 2, FLOOR_T + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
    part += block                  # bores cut on their own: flares would otherwise notch the hook plates
    part -= label_cut()
    for y in HOOK_Y:
        part += skadis.hooks(y, UPPER_Z)
    if serial:
        part -= skadis.serial_under(serial, B + (min(CENTRE_X) - B) / 2, L / 2, x_dir=(0, 1, 0))
    return part


def ghost():
    """Each tube about half full, for previews and the fit check."""
    g = None
    for (_, d, t, _, _), x, y in zip(COINS, CENTRE_X, CENTRE_Y):
        c = Pos(x, y, FLOOR_T) * Cylinder(d / 2, INNER_H / 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        g = c if g is None else g + c
    return g


if __name__ == "__main__":
    p = build()
    grams = sum(INNER_H / t * m for _, _, t, m, _ in COINS)
    moment = grams / 1000 * 9.81 * sum(CENTRE_X) / len(CENTRE_X) + 50 * DEPTH    # full tubes + 50 N lean
    skadis.report("Coin holder", p, HOOK_Y, moment, upper_z=UPPER_Z)
    print(f"  fit: overlap with the coins {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm; full of coins {grams:.0f} g; serial {SERIAL or 'none'}")
    for (label, d, t, _, _), b in zip(COINS, BORES):
        print(f"  {label}: bore {b:.1f}, holds {int(INNER_H // t)}, bottom window {WINDOW_COINS * t + 0.6:.1f} high")
    ink = skadis.flush_inlay(label_cut(), DEPTH)
    print(f"  black inlay: {ink.volume:.1f} mm3, {len(ink.solids())} solids, overlap with the body {(ink & p).volume:.3f} mm3")
    skadis.save_inlaid(p, ink, HERE, skadis.with_serial("coin_holder", SERIAL))
