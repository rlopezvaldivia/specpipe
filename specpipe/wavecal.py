"""
Wavelength calibration utilities for specpipe.

Replacement of IRAF apall + ecidentify + doecslit workflow.
"""

from pathlib import Path
import shutil

from astropy.io import fits


class WaveCalibrator:
    """
    Handle wavelength calibration and extraction.
    """

    def __init__(self, workdir="."):

        self.workdir = Path(workdir)

        self.iraf = None


    def _load_iraf(self):

        """
        Load IRAF only when needed.
        """

        if self.iraf is not None:
            return


        from specpipe.iraf_tasks import IRAFTasks

        self.iraf = IRAFTasks()



    def find_arc(self, fits_files):

        """
        Find arc exposure.
        """

        for filename in fits_files:

            with fits.open(filename) as hdul:

                imgtype = hdul[0].header.get(
                    "IMGTYPE",
                    ""
                )


                if imgtype.lower() == "arc":
                    return filename


        raise RuntimeError(
            "No arc exposure found"
        )



    def extract_arc(self, arc_file):

        """
        Extract Th-Ar spectrum.
        """

        self._load_iraf()

        self.iraf.apall(
            input="thar.fits",
            output="thar.fits",
            reference="trz.fits",
            format="echelle",
            interactive="yes",
            find="no",
            recenter="no",
            resize="no",
            edit="no",
            trace="no",
            fittrace="no",
            extract="yes",
            width=5.0,
            radius=10.0,
            minsep=5,
            maxsep=100000,
            order="increasing"
        )



    def identify_wavelengths(self):

        """
        Run IRAF ecidentify.
        """

        self._load_iraf()

        from pyraf import iraf

        iraf.ecidentify(
            "thar.ec.fits"
        )



    def load_reference_solution(
        self,
        filename
    ):

        """
        Copy wavelength solution.
        """

        database = self.workdir / "database"

        database.mkdir(
            exist_ok=True
        )


        shutil.copy(
            filename,
            database / Path(filename).name
        )



    def extract_objects(
        self,
        objects
    ):

        """
        Extract science spectra.
        """

        self._load_iraf()

        from pyraf import iraf


        iraf.doecslit.setParam(
            "apref",
            "trz.fits"
        )


        iraf.doecslit.setParam(
            "arcs",
            "thar.fits"
        )


        iraf.doecslit(
            objects=objects
        )



    def process(
        self,
        fits_files,
        objects,
        identify=True
    ):

        """
        Complete wavelength calibration.
        """

        arc = self.find_arc(
            fits_files
        )


        shutil.copy(
            arc,
            "thar.fits"
        )


        self.extract_arc(
            arc
        )


        if identify:

            self.identify_wavelengths()


        self.extract_objects(
            objects
        )


        output = Path(
            "final_spectra"
        )

        output.mkdir(
            exist_ok=True
        )


        for file in Path(".").glob(
            "*ec.fits"
        ):

            shutil.move(
                file,
                output / file.name
            )
