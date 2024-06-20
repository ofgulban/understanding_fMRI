"""Create two component complex vector."""

import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk

# =============================================================================
# Initial parameters
# =============================================================================
MAG1 = 50
DEG1 = 45
RAD1 = DEG1 / 360 * 2 * np.pi
VEC1 = MAG1 * np.cos(RAD1) + 1j * (MAG1 * np.sin(RAD1))

MAG2 = 50
DELTADEG = 30
DEG2 = DEG1 - DELTADEG
RAD2 = DEG2 / 360 * 2 * np.pi
VEC2 = MAG2 * np.cos(RAD2) + 1j * (MAG2 * np.sin(RAD2))

VEC3 = VEC1 + VEC2

THETA = np.arctan(20 / np.abs(VEC3))
THETA = THETA / (2*np.pi) * 360

TS_MAG = np.full(100, np.abs(VEC3))
TS_DEG = np.full(100, np.angle(VEC3) % (2*np.pi) * (180/np.pi))
TS_THETA = np.full(100, 50.)

# =============================================================================
# Functions
# =============================================================================
def plot_complex_data(ax, vector1, vector2, vector3):
    ax.cla()
    ax.set_aspect('equal')
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.axhline(y=0, color='black', linestyle='-')
    ax.axvline(x=0, color='black', linestyle='-')
    ax.set_xlim([-150, 150])
    ax.set_ylim([-150, 150])

    # Vectors
    ax.plot([0, vector1.real], [0, vector1.imag],
        linestyle='-', linewidth=1.5, color='gray')
    ax.plot([vector1.real, vector3.real], [vector1.imag, vector3.imag],
        linestyle='-', linewidth=1.5, color='red')
    ax.plot([0, vector3.real], [0, vector3.imag],
        linestyle='-', linewidth=1.5, color='black')
    fig1.canvas.draw_idle()

    # Spread circle
    circle = plt.Circle((vector3.real, vector3.imag), radius=20, color='black', 
        fill=False, linestyle='-', linewidth=0.5, label='Circle')
    ax.add_patch(circle)


def plot_timeseries(ax, mag, deg, theta):
    # Magnitude
    ax[0].cla()
    ax[0].set_xlabel('Time')
    ax[0].set_ylabel('Magnitude')
    ax[0].axhline(y=0, color='black', linestyle='-')
    ax[0].axvline(x=0, color='black', linestyle='-')
    ax[0].set_xlim([0, 100])
    ax[0].set_ylim([0, 200])
    ax[0].plot(np.arange(100), mag,
        linestyle='-', linewidth=1.5, color='gray')

    # Phase
    ax[1].cla()
    ax[1].set_xlabel('Time')
    ax[1].set_ylabel('Phase')
    ax[1].axhline(y=0, color='black', linestyle='-')
    ax[1].axvline(x=0, color='black', linestyle='-')
    ax[1].set_xlim([0, 100])
    ax[1].set_ylim([0, 360])
    print(deg)
    ax[1].plot(np.arange(100), deg,
        linestyle='-', linewidth=1.5, color='gray')

    # Apparent diameter
    ax[2].cla()
    ax[2].set_xlabel('Time')
    ax[2].set_ylabel('Angular Diameter')
    ax[2].axhline(y=0, color='black', linestyle='-')
    ax[2].axvline(x=0, color='black', linestyle='-')
    ax[2].set_xlim([0, 100])
    ax[2].set_ylim([0, 45])
    print(theta)
    ax[2].plot(np.arange(100), theta,
        linestyle='-', linewidth=1.5, color='gray')

    fig3.canvas.draw_idle()


def update(val):
    MAG1 = sMAG1.val
    DEG1 = sDEG1.val
    MAG2 = sMAG2.val
    DELTADEG = sDELTADEG.val

    # Compute complex vectors
    RAD1 = DEG1 / 360 * 2 * np.pi
    VEC1 = MAG1 * np.cos(RAD1) + 1j * (MAG1 * np.sin(RAD1))

    DEG2 = DEG1 - DELTADEG
    RAD2 = DEG2 / 360 * 2 * np.pi
    VEC2 = MAG2 * np.cos(RAD2) + 1j * (MAG2 * np.sin(RAD2))

    VEC3 = VEC1 + VEC2

    plot_complex_data(ax1, VEC1, VEC2, VEC3)

    global TS_MAG, TS_DEG, TS_THETA

    TS_MAG = np.roll(TS_MAG, -1)
    TS_MAG[-1] = np.abs(VEC3)

    TS_DEG = np.roll(TS_DEG, -1)
    TS_DEG[-1] = np.angle(VEC3) % (2*np.pi) * (180/np.pi)

    TS_THETA = np.roll(TS_THETA, -1)
    THETA = np.arctan(20 / np.abs(VEC3))
    THETA = THETA / (2*np.pi) * 360
    TS_THETA[-1] = THETA

    plot_timeseries(fig3ax, TS_MAG, TS_DEG, TS_THETA)


def close_all(event):
    plt.close('all')


# =============================================================================
# Plot
# =============================================================================
matplotlib.use('TkAgg')  # Needed for window positioning to work
plt.rcParams['font.family'] = 'monospace'  # Set typeface

fig1, (ax1) = plt.subplots(1, 1)
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("600x600+0+0")

# Plot
plot_complex_data(ax1, VEC1, VEC2, VEC3)

# =============================================================================
# Plot Controls
# =============================================================================
fig2 = plt.figure()
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("600x600+625+0")
axcolor = 'lightgoldenrodyellow'

# -----------------------------------------------------------------------------
# Sliders
# -----------------------------------------------------------------------------
# Position parameters [left, bottom, width, height]
pos_slider1 = [0.15, 0.90, 0.70, 0.05]
pos_slider2 = [0.15, 0.85, 0.70, 0.05]
pos_slider3 = [0.15, 0.80, 0.70, 0.05]
pos_slider4 = [0.15, 0.75, 0.70, 0.05]

axMAG1 = plt.axes(pos_slider1, facecolor=axcolor)
axDEG1 = plt.axes(pos_slider2, facecolor=axcolor)
axMAG2 = plt.axes(pos_slider3, facecolor=axcolor)
axDELTADEG = plt.axes(pos_slider4, facecolor=axcolor)

sMAG1 = Slider(axMAG1, "Mag 1", 0, 200, valinit=MAG1, valstep=1)
sDEG1 = Slider(axDEG1, "Deg 1", 0, 360, valinit=DEG1, valstep=1)
sMAG2 = Slider(axMAG2, "Mag 2", 0, 200, valinit=MAG2, valstep=1)
sDELTADEG = Slider(axDELTADEG, "Delta", 0, 360, valinit=DELTADEG, valstep=1)

sMAG1.on_changed(update)
sDEG1.on_changed(update)
sMAG2.on_changed(update)
sDELTADEG.on_changed(update)

# -----------------------------------------------------------------------------
# Buttons
# -----------------------------------------------------------------------------
# Position parameters [left, bottom, width, height]
pos_button1 = [0.05, 0.05, 0.2, 0.05]
axCLOSEALL = plt.axes(pos_button1, facecolor=axcolor)
bCLOSEALL = Button(axCLOSEALL, 'Close All')
bCLOSEALL.on_clicked(close_all)

# =============================================================================
# Plot line plots
# =============================================================================
fig3, fig3ax = plt.subplots(1, 3)
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("1225x250+0+670")

# -----------------------------------------------------------------------------
# Show plot
plt.show()
