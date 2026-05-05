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

navigation-api/
│── app/
│   ├── main.py        # FastAPI routes
│   ├── models.py      # Pydantic models
│   ├── logic.py       # Haversine, bearing, trend
│   └── state.py       # In-memory state
│── tests/             # (future)
│── requirements.txt
│── README.md


▶️ Run Locally
1. Clone the repository
   batch
   '''
git clone https://github.com/<your-username>/Navigation-API.git
cd Navigation-API
'''

2. Create a virtual environment
python -m venv venv
venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Start the server
uvicorn app.main:app --reload

5. Open the API docs
http://127.0.0.1:8000/docs


📌 Future Extensions
Speed estimation

ETA calculation

Position history

Map animation

SQLite storage

CLI client

