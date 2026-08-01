"""
CanHiS instrument configuration.
"""

from .base import Instrument


class CanHiS(Instrument):

    name = "canhis"

    parameters = {

        "dispaxis": 1,

        "bad_pixels": "bad_pixels.dat",

        "overscan": "[1:1601,1:2048]",

        "trimsec": "[250:1850,1:2048]",

        "ccdtype": "",

        "scantype": "shortscan",

        "readaxis": "line",

    }
