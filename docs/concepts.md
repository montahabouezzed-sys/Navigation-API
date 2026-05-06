# Navigation Concepts and Geodesy Fundamentals

This document provides the essential concepts used in  Navigation-API, including
definitions, formulas, and geometric intuition for distance, bearing, and trend
calculation. It is designed to make the project self‑contained and accessible to
readers without a GNSS or geodesy background.

---

## 1. Geographic Coordinates

### **Latitude (φ)**
- Measures how far north or south a point is from the equator.
- Range: **–90° to +90°**
- Positive = north, negative = south.

### **Longitude (λ)**
- Measures how far east or west a point is from the Prime Meridian.
- Range: **–180° to +180°**
- Positive = east, negative = west.

Together, latitude and longitude define a point on the Earth’s surface.

---

## 2. Haversine Distance

The **Haversine formula** computes the great‑circle distance between two points on a sphere.
It is widely used in navigation, aviation, and GPS systems.

### **Formula**

Given two points:

- Current position: (φ₁, λ₁)
- Destination: (φ₂, λ₂)

The distance **d** is:



\[
a = \sin^2\left(\frac{\Delta\varphi}{2}\right)
  + \cos(\varphi_1)\cos(\varphi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)
\]





\[
c = 2 \cdot \arctan2(\sqrt{a}, \sqrt{1-a})
\]





\[
d = R \cdot c
\]



Where:

- \( R = 6371000 \) m (mean Earth radius)
- \( \Delta\varphi = \varphi_2 - \varphi_1 \)
- \( \Delta\lambda = \lambda_2 - \lambda_1 \)

### **Interpretation**
This gives the shortest path along the Earth’s surface — the “as‑the‑crow‑flies” distance.

---

## 3. Bearing (Initial Azimuth)

**Bearing** is the direction from the current position to the destination,
expressed as an angle measured **clockwise from geographic north**.

It answers the question:

> “If I stand at point A, in which direction should I face to go toward point B?”

### **Formula**



\[
\theta = \arctan2\left(
\sin(\Delta\lambda)\cos(\varphi_2),
\cos(\varphi_1)\sin(\varphi_2)
- \sin(\varphi_1)\cos(\varphi_2)\cos(\Delta\lambda)
\right)
\]



Convert to degrees and normalize:



\[
\theta_{\text{deg}} = (\theta \cdot 180/\pi + 360) \mod 360
\]



### **Interpretation**
- 0° = North  
- 90° = East  
- 180° = South  
- 270° = West  

---

## 4. Trend Logic

The **trend** indicates whether the user is moving:

- **getting closer**  
- **getting farther**  
- **stationary**  
- **unknown** (first measurement)

### **Logic**

Given:
- previous distance: \( d_{\text{prev}} \)
- current distance: \( d_{\text{curr}} \)

We compare:

- If \( d_{\text{curr}} < d_{\text{prev}} \): **getting closer**
- If \( d_{\text{curr}} > d_{\text{prev}} \): **getting farther**
- If \( |d_{\text{curr}} - d_{\text{prev}}| < \epsilon \): **stationary**
- If no previous distance exists: **unknown**

Where \( \epsilon \) is a small threshold (e.g., 0.5 m).

---

## 5. Coordinate System Orientation

The Navigation API assumes:

- North is **0°**
- Angles increase **clockwise**
- Earth is approximated as a sphere (sufficient for short‑range navigation)

This matches common conventions in:
- aviation  
- maritime navigation  
- robotics  
- mobile GNSS applications  

---

## 6. Bearing Diagram (Placeholder)

A diagram will be added here showing:

- Current position  
- Destination  
- North direction  
- Bearing angle (clockwise from north)  
- Great‑circle path  

**File placeholder:**  
`docs/bearing_diagram.png`

---

## 7. References

- Movable Type Scripts — Great-circle distance and bearing formulas  
- FAA Navigation Handbook  
- GPS.gov — Positioning Basics  

---

This document is part of the Navigation API and supports clarity, reproducibility,
and technical understanding for future extensions (speed, ETA, history, animation).

