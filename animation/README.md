# Navigation Path Animation (Folium + Leaflet)

This project generates an animated navigation path on top of **ESRI World Imagery** using
Python, Folium, and custom JavaScript injected into the final HTML.

The animation shows:

- A **triangle heading marker** that rotates according to the computed bearing  
- A **trail polyline** following the movement  
- A **Play button** to start the animation  
- A **destination marker**  
- Smooth movement between GPS points  

The output is a standalone HTML file that runs entirely in the browser.

---

## 📁 Project Structure




---

## 📥 Input Data

The animation uses a list of GPS coordinates stored in:
positions_example.json



Example format:

```json
[
    [50.7100, 7.0900],
    [50.7103, 7.0902],
    [50.7106, 7.0904],
    ...
]
```

▶️ Running the Script

Generate the animation:
python animation_map.py

This creates:
bach

output/map_animation.html



🌐 Viewing the Animation
Because browsers block JavaScript in file:/// mode,
you must serve the file using a local HTTP server:

python -m http.server 8000

Then open:
http://localhost:8000/output/map_animation.html

You will see:

ESRI satellite imagery

A yellow triangle heading marker

A blue trail

A “Play Path” button

Smooth animated movement

🧠 How It Works
1. Bearing Calculation
The script computes the heading between each pair of GPS points using standard trigonometry.

2. Folium Map
A Folium map is created with ESRI World Imagery tiles.

3. JavaScript Injection
Custom JS is injected after Folium’s map initialization to ensure:

correct execution order

visible UI controls

working animation

4. Animation
The triangle rotates according to the bearing and moves along the path with a configurable frame delay.



✔ Requirements
Install dependencies:

bash
pip install folium
(Optional) If you use a virtual environment, ensure it is activated before running the script.

🎯 Features
ESRI satellite tiles

Rotating triangle heading marker

Play button UI

Smooth animation

Trail polyline

Fully offline HTML output

📸 Example Output
screenshot here





