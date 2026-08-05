"""
CanHiS instrument configuration.
"""

from .base import Instrument


class CanHiS(Instrument):

    name = "canhis"

    parameters = {

        "dispaxis": 1,

        "mode": "simple",

        "bad_pixels": "bad_pixels.dat",

        "overscan": "[2045:2048,1:2048]",

        "trimsec": "[770:1025,1:2048]",

        "ccdtype": "",

        "scantype": "shortscan",

        "readaxis": "line",

    }
