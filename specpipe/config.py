"""
Configuration manager for specpipe.
"""

from specpipe.instruments.canhis import CanHiS
from specpipe.instruments.ts23 import TS23


INSTRUMENTS = {
    "canhis": CanHiS,
    "ts23": TS23,
}


def get_instrument(name):
    """
    Return instrument configuration.
    """

    name = name.lower()

    if name not in INSTRUMENTS:
        raise ValueError(
            f"Unknown instrument: {name}"
        )

    return INSTRUMENTS[name]()
