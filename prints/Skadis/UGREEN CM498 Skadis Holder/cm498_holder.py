#!/usr/bin/env python3
"""SKÅDIS storage cup for a UGREEN PB205 power bank and a UGREEN CM498 9-in-1 USB-C hub (15600), both
standing sideways on a long edge, one behind the other.

The power bank stands in the back pocket, flat face against the plate. The hub stands in a front
pocket, leaning back on the power bank. (Side by side the holder would be ~287 mm wide, more than the
U1's 270 mm bed.) All the cup walls are only WALL_H tall, so both stick up out of the cup where you can
grab them. Each end wall of the hub pocket has a 6.5 mm slot down to the floor, so the hub's attached
USB-C cable lies in it and hangs outside, whichever way round the hub goes in. A small hook on the
front near each end is an open-top channel 4.5 mm wide: bring the cable round the corner from the slot
and tuck it down into the hook. The floors are open apart
from ledges, so ports on the bottom edges rest on nothing.

Sizes mostly from retailer listings; print the fit test first:
  PB205 (25,000 mAh, 145 W): about 160 x 80 x 26.7 mm, 0.51 kg (one catalogue says 20 mm thick)
  CM498 9-in-1: 140 mm long (measured, roughly); 48 x 15 mm and 90 g from a listing

The back wall is the plate: hook height is the SKÅDIS minimum, 48.3 mm. Two hook columns 120 apart;
tabs 8 mm thick (behind the board). To hang: lift ~6.5 mm, push all four hooks through, let it drop.
(Earlier designs: JRJP-CMH-0001, the hub on its own; JRJP-CMH-0002, without the cable slots;
JRJP-CMH-0003, without the cleats; JRJP-CMH-0004, cable cleats instead of hooks;
JRJP-CMH-0005, sized for a 115 mm hub.)

A serial number (SERIAL below) is engraved underneath, along the front ledge, reading from below.
Change it per copy before exporting ("" = off).

Prints upright on its floor; the 3MF carries tree supports (build plate only) for the hook tabs.
Run with python; writes cm498_pb205_holder_<SERIAL>.stl/.3mf next to this file.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))   # tools/u1
import skadis  # noqa: E402
from build123d import Box, Cylinder, Pos, RectangleRounded, extrude  # noqa: E402

SERIAL = "JRJP-CMH-0006"         # JRJP- starts every serial; change the number per copy; "" = off

# (along the board, out from it, standing height, kg)
BANK = (160.0, 26.7, 80.0, 0.51)   # UGREEN PB205
HUB = (140.0, 15.0, 48.0, 0.09)    # UGREEN CM498 9-in-1 (length measured by me)
CLEAR, RADIUS = 0.75, 2.0          # play per side; pocket corner radius
FLOOR_T, WALL, TAB_T = 3.0, 3.0, 8.0
WALL_H = 18.0                      # all cup walls but the plate
LEDGE_END, LEDGE_SIDE, LEDGE_FRONT = 8.0, 3.0, 5.0   # floor left under each unit (hub's front: serial)
CABLE_W = 6.5                      # slot in each of the hub pocket's end walls for its attached USB-C cable
CLIP_DY = 58.0                     # a cable hook on the front this far each side of centre
CLIP_W, CLIP_GAP, CLIP_T = 12.0, 4.5, 2.5   # hook width along the board; channel width; lip thickness
CLIP_FLOOR, CLIP_TOP = 10.0, 18.0  # channel floor and lip top heights
CLIP_OUT = CLIP_GAP + CLIP_T       # sticks out this far from the front wall
UPPER_Z = skadis.MIN_UPPER_Z
PLATE_H = skadis.MIN_TOP
B = skadis.BACK_T

BW, BD = BANK[0] + 2 * CLEAR, BANK[1] + 2 * CLEAR   # bank pocket
HW, HD = HUB[0] + 2 * CLEAR, HUB[1] + 2 * CLEAR     # hub pocket
W_OUT = BW + 2 * WALL
YC = W_OUT / 2
HOOK_Y = [YC - 60.0, YC + 60.0]
BX = B + BD / 2                    # bank pocket centre; its back wall is the plate
HX = B + BD + WALL + HD / 2        # hub pocket centre, behind it the divider
DEPTH = HX + HD / 2 + WALL
SERIAL_X = HX + HD / 2 - LEDGE_FRONT / 2 + WALL / 2   # middle of the hub's front ledge + wall strip


def pocket_cut(cx, d, w, back, front):
    """Pocket centred at X = cx (d out, w along) from the floor up, and its floor opening."""
    cut = Pos(cx, YC, FLOOR_T) * extrude(RectangleRounded(d, w, RADIUS), PLATE_H)
    od = d - back - front
    cut += Pos(cx - d / 2 + back + od / 2, YC, -1) * extrude(
        RectangleRounded(od, w - 2 * LEDGE_END, 2.0), FLOOR_T + 2)
    return cut


def cable_slots():
    """A slot down each end wall of the hub pocket to the floor, centred on the hub's thickness, so its
    attached cable can lie in it and hang outside, whichever way round the hub goes in."""
    cut = None
    for s in (-1, 1):
        y = YC + s * (HW / 2 + WALL / 2)
        c = Pos(HX, y, FLOOR_T + CABLE_W / 2) * Cylinder(CABLE_W / 2, WALL + 2, rotation=(90, 0, 0)) + \
            Pos(HX, y, FLOOR_T + CABLE_W / 2 + 25) * Box(CABLE_W, WALL + 2, 50)
        cut = c if cut is None else cut + c
    return cut


def clip(yc):
    """A small cable hook on the hub pocket's front face, centred at Y = yc: an open-top channel CLIP_GAP
    wide between the wall and an upstanding lip. Its underside rises at 45 degrees from the wall, so
    it prints without supports."""
    x0, x1 = DEPTH - 0.5, DEPTH + CLIP_OUT                  # sunk into the wall so they fuse
    zu = CLIP_FLOOR - 2.0                                   # 2 mm floor under the channel at the lip
    pts = [(x0, zu - (x1 - x0)), (x1, zu), (x1, CLIP_TOP - 0.8), (x1 - 0.8, CLIP_TOP),
           (DEPTH + CLIP_GAP, CLIP_TOP), (DEPTH + CLIP_GAP, CLIP_FLOOR), (x0, CLIP_FLOOR)]
    return skadis.profile_solid(pts, CLIP_W, yc - CLIP_W / 2)


def build(serial=SERIAL):
    part = Pos(BX, YC, 0) * extrude(RectangleRounded(BD + 2 * WALL, W_OUT, RADIUS + WALL), WALL_H)
    part += Pos(HX, YC, 0) * extrude(RectangleRounded(HD + 2 * WALL, HW + 2 * WALL, RADIUS + WALL), WALL_H)
    part += Pos(B / 2, YC, PLATE_H / 2) * Box(B, W_OUT, PLATE_H)              # the plate, full height
    part += Pos(BX / 2, YC, WALL_H / 2) * Box(BX, W_OUT, WALL_H)              # square back, flat on the board
    part -= pocket_cut(BX, BD, BW, LEDGE_SIDE, LEDGE_SIDE)
    part -= pocket_cut(HX, HD, HW, LEDGE_SIDE, LEDGE_FRONT)
    part -= cable_slots()
    for s in (-1, 1):
        part += clip(YC + s * CLIP_DY)
    for y in HOOK_Y:
        part += skadis.hooks(y, upper_z=UPPER_Z, tab_t=TAB_T)
    if serial:
        part -= skadis.serial_under(serial, SERIAL_X, YC, x_dir=(0, 1, 0))
    return part


def ghosts():
    """The power bank and hub standing in place, for the fit check."""
    return [Pos(cx, YC, FLOOR_T + u[2] / 2) * Box(u[1], u[0], u[2]) for cx, u in ((BX, BANK), (HX, HUB))]


if __name__ == "__main__":
    p = build()
    moment = BANK[3] * 9.81 * BX + HUB[3] * 9.81 * HX + 50 * (DEPTH + CLIP_OUT)    # stored + 50 N lean on the front
    skadis.report("PB205 + CM498 cup", p, HOOK_Y, moment, upper_z=UPPER_Z, tab_t=TAB_T)
    overlap = sum((g & p).volume for g in ghosts())
    print(f"  fit: overlap with the units {overlap:.3f} mm3; bank pocket {BD:.1f} x {BW:.1f}, hub pocket "
          f"{HD:.1f} x {HW:.1f}; {W_OUT:.1f} wide, {DEPTH:.1f} out; serial {SERIAL or 'none'}")
    skadis.save(p, HERE, skadis.with_serial("cm498_pb205_holder", SERIAL))
