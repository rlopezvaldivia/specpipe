"""
Main reduction pipeline for specpipe.

Controls the complete spectroscopic reduction workflow.
"""

from pathlib import Path
import shutil

from astropy.io import fits

from specpipe.ccd import CCDProcessor
from specpipe.apertures import ApertureProcessor
from specpipe.wavecal import WaveCalibrator


class ReductionPipeline:
    """
    Main controller for spectroscopic reductions.
    """


    def __init__(self, night_dir, instrument):

        self.night_dir = Path(night_dir)

        self.instrument = instrument

        self.workdir = Path.cwd()


        self.bias = []
        self.flats = []
        self.arcs = []
        self.objects = []


        self.ccd = CCDProcessor(
            instrument
        )

        self.apertures = None #ApertureProcessor()

        self.wavecal = None #WaveCalibrator()



    def classify_files(self):

        """
        Classify FITS files using IMGTYPE header.
        """

        files = sorted(
            self.night_dir.glob(
                "*.fits"
            )
        )


        for filename in files:

            with fits.open(filename) as hdul:

                imgtype = hdul[0].header.get(
                    "IMGTYPE",
                    ""
                ).lower()


            if imgtype in ["bias", "zero"]:

                self.bias.append(
                    filename
                )


            elif imgtype == "flat":

                self.flats.append(
                    filename
                )


            elif imgtype == "arc":

                self.arcs.append(
                    filename
                )


            else:

                self.objects.append(
                    filename
                )


        print(
            f"Bias: {len(self.bias)}"
        )

        print(
            f"Flat: {len(self.flats)}"
        )

        print(
            f"Arc: {len(self.arcs)}"
        )

        print(
            f"Objects: {len(self.objects)}"
        )



    def organize_files(self):

        """
        Create reduction folders.
        """

        folders = [

            "bias",
            "flat",
            "arc",
            "objects",
            "final_spectra"

        ]


        for folder in folders:

            Path(folder).mkdir(
                exist_ok=True
            )


        for item in self.bias:

            shutil.copy(
                item,
                "bias"
            )


        for item in self.flats:

            shutil.copy(
                item,
                "flat"
            )


        for item in self.arcs:

            shutil.copy(
                item,
                "arc"
            )


        for item in self.objects:

            shutil.copy(
                item,
                "objects"
            )



    def process_ccd(self):

        """
        Apply CCD corrections.
        """

        print(
            "CCD processing"
        )


        for filename in (

            self.bias
            +
            self.flats
            +
            self.objects
            +
            self.arcs

        ):


            output = Path(
                filename.name
            )


            self.ccd.process(
                filename,
                output
            )



    def run_apertures(
        self,
        object_list="objects.lst"
    ):

        """
        Run aperture extraction.
        """

        self.apertures.process(
            object_list
        )



    def run_wavelength_calibration(
        self,
        identify=True
    ):

        """
        Run wavelength calibration.
        """

        all_files = (

            self.arcs
            +
            self.objects

        )


        self.wavecal.process(

            all_files,

            "@list_objects.txt",

            identify=identify

        )



    def run(
        self,
        apertures=True,
        wavelength=True
    ):

        """
        Execute complete reduction.
        """

        print(
            "Starting specpipe"
        )


        self.classify_files()


        self.organize_files()


        self.process_ccd()


        if apertures:

            self.run_apertures()


        if wavelength:

            self.run_wavelength_calibration()


        print(
            "Reduction finished"
        )
