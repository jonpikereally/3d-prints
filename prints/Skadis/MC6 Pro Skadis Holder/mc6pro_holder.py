#!/usr/bin/env python3
"""SKÅDIS shelf for storing the Morningstar MC6 PRO lying flat: footswitches up, jacks to the wall.

MC6 PRO size: I measured mine at 180 x 92 mm (length x front to back, body). Published figures
disagree: an owner on the Morningstar forum and retailers give 180 x 98-100 x 50 (70 over the
footswitches, ~0.6 kg), and the tech-spec block on morningstar.io's MC6 PRO page is the MC8 PRO's
(260 x 123 x 52), so trust a ruler. Its rear jacks stick out up to 10 mm past that (after the
first print, JRJP-MSH-0001, had only 4 mm behind it), so BACK_GAP is 12.

Built with tools/u1/skadis.py like the other SKÅDIS holders: a pocket 4 mm bigger than the
unit plus the jack gap, a 12 mm front lip, end walls that brace it, an open floor frame, and a back
plate full thickness at the two hook columns (160 mm apart) and a 2 mm web between them. The first
print had an open gap there and strung on every layer as the nozzle crossed it. Tabs are 8 mm thick
(behind the board). To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath the right-hand end, running front to back and
reading from below, so it can be read with the shelf hung. Change it per copy before exporting ("" =
off). The fit test (one hook column on a 10 mm strip of back plate) gets none.

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes mc6pro_holder_<SERIAL>.stl/.3mf and mc6pro_holder_fit_test.stl/.3mf.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos  # noqa: E402

SERIAL = "JRJP-MSH-0002"           # JRJP- starts every serial; change the number per copy; "" = off

UNIT_L, UNIT_D, UNIT_H = 180.0, 92.0, 50.0    # length, front to rear panel (body), body height
UNIT_KG = 0.6
JACKS = 10.0                       # how far the rear jacks stick out past the body
SIDE_CLEAR, FRONT_CLEAR = 2.0, 2.0
BACK_GAP = JACKS + 2.0             # rear panel to back plate
WALL_T, STRIP, TAB_T = 4.0, 18.0, 8.0
INNER_L = UNIT_L + 2 * SIDE_CLEAR
INNER_D = BACK_GAP + UNIT_D + FRONT_CLEAR
L = INNER_L + 2 * WALL_T
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]


def build(serial=SERIAL):
    part, length, depth, _ = skadis.shelf(INNER_L, INNER_D, HOOK_Y, wall_t=WALL_T, strip=STRIP, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, depth / 2, length - (WALL_T + STRIP) / 2)
    return part


def fit_test():
    """One hook column on a 10 mm strip of back plate: checks the hooks drop in and hold before the full print."""
    z0 = skadis.UPPER_SLOT_Z - skadis.SLOT_PITCH - skadis.SLOT_SEAT - 4
    yc = HOOK_Y[0]
    return Pos(skadis.BACK_T / 2, yc, (z0 + skadis.BACK_H) / 2) * Box(skadis.BACK_T, 10, skadis.BACK_H - z0) + \
        skadis.hooks(yc, tab_t=TAB_T)


def ghost():
    """The MC6 PRO body and its jacks in place, for previews and the fit check."""
    x0, y0 = skadis.BACK_T + BACK_GAP, WALL_T + SIDE_CLEAR
    body = Pos(x0 + UNIT_D / 2, y0 + UNIT_L / 2, 3 + UNIT_H / 2) * Box(UNIT_D, UNIT_L, UNIT_H)
    return body + Pos(x0 - JACKS / 2, y0 + UNIT_L / 2, 3 + 25) * Box(JACKS, UNIT_L - 20, 30)


if __name__ == "__main__":
    p = build()
    depth = skadis.BACK_T + INNER_D + 3.5
    moment = UNIT_KG * 9.81 * (skadis.BACK_T + BACK_GAP + UNIT_D / 2) + 50 * depth   # stored + 50 N lean
    skadis.report("MC6 PRO shelf", p, HOOK_Y, moment, tab_t=TAB_T)
    print(f"  fit: overlap with the MC6 and its jacks {(ghost() & p).volume:.3f} mm3; pocket {INNER_L:.0f} x "
          f"{INNER_D:.0f}, sticks out {depth:.1f} mm; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("mc6pro_holder", SERIAL))
    skadis.save(fit_test(), HERE, "mc6pro_holder_fit_test")
