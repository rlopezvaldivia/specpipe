"""
CCD processing module.
"""

import numpy as np
from pathlib import Path

from astropy.io import fits



class CCDProcessor:
    """
    Apply CCD corrections.
    """



    def __init__(self, instrument):

        self.instrument = instrument






    def parse_iraf_section(self, section):

        """
        Convert IRAF section notation:

        [x1:x2,y1:y2]

        into Python indices.
        """

        section = section.strip("[]")


        xsec, ysec = section.split(",")



        def parse(value):

            start, end = value.split(":")

            return int(start), int(end)



        return parse(xsec), parse(ysec)







    def overscan_correct(self, data):

        """
        Apply overscan correction.
        """

        section = self.instrument.get(
            "overscan"
        )


        if section is None:

            return data



        (x1,x2),(y1,y2)=self.parse_iraf_section(
            section
        )


        overscan = data[
            y1-1:y2,
            x1-1:x2
        ]



        if overscan.size == 0:

            return data



        correction = np.median(
            overscan,
            axis=1
        )


        corrected = data - correction[:,None]



        return corrected







    def trim(self, data):

        """
        Apply CCD trimming.

        IRAF convention:
            [x1:x2,y1:y2]

        Python convention:
            data[y,x]
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
            y1-1:y2,
            x1-1:x2
        ]







    def bad_pixel_correction(self, data):

        """
        Apply bad pixel mask if available.
        """

        bad_file = self.instrument.get(
            "bad_pixels"
        )


        if bad_file is None:

            return data



        if not Path(bad_file).exists():

            print(
                f"Warning: {bad_file} not found"
            )

            return data



        bad_pixels = np.loadtxt(
            bad_file,
            dtype=int
        )



        corrected = data.copy()



        for y,x in bad_pixels:

            if (
                y < corrected.shape[0]
                and x < corrected.shape[1]
            ):

                corrected[y,x] = np.median(
                    corrected[
                        max(0,y-1):y+2,
                        max(0,x-1):x+2
                    ]
                )



        return corrected







    def process(self, input_file, output_file):

        """
        Complete CCD reduction.

        Steps:
            1. Read FITS
            2. Overscan correction
            3. Trim
            4. Bad pixel correction
            5. Save output
        """



        data, header = fits.getdata(
            input_file,
            header=True
        )



        data = self.overscan_correct(
            data
        )


        data = self.trim(
            data
        )


        data = self.bad_pixel_correction(
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



        fits.writeto(
            output_file,
            data,
            header,
            overwrite=True
        )
