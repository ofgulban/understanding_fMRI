"""Simulate T2* with interactive slider plot."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# =============================================================================
def relaxation_T2star(time, S0=100, T2star=28):
    return S0 * np.exp(-time/T2star)


def update(val):
    S0 = sS0.val
    T2star = sT2star.val
    l.set_ydata(relaxation_T2star(time, S0=S0, T2star=T2star))
    fig.canvas.draw_idle()


# =============================================================================
# Prepare signal
T2star = 28
S0 = 100
time = np.linspace(0, 100, 101)
signal = relaxation_T2star(time, S0, T2star)

# Prepare figure
fig, ax = plt.subplots()
ax.set_title(r"$S_0 * \exp(-t / T_{2}^*)$")
ax.set_xlabel("Time [ms]")
ax.set_ylabel("MRI signal")

plt.subplots_adjust(left=0.25, bottom=0.35)
plt.plot(time, signal, lw=3, color="red")  # initial curve
l, = plt.plot(time, signal, lw=3)
ax.margins(x=0)


# Sliders
axcolor = 'lightgoldenrodyellow'
axS0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axT2star = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)

sS0 = Slider(axS0, "$S_0$", 0, 200, valinit=100, valstep=10)
sT2star = Slider(axT2star, r"$T_{2}^*$", 1, 100, valinit=28, valstep=1)

sS0.on_changed(update)
sT2star.on_changed(update)

plt.show()
