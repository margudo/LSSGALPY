# -*- coding: utf-8 -*-
'''
This code contains the visualisation tools developed for the A&A Article Catalogues of isolated galaxies, isolated pairs, and isolated triplets in the local Universe by M. Argudo-Fernández, S. Verley, G. Bergond, S. Duarte Puertas, E. Ramos Carmona, J. Sabater, M, Fernández-Lorenzo, D. Espada, J. Sulentic, J. E. Ruiz, and S. Leon.

The basic functionality of this interactive tool is the use of a wedge diagram in the 3D space (right ascension, declination, and redshift) in combination with a mollweide projection to study the relation of the galaxies with the LSS.

For more information, see https://github.com/margudo/LSSGALPY
'''
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.widgets import Slider, Button, CheckButtons

# Input catalogues
[ra, dec, z], [ra_isol, dec_isol, z_isol], [ra_pair, dec_pair, z_pair], [ra_trip, dec_trip, z_trip] = [np.loadtxt(filename+'.txt', usecols = (0, 1, 2), unpack=True) for filename in ['SDSS_DR10_galaxy_local', 'table1', 'table2', 'table3']]

ra_tot, dec_tot, z_tot = [ra, ra_isol, ra_pair, ra_trip], [dec, dec_isol, dec_pair, dec_trip], [z, z_isol, z_pair, z_trip]

# Default values for reset button
decCen0, decDelta0, alpha0 = 0., 5., .2

# R.A. from degrees to radian for the polar representation
rad_tot = [np.radians(raval) for raval in ra_tot]

# Plot
fig = plt.figure("Wedge diagram", figsize=(16.3, 8.4))

# Condition for the declination range in the plots
cond_dec = [((decval > decCen0) & (decval < decCen0 + decDelta0)) for decval in dec_tot]

# Main plot: Wedge diagram
ax1, ax2 = [plt.axes(posval, polar=val, projection=pj) for posval, val, pj in zip([[0.05, 0.2, 0.9, 0.7], [0.74, 0.1, 0.25, 0.25]], [True, False], [None, 'mollweide'])]
[ax.grid(True) for ax in [ax1, ax2]]

# Plotting galaxy positions in the selected declination range
xyplt = [ax1.plot(rad_tot[i][cond_dec[i]], z_tot[i][cond_dec[i]], krgb, ms=mval, alpha=alpval, visible=visi)[0] for i, krgb, mval, alpval, visi in zip(range(0, 4), ['k.', 'ro', 'go', 'bo'], [1, 4, 4, 4], [alpha0, .7, .7, .7], [True, True, False, False])]

# Additional plot: Mollweide projection
x, y = [np.radians(val) for val in [-1*(ra - 180), dec]]

H, xedges, yedges = np.histogram2d(x.T, y.T, bins=50)
extent, levels = [xedges[0], xedges[-1], yedges[0], yedges[-1]], [1.0e2]*2

ax2.contourf(H.T, levels, origin='lower', colors='b', lw=1, extent=extent, alpha=.3)
[plt.setp(getval, fontsize=fontval, alpha=.6) for getval, fontval in zip([ax2.get_xticklabels(), ax2.get_yticklabels()], [8, 12])]
raCen, raDelta = 0., 180.
x_rect, y_rect = [np.radians(val) for val in [raCen+np.array([-1, -1, 1, 1, -1])*raDelta, decCen0+np.array([0, 1, 1, 0, 0])*decDelta0]]
ax2.fill(x_rect, y_rect, 'r', lw=0, alpha=.5)

# Location of sliders in the figure
axdec, axrang, axalpha = [plt.axes(val, axisbg='lightgoldenrodyellow') for val in [[0.25, 0.06, 0.5, 0.03], [0.25, 0.02, 0.5, 0.03], [0.05, 0.1, 0.07, 0.03]]]

# Definition of the sliders
sdec, srang, salpha = [Slider(axval, name, valmin, valmax, valinit=val0, valfmt=vfmt) for axval, name, valmin, valmax, val0, vfmt in zip([axdec, axrang, axalpha], ['Dec.', 'Range', 'Transp.'], [-20.0, 0.0, 0.0], [90.0, 90.0, 1.], [decCen0, decDelta0, alpha0], ['%1.1f', '%1.1f', '%1.2f'])]

# Text in the figure
fig_text = plt.figtext(0.5, 0.11, 'Wedge diagram within %1.1f$^\circ$ < Dec. < %1.1f$^\circ$' % (sdec.val, sdec.val+srang.val), ha='center', color='black', size='large')

# Update of the plot with values in the sliders
def update(val):
    '''This function updates the main and additional plots for new values of redshift, redshift range, and points transparency'''
    decDelta, decCen, newAlpha = [sval.val for sval in [srang, sdec, salpha]]
    cond_dec0 = [((decval > decCen) & (decval < decCen + decDelta)) for decval in dec_tot]
    # Update the value of the Text object
    fig_text.set_text('Wedge diagram within %1.1f$^\circ$ < Dec. < %1.1f$^\circ$' % (round(decCen,1), round(decCen,1)+round(decDelta,1)))
    ax2.cla()
    [xyp.set_data(rad_tot[i][cond_dec0[i]], z_tot[i][cond_dec0[i]]) for i, xyp in zip(range(0, 4), xyplt)]
    ax2.contourf(H.T, levels, origin='lower', colors='b', lw=1, extent=extent, alpha=.3)
    [ax.grid(True) for ax in [ax1, ax2]]
    y_rect = np.radians(decCen + np.array([0, 1, 1, 0, 0])*decDelta)
    ax2.fill(x_rect, y_rect, 'r', lw=0, alpha=.5)
    [plt.setp(getval, fontsize=fontval, alpha=.6) for getval, fontval in zip([ax2.get_xticklabels(), ax2.get_yticklabels()], [8, 12])]
    xyplt[0].set_alpha(alpha=newAlpha)
    plt.draw()
[sval.on_changed(update) for sval in [sdec, srang, salpha]]

# Samples selection box
rax, labels = plt.axes([0.05, 0.15, 0.07, 0.15]), ('LSS', 'Isolated', 'Pairs', 'Triplets')
check = CheckButtons(rax, labels, (True, True, False, False))
def func(label):
    '''This function allows the sample selection'''
    lab = labels.index(label)
    xyplt[lab].set_visible(not xyplt[lab].get_visible())
    plt.draw()
check.on_clicked(func)

# Reset button
resetax = plt.axes([0.05, 0.035, 0.07, 0.04])
button = Button(resetax, 'Reset', color='red', hovercolor='green')
def reset(event):
    '''This function reset the default values in the plots'''
    [sval.reset() for sval in [sdec, srang, salpha]]
button.on_clicked(reset)

plt.show()
