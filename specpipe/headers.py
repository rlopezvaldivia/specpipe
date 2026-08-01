"""
FITS header utilities for specpipe.
"""

from pathlib import Path
from astropy.io import fits


class FitsHeader:
    """
    Read and interpret FITS headers.
    """

    def __init__(self, filename):
        self.filename = Path(filename)

        with fits.open(self.filename) as hdul:
            self.header = hdul[0].header


    def get(self, key, default=None):
        """
        Get FITS header keyword.
        """
        return self.header.get(key, default)


    def image_type(self):
        """
        Determine image type.

        Priority:
        1. IMGTYPE keyword
        2. Filename convention
        """

        # TS23 style
        imgtype = self.get("IMGTYPE")

        if imgtype:
            imgtype = imgtype.lower()

            mapping = {
                "bias": "bias",
                "zero": "bias",
                "flat": "flat",
                "arc": "arc",
                "object": "object",
                "star": "object"
            }

            if imgtype in mapping:
                return mapping[imgtype]


        # CanHiS style
        name = self.filename.name.lower()


        if len(name) >= 14:

            code = name[-6]

            mapping = {
                "b": "bias",
                "f": "flat",
                "a": "arc",
                "o": "object"
            }

            if code in mapping:
                return mapping[code]


        return "unknown"


    def object_name(self):
        """
        Return object name if available.
        """
        return self.get(
            "OBJECT",
            self.filename.stem
        )


def classify_fits(files):
    """
    Classify a list of FITS files.

    Returns dictionary:
    
    {
      bias: [],
      flat: [],
      arc: [],
      object: []
    }
    """

    result = {
        "bias": [],
        "flat": [],
        "arc": [],
        "object": [],
        "unknown": []
    }


    for file in files:

        ftype = FitsHeader(file).image_type()

        result[ftype].append(file)


    return result
