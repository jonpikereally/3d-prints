#!/usr/bin/env python3
"""SKÅDIS holder for four Sennheiser EW-D / EW G4 handheld mics, hanging head-up side by side,
labelled MIC 1-4 like the bodypack holder, the Wireless Caddy and the cable tags. Its partner for
four bodypacks is in ../EW-D Bodypack Skadis Holder.

Handhelds: the EW-D SKM body is Ø40 (handles run Ø38.6-41.5) under a Ø50 head, so each drops
through a Ø44.5 hole and hangs by its head on a chamfered collar, heads 6 mm apart. The bodies hang
about 210 mm below the holder, 10 mm clear of the board, so keep that space free under it. A front
lip carries the labels (DIN Alternate Bold 7 mm, inlaid in black filament). Back plate full thickness only at the two hook
columns, 160 mm apart. To hang: lift ~6.5 mm, push all four hooks through, let it drop.

A serial number (SERIAL below) is engraved underneath, along the front strip in front of the holes,
reading from below. Change it per copy before exporting ("" = off).

Two colours: body on toolhead 1, labels on toolhead 2 (load black there). Prints upright on its floor;
the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes ewd_handheld_holder_<SERIAL>.3mf next to this file and body and
label STLs in parts/. Slice with ARRANGE=0 and two filaments ("A;B").
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Align, Box, Cone, Cylinder, Pos  # noqa: E402

SERIAL = "JRJP-EWM-0002"          # JRJP- starts every serial; change the number per copy; "" = off
LABELS = ["MIC 1", "MIC 2", "MIC 3", "MIC 4"]  # left to right

HEAD_D = 50.0                      # handheld head: it rests on the collar
RING_ID = 44.5                     # hole the handle drops through (handles up to Ø41.5)
COLLAR_OD, COLLAR_H = 54.0, 2.0    # raised ring round the hole, chamfered to centre the head
HEAD_GAP = 6.0                     # between neighbouring heads
PLATE_T, LIP_T, LIP_H = 4.0, 3.0, 16.0          # floor plate; front lip and its height above the plate
LABEL_CAP = 7.0
RAIL_H = PLATE_T + LIP_H           # back plate height between the hook columns
B = skadis.BACK_T
RING_X = B + 2.5 + HEAD_D / 2      # heads clear the back plate by 2.5 mm
RING_Y = [4 + HEAD_D / 2 + i * (HEAD_D + HEAD_GAP) for i in range(len(LABELS))]
L = RING_Y[-1] + HEAD_D / 2 + 4
DEPTH = RING_X + HEAD_D / 2 + 2.5 + LIP_T      # lip clears the heads by 2.5 mm
HOOK_Y = [L / 2 - 80.0, L / 2 + 80.0]


def label_cut():
    return skadis.front_label_cut(list(zip(LABELS, RING_Y)), DEPTH, PLATE_T + LIP_H / 2, LABEL_CAP)


def build(serial=SERIAL):
    part = skadis.back_plate(L)
    part -= skadis.back_windows(-20.0, L + 20.0, HOOK_Y, RAIL_H, span=(0, L))
    part += Pos(DEPTH / 2, L / 2, PLATE_T / 2) * Box(DEPTH, L, PLATE_T)                    # floor plate
    part += skadis.profile_solid([(DEPTH - LIP_T, 0), (DEPTH, 0), (DEPTH, PLATE_T + LIP_H - 1),
                                  (DEPTH - 1, PLATE_T + LIP_H), (DEPTH - LIP_T, PLATE_T + LIP_H)], L)
    for y in RING_Y:
        part += Pos(RING_X, y, PLATE_T) * Cylinder(COLLAR_OD / 2, COLLAR_H, align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos(RING_X, y, -1) * Cylinder(RING_ID / 2, PLATE_T + COLLAR_H + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        part -= Pos(RING_X, y, PLATE_T + COLLAR_H - 1.5) * Cone(RING_ID / 2, RING_ID / 2 + 1.6, 1.6,
                                                                 align=(Align.CENTER, Align.CENTER, Align.MIN))
    part -= label_cut()
    for y in HOOK_Y:
        part += skadis.hooks(y)
    if serial:
        hole_front = RING_X + RING_ID / 2
        part -= skadis.serial_under(serial, (hole_front + DEPTH) / 2, L / 2, x_dir=(0, 1, 0))
    return part


def ghost():
    """Four handhelds: head above the collar, body hanging below, for previews and the fit check."""
    g = None
    for y in RING_Y:
        m = Pos(RING_X, y, PLATE_T + COLLAR_H) * Cylinder(HEAD_D / 2, 55, align=(Align.CENTER, Align.CENTER, Align.MIN))
        m += Pos(RING_X, y, PLATE_T + COLLAR_H) * Cylinder(20.75, 210, align=(Align.CENTER, Align.CENTER, Align.MAX))
        g = m if g is None else g + m
    return g


if __name__ == "__main__":
    p = build()
    moment = len(LABELS) * 0.25 * 9.81 * RING_X + 50 * DEPTH            # four ~250 g mics + 50 N lean
    skadis.report("EW-D handheld holder", p, HOOK_Y, moment)
    print(f"  fit: overlap with the mics {(ghost() & p).volume:.3f} mm3; {L:.1f} mm wide, sticks out "
          f"{DEPTH:.1f} mm; serial {SERIAL or 'none'}")
    ink = skadis.flush_inlay(label_cut(), DEPTH)
    print(f"  black inlay: {ink.volume:.1f} mm3, {len(ink.solids())} solids, overlap with the body {(ink & p).volume:.3f} mm3")
    skadis.save_inlaid(p, ink, HERE, skadis.with_serial("ewd_handheld_holder", SERIAL))
