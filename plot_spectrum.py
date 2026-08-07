"""
Plot 1D or 2D spectra.
"""

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt

from astropy.io import fits



def plot_spectrum(

    filename,

    center=None,

    width=10

):

    """
    Plot a spectrum.

    Parameters
    ----------
    filename : str or Path
        FITS spectrum.

    center : int, optional
        Center row for 2D extraction.
        If None, use image center.

    width : int, optional
        Half-width (pixels) of the extraction.
    """


    filename = Path(

        filename

    )


    with fits.open(

        filename

    ) as hdul:


        data = hdul[0].data

        header = hdul[0].header


    if data.ndim == 1:


        spectrum = data


    elif data.ndim == 2:


        if center is None:

            center = data.shape[1] // 2


        y1 = max(

            0,

            center - width

        )


        y2 = min(

            data.shape[1],

            center + width

        )


        spectrum = np.sum(

            data[:, y1:y2],

            axis=1

        )


    else:

        raise ValueError(

            "Only 1D or 2D FITS files are supported."

        )


    if "CRVAL1" in header and "CDELT1" in header:


        x = (

            header["CRVAL1"]

            +

            np.arange(

                len(spectrum)

            )

            *

            header["CDELT1"]

        )


        xlabel = "Wavelength (Angstrom)"


    else:


        x = np.arange(

            len(spectrum)

        )


        xlabel = "Pixel"


    plt.figure(

        figsize=(12,5)

    )


    plt.plot(

        x,

        spectrum,

        lw=1

    )


    plt.xlabel(

        xlabel

    )


    plt.ylabel(

        "Counts"

    )


    plt.title(

        filename.name

    )


    plt.grid(

        alpha=0.3

    )


    plt.tight_layout()


    plt.show()



if __name__ == "__main__":


    import argparse


    parser = argparse.ArgumentParser(

        description="Plot 1D or 2D FITS spectra."

    )


    parser.add_argument(

        "file",

        help="Input FITS file"

    )


    parser.add_argument(

        "--center",

        type=int,

        default=None,

        help="Center row for 2D extraction"

    )


    parser.add_argument(

        "--width",

        type=int,

        default=10,

        help="Half-width of extraction"

    )


    args = parser.parse_args()


    plot_spectrum(

        args.file,

        center=args.center,

        width=args.width

    )
