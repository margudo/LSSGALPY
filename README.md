# LSSGalPy
Python tool for the interactive visualization of the large-scale environment around galaxies on the 3D space 

* Interactive visualisation tools

This code contains the visualisation tools developed for the A&A Article Catalogues of isolated galaxies, isolated pairs, and isolated triplets in the local Universe by M. Argudo-Fernández, S. Verley, G. Bergond, S. Duarte Puertas, E. Ramos Carmona, J. Sabater, M. Fernández-Lorenzo, D. Espada, J. Sulentic, J. E. Ruiz, and S. Leon.

These tools currently work as widgets in a local computer but could be also accessed remotely with a browser when they are implemented in an IPython Notebook Server (web-based interactive computational environment). You may also execute the Jupyter notebooks examples provided in the `IPyNBs`folder using the MyBinder platform.

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/margudo/LSSGALPY.git/master)

The basic functionality of these interactive tools is the use of different projections in the 3D space (right ascension, declination, and redshift) to study the relation of the galaxies with the LSS. In particular, we use a Mollweide projection (the code could also work with several tens of other types of projections) in combination with a wedge diagram, and viceversa. Therefore, we can visualise the locations of the galaxies in our study for different values of redshifts and redshift ranges. Similarly, for different values of the declinations and declination ranges, one can visualise how the isolated galaxies, isolated pairs, and isolated triplets are related to the galaxies in the LSS. Additionally, one can, very easily and quickly, add or remove samples, change the marker size, transparency, and/or symbol, etc. These tools have been tested using up to 30 million objects and still work perfectly and very smoothly on any standard laptop.

The code is also presented in the article LSSGalPy: Interactive Visualization of the Large-scale Environment Around Galaxies, for the special issue ''Techniques and Methods for Astrophysical Data Visualization'' of the PASP journal.

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

* Citing LSSGalPy

If you use LSSGalPy for work/research presented in a publication, we ask that you cite the LSSGalPy paper and the ASCL Software. 

LSSGalPy paper’s Bibtex entry to use:

```
@ARTICLE{2017PASP..129e8005A,
   author = {{Argudo-Fern{\'a}ndez}, M. and {Duarte Puertas}, S. and {Ruiz}, J.~E. and 
	{Sabater}, J. and {Verley}, S. and {Bergond}, G.},
    title = "{LSSGalPy: Interactive Visualization of the Large-scale Environment Around Galaxies}",
  journal = {\pasp},
archivePrefix = "arXiv",
   eprint = {1702.04268},
 primaryClass = "astro-ph.IM",
     year = 2017,
    month = may,
   volume = 129,
   number = 5,
    pages = {058005},
      doi = {10.1088/1538-3873/aa5785},
   adsurl = {http://adsabs.harvard.edu/abs/2017PASP..129e8005A},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```

LSSGalPy ASCL’s Bibtex entry to use:

```
@MISC{2015ascl.soft05012A,
   author = {{Argudo-Fern{\'a}ndez}, M. and {Duarte Puertas}, S. and {Verley}, S. and 
	{Sabater}, J. and {Ruiz}, J.~E.},
    title = "{LSSGALPY: Visualization of the large-scale environment around galaxies on the 3D space}",
 keywords = {Software},
howpublished = {Astrophysics Source Code Library},
     year = 2015,
    month = may,
archivePrefix = "ascl",
   eprint = {1505.012},
   adsurl = {http://adsabs.harvard.edu/abs/2015ascl.soft05012A},
  adsnote = {Provided by the SAO/NASA Astrophysics Data System}
}
```



