"""SKÅDIS pegboard parts shared by my SKÅDIS holders: hooks, back plates, shelves, cups, serials,
export, and a hook check against a board model.

Standard IKEA SKÅDIS: 5 mm board, 5 x 15 mm round-ended slots, 40 mm apart in a column, columns
20 mm apart with every other column 20 mm lower. Hook columns a multiple of COLUMN_STEP (40 mm)
apart have their slots at the same height.

Frame: X out from the board's front face (board = X -5..0), Y along the board (left to right as you
face it), Z up from the holder's bottom, which is its print-bed side.

hooks(yc): in one column, an upper tongue that goes through a slot and drops behind the board, and a
lower peg in the slot below. sim_board() hangs a holder on IKEA 5 x 15 and my printed 5.2 x 15.2
slots; for the MC6 Pro shelf (2026-10-31) it seated within 0.1 mm, dropped in when lifted
6.2-7.2 mm, the tab gripped 4.6 mm below the slot, and it had to be lifted 6 mm to come off.

Holders print upright on their floor, so the tabs hang in the air: save() puts tree supports from the
build plate on the 3MF object. A tab root then bends across the layers; tab_stress() turns the
holder's moment about its bottom edge into MPa there. Keep it near 6 MPa or less (about 3x margin on
PLA's layer strength): more columns, or a thicker tab (tab_t, it sits behind the board) if not.

On my first two prints (2026-11-01) each hook came out a straight bar with strings under it: the tab
had nothing under it, most likely because they were sliced from the STL (it can't carry the support
settings, and the U1 profile has supports off). I chose to keep these hooks and print with supports
(2026-11-02) over separate clips dropped into sockets during a pause: print the 3MF or the _U1.gcode,
or turn on tree supports, build plate only, when slicing an STL.

From a holder script anywhere under For Claude (they live in 3D Prints/Skadis/<project>/):
    sys.path.insert(0, str(next(p / "tools" / "u1" for p in HERE.parents if (p / "tools" / "u1").is_dir())))
    import skadis
"""
import sys
from pathlib import Path

from build123d import (Align, Box, Cylinder, Plane, Polygon, Pos, RectangleRounded, Rot, SlotCenterToCenter,
                       Text, Vector, export_stl, extrude)

sys.dont_write_bytecode = True

BOARD_T = 5.0                      # board thickness
SLOT_PITCH = 40.0                  # slot spacing within a column
COLUMN_STEP = 40.0                 # hook columns this far apart (or a multiple) sit at the same height

HOOK_W = 4.5                       # hook width across the 5 mm slot (5.2 on my printed board)
TONGUE_H = 5.0                     # tongue cross-section height
TAB_DROP = 6.0                     # how far the tab hangs below the tongue behind the board
TAB_T = 6.0                        # tab thickness behind the board
SLOT_SEAT = 6.2                    # tongue bottom rests this far below the slot centre (round end at 4.5 wide)
UPPER_SLOT_Z = 75.0                # upper slot centre above the holder's bottom; the peg's slot is 40 lower

BACK_T = 4.0                       # back plate thickness
BACK_H = 85.0                      # back plate height at a hook column
HOOK_ZONE = 32.0                   # full-thickness back plate this wide round each hook column
WEB_T = 2.0                        # elsewhere above the rail the plate thins to this web, flush with the board

MIN_UPPER_Z = 46.5                 # lowest upper slot height: the lower peg sits 0.3 above the bottom
MIN_TOP = 48.3                     # spine top for that height, 3 mm above the tongue (Osmo 360 spine, printed)
SPINE_W = 16.0                     # a full-thickness column just wide enough for the hooks
LOW_WEB_T = 1.2                    # low_back's web: it only keeps travel over plastic, so it carries nothing

SERIAL_CAP, SERIAL_DEPTH = 6.0, 0.6   # capital height; depth = 3 layers at 0.2 mm
# Liberation Sans Bold like the other prints' serials (OpenSCAD ships it); Arial Bold has the same metrics
SERIAL_FONT = next(f for f in ("/Applications/OpenSCAD.app/Contents/Resources/fonts/Liberation-2.00.1/ttf/"
                               "LiberationSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf")
                   if Path(f).exists())
LABEL_FONT = "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf"   # the Wireless Caddy's MIC labels

SUPPORTS = {"enable_support": "1", "support_type": "tree(auto)", "support_on_build_plate_only": "1"}


def profile_solid(pts, width, y0=0.0):
    """Extrude an XZ outline across Y from y0 to y0 + width. List pts counter-clockwise (X right, Z up):
    clockwise ones extrude from y0 to y0 - width."""
    return Pos(0, y0, 0) * extrude(Plane.XZ * Polygon(*pts, align=None), -width)


def hooks(yc, upper_z=UPPER_SLOT_Z, tab_t=TAB_T):
    """Upper hook and lower peg for the column centred at Y = yc (slots at upper_z and 40 below)."""
    y0 = yc - HOOK_W / 2
    tb = upper_z - SLOT_SEAT                                # tongue bottom
    back = -(BOARD_T + 0.5)                                 # tongue reaches 0.5 past the board's back face
    upper = profile_solid([(0, tb), (0, tb + TONGUE_H), (back - tab_t, tb + TONGUE_H),
                           (back - tab_t, tb - TAB_DROP + 1), (back - tab_t + 1, tb - TAB_DROP),
                           (back, tb - TAB_DROP), (back, tb)], HOOK_W, y0)
    pb = upper_z - SLOT_PITCH - SLOT_SEAT
    lower = profile_solid([(0, pb), (0, pb + TONGUE_H), (-BOARD_T + 0.5, pb + TONGUE_H),
                           (-BOARD_T + 0.5, pb)], HOOK_W, y0)
    return upper + lower


def back_plate(length, height=BACK_H):
    """Back plate along Y from 0 to length, chamfered along its top front edge."""
    return profile_solid([(0, 0), (BACK_T, 0), (BACK_T, height - 1.5), (BACK_T - 1.5, height), (0, height)],
                         length)


def back_windows(y0, y1, hook_ys, rail_h, zone=HOOK_ZONE, span=None, web=WEB_T):
    """Recesses, open at the top, that thin a back plate spanning y0..y1 to a web-thick web above rail_h
    except round the hook columns. (They were through-windows until the MC6 shelf printed with the
    nozzle stringing across the gap between its two hook posts on every layer; the web keeps travel
    over plastic.) Gaps under 14 mm stay solid, and so do gaps reaching less than 12.5 mm into span
    (the plate's real extent, when y0..y1 runs past its ends): no slivers. None when there's nothing to cut."""
    edges = [y0] + [v for yc in sorted(hook_ys) for v in (yc - zone / 2, yc + zone / 2)] + [y1]
    cut = None
    for a, b in zip(edges[::2], edges[1::2]):
        if b - a < 14 or (span and min(b, span[1]) - max(a, span[0]) < 12.5):
            continue
        w = Pos((web + BACK_T + 1) / 2, (a + b) / 2, rail_h + 50) * Rot(0, 90, 0) * \
            extrude(RectangleRounded(100, b - a, 6), (BACK_T + 1 - web) / 2, both=True)
        cut = w if cut is None else cut + w
    return cut


def low_back(length, spine_ys, rail_h, top=MIN_TOP, spine=SPINE_W, web=LOW_WEB_T):
    """Lean back plate for the minimum hook height (upper_z=MIN_UPPER_Z): a rail rail_h tall along Y from
    0 to length, BACK_T thick spines up to top at each of spine_ys, and a thin web between the spines so
    the nozzle never crosses a gap (see back_windows)."""
    part = back_plate(length, rail_h)
    y0, y1 = min(spine_ys) - spine / 2, max(spine_ys) + spine / 2
    part += Pos(0, y0, 0) * back_plate(y1 - y0, top)
    win = back_windows(y0, y1, spine_ys, rail_h, zone=spine, web=web)
    return part if win is None else part - win


def shelf(inner_l, inner_d, hook_ys, lip_h=12.0, floor_t=3.0, wall_t=4.0, lip_t=3.5, wall_top=34.0,
          rail_h=34.0, strip=18.0, walls=(True, True), tab_t=TAB_T, chamfer=2.5):
    """Open-frame shelf: a pocket inner_l along the board by inner_d out from the back plate, a front
    lip lip_h above the floor, end walls that brace it (wall_top high at the back plate, sloping down
    to the lip), and a floor frame of strip-wide strips round a window. The back plate is full thickness
    round the hook columns and a WEB_T web above rail_h elsewhere; chamfer fills the corner behind the device, so keep it
    under the device's gap to the back plate. Y = 0 is the outside of the left end wall (or the
    pocket's left side without one). Returns (part, length, depth, inner y0)."""
    wl = wall_t if walls[0] else 0.0
    wr = wall_t if walls[1] else 0.0
    length = inner_l + wl + wr
    lip_x = BACK_T + inner_d
    depth = lip_x + lip_t
    lip_top = floor_t + lip_h
    outline = [(0, 0), (depth, 0), (depth, lip_top - 1.5), (depth - 1.5, lip_top), (lip_x, lip_top),
               (lip_x, floor_t), (BACK_T + chamfer, floor_t), (BACK_T, floor_t + chamfer),   # in the back gap
               (BACK_T, BACK_H - 1.5), (BACK_T - 1.5, BACK_H), (0, BACK_H)]
    part = profile_solid(outline, length)
    win = back_windows(-20.0, length + 20.0, hook_ys, rail_h, span=(0, length))   # before the walls: never cuts them
    if win is not None:
        part -= win
    wall = [(0, 1), (lip_x + 1, 1), (lip_x + 1, lip_top), (0, max(wall_top, lip_top))]   # flush with the back
    if walls[0]:
        part += profile_solid(wall, wall_t)
    if walls[1]:
        part += profile_solid(wall, wall_t, length - wall_t)
    fx0, fx1, fy0, fy1 = BACK_T + strip, lip_x - strip, wl + strip, length - wr - strip
    if fx1 - fx0 > 16 and fy1 - fy0 > 16:
        part -= Pos((fx0 + fx1) / 2, (fy0 + fy1) / 2, floor_t / 2) * \
            extrude(RectangleRounded(fx1 - fx0, fy1 - fy0, 8), floor_t / 2 + 1, both=True)
    for yc in hook_ys:
        part += hooks(yc, tab_t=tab_t)
    return part, length, depth, wl


def cup(inner_w, inner_d, height, n_cols=1, radius=6.0, wall=2.4, floor_t=3.0, ledge=0.0, front_h=None,
        tab_t=TAB_T, plate_w=0.0):
    """A cup the device stands in, inner_w along the board by inner_d out from the back plate, height
    deep, on a full-height back plate (at least plate_w wide) with n_cols hook columns. ledge > 0
    leaves only a ledge that wide round an open bottom (for a cable plugged in underneath); front_h
    lowers the front wall so the device's front stays in view. Y = 0 is the plate's left edge.
    Returns (part, plate width, hook ys)."""
    w = inner_w + 2 * wall
    plate_w = max(w, (n_cols - 1) * COLUMN_STEP + HOOK_ZONE, plate_w)
    yc = plate_w / 2
    hook_ys = [yc + (i - (n_cols - 1) / 2) * COLUMN_STEP for i in range(n_cols)]
    cx = BACK_T + inner_d / 2                               # pocket centre; its back is the plate's front face
    part = back_plate(plate_w)
    part += Pos(cx, yc, 0) * extrude(RectangleRounded(inner_d + 2 * wall, w, radius + wall), height)
    part -= Pos(cx, yc, floor_t) * extrude(RectangleRounded(inner_d, inner_w, radius), height)
    if ledge:
        part -= Pos(cx, yc, -1) * extrude(RectangleRounded(inner_d - 2 * ledge, inner_w - 2 * ledge,
                                                           max(radius - ledge, 1.0)), floor_t + 2)
    if front_h is not None:
        span = inner_w - 2 * radius
        part -= Pos(BACK_T + inner_d + wall / 2, yc, front_h + 50) * Rot(0, 90, 0) * \
            extrude(RectangleRounded(100, span, 4), wall, both=True)
    for y in hook_ys:
        part += hooks(y, tab_t=tab_t)
    return part, plate_w, hook_ys


def wedge(width, y0, reach, top, tip_h, lip=0.0, lip_t=6.0):
    """A cantilever arm from the back plate, reach out from the board and width along Y from y0: flat on
    top at height top, tip_h thick at its end, its underside rising at 45 degrees so it prints without
    supports (running along the bed where 45 degrees would pass below Z = 0). lip adds an upstand at the
    end that stops whatever hangs on it sliding off; its inside face slopes at 45 degrees."""
    x0 = BACK_T - 0.5                                       # sunk into the plate so they fuse
    zt = top - tip_h
    low = [(x0, zt - (reach - x0))] if zt - (reach - x0) >= 0 else [(x0, 0), (reach - zt, 0)]
    if lip:
        end = [(reach, top + lip - 1.5), (reach - 1.5, top + lip), (reach - lip_t, top + lip),
               (reach - lip_t - lip, top)]
    else:
        end = [(reach, top)]
    return profile_solid(low + [(reach, zt)] + end + [(x0, top)], width, y0)


def fork(yc, slot_w, tine_w, slot_x, reach, top, tip_h, lip=0.0):
    """Two wedge tines either side of a front-open slot slot_w wide centred on Y = yc, whose round back
    end is centred slot_x out from the board. A short wedge bridges the tines at the plate. Something
    with a handle or nose hangs in the slot, its head or body resting across the tines."""
    r = slot_w / 2
    y0 = yc - r - tine_w
    part = wedge(tine_w, y0, reach, top, tip_h, lip) + wedge(tine_w, yc + r, reach, top, tip_h, lip) + \
        wedge(slot_w + 1, yc - r - 0.5, slot_x, top, tip_h)
    return part - (Pos(slot_x, yc, -1) * Cylinder(r, top + lip + 2, align=(Align.CENTER, Align.CENTER, Align.MIN)) +
                   Pos(slot_x + reach, yc, (top + lip) / 2) * Box(2 * reach, slot_w, top + lip + 4))


def text_cut(text, origin, x_dir, normal, cap=SERIAL_CAP, depth=SERIAL_DEPTH, font=SERIAL_FONT,
             align=(Align.CENTER, Align.CENTER)):
    """Solid to subtract for text engraved depth deep into a face at `origin` whose outward normal is
    `normal`, reading along x_dir (it reads the right way round looking at the face). cap = capital height."""
    fs = 10 * cap / Text("MSH", font_size=10, font_path=font).bounding_box().size.Y
    plane = Plane(Vector(origin) + Vector(normal) * 0.2, x_dir=x_dir, z_dir=normal)
    return plane * extrude(Text(text, font_size=fs, font_path=font, align=align), -(depth + 0.2))


def front_label_cut(items, x, z, cap, depth=1.0, font=LABEL_FONT):
    """Solid to subtract for labels on a front face at X = x: items = [(text, y), ...], centred at height z.
    1 mm deep because inlaid numerals have thin strokes and the slicer needs room to fill them."""
    cut = None
    for text, y in items:
        c = text_cut(text, (x, y, z), (0, 1, 0), (1, 0, 0), cap=cap, depth=depth, font=font)
        cut = c if cut is None else cut + c
    return cut


def flush_inlay(cut, x):
    """The inlay for a front_label_cut: the same solid trimmed flush with the front face at X = x."""
    return cut & (Pos(x - 25, 0, 0) * Box(50, 4000, 4000))


def serial_under(serial, x, y, x_dir=(-1, 0, 0)):
    """Serial engraved into the holder's underside, centred on (x, y), reading from below along x_dir."""
    return text_cut(serial, (x, y, 0), x_dir, (0, 0, -1))


def tab_stress(moment, n_cols, upper_z=UPPER_SLOT_Z, tab_t=TAB_T):
    """Pull per upper tab (N) and the bending stress at its root (MPa, across the layers) for a moment
    (N mm) about the holder's bottom edge, which presses on the board."""
    pull = moment / (upper_z - 7.5 - 2.4) / n_cols          # grip centre: 2.4 below the slot's bottom
    return pull, pull * 3.4 / (HOOK_W * tab_t ** 2 / 6)     # root to grip centre ~3.4 mm


def behind_board_ok(part, hook_ys, upper_z=UPPER_SLOT_Z, tab_t=TAB_T):
    """True when nothing but the hooks reaches behind the board's front face (X < 0)."""
    behind = (part & (Pos(-50, 0, 0) * Box(100, 2000, 2000))).volume
    return abs(behind - len(hook_ys) * hooks(0, upper_z, tab_t).volume) < 0.5


def sim_board(part, yc, upper_z=UPPER_SLOT_Z):
    """Hang one hook column of part on IKEA 5 x 15 and printed 5.2 x 15.2 slots. Returns, per board,
    (name, seat offset, lifts at which pushing in then dropping works, lift needed to come off)."""
    crop = part & (Pos(-10, yc, upper_z - 25) * Box(24, 14, 120))
    out = []
    for name, w, l in (("IKEA 5 x 15", 5.0, 15.0), ("printed 5.2 x 15.2", 5.2, 15.2)):
        b = Pos(-BOARD_T / 2, yc, upper_z - 25) * Box(BOARD_T, 20, 160)
        for c in (upper_z + 40, upper_z, upper_z - 40, upper_z - 80):
            b -= Pos(-BOARD_T - 1, yc, c) * Rot(0, 90, 0) * extrude(SlotCenterToCenter(l - w, w), BOARD_T + 2)

        def hit(dx, dz):
            return (Pos(dx, 0, dz) * crop & b).volume > 1e-3

        seat = next(dz / 100 for dz in range(-50, 100, 2) if not hit(0, dz / 100))
        lifts = [r / 10 for r in range(50, 86, 2)
                 if not any(hit(dx / 2, r / 10) for dx in range(24, -1, -1))
                 and not any(hit(0, z / 10) for z in range(r, int(seat * 10) + 1, -2))]
        off = next(dz / 10 for dz in range(int(seat * 10), 150)
                   if not any(hit(dx / 2, dz / 10) for dx in range(0, 25, 4)))
        out.append((name, seat, lifts, off - seat))
    return out


def with_serial(base, *serials):
    """File name carrying the print's serial(s), e.g. qc_mini_holder_JRJP-QCS-0001 (just base without one)."""
    return "_".join([base] + [s for s in serials if s])


def save(objects, out_dir, name, settings=SUPPORTS, gap=10.0, pauses=(), center=False):
    """Write name.stl and name.3mf (each object with settings, tree supports by default) into out_dir.
    objects: a part, or [(object name, part), ...] laid side by side along X. center=True puts the layout
    in the middle of the U1's 270 x 270 bed in the 3MF (else it sits at the bed corner, which Orca shows
    hard against the edges; the long hooks, 2026-11-16). pauses: [(z, message), ...]
    in the parts' own Z (their bottoms are put on the bed): the print pauses before the layer whose top is
    nearest z, to drop in magnets, nuts or other inserts (see orca3mf.write_3mf)."""
    import tempfile
    import trimesh
    from orca3mf import write_3mf
    if not isinstance(objects, list):
        objects = [(name, objects)]
    out_dir, placed, x = Path(out_dir), [], 0.0
    if pauses:
        assert all(abs(p.bounding_box().min.Z) < 1e-6 for _, p in objects), "pause heights assume Z = 0 is the bed"
    for oname, part in objects:
        bb = part.bounding_box()
        placed.append((oname, Pos(x - bb.min.X, -bb.min.Y, -bb.min.Z) * part))
        x += bb.size.X + gap
    if center:
        lay = placed[0][1]
        for _, p in placed[1:]:
            lay = lay + p
        bb = lay.bounding_box()
        dx, dy = 135 - (bb.min.X + bb.max.X) / 2, 135 - (bb.min.Y + bb.max.Y) / 2
        placed = [(n, Pos(dx, dy, 0) * p) for n, p in placed]
    whole = placed[0][1]
    for _, p in placed[1:]:
        whole = whole + p
    export_stl(whole, str(out_dir / f"{name}.stl"))
    meshes = []
    with tempfile.TemporaryDirectory() as tmp:            # not beside the model: Dropbox syncs temp files back
        for i, (oname, p) in enumerate(placed):
            f = Path(tmp) / f"{i}.stl"
            export_stl(p, str(f))
            meshes.append((oname, [("body", trimesh.load(str(f)), 1)], settings))
    write_3mf(str(out_dir / f"{name}.3mf"), meshes, pauses=pauses)


def save_inlaid(body, inlay, out_dir, name, settings=SUPPORTS, filament=2):
    """Two-colour holder: writes name.3mf (body on filament 1, inlay on `filament`, tree supports on the
    object) and parts/name_body.stl + parts/name_labels.stl, since one STL can't carry two colours. The
    part sits at the bed centre, clear of the prime tower: slice with ARRANGE=0 and one filament per
    toolhead ("A;B")."""
    import tempfile
    import trimesh
    from orca3mf import write_3mf
    out_dir, bb = Path(out_dir), body.bounding_box()
    (out_dir / "parts").mkdir(exist_ok=True)
    off = (135 - (bb.min.X + bb.max.X) / 2, 135 - (bb.min.Y + bb.max.Y) / 2, -bb.min.Z)
    meshes = {}
    with tempfile.TemporaryDirectory() as tmp:
        for key, shape in (("body", body), ("labels", inlay)):
            f = Path(tmp) / f"{key}.stl"
            export_stl(shape, str(f))
            export_stl(Pos(-bb.min.X, -bb.min.Y, -bb.min.Z) * shape, str(out_dir / "parts" / f"{name}_{key}.stl"))
            meshes[key] = trimesh.load(str(f), force="mesh").apply_translation(off)
    settings = {**settings, "support_filament": "1", "support_interface_filament": "1"}   # else supports go black too
    write_3mf(str(out_dir / f"{name}.3mf"), [(name, [("body", meshes["body"], 1), ("labels", meshes["labels"], filament)],
                                              settings)], title=name)


def report(name, part, hook_ys, moment, upper_z=UPPER_SLOT_Z, tab_t=TAB_T, sim=True):
    """Print the checks every holder gets: size, single solid, nothing behind the board but hooks,
    hook loads, and (sim=True) the board simulation on its first hook column."""
    bb = part.bounding_box()
    pull, mpa = tab_stress(moment, len(hook_ys), upper_z, tab_t)
    print(f"{name}: {bb.size.X:.1f} out x {bb.size.Y:.1f} along x {bb.size.Z:.1f} tall, "
          f"{part.volume / 1000:.1f} cm3, solids {len(part.solids())}, valid {part.is_valid}")
    print(f"  behind the board: {'hooks only' if behind_board_ok(part, hook_ys, upper_z, tab_t) else 'SOMETHING ELSE TOO'}")
    print(f"  {len(hook_ys)} hook column(s) at y {', '.join(f'{y:.1f}' for y in hook_ys)}: "
          f"{pull:.1f} N per tab, {mpa:.1f} MPa at the tab root")
    if sim:
        for bname, seat, lifts, off in sim_board(part, hook_ys[0], upper_z):
            ok = f"drops in when lifted {lifts[0]:.1f}-{lifts[-1]:.1f} mm" if lifts else "DOES NOT GO IN"
            print(f"  {bname}: seats {seat:+.2f}, {ok}, lift {off:.1f} mm to remove")
