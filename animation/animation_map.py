import json
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
