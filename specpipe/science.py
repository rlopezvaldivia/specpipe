"""
Science frame processing utilities for specpipe.
"""

from pathlib import Path
import numpy as np
from astropy.io import fits



class ScienceProcessor:
    """
    Apply calibration frames to science images.
    """



    def calibrate_object(self, filename, master_bias, master_flat, output):

        """
        Apply bias subtraction and flat correction.
        """

        data, header = fits.getdata(
            filename,
            header=True
        )


        bias = fits.getdata(
            master_bias
        )


        flat = fits.getdata(
            master_flat
        )


        calibrated = data - bias


        calibrated = calibrated / flat



        header["HISTORY"] = (
            "specpipe: master bias subtraction"
        )


        header["HISTORY"] = (
            "specpipe: flat field correction"
        )


        fits.writeto(
            output,
            calibrated,
            header,
            overwrite=True
        )
