"""
CCD processing utilities for specpipe.

Initial implementation replacing IRAF ccdproc.
"""

from pathlib import Path
import numpy as np
from astropy.io import fits


class CCDProcessor:
    """
    Basic CCD image processor.
    """


    def __init__(self, instrument):
        """
        Parameters
        ----------
        instrument :
            Instrument configuration object
            (CanHiS, TS23, ...)
        """

        self.instrument = instrument



    def read(self, filename):
        """
        Read FITS image.

        Returns
        -------
        data, header
        """

        data, header = fits.getdata(
            filename,
            header=True
        )

        return data, header



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



    def parse_iraf_section(self, section):
        """
        Convert IRAF section notation:

        [x1:x2,y1:y2]

        into Python indexes.
        """

        section = section.strip("[]")

        xsec, ysec = section.split(",")


        def parse(value):

            start, end = value.split(":")

            return (
                int(start)-1,
                int(end)
            )


        return (
            parse(xsec),
            parse(ysec)
        )



    def overscan_correct(self, data):
        """
        Subtract overscan level.

        Uses instrument overscan region.
        """

        section = self.instrument.get(
            "overscan"
        )


        if section is None:
            return data


        (x1, x2), (y1, y2) = self.parse_iraf_section(
            section
        )


        overscan = data[
            y1:y2,
            x1:x2
        ]


        level = np.median(
            overscan
        )


        corrected = data - level


        return corrected



    def fix_bad_pixels(self, data):
        """
        Correct bad pixel regions.

        The bad pixel file format follows IRAF:

        x1 x2 y1 y2

        Example:

        200 200 1 2048
        1635 1636 1 2048
        """

        filename = self.instrument.get(
            "bad_pixels"
        )


        if filename is None:
            return data


        if not Path(filename).exists():
            print(
                f"Warning: {filename} not found"
            )
            return data


        corrected = data.copy()


        with open(filename) as f:

            for line in f:

                if line.strip() == "":
                    continue


                x1, x2, y1, y2 = map(
                    int,
                    line.split()
                )


                # Convert to python indexes
                x1 -= 1
                x2 -= 1


                # Protect borders

                if x1 == 0 or x2 >= corrected.shape[1]-1:
                    continue


                left = corrected[
                    y1:y2,
                    x1-1
                ]


                right = corrected[
                    y1:y2,
                    x2+1
                ]


                corrected[
                    y1:y2,
                    x1:x2+1
                ] = (
                    left[:, None] +
                    right[:, None]
                ) / 2


        return corrected



    def trim(self, data):
        """
        Apply trimming region.
        """

        section = self.instrument.get(
            "trimsec"
        )


        if section is None:
            return data


        (x1, x2), (y1, y2) = self.parse_iraf_section(
            section
        )


        return data[
            y1:y2,
            x1:x2
        ]



    def process(self, input_file, output_file):
        """
        Complete CCD processing.

        Steps:

        1. Overscan correction
        2. Bad pixel correction
        3. Trim
        """

        data, header = self.read(
            input_file
        )


        data = self.overscan_correct(
            data
        )


        data = self.fix_bad_pixels(
            data
        )


        data = self.trim(
            data
        )


        self.write(
            output_file,
            data,
            header
        )
