"""Implement simplified Boxerman95 equations."""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk

# =============================================================================
# Initial parameters
# =============================================================================
S = 100  # Scaling term
THETA = 90.  # Degrees
R = 5.  # Vessel radius


# =============================================================================
# Functions
# =============================================================================
def intravascular(S, theta_rad):
    return S * (np.cos(theta_rad)**2 - 1/3)


def extravascular(S, theta_rad, psi_rad, R, r):
    return S * (R / r)**2 * np.sin(theta_rad)**2 * np.cos(2*psi_rad)


def compute_DeltaBvessel(S, theta_deg, R):
    # Create coordinates
    x = np.linspace(-10, 10, 101)
    xx, yy = np.meshgrid(x, x)
    coords = np.stack((xx, yy), axis=-1)
    coords = coords[:, :, 0] + 1j * coords[:, :, 1]
    norms = np.abs(coords)
    angles = np.angle(coords)
    dims = norms.shape

    # Compute intra and extreavascular signal
    idx = norms > R
    r = norms[idx]
    psi = angles[idx]
    theta_rad = theta_deg / 360 * (2*np.pi)
    ev = extravascular(S, theta_rad, psi, R, r)
    results = np.zeros(dims)
    results[idx] = ev
    results[~idx] = intravascular(S, theta_rad)
    return results


def plot_DeltaBVessel(ax, S, theta_deg, R):
    results = compute_DeltaBvessel(S, theta_deg, R)

    ax.cla()
    ax.imshow(results, cmap='twilight', origin='lower', vmin=-100, vmax=100)
    ax.set_xlabel('X coordinate')
    ax.set_ylabel('Y coordinate')
    ax.set_title('Heatmap of Norms of 2D Coordinates')
    ax.tick_params(bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)
    ax.grid(False)

    fig1.canvas.draw_idle()


def update(val):
    S = sS.val
    THETA = sTHETA.val
    R = sR.val
    plot_DeltaBVessel(ax1, S, THETA, R)


def close_all(event):
    plt.close('all')


# =============================================================================
# Plot
# =============================================================================
matplotlib.use('TkAgg')  # Needed for window positioning to work
plt.rcParams['font.family'] = 'monospace'  # Set typeface

# Image
fig1, (ax1) = plt.subplots(1, 1)
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("600x600+0+0")

# This part is needed to get the right colorbar
results = compute_DeltaBvessel(S, THETA, R)
im = ax1.imshow(results, cmap='twilight', origin='lower', vmin=-100, vmax=100)
cbar = plt.colorbar(im, ax=ax1, orientation='vertical',
    fraction=0.046, pad=0.06)
cbar.ax.yaxis.set_label_position('left')  # Set label position to left
cbar.set_label('$\Delta B_{vessel}$', loc="bottom", rotation=0)
cbar.ax.yaxis.label.set_y(-0.075)

# Actual plot with right customization
plot_DeltaBVessel(ax1, S, THETA, R)

# Controls
fig2 = plt.figure()
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("600x600+625+0")
axcolor = 'lightgoldenrodyellow'

# =============================================================================
# Plot Controls
# =============================================================================
# -----------------------------------------------------------------------------
# Sliders
# -----------------------------------------------------------------------------
# Position parameters [left, bottom, width, height]
pos_slider1 = [0.27, 0.90, 0.70, 0.05]
pos_slider2 = [0.27, 0.85, 0.70, 0.05]
pos_slider3 = [0.27, 0.80, 0.70, 0.05]

axS = plt.axes(pos_slider1, facecolor=axcolor)
axTHETA = plt.axes(pos_slider2, facecolor=axcolor)
axR = plt.axes(pos_slider3, facecolor=axcolor)

sS = Slider(axS, "Signal Multiplier", 0, 200, valinit=S, valstep=1)
sTHETA = Slider(axTHETA, "B0 angle", 0, 360, valinit=THETA, valstep=1)
sR = Slider(axR, "Radius", 0, 10, valinit=R, valstep=0.1)

sS.on_changed(update)
sTHETA.on_changed(update)
sR.on_changed(update)

# -----------------------------------------------------------------------------
# Buttons
# -----------------------------------------------------------------------------
# Position parameters [left, bottom, width, height]
pos_button1 = [0.05, 0.05, 0.2, 0.05]
axCLOSEALL = plt.axes(pos_button1, facecolor=axcolor)
bCLOSEALL = Button(axCLOSEALL, 'Close All')
bCLOSEALL.on_clicked(close_all)

# -----------------------------------------------------------------------------
# Show plot
plt.show()
