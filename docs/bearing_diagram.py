import matplotlib.pyplot as plt
import numpy as np

# Bearing angle in degrees (example: 60°)
theta_b = 60  

# Convert to radians
theta_rad = np.deg2rad(theta_b)

# Arrow length
r = 1.0

# Bearing vector
bx = r * np.sin(theta_rad)   # East component
by = r * np.cos(theta_rad)   # North component

# Create figure
fig, ax = plt.subplots(figsize=(6, 6))

# Draw axes
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)

# Draw grid
ax.grid(True, linestyle='--', linewidth=0.5, alpha=0.7)

# Draw North arrow
ax.arrow(0, 0, 0, 1.2, head_width=0.05, head_length=0.08,
         fc='black', ec='black', linewidth=1.2)
ax.text(0, 1.28, "N (0°)", ha='center', va='bottom', fontsize=12)

# Draw East label
ax.text(1.25, 0, "E (90°)", ha='left', va='center', fontsize=12)

# Draw bearing arrow
ax.arrow(0, 0, bx, by, head_width=0.05, head_length=0.08,
         fc='red', ec='red', linewidth=2)
ax.text(bx * 1.05, by * 1.05, f"θ_b = {theta_b}°", color='red',
        ha='left', va='bottom', fontsize=12)

# Draw angle arc
arc_theta = np.linspace(0, theta_rad, 100)
arc_x = 0.3 * np.sin(arc_theta)
arc_y = 0.3 * np.cos(arc_theta)
ax.plot(arc_x, arc_y, color='green', linewidth=2)
ax.text(0.22, 0.22, "θ_b", color='green', fontsize=12)

# Set limits
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)

# Equal aspect ratio
ax.set_aspect('equal', adjustable='box')

# Labels
ax.set_xlabel("East (X-axis)")
ax.set_ylabel("North (Y-axis)")

# Title
ax.set_title("Bearing Angle Diagram (Navigation Convention)")

# Save figure
plt.savefig("bearing_diagram.png", dpi=300, bbox_inches='tight')

plt.show()
