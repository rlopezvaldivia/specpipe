#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
from pathlib import Path
import sys


def plot_spectrum(filename):

    with fits.open(filename) as hdul:
        data = hdul[0].data
        header = hdul[0].header

    flux = data

    # Si existe información WCS
    if "CRVAL1" in header and "CDELT1" in header:
        wavelength = (
            header["CRVAL1"]
            + np.arange(len(flux)) * header["CDELT1"]
        )
    else:
        wavelength = np.arange(len(flux))

    plt.figure(figsize=(12,4))
    plt.plot(wavelength, flux)

    plt.xlabel("Wavelength")
    plt.ylabel("Flux")
    plt.title(Path(filename).name)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":

    plot_spectrum(sys.argv[1])
