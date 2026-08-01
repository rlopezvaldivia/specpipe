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

        self.instrument = instrument



    def read(self, filename):

        data, header = fits.getdata(
            filename,
            header=True
        )

        return data, header



    def write(self, filename, data, header=None):

        fits.writeto(
            filename,
            data,
            header=header,
            overwrite=True
        )



    def parse_iraf_section(self, section):

        """
        Convert IRAF section:

        [x1:x2,y1:y2]

        into Python indexes.
        """

        section = section.strip("[]")

        xsec, ysec = section.split(",")


        def parse(value):

            start, end = value.split(":")

            return int(start)-1, int(end)


        return parse(xsec), parse(ysec)



    def overscan_correct(self, data):

        """
        Subtract overscan level.
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


        return data - level



    def fix_bad_pixels(self, data):

        """
        Correct bad pixels using interpolation.

        Format:

        x1 x2 y1 y2
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


                x1 -= 1
                x2 -= 1


                if x1 <= 0:
                    continue


                if x2 >= corrected.shape[1]-1:
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
                    left[:,None] +
                    right[:,None]
                ) / 2


        return corrected



    def trim(self, data):

        """
        Apply CCD trimming.
        """

        section = self.instrument.get(
            "trimsec"
        )


        if section is None:
            return data


        (x1,x2),(y1,y2)=self.parse_iraf_section(
            section
        )


        return data[
            y1:y2,
            x1:x2
        ]



    def process(self, input_file, output_file):

        """
        Complete CCD reduction.

        Steps:

        1. Overscan correction
        2. Trim
        3. Bad pixel correction
        """

        data, header = self.read(
            input_file
        )


        data = self.overscan_correct(
            data
        )


        data = self.trim(
            data
        )


        data = self.fix_bad_pixels(
            data
        )


        header["HISTORY"] = (
            "specpipe: overscan correction"
        )

        header["HISTORY"] = (
            "specpipe: trim applied"
        )

        header["HISTORY"] = (
            "specpipe: bad pixel correction"
        )


        self.write(
            output_file,
            data,
            header
        )
