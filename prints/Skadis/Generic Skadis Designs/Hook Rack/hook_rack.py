#!/usr/bin/env python3
"""SKÅDIS hook rack, modelled on IKEA's white SKÅDIS hook rack 405.198.87: a 28 cm x 3 cm strip with 13
small upturned hooks along its bottom front edge, for keys, scissors, tape rolls and small cables.

IKEA lists 28 cm long x 3 cm tall x 3 cm deep; hook count and shape are read off their product photo,
not measured. At 3 cm it's too short for the standard hook + lower peg pair (they need 48 mm), so
like IKEA's it hangs from upper tongues only: three, 120 mm apart (columns a multiple of 40 apart sit
at the same height). The long rail pressing on the board stops it tipping; the tabs behind the board
stop it pulling off. To hang: lift ~6.5 mm, push the three tongues through, let it drop.

Prints UPRIGHT, back plate standing, hooks flat on the bed (so a load bends them along the layers);
the 3MF carries tree supports (build plate only) for the three tabs. 280 mm is longer than the U1's
270 mm bed, so the 3MF turns it 45 degrees on the plate.

Serial (SERIAL below) is engraved on the back, right of centre between two tongues, reading from
behind. "" = off. One file, printed once per rack you want.

Run with python; writes hook_rack_<SERIAL>.stl/.3mf next to this file, centred on the bed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Pos, Rot  # noqa: E402

SERIAL = "JRJP-HRK-0001"           # JRJP- first; one file, printed as many times as needed; "" = off

LENGTH = 280.0                     # IKEA: 28 cm, along the board (y -140..140)
HEIGHT = 30.0                      # IKEA: 3 cm
REACH = 30.0                       # IKEA: 3 cm out from the board, hooks included
PLATE_T = 5.0
HOOK_Y = [-120.0, 0.0, 120.0]      # tongue columns, 120 apart
UPPER_Z = 27.0                     # upper slot centre: tongue top 4.2 mm under the plate top
N, PITCH = 13, 20.0                # small hooks along the front
HOOK_W, ARM_H = 6.0, 6.0           # each hook's width along the board and its arm height (on the bed)
TIP_T, TIP_H = 4.0, 12.0           # upturned tip: thickness, top above the bed
TAB_T = 8.0
SERIAL_Y, SERIAL_Z = 60.0, 8.0     # serial centre on the back face


def tongue(yc):
    """skadis.hooks() without its lower peg (that slot is 40 mm below, past this strip's bottom)."""
    h = skadis.hooks(yc, upper_z=UPPER_Z, tab_t=TAB_T)
    return h & Pos(-10, yc, UPPER_Z) * Box(20, 20, 2 * (skadis.SLOT_SEAT + skadis.TAB_DROP + 1))


def small_hook(yc):
    x0 = PLATE_T - 0.5
    pts = [(x0, 0), (REACH, 0), (REACH, TIP_H - 1), (REACH - 1, TIP_H), (REACH - TIP_T, TIP_H),
           (REACH - TIP_T, ARM_H + 1.5), (REACH - TIP_T - 1.5, ARM_H), (x0, ARM_H)]
    return skadis.profile_solid(pts, HOOK_W, yc - HOOK_W / 2)


def build(serial=SERIAL):
    plate = skadis.profile_solid([(0, 0), (PLATE_T, 0), (PLATE_T, HEIGHT - 1.5), (PLATE_T - 1.5, HEIGHT),
                                  (0, HEIGHT)], LENGTH, -LENGTH / 2)
    part = plate
    for i in range(N):
        part += small_hook((i - (N - 1) / 2) * PITCH)
    for y in HOOK_Y:
        part += tongue(y)
    if serial:
        part -= skadis.text_cut(serial, (0, SERIAL_Y, SERIAL_Z), (0, -1, 0), (-1, 0, 0))
    return part


def check(part):
    bb = part.bounding_box()
    behind = (part & (Pos(-50, 0, 0) * Box(100, 2000, 2000))).volume
    one = tongue(0).volume
    print(f"Hook rack: {bb.size.X:.1f} out x {bb.size.Y:.1f} along x {bb.size.Z:.1f} tall, "
          f"{part.volume / 1000:.1f} cm3, solids {len(part.solids())}, valid {part.is_valid}")
    print(f"  behind the board: {'tongues only' if abs(behind - 3 * one) < 0.5 else 'SOMETHING ELSE TOO'}")
    moment = 3.0 * 9.81 * (REACH - TIP_T / 2)          # 3 kg spread over the hooks
    pull, mpa = skadis.tab_stress(moment, len(HOOK_Y), UPPER_Z, TAB_T)
    print(f"  3 kg on the hooks: {pull:.1f} N per tab, {mpa:.1f} MPa at the tab root")
    for bname, seat, lifts, off in skadis.sim_board(part, HOOK_Y[1], UPPER_Z):
        ok = f"drops in when lifted {lifts[0]:.1f}-{lifts[-1]:.1f} mm" if lifts else "DOES NOT GO IN"
        print(f"  {bname}: seats {seat:+.2f}, {ok}, lift {off:.1f} mm to remove")
    sb = skadis.text_cut(SERIAL, (0, SERIAL_Y, SERIAL_Z), (0, -1, 0), (-1, 0, 0)).bounding_box()
    print(f"  serial y {sb.min.Y:.1f}..{sb.max.Y:.1f}, z {sb.min.Z:.1f}..{sb.max.Z:.1f}; "
          f"tongues at y {HOOK_Y}, {skadis.HOOK_W} wide")


if __name__ == "__main__":
    p = build()
    check(p)
    skadis.save(Rot(0, 0, 45) * p, HERE, skadis.with_serial("hook_rack", SERIAL), center=True)
