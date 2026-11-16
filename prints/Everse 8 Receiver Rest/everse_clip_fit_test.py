"""Fit test for everse_clip.py: a 20 mm slice of the snap clip (pad, both arms with their hooks, a stub of
the plate, and a short pull tab on each side), to snap onto the EVERSE 8's handle bar before the full
print. No tray, no serial. 23 minutes, 7 g PETG.

It should click on with a firm press, sit snug with almost no rattle, and not lift off without pulling a
tab outward. It's a quarter of the clip's length, so it snaps on with about a quarter of the force.
If it won't go on, rattles, or the hooks don't catch, tell me which, and whether the bar's bottom edges
are rounded.

Run:    python everse_clip_fit_test.py    -> everse_clip_fit_test.stl
Slice:  ../../../tools/u1/u1-slice.sh everse_clip_fit_test.stl "0.20mm Standard" "Generic PETG"
"""
import sys
from pathlib import Path

from build123d import Pos, Rot, export_stl

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import everse_clip as c  # noqa: E402
import everse_rest as r  # noqa: E402

LENGTH = 20                                # along the bar
STUB = c.XO + c.TAB_OUT + 2                # plate stub half width

if __name__ == "__main__":
    s = c.clip(LENGTH, tab_len=LENGTH - 2) & r.box(-40, 40, -LENGTH / 2, LENGTH / 2, -60, r.FLOOR)
    s += r.box(-STUB, STUB, -LENGTH / 2, LENGTH / 2, r.PLATE_BOT, r.FLOOR)
    s = Rot(90, 0, 0) * s                                            # stand it on its front face
    bb = s.bounding_box()
    s = Pos(-bb.center().X, -bb.center().Y, -bb.min.Z) * s
    export_stl(s, str(HERE / "everse_clip_fit_test.stl"))
    bb = s.bounding_box().size
    f, strain, _ = c.snap_force(LENGTH)
    print(f"everse_clip_fit_test.stl: {bb.X:.1f} x {bb.Y:.1f} x {bb.Z:.1f} mm, {s.volume / 1000:.1f} cm3, "
          f"solids {len(s.solids())}, valid {s.is_valid}; spread force {f:.0f} N per side")
