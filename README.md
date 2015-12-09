# LSSGalPy
Python tool for the interactive visualization of the large-scale environment around galaxies on the 3D space 

* Interactive visualisation tools

This code contains the visualisation tools developed for the A&A Article Catalogues of isolated galaxies, isolated pairs, and isolated triplets in the local Universe by M. Argudo-Fernández, S. Verley, G. Bergond, S. Duarte Puertas, E. Ramos Carmona, J. Sabater, M. Fernández-Lorenzo, D. Espada, J. Sulentic, J. E. Ruiz, and S. Leon.

These tools currently work as widgets in a local computer but could be also accessed remotely with a browser when they are implemented in an IPython Notebook Server (web-based interactive computational environment).
The basic functionality of these interactive tools is the use of different projections in the 3D space (right ascension, declination, and redshift) to study the relation of the galaxies with the LSS. In particular, we use a Mollweide projection (the code could also work with several tens of other types of projections) in combination with a wedge diagram, and viceversa. Therefore, we can visualise the locations of the galaxies in our study for different values of redshifts and redshift ranges. Similarly, for different values of the declinations and declination ranges, one can visualise how the isolated galaxies, isolated pairs, and isolated triplets are related to the galaxies in the LSS. Additionally, one can, very easily and quickly, add or remove samples, change the marker size, transparency, and/or symbol, etc. These tools have been tested using up to 30 million objects and still work perfectly and very smoothly on any standard laptop.

*  Demonstration:

https://vimeo.com/133013373

https://vimeo.com/133013372

*  Installation:

Only copy all files in a directory and run LSSGALPY_mollweide.py or LSSGALPY_wedge.py to visualise the LSS environment using a mollweide projection or a wedge diagram, respectively.

* Software Requirements: 

  * NumPy: array processing for numbers, strings, records, and objects;
  * matplotlib: Python 2D plotting library;
  * basemap: add-on toolkit for matplotlib.

* License:

What you're allowed to do with LSSGALPY is listed in the LICENSE file.

