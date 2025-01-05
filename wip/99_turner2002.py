"""Create two component complex vector."""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk

# =============================================================================
# Initial parameters
# =============================================================================
BETA = 0.02  # capillary volume fraction in percent
CAP_LENGTH = 200  # mean cappillary length, in micro meter 
CAP_DIAMETER = 5  # capillary diameter in millimeters
VES_DIAMETER = 0.6  # millimeter
THICKNESS = 3  # cortical thickness in mm

# =============================================================================
# Functions
# =============================================================================
def turner2022_eq4(beta, d_c, l_c, d_v, t):
    """How much activated area a vein can drain?"""
    return (np.pi / (4*beta*d_c)) * d_v**3 * l_c / t

# =============================================================================
# Plot
# =============================================================================
# Initial number value
initial_value = turner2022_eq4(beta=BETA, d_c=CAP_DIAMETER, l_c=CAP_LENGTH,
                               d_v=VES_DIAMETER, t=THICKNESS)

# Set up the figure and axis
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.35)  # Make room for sliders

# Plot initial data
x = 0
y = turner2022_eq4(beta=BETA, d_c=CAP_DIAMETER, l_c=CAP_LENGTH,
                   d_v=VES_DIAMETER, t=THICKNESS)
point, = plt.plot(x, y, 'ro', label="Point")

# Add axis labels
# ax.set_xlim(-10, 10)
ax.set_ylim(0, 1000)
ax.axhline(0, color='black', linewidth=0.5)
ax.axvline(0, color='black', linewidth=0.5)

# Slider Axes
ax1 = plt.axes([0.40, 0.25, 0.5, 0.03])
ax2 = plt.axes([0.40, 0.20, 0.5, 0.03])
ax3 = plt.axes([0.40, 0.15, 0.5, 0.03])
ax4 = plt.axes([0.40, 0.10, 0.5, 0.03])
ax5 = plt.axes([0.40, 0.05, 0.5, 0.03])

# Sliders
slider1 = Slider(ax1, r"Capillary Volume Fraction, $\beta$ [%]", 0.01, 0.05,
                 valinit=BETA, valstep=0.001)
slider2 = Slider(ax2, r"Capillary Length, $l_c$ [um]",100, 300,
                 valinit=CAP_LENGTH, valstep=10)
slider3 = Slider(ax3, r"Capillary Diameter, $d_c$ [um]", 1, 10,
                 valinit=CAP_DIAMETER, valstep=1)
slider4 = Slider(ax4, r"Vessel Diameter, $d_v$ [mm]", 0.1, 1,
                 valinit=VES_DIAMETER, valstep=0.01)
slider5 = Slider(ax5, r"Thickness, $t$ [mm]", 2, 4,
                 valinit=THICKNESS, valstep=0.1)

# Update function for sliders
def update(val):
    BETA = slider1.val
    CAP_LENGTH = slider2.val
    CAP_DIAMETER = slider3.val
    VES_DIAMETER = slider4.val
    THICKNESS = slider5.val
    y_new = turner2022_eq4(beta=BETA, d_c=CAP_DIAMETER, l_c=CAP_LENGTH, 
                           d_v=VES_DIAMETER, t=THICKNESS)
    point.set_ydata([y_new])
    fig.canvas.draw_idle()

# Connect sliders to update function
slider1.on_changed(update)
slider2.on_changed(update)
slider3.on_changed(update)
slider4.on_changed(update)
slider5.on_changed(update)

ax.grid(axis='y', linestyle='--', color='gray')
ax.get_xaxis().set_visible(False)  # Hide the y-axis
ax.set_title(r"WIP... $(\pi / (4 \beta d_c)) d_v^3 l_c / t$")
ax.set_ylabel("Drained Region [$mm^2$]")

plt.show()

