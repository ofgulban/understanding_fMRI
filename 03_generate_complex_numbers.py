"""Create a bunch of complex numbers."""

import random
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import tkinter as tk

global COMP

NR_SAMPLES = 1000
SEED = 0

MEAN_X = 100.
MEAN_Y = 100.
STD = 20.

COMP = MEAN_X + 1j * MEAN_Y
MAG = np.abs(COMP)
PHA = np.angle(COMP) % (2*np.pi) * (180/np.pi)

# =============================================================================
def generate_complex_data(nr_samples=9, mean_x=0, mean_y=0, std=1, seed=0):
    np.random.seed(seed)
    data_real = np.random.normal(loc=mean_x, scale=std, size=nr_samples)
    data_imag = np.random.normal(loc=mean_y, scale=std, size=nr_samples)
    return data_real + 1j * data_imag


def plot_complex_data(ax, data):
    ax.cla()
    ax.scatter(data.real, data.imag, s=3, alpha=1, color='black', marker='o', 
        linewidth=0)
    ax.set_aspect('equal')
    ax.set_xlabel('Re')
    ax.set_ylabel('Im')
    ax.set_title('Complex Signal')
    ax.axhline(y=0, color='black', linestyle='-')
    ax.axvline(x=0, color='black', linestyle='-')
    ax.set_xlim([-150, 150])
    ax.set_ylim([-150, 150])


def plot_lines(ax, mean_x, mean_y, std):
    # Maginute line
    ax.plot([0, mean_x], [0, mean_y], color='black', linestyle='-', 
        linewidth=0.5)

    # Spread circle
    circle = plt.Circle((mean_x, mean_y), radius=std, color='black', 
        fill=False, linestyle='-', linewidth=0.5, label='Circle')
    ax.add_patch(circle)


def update(val):
    MAG = sMAG.val
    PHA = sPHA.val / 360 * 2 * np.pi
    COMP = MAG* np.cos(PHA) + 1j * (MAG* np.sin(PHA))

    sMEAN_X.set_val(COMP.real)
    sMEAN_Y.set_val(COMP.imag)

    data = generate_complex_data(NR_SAMPLES, sMEAN_X.val, sMEAN_Y.val, sSTD.val, sSEED.val)
    plot_complex_data(fig1ax1, data)
    plot_lines(fig1ax1, sMEAN_X.val, sMEAN_Y.val, sSTD.val)
    fig1.canvas.draw_idle()
    update_histograms(fig3ax, data)
    fig3.canvas.draw_idle()


def close_all(event):
    plt.close('all')


# =============================================================================
# Plot Data
# =============================================================================
# Set the backend to TkAgg
matplotlib.use('TkAgg')  # Needed for window positioning to work

# Set global typeface
plt.rcParams['font.family'] = 'monospace'  

# Prepare figure
fig1, (fig1ax1) = plt.subplots(1, 1)

manager = plt.get_current_fig_manager()
manager.window.wm_geometry("500x500+0+0")

# Plot
data = generate_complex_data(NR_SAMPLES, MEAN_X, MEAN_Y, STD, SEED)
plot_complex_data(fig1ax1, data)
plot_lines(fig1ax1, MEAN_X, MEAN_Y, STD)

# =============================================================================
# Plot Controls
# =============================================================================
fig2 = plt.figure()
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("500x500+550+0")
axcolor = 'lightgoldenrodyellow'

# -----------------------------------------------------------------------------
# Sliders
# -----------------------------------------------------------------------------
# [left, bottom, width, height]
axSEED = plt.axes([0.15, 0.90, 0.70, 0.05], facecolor=axcolor)
axMEAN_X = plt.axes([0.15, 0.85, 0.70, 0.05], facecolor=axcolor)
axMEAN_Y = plt.axes([0.15, 0.80, 0.70, 0.05], facecolor=axcolor)
axSTD = plt.axes([0.15, 0.75, 0.70, 0.05], facecolor=axcolor)
axMAG = plt.axes([0.15, 0.70, 0.70, 0.05], facecolor=axcolor)
axPHA = plt.axes([0.15, 0.65, 0.70, 0.05], facecolor=axcolor)

sSEED = Slider(axSEED, "Seed", 0, 100, valinit=SEED, valstep=1)
sMEAN_X = Slider(axMEAN_X, "Mean X", -150, 150, valinit=MEAN_X, valstep=1)
sMEAN_Y = Slider(axMEAN_Y, "Mean Y", -150, 150, valinit=MEAN_Y, valstep=1)
sSTD = Slider(axSTD, "Std. X", 0, 50, valinit=STD, valstep=1)
sMAG = Slider(axMAG, "Mag.", 0, 200, valinit=MAG, valstep=1)
sPHA = Slider(axPHA, "Pha.", 0, 360, valinit=PHA, valstep=1)

sSEED.on_changed(update)
sSTD.on_changed(update)
sMAG.on_changed(update)
sPHA.on_changed(update)

# -----------------------------------------------------------------------------
# Buttons
# -----------------------------------------------------------------------------
# [left, bottom, width, height]
axCLOSEALL = plt.axes([0.05, 0.05, 0.2, 0.05], facecolor=axcolor)
bCLOSEALL = Button(axCLOSEALL, 'Close All')
bCLOSEALL.on_clicked(close_all)


# =============================================================================
# Plot Histograms
# =============================================================================
fig3, fig3ax = plt.subplots(2, 2)
manager = plt.get_current_fig_manager()
manager.window.wm_geometry("1050x400+0+575")

def update_histograms(ax, data):
    ax[0, 0].clear()
    ax[0, 0].hist(data.real, range=(-200, 200), bins=200, edgecolor=None)
    ax[0, 0].set_title('Real')

    ax[0, 1].clear()
    ax[0, 1].hist(data.imag, range=(-200, 200), bins=200, edgecolor=None)
    ax[0, 1].set_title('Imag')

    MAG = np.abs(data)
    PHA = np.angle(data) % (2*np.pi) * (180/np.pi)

    ax[1, 0].clear()
    ax[1, 0].hist(MAG, range=(0, 400), bins=200, edgecolor=None)
    ax[1, 0].set_title('Magnitude')

    ax[1, 1].clear()
    ax[1, 1].hist(PHA, range=(0, 360), bins=180, edgecolor=None)
    ax[1, 1].set_title('Phase [deg]')

update_histograms(fig3ax, data)
fig3.tight_layout()

# -----------------------------------------------------------------------------
# Show plot
plt.show()
