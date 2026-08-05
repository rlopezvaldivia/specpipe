"""
Calibration utilities for specpipe.
"""

from pathlib import Path
import numpy as np
from astropy.io import fits



class Calibration:

    """
    Create master calibration frames.
    """



    def combine_images(self, files, output):

        """
        Median combine FITS images.
        """

        data = []


        for filename in files:

            image = fits.getdata(
                filename
            )

            data.append(
                image
            )


        combined = np.median(
            np.array(data),
            axis=0
        )


        fits.writeto(
            output,
            combined,
            overwrite=True
        )



    def create_master_bias(self, bias_files, output):

        """
        Create master bias.
        """

        self.combine_images(
            bias_files,
            output
        )



    def create_master_flat(self, flat_files, master_bias, output):

        """
        Create normalized master flat.
        """

        flats = []


        bias = fits.getdata(
            master_bias
        )


        for filename in flat_files:

            data = fits.getdata(
                filename
            )


            data = data - bias


            flats.append(
                data
            )


        master = np.median(
            np.array(flats),
            axis=0
        )


        master /= np.median(
            master
        )


        fits.writeto(
            output,
            master,
            overwrite=True
        )
