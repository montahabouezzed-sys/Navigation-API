# Navigation Concepts and Geodesy Fundamentals

This document explains the mathematical and navigational concepts used in the Navigation API.
It is designed to be self‑contained, technically precise, and accessible to readers without
a geodesy background.

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

A point on Earth is represented as:
```math
(\varphi, \lambda)
```
---

2. Haversine Distance

The **Haversine formula** computes the great‑circle distance between two points on a sphere.

Given:
- Current position:
```math
- Current position: ```math
(\varphi_1, \lambda_1)
```
- Destination:
```math
  \( (\varphi_2, \lambda_2) \)
```

Define:
```math
\[
\Delta\varphi = \varphi_2 - \varphi_1, \qquad
\Delta\lambda = \lambda_2 - \lambda_1
\]
```

Compute:

```math
\[
a = \sin^2\left(\frac{\Delta\varphi}{2}\right)
  + \cos(\varphi_1)\cos(\varphi_2)\sin^2\left(\frac{\Delta\lambda}{2}\right)
\]
```



```math
\[
c = 2 \cdot \arctan2\left(\sqrt{a}, \sqrt{1-a}\right)
\]

```

Distance:



```math
\[
d = R \cdot c
\]
```


Where:


```math
\[
R = 6\,371\,000 \text{ m}
\]
```


---

## 3. Bearing (Initial Azimuth)

**Bearing** is the direction from the current position to the destination,
measured **clockwise from geographic north**.

It answers:

> “If I stand at point A, which direction should I face to reach point B?”

Formula:

```math

\[
\theta =
\arctan2\left(
\sin(\Delta\lambda)\cos(\varphi_2),
\cos(\varphi_1)\sin(\varphi_2)
- \sin(\varphi_1)\cos(\varphi_2)\cos(\Delta\lambda)
\right)
\]
```


Convert to degrees and normalize:

```math

\[
\theta_{\text{deg}} = (\theta \cdot \frac{180}{\pi} + 360) \bmod 360
\]
```


### **Interpretation**
```math
- \(0^\circ\) = North  
- \(90^\circ\) = East  
- \(180^\circ\) = South  
- \(270^\circ\) = West  
```
---

## 4. Trend Logic

The **trend** indicates whether the user is moving toward or away from the destination.

Given:
- Previous distance: 
```math  \( d_{\text{prev}} \) ```
- Current distance: 
```math \( d_{\text{curr}} \) ```

We compare:

```math

\[
\text{If } d_{\text{curr}} < d_{\text{prev}} \Rightarrow \text{getting closer}
\]
```

```math
\[
\text{If } d_{\text{curr}} > d_{\text{prev}} \Rightarrow \text{getting farther}
\]
```
```math
\[
\text{If } |d_{\text{curr}} - d_{\text{prev}}| < \varepsilon \Rightarrow \text{stationary}
\]
```

```math
\[
\text{If no previous distance exists} \Rightarrow \text{unknown}
\]
```


Where:


```math
\[
\varepsilon \approx 0.5 \text{ m}
\]
```


---

## 5. Coordinate System Orientation

The Navigation API uses the standard geodesy convention:

- North is \(0^\circ\)
- Angles increase clockwise
- Earth is approximated as a sphere (sufficient for short‑range navigation)

This matches conventions in:
- aviation  
- maritime navigation  
- robotics  
- GNSS receivers  

---

## 6. Bearing Diagram (Placeholder)

A diagram will be added here showing:

- Current position  
- Destination  
- North direction  
- Bearing angle  
- Great‑circle path  

**File placeholder:**  
`docs/bearing_diagram.png`

---

## 7. References

- Movable Type Scripts — Great‑circle distance and bearing formulas  
- FAA Navigation Handbook  
- GPS.gov — Positioning Basics  

---

This document supports clarity, reproducibility, and technical understanding for future extensions
(speed, ETA, history, animation).
