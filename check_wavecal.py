from astropy.io import fits
import matplotlib.pyplot as plt
import numpy as np

from specpipe.wavelength import WavelengthCalibration


arc_file = "20260326/arc_spectra/test_arc.fits"

solution_file = "20260326/calibration/wavelength_solution.dat"


flux = fits.getdata(arc_file)


w = WavelengthCalibration()


coef = w.load_solution(
    solution_file
)


wave = w.wavelength_array(
    len(flux),
    coef
)


plt.figure(figsize=(12,5))


plt.plot(
    wave,
    flux
)


plt.xlabel(
    "Wavelength (Angstrom)"
)

plt.ylabel(
    "Flux"
)


plt.title(
    "ThAr/Li arc spectrum"
)


plt.gca().invert_xaxis()

plt.grid()

plt.tight_layout()

plt.show()
