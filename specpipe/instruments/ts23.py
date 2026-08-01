"""
TS23 echelle instrument configuration.
"""

from .base import Instrument


class TS23(Instrument):

    name = "ts23"

    parameters = {

        "dispaxis": 1,

        "orders": 52,

        "bad_pixels": "bad_pixels.dat",

        "overscan": "[1:1601,1:2048]",

        "trimsec": "[250:1850,1:2048]",

        "mode": "echelle",

    }
