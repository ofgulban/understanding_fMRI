"""Interactive SS-SI-VASO (Slice Selective Slab Inversion Vascular Space 
Occupancy) longitudinal magnetization (M_z) simulation.

References
---------
- [Renzo Huber's PhD Thesis Fig. 3.2 Panel C Page 47.] Mapping Human Brain 
Activity by Functional Magnetic Resonance Imaging of Blood Volume. 2014. Der 
Fakultät für Physik und Geowissenschaften der Universität Leipzig eingereichte

- [Also see] Akbari, A., Bollmann, S., Ali, T.S., Barth, M., 2022. Modelling the 
depth-dependent VASO and BOLD responses in human primary visual cortex. 
Human Brain Mapping hbm.26094. https://doi.org/10.1002/hbm.26094

"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


# =============================================================================
# Functions that will be put into the library
# =============================================================================
def Mz(time, M0_equi, M0_init, FA_rad, T1):
    """Longitudinal magnetization."""
    return M0_equi - (M0_equi - M0_init * np.cos(FA_rad)) * np.exp(-time/T1)


def compute_SS_SI_VASO_Mz_signal(time, T1, Tr, Ti1, Ti2, mode_nonblood=False):
    """Compute VASO Mz signal."""
    signal = np.zeros(time.shape)
    M0_equi = 1.  # This never changes
    M0_init = 1.

    # Prepare condition array
    cond = np.full(time.shape, 3)
    idx2 = time % (Tr*2) < (Ti2+Tr)  # Stages after 180 deg pulse
    idx1 = time % (Tr*2) < Ti1  # Stages after the first 90 deg pulse
    cond[idx2] = 2
    cond[idx1] = 1
    for i, t in enumerate(time):
        t %= 2*Tr
        # ---------------------------------------------------------------------
        # Handle first signal separately
        # ---------------------------------------------------------------------
        if i == 0:
            signal[i] = Mz(time=t, M0_equi=M0_equi, M0_init=M0_init,
                           FA_rad=np.deg2rad(180), T1=T1)
        # ---------------------------------------------------------------------
        # After 180 degree pulse
        # ---------------------------------------------------------------------
        elif cond[i] == 1:
            if mode_nonblood:
                if cond[i] != cond[i-1]:  # Update M0 upon condition switch
                    M0_init = Mz(time=Tr-Ti2, M0_equi=M0_equi, M0_init=M0_init,
                                 FA_rad=np.deg2rad(90), T1=T1)
            signal[i] = Mz(time=t, M0_equi=M0_equi, M0_init=M0_init,
                           FA_rad=np.deg2rad(180), T1=T1)
        # ---------------------------------------------------------------------
        # After the first 90 degree pulse
        # ---------------------------------------------------------------------
        elif cond[i] == 2:
            signal[i] = Mz(time=t-Ti1, M0_equi=M0_equi, M0_init=M0_init,
                           FA_rad=np.deg2rad(90), T1=T1)
        # ---------------------------------------------------------------------
        # After the second 90 degree pulse
        # ---------------------------------------------------------------------
        else:
            signal[i] = Mz(time=t-Tr-Ti2, M0_equi=M0_equi, M0_init=M0_init,
                           FA_rad=np.deg2rad(90), T1=T1)
    return signal


def plot_SS_SI_VASO_Mz_signal(ax, max_time, T1_ref, T1, Tr, Ti1, Ti2):
    """Protocol to plot VASO longitudinal magnetization."""
    time = np.linspace(0, max_time, 1001)
    signal1 = compute_SS_SI_VASO_Mz_signal(time, T1, Tr, Ti1, Ti2,
                                           mode_nonblood=True)
    signal2 = compute_SS_SI_VASO_Mz_signal(time, T1_ref, Tr, Ti1, Ti2,
                                           mode_nonblood=False)

    ax.cla()
    ax.plot(time, signal1, lw=2, color="blue")
    ax.plot(time, signal2, lw=2, color="red")

    ax.set_title("SI-SS-VASO")
    ax.set_xlabel("Time [s]")
    ax.set_ylabel(r"$M_z$")
    ax.set_xlim([0, max_time])
    ax.set_ylim([-1, 1])
    ax.legend(['Tissue X', 'Blood'], loc="upper left")

    # -------------------------------------------------------------------------
    # Horizontal lines
    ax.hlines([0], 0, max_time, linestyle='solid', color='lightgray', zorder=0)

    # Vertical lines
    trans = ax.get_xaxis_transform()

    event_180deg = np.arange(0, max_time, 2*Tr)
    ax.vlines(event_180deg, -1, 1, linestyle=':', color='gray', zorder=0)
    for x in event_180deg:
        ax.text(x, 0.02, r"$180\degree$ pulse", rotation=90, transform=trans)

    event_90deg_1 = np.arange(Ti1, max_time, 2*Tr)
    for x in event_90deg_1:
        ax.text(x, 0.02, r"$90\degree$ pulse", rotation=90, transform=trans)
    ax.vlines(event_90deg_1, -1, 1, linestyle=':', color='gray', zorder=0)

    event_90deg_2 = np.arange(Tr+Ti2, max_time, 2*Tr)
    for x in event_90deg_2:
        ax.text(x, 0.02, r"$90\degree$ pulse", rotation=90, transform=trans)
    ax.vlines(event_90deg_2, -1, 1, linestyle=':', color='gray', zorder=0)


def update(val):
    """Update plot data after each slider interaction."""
    T1 = sT1.val
    max_time = sTime.val
    Ti1 = sTi1.val
    Ti2 = sTi2.val
    Tr = sTr.val

    plot_SS_SI_VASO_Mz_signal(ax1, max_time, T1_ref=T1b, T1=T1, Tr=Tr,
                              Ti1=Ti1, Ti2=Ti2)
    fig1.canvas.draw_idle()


# =============================================================================
# Initial parameters (direct translation of gnuplot conditions)
# =============================================================================
T1gm = 1.9
T1b = 2.1  # steady state blood

Ti1 = 1.45561
Ti2 = 1.7
Tr = 2.

max_time = 5 * Tr
time = np.linspace(0, max_time, 1001)

# =============================================================================
# Plotting
# =============================================================================
# Prepare figure
fig1, (ax1) = plt.subplots(1, 1)
plot_SS_SI_VASO_Mz_signal(ax1, max_time, T1_ref=T1b, T1=T1gm, Tr=Tr,
                          Ti1=Ti1, Ti2=Ti2)

# -----------------------------------------------------------------------------
# Sliders
# -----------------------------------------------------------------------------
fig2 = plt.figure()
axcolor = 'lightgoldenrodyellow'

# [left, bottom, width, height]
axT1 = plt.axes([0.15, 0.9, 0.70, 0.03], facecolor=axcolor)
axTime = plt.axes([0.15, 0.85, 0.70, 0.03], facecolor=axcolor)
axTi1 = plt.axes([0.15, 0.80, 0.70, 0.03], facecolor=axcolor)
axTi2 = plt.axes([0.15, 0.75, 0.70, 0.03], facecolor=axcolor)
axTr = plt.axes([0.15, 0.70, 0.70, 0.03], facecolor=axcolor)

sT1 = Slider(axT1, r"$T_1$", 0, 6.0, valinit=T1gm, valstep=0.1)
sTime = Slider(axTime, r"$Max. Time$", 1, 30, valinit=max_time, valstep=0.5)
sTi1 = Slider(axTi1, r"$Ti_1$", 0, 6.0, valinit=Ti1, valstep=0.1)
sTi2 = Slider(axTi2, r"$Ti_2$", 0, 6.0, valinit=Ti2, valstep=0.1)
sTr = Slider(axTr, r"$Tr$", 0, 6.0, valinit=Tr, valstep=0.1)

sT1.on_changed(update)
sTime.on_changed(update)
sTi1.on_changed(update)
sTi2.on_changed(update)
sTr.on_changed(update)

plt.show()
