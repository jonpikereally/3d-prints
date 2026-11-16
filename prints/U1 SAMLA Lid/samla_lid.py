"""Snapmaker U1 top cover from an IKEA SAMLA 45 L box (56x39x28 cm, art. 301.029.74, no lid needed).

Parts: Beaver Works' "Snapmaker U1 Top Cover Modding for IKEA SAMLA 45L" (MakerWorld 2031310,
CC BY-NC-SA), the "No Cable disconnecting" version — the STEP plates in
../Makerworld Downloads/Snapmaker+U1+Top+Cover+Modding+for+IKEA+SAMLA+45L/.
Each STEP is already one bed's worth of pieces laid out for a 256 mm bed, so each becomes one plate.

The only change here is the serial: engraved 0.6 mm into the underside (bed face) of the rear
"above" piece, at its right-hand end as seen from below, reading from below.

    python samla_lid.py      → parts/<plate>_<SERIAL>.stl, then slice each with u1-slice.sh
"""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
from build123d import Align, Plane, Pos, Rot, Text, export_stl, extrude, import_step

SERIAL = "JRJP-SAM-0001"     # "" = off; change per copy

HERE = Path(__file__).resolve().parent
SRC = HERE.parent / "Makerworld Downloads" / "Snapmaker+U1+Top+Cover+Modding+for+IKEA+SAMLA+45L"
OUT = HERE / "parts"
FONT = "/Applications/OpenSCAD.app/Contents/Resources/fonts/Liberation-2.00.1/ttf/LiberationSans-Bold.ttf"

PLATES = ["under_front", "under_middle", "under_rear",
          "above_front", "above_middle", "above_rear_no_cable_disconnecting", "pins"]
SERIAL_PLATE = "above_rear_no_cable_disconnecting"
REAR_ANGLE = 44.52           # the rear piece lies diagonally on its plate; this squares it up
DEPTH, CAP_H = 0.6, 6.0      # engraving depth, capital height (Liberation cap height = 0.729 em)


def engrave(part):
    """Cut SERIAL into the rear piece's bed face: square it up, cut, put it back where it was."""
    bb = part.bounding_box()
    centre = bb.center()
    sq = Rot(0, 0, REAR_ANGLE) * Pos(-centre.X, -centre.Y, -bb.min.Z) * part
    sb = sq.bounding_box()
    # solid band (no tabs) is the low-Y side; text centred 12 mm in from that edge, 42 mm from the
    # low-X end, which is the right-hand end when the piece is flipped over and read from below
    x, y = sb.min.X + 42, sb.min.Y + 12
    face = Plane(origin=(x, y, 0), x_dir=(-1, 0, 0), z_dir=(0, 0, -1))   # reads correctly from below
    txt = Text(SERIAL, CAP_H / 0.729, font_path=FONT, align=(Align.CENTER, Align.CENTER))
    cutter = extrude(face * txt, amount=-DEPTH)                           # into the part (+Z)
    removed = (sq & cutter).volume
    assert abs(removed - cutter.volume) < 0.02 * cutter.volume, "serial runs off the solid face"
    sq = sq - cutter
    return Pos(centre.X, centre.Y, bb.min.Z) * Rot(0, 0, -REAR_ANGLE) * sq


def with_serial(name):
    return f"{name}_{SERIAL}" if SERIAL else name


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for name in PLATES:
        part = import_step(str(SRC / f"{name}.stp"))
        if SERIAL and name == SERIAL_PLATE:
            part = engrave(part)
        bb = part.bounding_box()
        part = Pos(-bb.min.X, -bb.min.Y, -bb.min.Z) * part
        out = OUT / f"{with_serial(name)}.stl"
        export_stl(part, str(out), tolerance=0.05, angular_tolerance=0.2)
        print(out.name, f"{bb.size.X:.0f}x{bb.size.Y:.0f}x{bb.size.Z:.1f}")
