"""THE TRAY of the bolted EVERSE 8 receiver rest: JRJP-E8R-0002, printed 2026-11, "the top fits well".
It bolts to the one-piece bottom in everse_rest_bottom.py (this folder) with 4x M5 x 25. The two jaws
below were its first bottom (M5 x 40); they and their sleeves are in Earlier designs/2. This script now
exports the tray on its own; jaw() stays because everse_rest_bottom.py and the snap-on clip
(../Snap-on clip (no screws)/everse_clip.py, which reuses tray()) import this file.

Bolt-on rest for a Sennheiser EW-DP EK receiver on the top handle of an Electro-Voice EVERSE 8,
after EV's own EVERSE8-TRAY: a tray for the EK plus two jaws, clamped round the handle bar with four
M5 bolts.

The EVERSE 8's handle is a bar running front to back across the top, over a recess: wells either
side of it and a finger gap underneath. EV's tray clips an adapter round that bar and screws the tray
to it. Here the tray's saddle sits on the bar's top face, with a skirt down each side, and two jaws
go under the bar in the finger gap. Each jaw takes two bolts that come down through the skirts,
beside the bar. Tightening them squeezes the bar between saddle and jaws, whatever its real
thickness is (bars ~11-26 mm thick work with M5 x 40).

Hardware: 4x M5 x 40 socket head cap screws, 4x M5 hex nuts, 4 mm hex key. The nuts press into the
traps under the jaws, so you only turn the bolts from above. The heads sit flush in the pocket floor
and the EK sits on top of them. Wing nuts under plain jaws would work too, but the traps are easier.

Current bottom (2026-11-10): everse_rest_bottom.py, a one-piece cradle with nut towers in place of
the two jaws, for M5 x 25 bolts, sized to my measured bar (30 wide, 25.5 thick, ~20 mm under it).
The jaws and the long-bolt sleeves are superseded; the sleeves are in Earlier designs. This tray
(JRJP-E8R-0002, printed, fits) is unchanged and takes either bottom.
Screwless alternative (2026-11-15): everse_clip.py, the same tray with snap-on clip arms instead.

Fitting: press the nuts into the jaws. Drop each jaw into a well beside the bar, swing it under the
bar so it lies across, nut side down. Set the tray on the bar (fence toward the speaker's front, as the
arrow on EV's adapter points), start each bolt into its jaw's nut, then tighten all four evenly until
it doesn't move. Not so tight that the tray plate bends.

The EK lies flat in the pocket with its display toward the back of the speaker (where you stand at the
inputs), antennas up behind it, and MIC OUT on the +x end, where a low ramp replaces the wall so
the plug clears. A tall fence on the front side stops it sliding off the front.

Handle sizes, read off EV's to-scale datasheet drawings (Fig. 1, 3.06 px/mm at 600 dpi) and EV's
straight-down product render (5.8 px/mm). Not measured on a real speaker:
  - the bar is ~30 mm wide (a ~21 mm flat top with chamfered sides) for ~140 mm between its wider
    front cap (44 mm) and the flare where it bends down the back; the channel is 34 mm.
  - the top tilts ~4 deg down toward the back, so the saddle is wedged to keep the tray level.
Print everse_rest_fit_test.py first: a 20 mm slice of the saddle with one bolt each side and a short
jaw, so the channel and the clamp can be tried on the bar with two of the bolts.

The tray covers the middle of the bar, so carry the speaker by the bar's ends or take the tray off;
don't lift the speaker by the tray.

Coordinates (in use): x across the speaker (+x = the EK's jack end), y toward the back of the speaker
(the operator side), z up from the bar's top face at the middle of the saddle.

Print pose: the tray stands on its fence face, so every wall prints upright, the back lip's inside is a
45-degree slope, and the bolt holes are horizontal teardrops. The jaws lie on their top faces, nut
traps up. No supports. PETG (outdoor gigs in the sun); PLA is fine indoors. Tray + 2 jaws on one
plate: 2h01, 46 g Generic PETG at 0.20 Standard. Fit test: 29 min, 11 g.

Run:    python everse_rest.py     -> everse_rest_<SERIAL>.stl / .3mf (the tray alone)
Slice:  ../../../tools/u1/u1-slice.sh everse_rest_<SERIAL>.3mf "0.20mm Standard" "Generic PETG"
        (not ARRANGE=0: save() puts the parts at the bed's corner, outside the print area)
"""
import math
import sys
from pathlib import Path

from build123d import Align, Box, Cylinder, Plane, Polygon, Pos, Rectangle, RegularPolygon, Rot, chamfer, extrude

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))
import skadis  # noqa: E402  (serial engraving and STL/3MF export)

# "" = no serial; new numbers for every copy and every design change. 0001 was the strap version.
SERIAL = "JRJP-E8R-0002"                                 # tray
JAW_SERIALS = ("JRJP-E8J-0001", "JRJP-E8J-0002")         # front jaw, back jaw (identical parts)

# EVERSE 8 handle (estimated from EV's drawings and renders, see above)
BAR_W = 30                                 # bar width across its narrow middle section
TILT = 4.0                                 # top of the speaker slopes down toward the back by this much

# EW-DP EK receiver: 86 x 67 x 28 mm, lying flat
RX_W, RX_D = 86, 67
PW, PD = RX_W + 2, RX_D + 2                # pocket, 1 mm play all round
LIP = 4.75                                 # side wall thickness
FENCE, FENCE_H = 4, 10                     # front fence: thickness, height above the floor
BACK_H, BACK_TOP = 5, 2                    # back lip: height, flat top (its inside is a 45-degree slope)

# saddle
THROAT = 34                                # channel width (2 mm play a side on a 30 mm bar)
SKIRT_T, SKIRT_D = 12, 6                   # skirt thickness (a bolt runs down each), depth below the bar's top
LEAD = 2                                   # lead-in chamfer on the skirts' inner bottom edges
PLATE_BOT, PLATE = 3, 5                    # tray plate underside (outside the saddle), thickness
FLOOR = PLATE_BOT + PLATE                  # pocket floor height (8 above the bar): room for the bolt heads

# bolts: M5 socket head cap screws, nuts captive in the jaws
BOLT_D, HEAD_D, HEAD_SINK = 5.5, 9.5, 5.6  # clearance hole, counterbore, counterbore depth (head is 5 tall)
NUT_AF, NUT_DEPTH = 8.2, 4.5               # M5 nut is 8.0 across flats, 4.0 thick: a snug press fit
BX = THROAT / 2 + SKIRT_T / 2              # bolts this far either side of the bar's centre line (23)
BY = 28                                    # bolt pairs this far in front of / behind the saddle's middle
BOLT_L = 40

# jaws
JAW_L, JAW_W, JAW_T = 68, 16, 9            # across the bar (fits the 61 mm serial), along it, thick

X0 = PW / 2 + LIP                          # tray half width (48.75)
SX = THROAT / 2 + SKIRT_T                  # saddle half width (29)
LEN = FENCE + PD + BACK_H + BACK_TOP       # tray length front to back (80)
Y0 = -LEN / 2                              # front edge (fence face)
Y_POCKET = Y0 + FENCE                      # pocket front
Y_PE = Y_POCKET + PD                       # pocket back, at floor level
Y_END = Y0 + LEN                           # back edge (lip face)
SIN, COS = math.sin(math.radians(TILT)), math.cos(math.radians(TILT))


def box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def prism_x(pts, x0, x1):
    """Extrude a polygon drawn as (y, z) along x from x0 to x1."""
    return Pos(x0, 0, 0) * extrude(Plane.YZ * Polygon(*pts), x1 - x0, dir=(1, 0, 0))


def prism_y(pts, y0, y1):
    """Extrude a polygon drawn as (x, z) along y from y0 to y1."""
    return Pos(0, y1, 0) * (Rot(90, 0, 0) * extrude(Polygon(*pts), y1 - y0, dir=(0, 0, 1)))


def tilted(part):
    """Tilt a bar-frame part so its +y (back) end goes down, matching the speaker's top."""
    return Rot(-TILT, 0, 0) * part


def teardrop(d, z0, z1):
    """Vertical hole of diameter d from z0 to z1, with a 45-degree point toward +y: the tray prints
    standing on its front face, so +y is up and the point keeps the hole's roof from sagging."""
    r, h = d / 2, z1 - z0
    hole = Pos(0, 0, z0) * Cylinder(r, h, align=(Align.CENTER, Align.CENTER, Align.MIN))
    point = Pos(0, 0, z0) * (Rot(0, 0, 45) * Box(2 * r, 2 * r, h, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return hole + (point & Pos(0, r * 2, z0 + h / 2) * Box(4 * r, 4 * r, h + 1))


def bar_z_for_floor_depth(y, depth):
    """Bar-frame z of the point at bar-frame y that ends up `depth` below the level pocket floor."""
    return (FLOOR - depth + y * SIN) / COS


def bolt_holes(ys):
    """Bolt holes in the bar frame: clearance down through the skirts, counterbores from the floor."""
    cut = None
    for x in (-BX, BX):
        for y in ys:
            zc = bar_z_for_floor_depth(y, HEAD_SINK + HEAD_D / 2 * math.tan(math.radians(TILT)))
            c = Pos(x, y, 0) * (teardrop(BOLT_D, -SKIRT_D - 1, FLOOR + 10) + teardrop(HEAD_D, zc, FLOOR + 10))
            cut = c if cut is None else cut + c
    return cut


def saddle(length=120, ys=(-BY, BY)):
    """Saddle in the bar's own frame (bar top = z 0), long and tall so it can be tilted then trimmed."""
    t = THROAT / 2
    outer = [(-SX, FLOOR + 8), (-SX, -SKIRT_D + 1), (-SX + 1, -SKIRT_D), (-t - LEAD, -SKIRT_D), (-t, -SKIRT_D + LEAD),
             (-t, 0), (t, 0), (t, -SKIRT_D + LEAD), (t + LEAD, -SKIRT_D), (SX - 1, -SKIRT_D), (SX, -SKIRT_D + 1),
             (SX, FLOOR + 8)]
    return prism_y(outer, -length / 2, length / 2) - bolt_holes(ys)


def tray():
    """Plate and pocket walls, level, with the pocket floor at z = FLOOR."""
    sk = Pos(0, (Y0 + Y_END) / 2) * Rectangle(2 * X0, LEN)
    outline = chamfer([v for v in sk.vertices() if v.Y > 0], 6)          # back corners
    plate = Pos(0, 0, PLATE_BOT) * extrude(outline, PLATE)
    walls = Pos(0, 0, FLOOR) * extrude(outline, FENCE_H)
    walls -= box(-PW / 2, PW / 2, Y_POCKET, Y_PE, FLOOR - 1, FLOOR + FENCE_H + 1)
    # side walls slope from the fence's height down to the back lip's
    k = (FENCE_H - BACK_H) / (Y_END - Y_POCKET)
    far = Y_END + 5
    walls -= prism_x([(Y_POCKET, FLOOR + FENCE_H), (far, FLOOR + FENCE_H - k * (far - Y_POCKET)),
                      (far, FLOOR + 40), (Y_POCKET, FLOOR + 40)], -X0 - 5, X0 + 5)
    # back lip: 45-degree inside face, so it prints without support standing on the fence
    walls -= prism_x([(Y_PE, FLOOR), (Y_PE + BACK_H, FLOOR + BACK_H), (Y_PE + BACK_H, FLOOR + 40),
                      (Y_PE, FLOOR + 40)], -PW / 2, PW / 2)
    # jack end: a low 45-degree ramp instead of a wall, clear of the MIC OUT plug
    walls -= box(PW / 2, X0 + 1, Y_POCKET, Y_PE, FLOOR, FLOOR + FENCE_H + 1)
    ramp = prism_y([(PW / 2, FLOOR), (X0, FLOOR + LIP), (X0, FLOOR)], Y_POCKET, Y_PE)
    return plate + walls + ramp


def rest():
    """The tray with its saddle, in use (bar frame at the saddle's middle, tray level)."""
    s = tilted(saddle()) & box(-SX - 1, SX + 1, Y0, Y_END, -40, FLOOR)   # trim to the tray, under the floor
    part = tray() + s - tilted(bolt_holes((-BY, BY)))                     # holes through the plate too
    if SERIAL:
        # on the back face (the operator side), low, at the right-hand end as you read it from behind
        z = PLATE_BOT + (FLOOR + BACK_H - PLATE_BOT) / 2
        cut = skadis.text_cut(SERIAL, (0, Y_END, z), (-1, 0, 0), (0, 1, 0), align=(Align.MAX, Align.CENTER))
        part -= Pos(-(X0 - 6 - 4), 0, 0) * cut
    return part


def jaw(serial=""):
    """A jaw in its own frame: top face (against the bar's underside) at z 0, nut traps underneath,
    serial on its +y face reading from behind."""
    j = box(-JAW_L / 2, JAW_L / 2, -JAW_W / 2, JAW_W / 2, -JAW_T, 0)
    j = chamfer(j.edges(), 0.8)
    for x in (-BX, BX):
        j -= Pos(x, 0, -JAW_T - 1) * Cylinder(BOLT_D / 2, JAW_T + 2, align=(Align.CENTER, Align.CENTER, Align.MIN))
        j -= Pos(x, 0, -JAW_T - 1) * extrude(RegularPolygon(NUT_AF / math.sqrt(3), 6), NUT_DEPTH + 1)
    if serial:
        j -= skadis.text_cut(serial, (0, JAW_W / 2, -JAW_T / 2), (-1, 0, 0), (0, 1, 0))
    return j


def print_pose(part):
    """Stand the tray on its fence face: +y (the back) up."""
    part = Rot(90, 0, 0) * part
    bb = part.bounding_box()
    return Pos(-bb.center().X, -bb.center().Y, -bb.min.Z) * part


def jaw_pose(part):
    """Jaw on its top face, nut traps up."""
    part = Rot(180, 0, 0) * part
    return Pos(0, 0, -part.bounding_box().min.Z) * part


def check(part):
    bb = part.bounding_box()
    print(f"tray: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm (x across, y front-back, z), "
          f"{part.volume / 1000:.1f} cm3, solids {len(part.solids())}, valid {part.is_valid}")
    j = jaw(JAW_SERIALS[0])
    print(f"jaw: {JAW_L} x {JAW_W} x {JAW_T} mm, {j.volume / 1000:.1f} cm3, solids {len(j.solids())}, valid {j.is_valid}")
    for y in (Y0, Y_END):
        print(f"  bar top under y {y:+.0f}: z {-y * math.tan(math.radians(TILT)):+.2f}")
    # each bolt: where its head seats, and the bar thickness range M5 x BOLT_L covers
    for y in (-BY, BY):
        zc = bar_z_for_floor_depth(y, HEAD_SINK + HEAD_D / 2 * math.tan(math.radians(TILT)))
        rim = FLOOR - (-y * SIN + zc * COS) - HEAD_D / 2 * math.tan(math.radians(TILT))
        # the nut sits at the top of its trap: its bottom face is (NUT_DEPTH - 4) above the jaw's bottom
        hi = BOLT_L - zc - JAW_T + (NUT_DEPTH - 4)       # thickest bar with the tip through the whole nut
        print(f"  bolts at y {y:+.0f}: head seat {zc:.2f} above the bar top (bar frame), head sunk "
              f"{rim:.2f} below the floor at its shallow edge; M5x{BOLT_L} takes a full nut on bars up to "
              f"{hi:.1f} mm thick, sticks out {BOLT_L - zc - JAW_T - 20:.1f} mm under the jaw on a 20 mm bar")
    # nothing of the tray below the skirts, and the skirts clear the bar
    lb = part.bounding_box()
    print(f"  tray lowest point z {lb.min.Z:.1f}; channel {THROAT} on a {BAR_W} bar")


if __name__ == "__main__":
    part = rest()
    check(part)
    name = skadis.with_serial("everse_rest", SERIAL)          # the tray alone; the jaws are retired
    skadis.save(print_pose(part), HERE, name, settings={})
    print(f"wrote {name}.stl / .3mf")
