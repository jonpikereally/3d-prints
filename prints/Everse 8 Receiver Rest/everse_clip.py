"""Snap-on rest for a Sennheiser EW-DP EK receiver on the EVERSE 8's top handle: no screws, one piece.
The same tray and pocket as everse_rest.py (JRJP-E8R-0002, printed, "the top fits well"), but instead
of skirts, bolts and a bottom piece it has a springy clip arm down each side of the handle bar,
running the tray's full length, with a hook along its bottom that snaps under the bar's bottom edge.

Bar, measured by me 2026-11-10: 30 mm wide, 25.5 mm thick, ~20 mm of room under it. I printed the
first fit test (JRJP-E8R-0003's clip, gripping 25.5) 2026-11-15: "width is good, but try again 15% less
tall" -> 21.7 mm (JRJP-E8R-0004). Its fit test, also printed: "try 8% less tall" (than that one) ->
the grip height (pad on the bar's top face to the hooks) is now 20.0 mm (JRJP-E8R-0005, printed 2026-11-16:
"the snap-on design works"). 0006: the handle's top face is rounded, not flat, so the pad's underside is now
a shallow arc (0.6 mm deeper at its edges than its middle, radius 120) that cups it instead of touching only
along its middle. The middle stays where 0005's flat pad was, so the grip is unchanged; the crown wasn't
measured, so it errs shallow (too deep would let the edges touch first and tighten the grip). Arms, hooks,
plate and tray are unchanged. 0007 (2026-11-16, before printing 0006): "a bit deeper, like 1 mm":
CROWN 0.6 -> 1.0 (radius 72). 0008 (same day, before printing either): the top isn't curved, "a level
middle and then angles off the sides. its level about 18.5mm wide, then angles down and goes about 5mm lower
than the top of the handle". So the pad is flat again in the middle (where 0005's touched, grip unchanged),
and wider (25 mm) with its sides angled down to follow the handle's slopes, 0.5 mm clear of them, so it sits
on the flat and the slopes keep it centred. Assumed: the slopes reach their 5 mm at the handle's 30 mm
width (about 41 deg). The pad ends 2.8 mm short of each arm so the arms flex exactly as before.
0008 printed 2026-11-16: "the design works well". 0009: "try it with the arms 15% shorter" (the part
that snaps on): grip height 20.0 -> 17.0, the hooks 3 mm higher; everything else as 0008.
0009's fit test printed 2026-11-16: "make the arms 2mm shorter" -> 0010: grip 15.0.
0003-0009 and their fit tests are in Earlier designs/3 to /9.

Putting it on: hook one arm under its side of the bar first, then press the other side down until it
clicks (only one arm has to flex at a time, about 13 kg of push). Straight down onto both at once is
about twice that. Taking it off: pull one arm's tab outward (it sits in the recess beside the bar) and
lift that side. It's meant not to come off by lifting alone: the hooks' holding faces are 35 deg, so a
straight pull needs about 42 kg. (Estimates for PETG, E = 2 GPa, friction 0.3.)

Clip geometry (bar frame, see everse_rest.py): arm inner faces 0.3 mm off the bar's sides, 2.2 mm
thick, flexing from the plate's underside; hook catches 2 mm under the bar with 0.2 mm vertical play,
holding face 35 deg, 45-deg lead-in ramp. A pad on the bar's top face (24 mm wide) carries the weight.
Everything below the plate is sized to my measurements; the bar's bottom edges are assumed square
(a rounded edge still catches on the sloped holding face). Print everse_clip_fit_test.py first: a
20 mm slice of the clip, 23 min 7 g, to feel the snap and check the hooks catch.

Print pose: standing on its front (fence) face like everse_rest, so the arms are upright walls the full
height of the print, the hooks and tabs are vertical faces, and the tabs' undersides are 45 deg. No
supports. JRJP-E8R-0010: 1h43, 44 g Generic PETG at 0.20 Standard. PETG (springier and tougher than PLA, and outdoor sun). The arms flex 2 mm: about 1.2%
strain, well inside PETG's range for repeated snapping.

Run:    python everse_clip.py      -> everse_clip_<SERIAL>.stl / .3mf
Slice:  ../../../tools/u1/u1-slice.sh everse_clip_<SERIAL>.3mf "0.20mm Standard" "Generic PETG"
"""
import math
import sys
from pathlib import Path

from build123d import Align, Polygon, Pos, extrude

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
                                         # everse_rest.py (copied beside it): the tray it shares
sys.dont_write_bytecode = True
import everse_rest as r  # noqa: E402  (tray, frames, helpers)
import skadis  # noqa: E402  (on sys.path via everse_rest)

SERIAL = "JRJP-E8R-0010"                   # "" = no serial; new number for every copy and every design change

BAR_W = 30.0                               # measured; the first fit test confirmed it
BAR_T = 15.0                               # grip height, pad to hooks: 25.5, 21.7, 20.0 (0005-0008), 17.0, then 15.0
PLAY = 0.3                                 # each side, arm to bar
VPLAY = 0.2                                # hook below the bar's underside
ARM_T = 2.2                                # arm thickness (sets snap force)
CATCH = 2.0                                # how far each hook reaches under the bar
HOLD = 35.0                                # holding face, degrees from horizontal
LEAD = 45.0                                # lead-in ramp, degrees from horizontal
TIP = 0.6                                  # flat on the hook tip
PAD_W = 25.0                               # pad on the bar's top face
TOP_FLAT = 18.5                            # handle's level top, 2026-11-16
EDGE_DROP = 5.0                            # its sides angle down this far by the handle's full width
SLOPE_PLAY = 0.5                           # pad's sloped sides this far (sideways) clear of the handle's
TAB_OUT, TAB_LEN, TAB_H = 6.0, 16.0, 4.0   # pull tabs: reach outward, length along the bar, height
E_PETG = 2000.0                            # MPa, for the force estimate

XI = BAR_W / 2 + PLAY                      # arm inner face (15.3)
XO = XI + ARM_T                            # arm outer face (17.5)
Z_HOLD = -BAR_T - VPLAY                    # holding face starts here at the arm's inner face
Z_TIP_TOP = Z_HOLD - CATCH * math.tan(math.radians(HOLD))
Z_TIP_BOT = Z_TIP_TOP - TIP
Z_BOT = Z_TIP_BOT - (XO - (XI - CATCH)) * math.tan(math.radians(LEAD))   # arm bottom, outer face
Z_TOP = r.FLOOR + 10                       # build tall, trim at the floor after tilting


def arm_profile(side):
    """Arm + hook cross-section (x, z) for side = +1 / -1."""
    pts = [(XI, Z_TOP), (XO, Z_TOP), (XO, Z_BOT), (XI - CATCH, Z_TIP_BOT), (XI - CATCH, Z_TIP_TOP), (XI, Z_HOLD)]
    return [(side * x, z) for x, z in pts]


def tab(side, length=TAB_LEN):
    """Pull tab on an arm's outer face at its bottom, centred along the bar. Its -y edge is 45 deg so it
    prints standing on the tray's front face."""
    x0, x1, h = XO - 0.5, XO + TAB_OUT, length / 2
    pts = [(x0, -h), (x1, -h + TAB_OUT + 0.5), (x1, h), (x0, h)]
    sk = Polygon(*[(side * x, y) for x, y in pts])
    return Pos(0, 0, Z_BOT) * extrude(sk, TAB_H, dir=(0, 0, 1))   # mirrored outline winds the other way


def bar_top_z(x):
    """Height of the handle's top surface at x: level across TOP_FLAT, then sloping down to -EDGE_DROP
    at the handle's sides."""
    run = abs(x) - TOP_FLAT / 2
    return 0.0 if run <= 0 else -run * EDGE_DROP / (BAR_W / 2 - TOP_FLAT / 2)


def pad_z(x):
    """Pad underside at x: the handle's profile moved SLOPE_PLAY outward on each side."""
    return bar_top_z(max(0.0, abs(x) - SLOPE_PLAY))


def pad(length):
    """Pad on the handle's top: flat on its level middle (at z 0, where 0005's flat pad sat, so the tested
    grip height is measured from here), with angled sides that follow the handle's slopes to keep it centred."""
    h, f = PAD_W / 2, TOP_FLAT / 2 + SLOPE_PLAY
    pts = [(-h, pad_z(h)), (-f, 0), (f, 0), (h, pad_z(h)), (h, Z_TOP), (-h, Z_TOP)]
    return r.prism_y(pts, -length / 2, length / 2)


def clip(length=120, tab_len=TAB_LEN):
    """Pad, arms, hooks and tabs in the bar frame (bar top = z 0), long so they can be tilted then trimmed."""
    part = pad(length)
    for side in (-1, 1):
        part += r.prism_y(arm_profile(side), -length / 2, length / 2)
        if tab_len:
            part += tab(side, tab_len)
    return part


def rest():
    c = r.tilted(clip()) & r.box(-r.X0, r.X0, r.Y0, r.Y_END, -60, r.FLOOR)
    part = r.tray() + c
    if SERIAL:
        z = r.PLATE_BOT + (r.FLOOR + r.BACK_H - r.PLATE_BOT) / 2
        cut = skadis.text_cut(SERIAL, (0, r.Y_END, z), (-1, 0, 0), (0, 1, 0), align=(Align.MAX, Align.CENTER))
        part -= Pos(-(r.X0 - 6 - 4), 0, 0) * cut
    return part


def snap_force(length):
    """Spread force per arm (N) to push the hooks 2 mm out, and the arm's root strain, for an arm
    `length` long, flexing from the plate's underside (bar-frame z = PLATE_BOT) down to the hook."""
    L = r.PLATE_BOT - Z_HOLD
    inertia = length * ARM_T ** 3 / 12
    f = 3 * E_PETG * inertia * CATCH / L ** 3
    return f, 3 * ARM_T * CATCH / (2 * L ** 2), L


def check(part):
    bb = part.bounding_box()
    print(f"clip tray: {bb.size.X:.1f} x {bb.size.Y:.1f} x {bb.size.Z:.1f} mm, {part.volume / 1000:.1f} cm3, "
          f"solids {len(part.solids())}, valid {part.is_valid}")
    print(f"  hooks: holding face from z {Z_HOLD:.1f} to {Z_TIP_TOP:.2f}, arm bottom {Z_BOT:.2f} "
          f"({-BAR_T - Z_BOT:.1f} below the bar, room ~20)")
    f, strain, L = snap_force(r.LEN)
    mu = math.degrees(math.atan(0.3))
    push = f * math.tan(math.radians(LEAD + mu))
    pull = f / math.tan(math.radians(HOLD - mu))
    print(f"  arm: free length {L:.1f}, spread force {f:.0f} N per side, root strain {strain * 100:.2f}%")
    print(f"  push on one side at a time ~{push:.0f} N ({push / 9.81:.1f} kg); both at once ~{2 * push:.0f} N; "
          f"straight pull-off ~{2 * pull:.0f} N ({2 * pull / 9.81:.0f} kg)")
    # nothing overlaps the bar (bar frame box, tilted like the speaker)
    h, f = BAR_W / 2, TOP_FLAT / 2
    bar = r.tilted(r.prism_y([(-h, -BAR_T), (h, -BAR_T), (h, -EDGE_DROP), (f, 0), (-f, 0), (-h, -EDGE_DROP)], -70, 70))
    print(f"  pad: flat {TOP_FLAT + 2 * SLOPE_PLAY} mm, sides down {-pad_z(PAD_W / 2):.2f} mm at {PAD_W} wide, "
          f"{XI - PAD_W / 2:.1f} mm gap to each arm")
    print(f"  overlap with a {BAR_W} x {BAR_T} handle, {TOP_FLAT} flat top, sides {EDGE_DROP} down: {(part & bar).volume:.3f} mm3")


if __name__ == "__main__":
    part = rest()
    check(part)
    name = skadis.with_serial("everse_clip", SERIAL)
    skadis.save(r.print_pose(part), HERE, name, settings={})
    print(f"wrote {name}.stl / .3mf")
