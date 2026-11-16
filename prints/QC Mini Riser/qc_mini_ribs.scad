// Quad Cortex Mini rib riser ("design 2", rev B: screen window + port bay)
//  - Angled ribs ("sliders") run front-to-back under the QC Mini. Each is topped with a
//    flat pad that has a recess for a velcro / Dual Lock strip. A low lip stops the QC sliding off.
//  - The power bank slides in from the LEFT, PORTS FIRST, with its screen facing you (the front).
//    It runs along the front of the frame through arch openings in the ribs, resting on two rails.
//  - Screen + button: a window in the front wall lines up with them.
//  - Ports end: sits in a protected bay at the right end of the frame (open at the right side, so
//    you can plug in or charge in place). The USB plug has room to stick straight out and bend
//    gently; the cable then turns into a channel behind the battery and leaves through a slot in
//    the back wall, right under the QC's DC input. Nothing sticks out of the sides.
//  - A sprung tongue in the floor clicks up behind the battery's plain end to lock it in.
//    To remove: unplug the cable in the bay, press the ridged tab under the left opening down,
//    slide the battery out to the left. The tongue flexes into the space under the frame,
//    so USE THE STICK-ON FEET.
//
// Axes: X = width (left -> right as you stand at the front), Y = depth (front -> back), Z = up.
// All dimensions in mm. MEASURE YOUR UNITS WITH CALIPERS and edit below.

/* [What to show / export] */
// test_mouth = the latch end (already proven); test_ports = the right end, to check the
// screen window, the end stop and the plug + cable bend before printing the whole frame
part = "assembly"; // [assembly, frame, test_mouth, test_ports]

/* [Quad Cortex Mini] */
qc_w = 228;          // spec (too long for the calipers; depth matched spec, so trusted)
qc_d = 118;          // measured 117.95
qc_h = 50;           // measured 49.95 - only used for the ghost preview
qc_clr = 1.0;        // clearance per side

/* [Battery: UGREEN PB205] */
bat_l = 160;         // UGREEN spec (too long for the calipers); runs left -> right, ports end on the right
bat_w = 80.8;        // measured 80.68, spec 80.8
bat_h = 26.8;        // measured 26.8, spec 26.7
bat_clr = 0.75;

/* [Battery screen, button and plug] */
scr_from = 5;        // screen window starts this far from the battery's ports end ...
scr_to = 52;         // ... and ends this far. It must cover the screen AND the button - measure.
scr_margin = 3;      // window margin from the battery's top and bottom faces
plug_len = 30;       // how far the USB plug + its stiff strain relief stick out of the battery - measure
stop_w = 7;          // end-stop posts the ports end rests against (front and back edges of the end face)

/* [Ribs] */
tilt = 6;            // deck angle in degrees (0 = flat)
rib_n = 4;           // number of ribs
rib_t = 6;           // rib thickness
pad_w = 32;          // pad on top of each rib (wide enough for a 25 mm strip under the QC)
pad_t = 3;           // pad thickness
rib_cap = 3;         // minimum rib material over the battery opening
skin = 3;            // front wall thickness (also the front side of the battery passage)

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
tw = 2.4;            // passage back wall and end-stop thickness
tun_floor = 2.4;     // floor rails, tongue and cross bars
ledge_w = 12;        // floor rail width (the battery rests on these)
mouth_ext = 4.5;     // passage extends this far past the battery end (room for the catch)
bar_x = [100];       // extra floor cross bars

/* [Battery latch] */
tongue_w = 24;       // sprung tongue in the floor
tongue_len = 40;     // flex length
bump_h = 1.6;        // catch height (how far it rises behind the battery)
catch_play = 1.0;    // end play between catch and battery = how much longer than bat_l the battery may be
tab_len = 8;         // press tab sticking out of the left opening

/* [Cable route] */
dc_x = 150;          // QC's DC input: distance from the QC's left end (standing at the front) - measure
chan_w = 14;         // cable tunnel through any rib in the way (width)
chan_h = 10;         // tunnel height before its 45-degree peak
exit_w = 9;          // slot in the back wall where the cable comes out (open at the top)

/* [Feet] */
foot_d = 12.7;       // stick-on bumper diameter (needs to be at least ~2.5 mm tall)
foot_depth = 1;      // recess depth
foot_pad_d = 17;     // printed pad the bumper sits on

$fn = 48;

// ---------- derived ----------
W = qc_w + 2*qc_clr + 2*lug_t;
D = qc_d + 2*qc_clr + lug_t;           // lip on the front only, back stays open
t = tan(tilt);

in_len = mouth_ext + bat_l + 2*bat_clr; // left opening -> end stop
in_w   = bat_w + 2*bat_clr;
in_h   = bat_h + 2*bat_clr;
by0    = skin;                          // passage runs right behind the front wall
by1    = by0 + in_w;                    // back of the passage
pw1    = by1 + tw;                      // back face of the passage back wall
yc     = (by0 + by1)/2;
in_z0  = tun_floor;                     // battery rests at this height
bore_top = in_z0 + in_h;
gus    = (pad_w - rib_t)/2;             // 45-degree support under each pad

stop_x = in_len;                        // ports end of the battery rests here
bay_x0 = in_len + tw;                   // port bay: from here to the right side
bay_len = W - bay_x0;

front_h = bore_top + rib_cap + pad_t - by0*t;   // pad top at the front edge
back_h  = front_h + D*t;
function deck_z(y) = front_h + y*t;
function rib_x(i) = pad_w/2 + i*(W - pad_w)/(rib_n - 1);
// keep each velcro strip on its pad AND under the QC (clear of the side lips)
function strip_lo(i) = max(rib_x(i) - pad_w/2, lug_t + qc_clr) + velcro_w/2 + 0.5;
function strip_hi(i) = min(rib_x(i) + pad_w/2, W - lug_t - qc_clr) - velcro_w/2 - 0.5;
function strip_x(i) = min(max(rib_x(i), strip_lo(i)), strip_hi(i));
feet = [for (i = [0:rib_n-1]) for (y = [9, D - 9]) [rib_x(i), y]];

// cable exit under the QC's DC input, nudged sideways if it would land on a rib
exit_req = lug_t + qc_clr + dc_x;
exit_hit = [for (i = [0:rib_n-1]) if (abs(exit_req - rib_x(i)) < rib_t/2 + exit_w/2 + 1) i];
exit_x = len(exit_hit) > 0 ? rib_x(exit_hit[0]) + rib_t/2 + exit_w/2 + 1 : exit_req;
chan_x0 = min(exit_x - exit_w/2, bay_x0);        // channel behind the battery: exit <-> bay
chan_x1 = max(exit_x + exit_w/2, bay_x0 + 1);
cy1 = D - tw - 2;                               // tunnel runs along the back wall
cy0 = cy1 - chan_w;

// screen window (x along the battery, z up its side)
win_x0 = stop_x - scr_to;
win_x1 = stop_x - scr_from;
win_z0 = in_z0 + scr_margin;
win_z1 = in_z0 + bat_h - scr_margin;

echo(str("Footprint: ", W, " x ", D, " mm   front ", front_h, " mm, back ", back_h, " mm (plus ", lug_h, " mm lip)"));
echo(str("Ribs at x = ", [for (i = [0:rib_n-1]) rib_x(i)]));
echo(str("Battery passage: ", in_len, " long, opening ", in_w, " x ", in_h, " mm"));
echo(str("Screen window: x ", win_x0, " to ", win_x1, " (", scr_from, " to ", scr_to, " mm from the ports end), ",
         win_z1 - win_z0, " mm tall"));
echo(str("Port bay: ", bay_len, " mm long for a ", plug_len, " mm plug   cable exit at x = ", exit_x,
         (exit_x != exit_req) ? str(" (moved off a rib; DC input is at ", exit_req, ")") : ""));
assert(D - tw - pw1 >= chan_w + 4, "No room for the cable channel behind the battery");
assert(bay_len >= plug_len + 20, "Port bay is too short for the plug plus a gentle bend");
assert(mouth_ext + 2*bat_clr - catch_play >= 3, "Catch too close to the mouth - increase mouth_ext");
assert(win_x0 > tongue_len + 10, "Screen window runs into the latch area");
for (i = [0:rib_n-1]) assert(strip_lo(i) <= strip_hi(i) + 0.01, str("Velcro strip doesn't fit on pad ", i, " - widen pad_w"));
for (i = [0:rib_n-1]) assert(rib_x(i) + rib_t/2 < stop_x || rib_x(i) - rib_t/2 > bay_x0, str("Rib ", i, " collides with the end stop"));

module on_deck() {
    translate([0,0,front_h]) multmatrix([[1,0,0,0],[0,1,0,0],[0,t,1,0],[0,0,0,1]]) children();
}
// side profile up to the pads (top = offset from the deck surface), extruded across x0..x1
module profile(x0, x1, y_from = 0, y_to = D, top = -pad_t + 0.5) {
    translate([x0, 0, 0]) rotate([90,0,90]) linear_extrude(x1 - x0)
        polygon([[y_from, 0], [y_to, 0], [y_to, deck_z(y_to) + top], [y_from, deck_z(y_from) + top]]);
}

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
    profile(0, bay_x0, by1 - 0.01, pw1);            // passage back wall, as far as the end stop
    profile(0, W, D - tw, D);                       // back wall
}
module lips() {
    on_deck() {
        translate([0, 0, -0.5]) cube([W, lug_t, lug_h + 0.5]);                                  // front
        translate([W - lug_t, 0, -0.5]) cube([lug_t, D - side_trim, lug_h + 0.5]);              // right
        translate([0, 0, -0.5]) cube([lug_t, lug_t + qc_clr + btn_from, lug_h + 0.5]);          // left, short
    }
}
// battery passage + port bay: one opening right through, from the left side to the right side
module bore() { translate([-1, by0, -1]) cube([W + 2, in_w, bore_top + 1]); }

module screen_window() {
    c = 1.5;   // chamfer on the outside edge, for a wider viewing angle
    hull() {
        translate([win_x0, by0 + 0.5, win_z0]) cube([win_x1 - win_x0, 0.01, win_z1 - win_z0]);
        translate([win_x0 - c, -0.01, win_z0 - c]) cube([win_x1 - win_x0 + 2*c, 0.01, win_z1 - win_z0 + 2*c]);
    }
    translate([win_x0 - c, -1, win_z0 - c]) cube([win_x1 - win_x0 + 2*c, 1, win_z1 - win_z0 + 2*c]);
}

module cable_route() {
    // tunnel (with a self-supporting 45-degree peak) through any rib between the bay and the exit
    translate([chan_x0, 0, 0]) rotate([90,0,90]) linear_extrude(chan_x1 - chan_x0)
        polygon([[cy0, tun_floor - 0.01], [cy1, tun_floor - 0.01], [cy1, tun_floor + chan_h],
                 [(cy0 + cy1)/2, tun_floor + chan_h + chan_w/2], [cy0, tun_floor + chan_h]]);
    // exit slot through the back wall, open at the top so the cable drops in from above
    translate([exit_x - exit_w/2, D - tw - 1, tun_floor]) cube([exit_w, tw + 2, 200]);
}

module velcro_recesses() {
    on_deck() for (i = [0:rib_n-1])
        translate([strip_x(i) - velcro_w/2, (D - velcro_len)/2, -velcro_depth]) cube([velcro_w, velcro_len, velcro_depth + 1]);
}

module vents() {
    // slots in the passage back wall (into the cable channel), between the ribs, clear of the gussets
    for (i = [0:rib_n-2]) {
        xa = rib_x(i) + pad_w/2 + 4; xb = min(rib_x(i+1) - pad_w/2 - 4, stop_x - 4);
        if (xb - xa > 10)
            for (x = [xa : 8 : xb - 4]) translate([x, by1 - 1, in_z0 + 5]) cube([4, tw + 2, in_h - 10]);
    }
}

module end_stop() {
    // two posts the ports end rests against; the middle stays open for the plugs
    for (y = [by0 - 0.5, by1 - stop_w]) translate([stop_x, y, 0]) cube([tw, stop_w + 0.5, bore_top + 0.5]);
}

module floor_parts() {
    // rails the battery rests on, continued through the port bay
    translate([0, by0 - 0.5, 0]) cube([W, ledge_w + 0.5, tun_floor]);
    translate([0, by1 - ledge_w, 0]) cube([W, ledge_w + 0.5, tun_floor]);
    // cross bars (the first one is the tongue's root)
    for (x = concat([tongue_len], bar_x)) translate([x, by0 - 0.5, 0]) cube([8, in_w + 1, tun_floor]);
    // floor under the cable channel (the middle of the bay stays open so the rib arch over it
    // can have build-plate supports)
    translate([chan_x0, by1 - 0.5, 0]) cube([W - chan_x0, D - tw - by1 + 1, tun_floor]);
    // sprung tongue + press tab, printed flat on the bed
    translate([-tab_len, yc - tongue_w/2, 0]) cube([tab_len + tongue_len + 0.5, tongue_w, tun_floor]);
    for (x = [-tab_len + 1 : 2.5 : -1]) translate([x, yc - tongue_w/2, tun_floor - 0.01]) cube([1, tongue_w, 0.8]);
    // catch: ramp toward the mouth, square face against the battery's end
    catch_x = mouth_ext + 2*bat_clr - catch_play;
    translate([0, yc + tongue_w/2, 0]) rotate([90,0,0]) linear_extrude(tongue_w)
        polygon([[0.5, tun_floor - 0.01], [catch_x, tun_floor - 0.01], [catch_x, tun_floor + bump_h], [catch_x - 2, tun_floor + bump_h]]);
    // pads for the stick-on feet
    for (f = feet) translate([f[0], f[1], 0]) cylinder(d = foot_pad_d, h = tun_floor);
    end_stop();
}

module frame() {
    difference() {
        union() {
            difference() {
                union() { ribs(); pads(); walls(); lips(); }
                bore();
                vents();
                screen_window();
                cable_route();
                velcro_recesses();
            }
            floor_parts();
        }
        for (f = feet) translate([f[0], f[1], -0.01]) cylinder(d = foot_d + 0.5, h = foot_depth);
    }
}

// =====================================================================
if (part == "assembly") {
    color("SteelBlue") frame();
    %on_deck() translate([lug_t + qc_clr, lug_t + qc_clr, 0]) cube([qc_w, qc_d, qc_h]);
    %translate([stop_x - bat_l, by0 + bat_clr, in_z0]) cube([bat_l, bat_w, bat_h]);
    %translate([stop_x, yc - 6, in_z0 + bat_h/2 - 4]) cube([plug_len, 12, 8]);       // USB plug
}
if (part == "frame") frame();
if (part == "test_mouth")
    // the left end: tongue, catch, rails and the first rib, to check the battery fit and click
    translate([tab_len, 1, 0]) intersection() {
        frame();
        translate([-tab_len - 1, -1, -1]) cube([tab_len + tongue_len + 14, pw1 + 2, 200]);
    }
if (part == "test_ports") {
    // the right end, cut off just below the top of the battery opening (so nothing needs
    // support): screen window, end stop, port bay and cable exit
    x0 = win_x0 - 8;
    x1 = min(bay_x0 + plug_len + 20, rib_x(rib_n - 1) - rib_t/2 - 2);
    translate([-x0, 0, 0]) intersection() {
        frame();
        translate([x0, -1, -1]) cube([x1 - x0, D + 2, bore_top - 0.5 + 1]);
    }
}
