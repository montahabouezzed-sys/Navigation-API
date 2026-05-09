import json
import math
import folium
from folium.features import CustomIcon
from pathlib import Path

# ------------------------------------------------------------
# Configuration
# ------------------------------------------------------------

FRAME_DELAY_MS = 200  # Animation speed (200 ms per frame)
INPUT_FILE = Path(__file__).parent / "positions_example.json"
OUTPUT_FILE = Path(__file__).parent / "output" / "map_animation.html"

# ------------------------------------------------------------
# Bearing calculation (φ = lat, θ = lon)
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
# Create Folium map
# ------------------------------------------------------------

start_lat, start_lon = positions[0]
#m = folium.Map(location=[start_lat, start_lon], zoom_start=16)
m = folium.Map(
    location=[start_lat, start_lon],
    zoom_start=16,
    tiles="https://tile.openstreetmap.fr/hot/{z}/{x}/{y}.png",
    attr="OSM HOT"
)


# Add destination marker
dest_lat, dest_lon = positions[-1]
folium.Marker(
    location=[dest_lat, dest_lon],
    popup="Destination",
    icon=folium.Icon(color="green", icon="flag")
).add_to(m)

# ------------------------------------------------------------
# Add JS animation logic
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

# Convert Python lists to JS arrays
js_positions = json.dumps(positions)
js_bearings = json.dumps(bearings)

animation_js = f"""
<script>

{triangle_icon}

var positions = {js_positions};
var bearings = {js_bearings};
var frameDelay = {FRAME_DELAY_MS};

var marker = L.marker(positions[0]).addTo({m.get_name()});
var heading = L.marker(positions[0], {{icon: triangleIcon}}).addTo({m.get_name()});

var trail = L.polyline([positions[0]], {{color: 'blue'}}).addTo({m.get_name()});

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

    // Rotate triangle
    var iconEl = heading.getElement().querySelector("div");
    iconEl.style.transform = "rotate(" + brg + "deg)";

    // Extend trail
    trail.addLatLng(pos);

    setTimeout(updateFrame, frameDelay);
}}

function startAnimation() {{
    if (!playing) {{
        playing = true;
        updateFrame();
    }}
}}

var playButton = L.control({{position: 'topright'}});
playButton.onAdd = function(map) {{
    var div = L.DomUtil.create('div', 'play-button');
    div.innerHTML = '<button style="font-size:16px;padding:6px;">▶ Play</button>';
    div.onclick = startAnimation;
    return div;
}};
playButton.addTo({m.get_name()});

</script>
"""

m.get_root().html.add_child(folium.Element(animation_js))

# ------------------------------------------------------------
# Save output
# ------------------------------------------------------------

OUTPUT_FILE.parent.mkdir(exist_ok=True)
m.save(str(OUTPUT_FILE))

print(f"Animation saved to: {OUTPUT_FILE}")

