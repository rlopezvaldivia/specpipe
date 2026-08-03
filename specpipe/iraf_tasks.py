"""
IRAF wrapper functions for specpipe.

PyRAF is an optional dependency.
"""

try:
    from pyraf import iraf
    PYRAF_AVAILABLE = True

except ImportError:
    iraf = None
    PYRAF_AVAILABLE = False



class IRAFTasks:
    """
    Wrapper around IRAF tasks.
    """

    def __init__(self):

        if not PYRAF_AVAILABLE:
            raise ImportError(
                "PyRAF is required for IRAF operations. "
                "Install PyRAF/IRAF or run non-IRAF modules."
            )


        iraf.noao()
        iraf.imred()
        iraf.ccdred()
        iraf.onedspec()
        iraf.twodspec()
        iraf.apextract()
        iraf.echelle()



    def apall(self, input, **kwargs):

        for key, value in kwargs.items():

            key = self._translate_parameter(key)

            iraf.apall.setParam(
                key,
                value
            )

        iraf.apall(
            input=input
        )



    def apscatter(self, input, **kwargs):

        for key, value in kwargs.items():

            key = self._translate_parameter(key)

            iraf.apscatter.setParam(
                key,
                value
            )

        iraf.apscatter(
            input=input
        )



    def _translate_parameter(self, key):

        mapping = {

            "reference": "referen",
            "interactive": "interac",
            "recenter": "recente",
            "fittrace": "fittrac",
            "threshold": "thresho",
            "avglimits": "avglimi",
            "t_niterate": "t_niter",
            "fitscatter": "fitscat",
            "fitsmooth": "fitsmoo",
            "subtract": "subtrac",

        }

        return mapping.get(
            key,
            key
        )
