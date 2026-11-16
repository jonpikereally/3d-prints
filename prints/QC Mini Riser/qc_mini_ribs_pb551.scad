// Quad Cortex Mini rib riser - version for the UGREEN PB551 power bank, with a pocket in front for an
// M-VAVE Chocolate Plus MIDI foot controller
// (bank: 20,000 mAh, 145 W, built-in USB-C cable; 139 x 80 x 26.7 mm)
// (pedal: 4 footswitches, 212 x 36 x 17 mm body per M-VAVE's drawing; all its ports on the back edge)
//  - Angled ribs ("sliders") run front-to-back under the QC Mini. Each is topped with a
//    flat pad that has a recess for a velcro / Dual Lock strip. A low lip stops the QC sliding off.
//  - The Chocolate Plus drops into a pocket at floor level in front of the QC Mini, switches up and
//    display facing you. A low lip, end walls and a ledge behind it hold it. Behind the ledge, a
//    channel along the riser's front leaves room for right-angle plugs in its back-edge ports (power
//    switch, USB-C, USB-A host, expression jack) and a fingertip for the power switch; cables leave
//    the channel at either end. Three more stick-on feet go under the pocket.
//  - One piece. The power bank slides straight in from the LEFT, BOTTOM FIRST (bottom = the small
//    end away from the ports), logo up. Its side screen and button then face a slot in the back wall.
//  - The bank goes in as far as it fits: its far end stops against the right-hand end wall and its
//    ports end sits 93 mm inside the opening, so the plugs and the built-in cable stay in a
//    bay inside the riser. Your power cable leaves through a window in the back wall next to the
//    ports. Nothing comes out of either side.
//  - A sprung tongue in the bay floor clicks up in front of the ports end to hold the bank in.
//    To remove: unplug, then pull the bank out by its built-in cable (UGREEN sells it as a lanyard);
//    the catch lets go with a firm pull. Pressing the tongue down just in front of the ports end
//    makes it easier. The tongue flexes into the space under the frame, so USE THE STICK-ON FEET.
//  - Undock the built-in cable before sliding the bank in: docked, its plug catches on the wall.
//  - A serial number (SERIAL, just below) is engraved low on the back wall at the right-hand end.
//
// Axes: X = width (left -> right as you stand at the front), Y = depth (front -> back), Z = up.
// The riser body runs from y = 0 back; the pedal pocket sits in front of it, at y < 0.
// All dimensions in mm. MEASURE YOUR UNITS WITH CALIPERS and edit below.

// Serial number, engraved low on the back wall at the right-hand end. Every serial starts with JRJP-.
// Give each printed copy and each design change its own number, and put it in the exported file
// names (ribs_pb551_frame_<SERIAL>.stl / .3mf / _U1.gcode). "" leaves it off.
SERIAL = "JRJP-QCR-551-0004";

/* [What to show / export] */
// test_left = the opening end only (bay, latch, ports window and screen slot), to check the click,
// the pull-out and the window positions before printing the whole frame
part = "assembly"; // [assembly, frame, test_left]

/* [Quad Cortex Mini] */
qc_w = 228;          // spec (too long for the calipers; depth matched spec, so trusted)
qc_d = 118;          // measured 117.95
qc_h = 50;           // measured 49.95 - only used for the ghost preview
qc_clr = 1.0;        // clearance per side

/* [Battery: UGREEN PB551] */
bat_l = 139;         // UGREEN spec 139 x 80 x 26.7 - measure. Bottom end goes in first
bat_w = 80;
bat_h = 26.7;
bat_clr = 0.75;
end_play = 1.5;      // room past the bank's bottom end, so a slightly long bank still clicks in

/* [Battery screen, button and ports] */
scr_from = 3;        // back-wall slot starts this far from the bank's ports end ...
scr_to = 42;         // ... and ends this far. It must cover the screen AND the button - measure.
scr_margin = 3;      // slot margin from the bank's top and bottom faces
plug_len = 30;       // USB plug + stiff strain relief in the bank's port - measure
bay_len = 0;         // opening to the bank's ports end. 0 = as deep as it fits: the bank's far end against
                     // the right-hand end wall (93 mm with the spec bank). It was 52 up to JRJP-QCR-551-0002.
port_win_h = 21;     // ports / cable window in the back wall: how high it reaches above the bank's bottom

/* [Ribs] */
tilt = 6;            // deck angle in degrees (0 = flat)
rib_xs = [16, 146, 183, 220];  // rib centres from the left, kept clear of the screen slot and the
                               // cable window (both follow the bank: x 49-89 and 96-135 here)
rib_t = 6;           // rib thickness
pad_w = 32;          // pad on top of each rib (wide enough for a 25 mm strip under the QC)
pad_t = 3;           // pad thickness
rib_cap = 3;         // minimum rib material over the battery opening
skin = 3;            // front wall thickness

/* [Lip] */
lug_t = 3;           // lip thickness
lug_h = 12;          // lip height above the pads
side_trim = 30;      // right lip stops this far short of the back
btn_from = 35;       // left lip stops here (mm back from the QC's front edge) to clear the volume buttons

/* [Velcro] */
velcro_w = 25;
velcro_len = 90;
velcro_depth = 1.0;

/* [Battery passage] */
tw = 2.4;            // passage front wall and end-stop thickness
tun_floor = 2.4;     // floor rails, bay floor, tongue and cross bars
ledge_w = 12;        // floor rail width (the bank slides on these)
bar_from = [48, 98]; // floor cross bars under the bank, measured from its ports end

/* [Latch] */
tongue_w = 24;       // sprung tongue in the bay floor (same section as the tested mouth piece)
tongue_len = 40;     // flex length
bump_h = 1.6;        // how far the catch rises in front of the ports end
catch_angle = 50;    // slope of the catch face: 90 = square (hard lock, press the tongue to release);
                     // lower = easier to pull out. 50 should hold roughly 1 kg of pull.
ramp_angle = 30;     // lead-in slope the bank's bottom end rides over going in
catch_play = 0.6;    // gap between the catch and the ports end
slot_gap = 1;        // gap around the tongue

/* [Cable route] */
cable_clips = false; // J-hooks on the back wall that carry the power cable to the QC's DC input
                     // (on up to JRJP-QCR-551-0003, removed in 0004)
dc_x = 150;          // QC's DC input: distance from the QC's left end (standing at the front) - only
                     // places the clips

/* [MIDI pedal: M-VAVE Chocolate Plus] */
choc_l = 212;        // along the 4 switches (M-VAVE's drawing: 212 x 36 x 17) - measure
choc_w = 36;         // front to back - measure
choc_h = 17;         // body, not counting the switches - measure
choc_clr = 0.75;     // clearance per side
chan_w = 16;         // cable channel behind the pedal: right-angle plugs, fingertip for the power switch
pk_floor = 3;        // pocket floor
pk_lip_h = 8;        // front lip, above the pocket floor
pk_end_h = 14;       // end walls, above the pocket floor (lower than the pedal, so you can grip it)
pk_ledge_h = 3;      // low ledge behind the pedal: keeps it out of the channel, stays under its ports
pk_hook = 6;         // the end walls wrap this far round the pedal's back corners (clear of the ports)
pk_chamfer = 1.5;    // lead-in on the inside top edges of the lip and end walls

/* [Serial number] */
serial_cap = 6;                     // capital height, Liberation Sans Bold
serial_size = serial_cap / 0.956;   // OpenSCAD text size giving those capitals (cap height = 0.956 x size)
serial_depth = 0.6;                 // engraving depth (the back wall is 2.4 mm)

/* [Feet] */
foot_d = 12.7;       // stick-on bumper diameter (needs to be at least ~2.5 mm tall)
foot_depth = 1;      // recess depth
foot_pad_d = 17;     // printed pad the bumper sits on

$fn = 48;

// ---------- derived ----------
rib_n = len(rib_xs);
function rib_x(i) = rib_xs[i];
W = qc_w + 2*qc_clr + 2*lug_t;
D = qc_d + 2*qc_clr + lug_t;           // lip on the front only, back stays open
t = tan(tilt);

// along the passage, from the opening (x = 0) inward
x_p    = bay_len > 0 ? bay_len : W - tw - end_play - bat_l;   // bank's ports end
x_b    = x_p + bat_l;                   // bank's bottom end
in_len = x_b + end_play;                // end stop
x_tip  = x_p - catch_play;              // tongue tip = foot of the catch face
x_root = x_tip - tongue_len;            // tongue root (the bay floor)

in_w   = bat_w + 2*bat_clr;
in_h   = bat_h + 2*bat_clr;
by1    = D - tw;                        // passage runs along the back wall (screen side)
by0    = by1 - in_w;                    // front of the passage
pf0    = by0 - tw;                      // front face of the passage front wall
yc     = (by0 + by1)/2;
bat_z0 = tun_floor;                     // the bank slides on the floor rails
bore_top = bat_z0 + in_h;
gus    = (pad_w - rib_t)/2;             // 45-degree support under each pad

front_h = bore_top + rib_cap + pad_t - by0*t;   // pad top at the front edge
back_h  = front_h + D*t;
function deck_z(y) = front_h + y*t;
// keep each velcro strip on its pad AND under the QC (clear of the side lips)
function strip_lo(i) = max(rib_x(i) - pad_w/2, lug_t + qc_clr) + velcro_w/2 + 0.5;
function strip_hi(i) = min(rib_x(i) + pad_w/2, W - lug_t - qc_clr) - velcro_w/2 - 0.5;
function strip_x(i) = min(max(rib_x(i), strip_lo(i)), strip_hi(i));

// pedal pocket, in front of the riser body (y < 0): front lip | pedal well | ledge | cable channel
pk_in_l = choc_l + 2*choc_clr;
pk_in_w = choc_w + 2*choc_clr;
pk_d    = tw + pk_in_w + tw + chan_w;   // how far the pocket sticks out in front of the riser body
pk_x0   = (W - pk_in_l)/2;              // pedal well, centred under the QC
pk_x1   = pk_x0 + pk_in_l;
pk_y0   = -pk_d + tw;                   // well front ...
pk_y1   = pk_y0 + pk_in_w;              // ... and back; the ledge runs from here
ch_y0   = pk_y1 + tw;                   // the channel runs from here to the riser's front wall (y = 0)
pk_yc   = (pk_y0 + pk_y1)/2;
D_all   = D + pk_d;                     // whole riser, front to back

feet = concat([for (i = [0:rib_n-1]) for (y = [9, D - 9]) [rib_x(i), y]],
              [for (x = [rib_x(0), W/2, rib_x(rib_n-1)]) [x, pk_yc]]);    // + 3 under the pedal

// back-wall openings
scr_x0 = x_p + scr_from;
scr_x1 = x_p + scr_to;
scr_z0 = bat_z0 + scr_margin;
scr_z1 = bat_z0 + bat_h - scr_margin;
c_win  = 1.5;                           // outside chamfer on the screen slot
pw_x0  = max(8, x_p - 44);              // ports / cable window: the 40 mm of the bay next to the ports, low down ...
pw_x1  = x_p - 4;                       // ... stopping short of the ports end
pw_z1  = bat_z0 + port_win_h;           // the back wall bridges over it

// cable: out of the ports window, then (with cable_clips on, and if the DC input is further along)
// along the top of the back wall in two clips, above the screen slot
exit_req = lug_t + qc_clr + dc_x;
clip_z = scr_z1 + c_win + 8;
clip_xs = !cable_clips ? []
        : exit_req > pw_x1 + 15 ? [pw_x1 + 8, exit_req - 6]
        : exit_req < pw_x0 - 15 ? [exit_req + 6, pw_x0 - 8] : [];

echo(str("Footprint: ", W, " x ", D_all, " mm (riser body ", D, " deep + pedal pocket ", pk_d,
         ")   QC front ", front_h, " mm, back ", back_h, " mm (plus ", lug_h, " mm lip)"));
echo(str("Pedal well: ", pk_in_l, " x ", pk_in_w, " mm at x ", pk_x0, " to ", pk_x1, ", channel ", chan_w,
         " mm; plug room from the pedal's back face to the riser ", choc_clr - pk_y1, " mm"));
echo(str("Ribs at x = ", rib_xs));
echo(str("Passage: ", in_len, " long, opening ", in_w, " x ", bore_top - bat_z0, " mm"));
echo(str("Bay: ", x_p, " mm for a ", plug_len, " mm plug   ports end at x = ", x_p, ", latch tongue x ", x_root, " to ", x_tip));
echo(str("Back wall: ports window x ", pw_x0, " to ", pw_x1, " (", pw_z1, " mm high), screen slot x ", scr_x0, " to ", scr_x1,
         " (", scr_from, " to ", scr_to, " mm from the ports end), ", scr_z1 - scr_z0, " mm tall"));
echo(cable_clips ? str("Cable clips at x = ", clip_xs, " (DC input at x = ", exit_req, ")") : "Cable clips: none");
echo(str("Serial: ", SERIAL == "" ? "none" : SERIAL));
assert(W <= 270 && D_all <= 270, "Too big for the U1's 270 x 270 mm bed");
assert(pk_x0 - tw >= 0, "The pedal pocket is wider than the riser");
assert(pk_ledge_h + 2 < pk_lip_h && pk_lip_h <= pk_end_h, "Pocket walls: keep ledge < lip <= end walls");
assert(by0 > skin + 15, "Battery passage is too deep for the frame");
assert(x_p >= plug_len + 20, "Bay is too short for the plug plus a gentle bend");
assert(in_len + tw <= W + 0.01, "Bank + bay too long for the frame");
for (i = [0:rib_n-1]) assert(rib_x(i) + rib_t/2 < pw_x0 - 2 || rib_x(i) - rib_t/2 > pw_x1 + 2 || x_p <= 52,
                             str("Rib ", i, " runs through the cable window"));
assert(x_root >= 8, "Latch tongue doesn't fit in the bay - shorten tongue_len or lengthen bay_len");
assert(pw_z1 < bore_top - 3, "Ports window is too tall - the back wall needs some height above it");
for (i = [0:rib_n-1]) assert(strip_lo(i) <= strip_hi(i) + 0.01, str("Velcro strip doesn't fit on pad ", i, " - widen pad_w"));
for (i = [0:rib_n-1]) assert(rib_x(i) + rib_t/2 < scr_x0 - c_win - 2 || rib_x(i) - rib_t/2 > scr_x1 + c_win + 2,
                             str("Rib ", i, " runs through the screen slot"));
for (i = [0:rib_n-1]) assert(rib_x(i) + rib_t/2 < in_len || rib_x(i) - rib_t/2 > in_len + tw,
                             str("Rib ", i, " collides with the end stop"));

module on_deck() {
    translate([0,0,front_h]) multmatrix([[1,0,0,0],[0,1,0,0],[0,t,1,0],[0,0,0,1]]) children();
}
// side profile up to the pads (top = offset from the deck surface), extruded across x0..x1
module profile(x0, x1, y_from = 0, y_to = D, top = -pad_t + 0.5) {
    translate([x0, 0, 0]) rotate([90,0,90]) linear_extrude(x1 - x0)
        polygon([[y_from, 0], [y_to, 0], [y_to, deck_z(y_to) + top], [y_from, deck_z(y_from) + top]]);
}

// =====================================================================
// FRAME
// =====================================================================
module ribs() {
    for (i = [0:rib_n-1]) {
        xc = rib_x(i);
        profile(xc - rib_t/2, xc + rib_t/2);
        // 45-degree gusset so the pad prints without support
        on_deck() translate([0, D, 0]) rotate([90,0,0]) linear_extrude(D)
            polygon([[xc - pad_w/2, -pad_t + 0.5], [xc + pad_w/2, -pad_t + 0.5], [xc + pad_w/2, -pad_t],
                     [xc + rib_t/2, -pad_t - gus], [xc - rib_t/2, -pad_t - gus], [xc - pad_w/2, -pad_t]]);
    }
}
module pads()  { on_deck() for (i = [0:rib_n-1]) translate([rib_x(i) - pad_w/2, 0, -pad_t]) cube([pad_w, D, pad_t]); }
module walls() {
    profile(0, W, 0, skin, 0);                      // front wall, up to the deck so the lip sits on it
    profile(0, W, pf0, by0 + 0.01);                 // passage front wall
    profile(0, W, by1 - 0.01, D);                   // back wall (the passage's back side)
    profile(in_len, in_len + tw, pf0, D);           // end stop at the far end of the passage
}
module lips() {
    on_deck() {
        translate([0, 0, -0.5]) cube([W, lug_t, lug_h + 0.5]);                                  // front
        translate([W - lug_t, 0, -0.5]) cube([lug_t, D - side_trim, lug_h + 0.5]);              // right
        translate([0, 0, -0.5]) cube([lug_t, lug_t + qc_clr + btn_from, lug_h + 0.5]);          // left, short
    }
}
module bore() { translate([-1, by0, -1]) cube([in_len + 1, in_w, bore_top + 1]); }

module back_windows() {
    // screen + button slot, chamfered on the outside for a wider viewing angle
    hull() {
        translate([scr_x0, by1 - 0.5, scr_z0]) cube([scr_x1 - scr_x0, 0.01, scr_z1 - scr_z0]);
        translate([scr_x0 - c_win, D, scr_z0 - c_win]) cube([scr_x1 - scr_x0 + 2*c_win, 0.01, scr_z1 - scr_z0 + 2*c_win]);
    }
    translate([scr_x0 - c_win, D, scr_z0 - c_win]) cube([scr_x1 - scr_x0 + 2*c_win, 1, scr_z1 - scr_z0 + 2*c_win]);
    // ports / cable window along the bay, from the floor up
    translate([pw_x0, by1 - 1, -1]) cube([pw_x1 - pw_x0, tw + 2, pw_z1 + 1]);
}

module velcro_recesses() {
    on_deck() for (i = [0:rib_n-1])
        translate([strip_x(i) - velcro_w/2, (D - velcro_len)/2, -velcro_depth]) cube([velcro_w, velcro_len, velcro_depth + 1]);
}

module vents() {
    // slots in the passage front wall, between the ribs (clear of the gussets)
    for (i = [0:rib_n-2]) {
        xa = rib_x(i) + pad_w/2 + 4; xb = min(rib_x(i+1) - pad_w/2 - 4, in_len - 4);
        if (xb - xa > 10)
            for (x = [xa : 8 : xb - 4]) translate([x, pf0 - 1, bat_z0 + 5]) cube([4, tw + 2, in_h - 10]);
    }
}

module floor_parts() {
    // rails the bank slides on
    translate([0, by0 - 0.5, 0]) cube([in_len + 0.5, ledge_w + 0.5, tun_floor]);
    translate([0, by1 - ledge_w, 0]) cube([in_len + 0.5, ledge_w + 0.5, tun_floor]);
    // closed floor under the bay so the cables don't drop through, slotted around the tongue
    difference() {
        translate([0, by0 - 0.5, 0]) cube([x_p + 4, in_w + 1, tun_floor]);
        translate([x_root, yc - tongue_w/2 - slot_gap, -1]) cube([x_tip + slot_gap - x_root, tongue_w + 2*slot_gap, tun_floor + 2]);
    }
    // cross bars under the bank
    for (b = bar_from) translate([x_p + b, by0 - 0.5, 0]) cube([8, in_w + 1, tun_floor]);
    // sprung tongue, printed flat on the bed, growing out of the bay floor
    translate([x_root - 0.5, yc - tongue_w/2, 0]) cube([x_tip - x_root + 0.5, tongue_w, tun_floor]);
    // catch at the tip: lead-in ramp toward the opening, sloped catch face against the ports end
    s = bump_h / tan(catch_angle);
    translate([0, yc + tongue_w/2, 0]) rotate([90,0,0]) linear_extrude(tongue_w)
        polygon([[x_tip - s - 1.5 - bump_h/tan(ramp_angle), tun_floor - 0.01], [x_tip, tun_floor - 0.01],
                 [x_tip - s, tun_floor + bump_h], [x_tip - s - 1.5, tun_floor + bump_h]]);
    // pads for the stick-on feet
    for (f = feet) translate([f[0], f[1], 0]) cylinder(d = foot_pad_d, h = tun_floor);
}

module pedal_pocket() {
    zt = pk_floor;
    c = pk_chamfer;
    difference() {
        union() {
            // floor under the pedal and the channel, full width (runs into the riser's front wall)
            translate([0, -pk_d, 0]) cube([W, pk_d + skin/2, zt]);
            // front lip, full width
            translate([0, -pk_d, 0]) cube([W, tw, zt + pk_lip_h]);
            for (s = [0, 1]) {
                // end walls, from the lip back to the channel ...
                translate([s == 0 ? pk_x0 - tw : pk_x1, -pk_d, 0]) cube([tw, ch_y0 + pk_d, zt + pk_end_h]);
                // ... wrapping round the pedal's back corners
                translate([s == 0 ? pk_x0 - 0.01 : pk_x1 - pk_hook, pk_y1, 0]) cube([pk_hook + 0.01, tw, zt + pk_end_h]);
            }
            // low ledge behind the pedal
            translate([pk_x0, pk_y1, 0]) cube([pk_in_l, tw, zt + pk_ledge_h]);
        }
        // lead-in chamfers on the inside top edges of the lip ...
        translate([pk_x0, 0, 0]) rotate([90, 0, 90]) linear_extrude(pk_in_l)
            polygon([[pk_y0 + 0.01, zt + pk_lip_h - c], [pk_y0 + 0.01, zt + pk_lip_h + 0.01], [pk_y0 - c - 0.01, zt + pk_lip_h + 0.01]]);
        // ... and the end walls
        for (s = [0, 1]) {
            xe = s == 0 ? pk_x0 : pk_x1;    // inner face
            d = s == 0 ? -1 : 1;            // into the wall
            translate([0, pk_y1, 0]) rotate([90, 0, 0]) linear_extrude(pk_in_w)
                polygon([[xe - d*0.01, zt + pk_end_h - c], [xe - d*0.01, zt + pk_end_h + 0.01], [xe + d*(c + 0.01), zt + pk_end_h + 0.01]]);
        }
    }
}

module cable_clip(x, cz) {
    // J-hook on the back face; the cable drops in from above
    translate([x - 4, 0, 0]) rotate([90,0,90]) linear_extrude(8)
        polygon([[D-0.5, cz-7], [D+5, cz-2], [D+7, cz-2], [D+7, cz+5], [D+5.5, cz+5], [D+5.5, cz], [D-0.5, cz]]);
}

module serial_text() {
    // reads left to right as you look at the back; starts near the right-hand end of the riser
    translate([W - 8, D - serial_depth, 6]) rotate([90, 0, 180]) linear_extrude(serial_depth + 1)
        text(SERIAL, size = serial_size, font = "Liberation Sans:style=Bold", halign = "left", valign = "bottom");
}

module frame() {
    difference() {
        union() {
            difference() {
                union() { ribs(); pads(); walls(); lips(); }
                bore();
                vents();
                back_windows();
                velcro_recesses();
            }
            floor_parts();
            pedal_pocket();
            for (x = clip_xs) cable_clip(x, clip_z);
        }
        for (f = feet) translate([f[0], f[1], -0.01]) cylinder(d = foot_d + 0.5, h = foot_depth);
        if (SERIAL != "") serial_text();
    }
}

// =====================================================================
module bank_ghosts() {
    %translate([x_p, by1 - bat_clr - bat_w, bat_z0]) cube([bat_l, bat_w, bat_h]);
    // USB plug in the USB-C port, which sits toward the screen side of the ports end
    %translate([x_p - plug_len, by1 - bat_clr - 26, bat_z0 + bat_h/2 - 4]) cube([plug_len, 12, 8]);
}
module pedal_ghost() {
    x0 = pk_x0 + choc_clr;  y0 = pk_y0 + choc_clr;  z0 = pk_floor + 1.5;    // standing on its rubber feet
    %translate([x0, y0, z0]) cube([choc_l, choc_w, choc_h]);
    // footswitches A-D (positions read off M-VAVE's port diagram)
    for (i = [0:3]) %translate([x0 + 15.5 + i*60.3, y0 + choc_w/2, z0 + choc_h]) cylinder(d = 12, h = 13);
    // a right-angle USB-C plug in its USB-C port, about 35 mm from the left end of the back edge
    %translate([x0 + 35 - 6, y0 + choc_w, z0 + 5]) cube([12, 13, 7]);
}
if (part == "assembly") {
    color("SteelBlue") frame();
    %on_deck() translate([lug_t + qc_clr, lug_t + qc_clr, 0]) cube([qc_w, qc_d, qc_h]);
    bank_ghosts();
    pedal_ghost();
}
if (part == "frame") frame();
if (part == "test_left")
    // the opening end: bay, latch, rails, ports window and screen slot, cut off just below the top of
    // the opening so nothing needs support
    translate([1, -(pf0 - 1), 0]) intersection() {
        frame();
        translate([-1, pf0 - 1, -1]) cube([1 + scr_x1 + c_win + 6, D - pf0 + 11, bore_top - 1.5 + 1]);
    }
