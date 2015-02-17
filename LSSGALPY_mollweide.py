# -*- coding: utf-8 -*-
'''
This code contains the visualisation tools developed for the A&A Article Catalogues of isolated galaxies, isolated pairs, and isolated triplets in the local Universe by M. Argudo-Fernández, S. Verley, G. Bergond, S. Duarte Puertas, E. Ramos Carmona, J. Sabater, M, Fernández-Lorenzo, D. Espada, J. Sulentic, J. E. Ruiz., and S. Leon.

The basic functionality of this interactive tool is the use of a Mollweide projection in the 3D space (right ascension, declination, and redshift) in combination with a wedge diagram to study the relation of the galaxies with the LSS.

For more information, see https://github.com/margudo/LSSGALPY 
'''
import numpy as np, matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.widgets import Slider, Button, CheckButtons

# Input catalogues
[ra, dec, z], [ra_isol, dec_isol, z_isol], [ra_pair, dec_pair, z_pair], [ra_trip, dec_trip, z_trip] = [np.loadtxt(filename+'.txt', usecols = (0, 1, 2), unpack=True) for filename in ['SDSS_DR10_galaxy_local', 'table1', 'table2', 'table3']]

ra_tot, dec_tot, z_tot = [ra, ra_isol, ra_pair, ra_trip], [dec, dec_isol, dec_pair, dec_trip], [z, z_isol, z_pair, z_trip]
cond_z_tot = lambda zi, rangi: [((zval > zi) & (zval < zi + rangi)) for zval in z_tot] # Condition for the redshift range in the plots

# Default values for reset button
z0, rang0, dec0, alpha0 = .030, .005, 30., .2

# Main plot: Mollweide projection
fig = plt.figure("Mollweide projection", figsize=(16.3, 8.4))
plt.subplot(111, xticks=[], yticks=[], frameon=False)
ax2, ax1 = plt.axes([0.79, 0.05, 0.25, 0.25], polar=True), fig.add_axes([0.05, 0.14, 0.9, 0.8])

m = Basemap(projection='moll', lon_0=180, resolution='c', celestial=True, ax=ax1)
m.drawmeridians(np.arange(0., 420., 60.)) ; m.drawparallels(np.arange(-90., 120., 30.), labels=[1, 0, 0, 1]) ; m.drawmapboundary(fill_color='w')
x, y = [[m(raval, decval)[i] for raval, decval in zip(ra_tot, dec_tot)] for i in range(0, 2)] # Translation of R.A. and Dec. positions to Mollweide projection

# Plotting galaxy positions in the selected redshift range
xyplt = [plt.plot(x[i][cond_z_tot(z0, rang0)[i]], y[i][cond_z_tot(z0, rang0)[i]], krgb, ms=mval, alpha=alpval, visible=visi)[0] for i, krgb, mval, alpval, visi in zip(range(0, 4), ['ko', 'ro', 'go', 'bo'], [1, 4, 4, 4], [alpha0, .7, .7, .7], [True, True, False, False])]

# Additional plot: Wedge diagram
def wedgefig(zini, rangi):
    cond_dec = (dec > -1.) & (dec <= 1.)
    cond_z = (z[cond_dec] >= zini) & (z[cond_dec] < zini + rangi)
    [ax2.scatter(np.radians(raval - 95), zval, c=colors, s=1, marker=',', lw=0, alpha=alpval) for raval, zval, colors, alpval in zip([ra[cond_dec], ra[cond_dec][cond_z]], [z[cond_dec], z[cond_dec][cond_z]], [z[cond_dec], 'r'], [.1, 1])]
    ax2.bar(0., rangi, width=2*np.pi, bottom=zini, color='r', edgecolor='r', lw=0, alpha=.4)
    ax2.set_rmax(.1)
    [plt.setp(getval, fontsize=fontval) for getval, fontval in zip([ax2.get_xticklabels(), ax2.get_yticklabels()], [10, 8])]
wedgefig(z0, rang0)

# Location of sliders in the figure
axz, axrang, axalpha = [plt.axes(val, axisbg='lightgoldenrodyellow') for val in [[0.25, 0.06, 0.5, 0.03], [0.25, 0.02, 0.5, 0.03], [0.05, 0.1, 0.07, 0.03]]]

# Definition of the sliders
sz, srang, salpha = [Slider(axval, names, 0.0, valmax, valinit=val0, valfmt=vfmt) for axval, names, valmax, val0, vfmt in zip([axz, axrang, axalpha], ['z', 'Range', 'Transp.'], [.1, .1, 1.], [z0, rang0, alpha0], ['%1.3f', '%1.3f', '%1.2f'])]

# Text in the figure
fig_text = plt.figtext(0.5, 0.11, 'Mollweide projection within %1.3f < z < %1.3f' % (sz.val, sz.val+srang.val), ha='center', color='black', size='large')

# Update of the plot with values in the sliders
def update(val):
    '''This function updates the main and additional plots for new values of redshift, redshift range, and points transparency'''
    rang, zCen, newAlpha = [sval.val for sval in [srang, sz, salpha]]
    # Update the value of the Text object
    fig_text.set_text('Mollweide projection within %1.3f < z < %1.3f' % (round(zCen,3), round(zCen,3)+round(rang,3)))
    ax2.cla()
    [xyp.set_data(x[i][cond_z_tot(zCen, rang)[i]], y[i][cond_z_tot(zCen, rang)[i]]) for xyp, i in zip(xyplt, range(0, 4))]
    xyplt[0].set_alpha(alpha=newAlpha)
    wedgefig(zCen, rang)
    plt.draw()
[sval.on_changed(update) for sval in [sz, srang, salpha]]

# Samples selection box
rax, labels = plt.axes([0.05, 0.15, 0.07, 0.15]), ('LSS','Isolated', 'Pairs', 'Triplets')
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
    [sval.reset() for sval in [sz, srang, salpha]]
button.on_clicked(reset)

plt.show()
