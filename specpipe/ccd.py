"""
CCD processing utilities.

First implementation replacing IRAF ccdproc.
"""

from pathlib import Path
import numpy as np
from astropy.io import fits


class CCDProcessor:
    """
    Basic CCD image processing.
    """


    def __init__(self, instrument):
        """
        instrument:
            CanHiS or TS23 configuration
        """

        self.instrument = instrument



    def read(self, filename):
        """
        Read FITS image.
        """

        return fits.getdata(filename)



    def write(self, filename, data, header=None):
        """
        Write FITS image.
        """

        fits.writeto(
            filename,
            data,
            header=header,
            overwrite=True
        )



    def trim(self, data):
        """
        Apply trimming region.

        Current implementation:
        supports IRAF style sections.
        """

        section = self.instrument.get(
            "trimsec"
        )

        if section is None:
            return data


        # remove IRAF brackets
        section = section.strip("[]")

        xsec, ysec = section.split(",")


        def parse(section):
            start, end = section.split(":")
            return int(start)-1, int(end)


        x1, x2 = parse(xsec)
        y1, y2 = parse(ysec)


        return data[y1:y2, x1:x2]



    def overscan_correct(self, data):
        """
        Simple overscan subtraction.

        Placeholder for first version.
        """

        return data



    def process(self, input_file, output_file):
        """
        Run basic CCD processing.
        """

        data, header = fits.getdata(
            input_file,
            header=True
        )


        data = self.overscan_correct(data)

        data = self.trim(data)


        self.write(
            output_file,
            data,
            header
        )


