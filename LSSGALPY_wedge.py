# -*- coding: utf-8 -*-
'''
This code contains the visualisation tools developed for the A&A Article Catalogues of isolated galaxies, isolated pairs, and isolated triplets in the local Universe by M. Argudo-Fernández, S. Verley, G. Bergond, S. Duarte Puertas, E. Ramos Carmona, J. Sabater, M, Fernández-Lorenzo, D. Espada, J. Sulentic, and J. E. Ruiz.

The basic functionality of this interactive tool is the use of a wedge diagram in the 3D space (right ascension, declination, and redshift) in combination with a mollweide projection to study the relation of the galaxies with the LSS.

For more information, see https://github.com/margudo/LSSGALPY
'''
import matplotlib
import numpy as np, matplotlib.pyplot as plt
from astropy import coordinates as coord, units as u, constants, cosmology
from mpl_toolkits.basemap import Basemap
from mpl_toolkits.mplot3d import axes3d
from matplotlib.widgets import Slider, Button, RadioButtons, CheckButtons

#----------------------------------------------------------------------
# input catalogues
ra, dec, z    = np.loadtxt('SDSS_DR10_galaxy_local.txt', usecols = (0,1,2), unpack=True)  # catalogue of ~300000 galaxies in the local Universe
ra_isol, dec_isol, z_isol = np.loadtxt('table1.txt', usecols = (0,1,2), unpack=True)      # table1: position and redshift for isolated galaxies 
ra_pair, dec_pair, z_pair = np.loadtxt('table2.txt', usecols = (0,1,2), unpack=True)      # table2: position and redshift for isolated pairs 
ra_trip, dec_trip, z_trip = np.loadtxt('table3.txt', usecols = (0,1,2), unpack=True)      # table3: position and redshift for isolated triplets

#----------------------------------------------------------------------
# traslate RA from degrees to radian for the polar representation
rad, rad_isol, rad_pair, rad_trip = np.radians(ra), np.radians(ra_isol), np.radians(ra_pair), np.radians(ra_trip) #shift to radians

#----------------------------------------------------------------------
# Plot
fig = plt.figure("Wedge diagram", figsize=(16.3, 8.4))

# default values for reset button
decCen0, decDelta0, alpha0 = 0., 2., .2
# Condition for the declination range in the plots
cond = (dec > decCen0) & (dec < decCen0+decDelta0)
cond_isol = (dec_isol > decCen0) & (dec_isol < decCen0+decDelta0)
cond_pair = (dec_pair > decCen0) & (dec_pair < decCen0+decDelta0)
cond_trip = (dec_trip > decCen0) & (dec_trip < decCen0+decDelta0)

# Main plot: Wedge diagram
ax = plt.axes([0.05, 0.2, 0.9, 0.7], polar=True)
# Plotting galaxy positions in the selected declination range
a, = plt.plot(rad[cond], z[cond], 'k.', ms=2, alpha=.2)
b, = plt.plot(rad_isol[cond_isol], z_isol[cond_isol], 'ro', ms=4, alpha=.7)
c, = plt.plot(rad_pair[cond_pair], z_pair[cond_pair], 'go', ms=4, alpha=.7, visible=False)
d, = plt.plot(rad_trip[cond_trip], z_trip[cond_trip], 'bo', ms=4, alpha=.7, visible=False)

# Additional plot: Mollweide projection
ax2 = plt.axes([0.74, 0.1, 0.25, 0.25], projection='mollweide', celestial=True)
plt.grid(True)
cond_z = (z >= .030) & (z < .031)
x, y = np.radians(ra-180), np.radians(dec)
ax2.scatter(x[cond_z], y[cond_z], c=y[cond_z], linewidths=0, s=10, alpha=.8)
plt.setp(ax2.get_xticklabels(), fontsize=8, alpha=.6)
plt.setp(ax2.get_yticklabels(), fontsize=12, alpha=.6)
raCen, raDelta, decCen, decDelta = 0., 180., 0., 2.
x_rect, y_rect = np.radians(raCen+np.array([-1, -1, 1, 1, -1])*raDelta), np.radians(decCen+np.array([0, 1, 1, 0, 0])*2*decDelta)
ax2.fill(x_rect, y_rect, 'r', lw=0, alpha=.5)

# Location of sliders in the figure
axcolor = 'lightgoldenrodyellow'
axdec = plt.axes([0.25, 0.06, 0.5, 0.03], axisbg=axcolor)
axrang  = plt.axes([0.25, 0.02, 0.5, 0.03], axisbg=axcolor)
axalpha = plt.axes([0.05, 0.1, 0.07, 0.03], axisbg=axcolor)
# Definition of the sliders
sdec = Slider(axdec, 'Dec', -20.0, 90.0, valinit=decCen0)
srang = Slider(axrang, 'Range', 0.0, 90.0, valinit=decDelta0)
salpha = Slider(axalpha, 'Transp.', 0., 1., valinit=alpha0)

# the text on the figure
fig_text = plt.figtext(0.5, 0.965, 'Wedge diagram within '+str(sdec.val)+' < DEC < '+str(sdec.val+srang.val), ha='center', color='black', weight='bold', size='large')

# Update of the plot with values in the sliders
def update(val):
    '''This function updates the main and additional plots for new values of redshift, redshift range, and points transparency'''   
    decDelta = srang.val
    decCen = sdec.val
    newAlpha = salpha.val
    cond = (dec > decCen) & (dec < decCen+decDelta)
    cond_isol = (dec_isol > decCen) & (dec_isol < decCen+decDelta)
    cond_pair = (dec_pair > decCen) & (dec_pair < decCen+decDelta)
    cond_trip = (dec_trip > decCen) & (dec_trip < decCen+decDelta)
    # update the value of the Text object
    fig_text.set_text('Wedge diagram within '+str(round(decCen,2))+' < DEC < '+str(round(decCen,2)+round(decDelta,2)))
    a.set_data(rad[cond], z[cond])
    b.set_data(rad_isol[cond_isol], z_isol[cond_isol])
    c.set_data(rad_pair[cond_pair], z_pair[cond_pair])
    d.set_data(rad_trip[cond_trip], z_trip[cond_trip])
    ax2.cla()
    ax2.scatter(x[cond_z], y[cond_z], c=y[cond_z], linewidths=0, s=10, alpha=.8)
    ax2.grid(True, alpha=.6)
    y_rect = np.radians(decCen+np.array([0, 1, 1, 0, 0])*2*decDelta)
    ax2.fill(x_rect, y_rect, 'r', lw=0, alpha=.5)
    plt.setp(ax2.get_xticklabels(), fontsize=8, alpha=.6)
    plt.setp(ax2.get_yticklabels(), fontsize=12, alpha=.6)
    a.set_alpha(alpha=newAlpha)
    plt.draw()
sdec.on_changed(update)
srang.on_changed(update)
salpha.on_changed(update)

# Sample selection box
rax = plt.axes([0.05, 0.15, 0.07, 0.15])
check = CheckButtons(rax, ('LSS','Isolated', 'Pairs', 'Triplets'), (True, True, False, False))
def func(label):
    '''This function allows the sample selection'''
    if   label == 'LSS':      a.set_visible(not a.get_visible())
    elif label == 'Isolated': b.set_visible(not b.get_visible())
    elif label == 'Pairs':    c.set_visible(not c.get_visible())
    elif label == 'Triplets': d.set_visible(not d.get_visible())
    plt.draw()
check.on_clicked(func)

# Reset button
resetax = plt.axes([0.05, 0.035, 0.07, 0.04])
button = Button(resetax, 'Reset', color='red', hovercolor='green')
def reset(event):
    '''This function reset the default values in the plots'''
    sdec.reset()
    srang.reset()
    salpha.reset()
button.on_clicked(reset)

plt.show()
