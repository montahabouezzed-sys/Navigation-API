📍 Navigation API — Minimal GNSS Distance & Bearing Service
A lightweight FastAPI service that computes:

Distance to a destination (Haversine)

Bearing (initial azimuth)

Trend: getting closer / farther / stationary

This project demonstrates clean API design, geodesy fundamentals, and a modular Python architecture suitable for extension (speed, ETA, history, map animation (under construction)).


🚀 Features
Set a destination (lat/lon)

Update current position

Compute:

Distance (meters)

Bearing (degrees)

Trend (closer / farther / unknown)

Simple in‑memory state

Fully modular structure


🗂 Project Structure
```text
📂 navigation-api/
├── 📂 app/
│   ├── main.py
│   ├── models.py
│   ├── logic.py
│   ├── state.py
│   └── tests/
├── 📂 docs/
│   ├── concepts.md
│   ├── bearing_diagram.py
│   ├── bearing_diagram.png
│── 📂 animation/
│   ├── animation_map.py
│   ├── positions_example.json
│   └── output/
│       └── ...
├── requirements.txt
└── README.md
```
 
▶️ Run Locally
1. Clone the repository
```bash 

git clone https://github.com/montahabouezzed-sys/Navigation-API.git
cd Navigation-API
```

2. Create a virtual environment
 ```bash 
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies
```bash 
   pip install -r requirements.txt
   ```

4. Start the server
```bash 
uvicorn app.main:app --reload
   ```

5. Open the API docs, visit:
```bash    
http://127.0.0.1:8000/docs
 ```

📌 Future Extensions
Speed estimation

ETA calculation

Position history

Map animation

SQLite storage

CLI client

