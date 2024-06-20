"""Simulate T2* with interactive slider plot."""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# =============================================================================
def relaxation_T2star(time, S0=100, T2star=28):
    return S0 * np.exp(-time/T2star)


def relaxation_T2star_Uludag2009(time, S0=100, T2star_in=22.3, T2star_ex=25.1,
                                 CBV=0.01):
    Sex = relaxation_T2star(time, S0, T2star_ex)
    Sin = relaxation_T2star(time, S0, T2star_in)
    return (1 - CBV) * Sex + CBV * Sin


def update(val):
    S0 = sS0.val
    T2star_ex = sT2star_ex.val
    T2star_in = sT2star_in.val
    CBV = sCBV.val
    l.set_ydata(relaxation_T2star_Uludag2009(
        time, S0=S0, CBV=CBV, T2star_in=T2star_in, T2star_ex=T2star_ex))
    fig.canvas.draw_idle()


# =============================================================================
# Prepare signal
T2star_a = 37.5
T2star_v = 12.2
T2star_c = (T2star_a + T2star_v) / 2
T2star_in = 0.2 * T2star_a + 0.4 * T2star_v + 0.4 * T2star_c
T2star_ex = 25.1
S0 = 100
CBV = 0.05
time = np.linspace(0, 100, 101)
signal = relaxation_T2star_Uludag2009(time, S0, T2star_in, T2star_ex, CBV)

# Prepare figure
fig, ax = plt.subplots()
ax.set_title(r"$S_0 * \left((1 - CBV) * \exp(-t / T_{2,ex}^*) + CBV * \exp(-t / T_{2,in}^*) \right)$")
ax.set_xlabel("Time [ms]")
ax.set_ylabel("MRI signal")

plt.subplots_adjust(left=0.25, bottom=0.35)
plt.plot(time, signal, lw=3, color="red")  # initial curve
l, = plt.plot(time, signal, lw=3)
ax.margins(x=0)


# Sliders
axcolor = 'lightgoldenrodyellow'
axS0 = plt.axes([0.25, 0.2, 0.65, 0.03], facecolor=axcolor)
axT2star_ex = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
axT2star_in = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
axCBV = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

sS0 = Slider(axS0, "$S_0$", 0, 200, valinit=100, valstep=10)
sT2star_ex = Slider(axT2star_ex, r"$T_{2,ex}^*$", 1, 100, valinit=T2star_ex, valstep=1)
sT2star_in = Slider(axT2star_in, r"$T_{2,in}^*$", 1, 100, valinit=T2star_in, valstep=1)
sCBV = Slider(axCBV, "$CBV$", 0, 1, valinit=0.1, valstep=0.01)

sS0.on_changed(update)
sT2star_ex.on_changed(update)
sT2star_in.on_changed(update)
sCBV.on_changed(update)


plt.show()
