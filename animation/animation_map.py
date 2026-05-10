import json
import math
import folium
from pathlib import Path

# --- Configuration ---
FRAME_DELAY_MS = 300
OUTPUT_FILE = Path(__file__).parent / "map_animation.html"

# JSON data
positions = [
    [50.710000, 7.090000], [50.710300, 7.090200], [50.710600, 7.090450],
    [50.710900, 7.090700], [50.711200, 7.090950], [50.711500, 7.091200],
    [50.711800, 7.091450], [50.712100, 7.091700], [50.712400, 7.091950],
    [50.712700, 7.092200]
]


def compute_bearing(lat1, lon1, lat2, lon2):
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_theta = math.radians(lon2 - lon1)
    x = math.sin(delta_theta) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(delta_theta)
    return (math.degrees(math.atan2(x, y)) + 360) % 360


# Calculate bearings for each segment
bearings = [compute_bearing(*positions[i], *positions[i + 1]) for i in range(len(positions) - 1)]
bearings.append(bearings[-1])  # Keep last heading

# --- Create Map ---
m = folium.Map(
    location=positions[0],
    zoom_start=17,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{x}/{y}",
    attr="Esri World Imagery"
)

# --- CSS and JS Elements ---
map_id = m.get_name()

style = """
<style>
    .play-btn-ctrl {
        background: white; padding: 10px; border: 2px solid #666; 
        border-radius: 5px; cursor: pointer; font-weight: bold;
    }
    .arrow-icon {
        width: 0; height: 0; 
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        border-bottom: 16px solid yellow;
    }
</style>
"""

script = f"""
<script>
document.addEventListener("DOMContentLoaded", function() {{
    var posData = {json.dumps(positions)};
    var brgData = {json.dumps(bearings)};
    var map = {map_id};

    var idx = 0;
    var isPlaying = false;

    // Initial Marker and Trail
    var mainMarker = L.marker(posData[0]).addTo(map);
    var trail = L.polyline([posData[0]], {{color: 'cyan', weight: 3}}).addTo(map);

    var headIcon = L.divIcon({{
        className: 'arrow-parent',
        html: '<div class="arrow-icon" id="arrow"></div>',
        iconSize: [16, 16],
        iconAnchor: [8, 8]
    }});
    var headMarker = L.marker(posData[0], {{icon: headIcon}}).addTo(map);

    function step() {{
        if (!isPlaying || idx >= posData.length - 1) {{
            isPlaying = false;
            return;
        }}
        idx++;
        var p = posData[idx];
        var b = brgData[idx];

        mainMarker.setLatLng(p);
        headMarker.setLatLng(p);

        // Rotate the arrow
        var el = document.getElementById('arrow');
        if (el) el.style.transform = "rotate(" + b + "deg)";

        trail.addLatLng(p);
        map.panTo(p);

        setTimeout(step, {FRAME_DELAY_MS});
    }}

    var Control = L.Control.extend({{
        options: {{ position: 'topright' }},
        onAdd: function() {{
            var btn = L.DomUtil.create('div', 'play-btn-ctrl');
            btn.innerHTML = '▶ Play Path';
            btn.onclick = function() {{
                if (!isPlaying) {{
                    isPlaying = true;
                    step();
                }}
            }};
            return btn;
        }}
    }});
    map.addControl(new Control());
}});
</script>
"""

m.get_root().header.add_child(folium.Element(style))
m.get_root().html.add_child(folium.Element(script))

# Save
OUTPUT_FILE.parent.mkdir(exist_ok=True)
m.save(str(OUTPUT_FILE))
print(f"Success! Open: {{OUTPUT_FILE}}")import json
import math
import folium
from pathlib import Path

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

FRAME_DELAY_MS = 200  # Animation speed (200 ms per frame)
INPUT_FILE = Path(__file__).parent / "positions_example.json"
OUTPUT_FILE = Path(__file__).parent / "output" / "map_animation.html"

# ------------------------------------------------------------
# Bearing calculation
# ------------------------------------------------------------

def compute_bearing(lat1, lon1, lat2, lon2):
    """
    Compute bearing from point 1 to point 2 using navigation convention:
    - North = 0°
    - East = 90°
    - Bearing measured clockwise
    """
    φ1, φ2 = math.radians(lat1), math.radians(lat2)
    Δθ = math.radians(lon2 - lon1)

    x = math.sin(Δθ) * math.cos(φ2)
    y = math.cos(φ1) * math.sin(φ2) - math.sin(φ1) * math.cos(φ2) * math.cos(Δθ)

    θ = math.atan2(x, y)
    bearing = (math.degrees(θ) + 360) % 360
    return bearing

# ------------------------------------------------------------
# Load positions
# ------------------------------------------------------------

with open(INPUT_FILE, "r") as f:
    positions = json.load(f)

if len(positions) < 2:
    raise ValueError("Need at least two positions for animation.")

# Compute bearings for each step
bearings = []
for i in range(len(positions) - 1):
    lat1, lon1 = positions[i]
    lat2, lon2 = positions[i + 1]
    bearings.append(compute_bearing(lat1, lon1, lat2, lon2))

# Last bearing = same as previous
bearings.append(bearings[-1])

# ------------------------------------------------------------
# Create Folium map (ESRI Satellite)
# ------------------------------------------------------------

start_lat, start_lon = positions[0]

m = folium.Map(
    location=[start_lat, start_lon],
    zoom_start=16,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{x}/{y}",
    attr="Esri World Imagery"
)

# ------------------------------------------------------------
# Destination marker
# ------------------------------------------------------------

dest_lat, dest_lon = positions[-1]
folium.Marker(
    location=[dest_lat, dest_lon],
    popup="Destination",
    icon=folium.Icon(color="green", icon="flag")
).add_to(m)

# ------------------------------------------------------------
# JavaScript animation logic
# ------------------------------------------------------------

triangle_icon = """
var triangleIcon = L.divIcon({
    className: "triangle-icon",
    html: `<div style="
        width: 0;
        height: 0;
        border-left: 10px solid transparent;
        border-right: 10px solid transparent;
        border-bottom: 20px solid red;
        transform: rotate(0deg);
    "></div>`,
    iconSize: [20, 20],
    iconAnchor: [10, 10]
});
"""

js_positions = json.dumps(positions)
js_bearings = json.dumps(bearings)


style = """
<style>
.play-button-container {
    background: white;
    padding: 6px;
    border-radius: 6px;
    box-shadow: 0 0 6px rgba(0,0,0,0.4);
    position: relative;
    z-index: 9999;
}
.leaflet-top.leaflet-right {
    overflow: visible !important;
}
#play-btn {
    font-size: 16px;
    padding: 6px 10px;
    cursor: pointer;
}
</style>
"""


m.get_root().header.add_child(folium.Element(style))


## --. Animation -- 
animation_js = f"""
<script>

{triangle_icon}

var positions = {js_positions};
var bearings = {js_bearings};
var frameDelay = {FRAME_DELAY_MS};

var marker = L.marker(positions[0]).addTo({m.get_name()});
var heading = L.marker(positions[0], {{icon: triangleIcon}}).addTo({m.get_name()});

var trail = L.polyline([positions[0]], {{color: 'yellow'}}).addTo({m.get_name()});

var currentIndex = 0;
var playing = false;

function updateFrame() {{
    if (!playing) return;

    currentIndex++;
    if (currentIndex >= positions.length) {{
        playing = false;
        return;
    }}

    var pos = positions[currentIndex];
    var brg = bearings[currentIndex];

    marker.setLatLng(pos);
    heading.setLatLng(pos);

    var iconEl = heading.getElement().querySelector("div");
    iconEl.style.transform = "rotate(" + brg + "deg)";

    trail.addLatLng(pos);

    setTimeout(updateFrame, frameDelay);
}}

function startAnimation() {{
    if (!playing) {{
        playing = true;
        updateFrame();
    }}
}}

</script>
"""
m.get_root().html.add_child(folium.Element(animation_js))

# ----- Add playy button ----------------
play_button_js = f"""
<script>

var playControl = L.Control.extend({{
    onAdd: function(map) {{
        var div = L.DomUtil.create('div', 'play-button-container');
        div.innerHTML = '<button id="play-btn" style="font-size:16px;padding:6px;cursor:pointer;">▶ Play</button>';
        div.onclick = function() {{
            startAnimation();
        }};
        return div;
    }},
    onRemove: function(map) {{}}
}});

(new playControl({{ position: 'topright' }})).addTo({m.get_name()});

</script>
"""
m.get_root().html.add_child(folium.Element(play_button_js))


# ------------------------------------------------------------
# Save output
# ------------------------------------------------------------

OUTPUT_FILE.parent.mkdir(exist_ok=True)
m.save(str(OUTPUT_FILE))

print(f"Animation saved to: {OUTPUT_FILE}")
