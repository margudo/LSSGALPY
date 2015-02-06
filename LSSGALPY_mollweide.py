# -*- coding: utf-8 -*-
'''
This code contains the visualisation tools developed for the A&A Article Catalogues of isolated galaxies, isolated pairs, and isolated triplets in the local Universe by M. Argudo-Fernández, S. Verley, G. Bergond, S. Duarte Puertas, E. Ramos Carmona, J. Sabater, M, Fernández-Lorenzo, D. Espada, J. Sulentic, and J. E. Ruiz.

The basic functionality of this interactive tool is the use of a Mollweide projection in the 3D space (right ascension, declination, and redshift) in combination with a wedge diagram to study the relation of the galaxies with the LSS.

For more information, see https://github.com/margudo/LSSGALPY 
'''
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
# defining cosmology
cosmo = cosmology.FlatLambdaCDM(H0=70., Om0=0.3)
d = constants.c.to('km/s') * z / cosmo.H0

#----------------------------------------------------------------------
# Plot
plt.figure("Mollweide projection", figsize=(16.3, 8.4))
plt.subplot(111)

# default values for reset button
z0, rang0, dec0, alpha0 = .030, .005, 30., .2
zmin, zmax = z0, z0+rang0
# Condition for the redhift range in the plots
cond = (z >= z0) & (z < z0+rang0)
cond_isol = (z_isol >= z0) & (z_isol < z0+rang0)
cond_pair = (z_pair >= z0) & (z_pair < z0+rang0)
cond_trip = (z_trip >= z0) & (z_trip < z0+rang0)

# Main plot: Mollweide projection
m = Basemap(projection='moll', lon_0=180, resolution='c', celestial=True)
m.drawmeridians(np.arange(0.,420.,60.)) ; m.drawparallels(np.arange(-90.,120.,30.), labels=[1,0,0,1])
m.drawmapboundary(fill_color='w')
# Translation of RA and DEC positions to Mollweide projection
x, y = m(ra, dec)
x_isol, y_isol = m(ra_isol, dec_isol)
x_pair, y_pair = m(ra_pair, dec_pair)
x_trip, y_trip = m(ra_trip, dec_trip)
# Plotting galaxy positions in the selected redhift range
b, = plt.plot(x[cond], y[cond], 'ko', ms=1, alpha=alpha0)
c, = plt.plot(x_isol[cond_isol],y_isol[cond_isol], 'ro', ms=4, alpha=.7)
d, = plt.plot(x_pair[cond_pair],y_pair[cond_pair], 'go', ms=4, alpha=.7, visible=False)
e, = plt.plot(x_trip[cond_trip],y_trip[cond_trip], 'bo', ms=4, alpha=.7, visible=False)

# Additional plot: wedge diagram
ax2 = plt.axes([0.79, 0.05, 0.25, 0.25], polar=True)
zeta = [0, 1, 1, 0]
cond_dec = (dec > -1.) & (dec <= 1.)
cond_z = (z[cond_dec] >= z0) & (z[cond_dec] < z0 + rang0)
ax2.scatter(np.radians(ra[cond_dec]-95.), z[cond_dec], c=z[cond_dec], s=1, marker=',', lw=0, alpha=.1)
ax2.scatter(np.radians(ra[cond_dec][cond_z]-95.), z[cond_dec][cond_z], c='r', s=1, marker=',', lw=0, alpha=1)
ax2.bar(0., rang0, width=2*np.pi, bottom=z0, color='r', edgecolor='r', linewidth=0, alpha=.4)
ax2.set_rmax(.1)
plt.setp(ax2.get_xticklabels(), fontsize=10)
plt.setp(ax2.get_yticklabels(), fontsize=8)

# Location of sliders in the figure
axcolor = 'lightgoldenrodyellow'
axz = plt.axes([0.25, 0.06, 0.5, 0.03], axisbg=axcolor)
axrang  = plt.axes([0.25, 0.02, 0.5, 0.03], axisbg=axcolor)
axalpha = plt.axes([0.05, 0.1, 0.07, 0.03], axisbg=axcolor)
# Definition of the sliders
sz = Slider(axz, 'z', 0.0, .1, valinit=z0, valfmt='%1.3f')
srang = Slider(axrang, 'Range', 0.0, .1, valinit=rang0, valfmt='%1.3f')
salpha = Slider(axalpha, 'Transp.', 0.00, 1., valinit=alpha0)

# the text on the figure
fig_text = plt.figtext(0.5, 0.965, 'Mollweide projection within '+str(sz.val)+' < z < '+str(sz.val+srang.val), ha='center', color='black', weight='bold', size='large')

# Update of the plot with values in the sliders
def update(val):
    '''This function updates the main and additional plots for new values of redshift, redshift range, and points transparency'''
    rang = srang.val
    zCen = sz.val
    newAlpha = salpha.val
    cond = (z >= zCen) & (z < zCen+rang)
    cond_isol = (z_isol >= zCen) & (z_isol < zCen+rang)
    cond_z = (z[cond_dec] >= zCen) & (z[cond_dec] < zCen+rang)
    cond_pair = (z_pair >= zCen) & (z_pair < zCen+rang)
    cond_trip = (z_trip >= zCen) & (z_trip < zCen+rang)
    # update the value of the Text object
    fig_text.set_text('Mollweide projection within '+str(round(zCen,3))+' < z < '+str(round(zCen,3)+round(rang,3)))
    ax2.cla()
    ax2.scatter(np.radians(ra[cond_dec]-95.), z[cond_dec], c=z[cond_dec],  s=1, marker=',', lw=0, alpha=.05)
    b.set_data(x[cond], y[cond])
    c.set_data(x_isol[cond_isol], y_isol[cond_isol])
    d.set_data(x_pair[cond_pair], y_pair[cond_pair])
    e.set_data(x_trip[cond_trip], y_trip[cond_trip])
    b.set_alpha(alpha=newAlpha)
    ax2.scatter(np.radians(ra[cond_dec][cond_z]-95.), z[cond_dec][cond_z], c='r', s=1, marker=',', lw=0, alpha=1)
    plt.setp(ax2.get_xticklabels(), fontsize=10)
    plt.setp(ax2.get_yticklabels(), fontsize=8)
    ax2.bar(0., rang, width=2*np.pi, bottom=zCen, color='r', edgecolor='r', linewidth=0, alpha=.4)
    ax2.set_rmax(.1)   
    plt.draw()
sz.on_changed(update)
srang.on_changed(update)
salpha.on_changed(update)

# Sample selection box
rax = plt.axes([0.05, 0.15, 0.07, 0.15])
check = CheckButtons(rax, ('LSS','Isolated', 'Pairs', 'Triplets'), (True, True, False, False))
def func(label):
    '''This function allows the sample selection'''
    if   label == 'LSS':      b.set_visible(not b.get_visible())
    elif label == 'Isolated': c.set_visible(not c.get_visible())
    elif label == 'Pairs':    d.set_visible(not d.get_visible())
    elif label == 'Triplets': e.set_visible(not e.get_visible())
    plt.draw()
check.on_clicked(func)

# Reset button
resetax = plt.axes([0.05, 0.035, 0.07, 0.04])
button = Button(resetax, 'Reset', color='red', hovercolor='green')
def reset(event):
    '''This function reset the default values in the plots'''
    sz.reset()
    srang.reset()
    salpha.reset()
button.on_clicked(reset)

plt.show()
