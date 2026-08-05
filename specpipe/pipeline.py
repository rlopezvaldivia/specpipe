"""
Main reduction pipeline controller.
"""

from pathlib import Path
import shutil

from specpipe.ccd import CCDProcessor
from specpipe.apertures import ApertureProcessor
from specpipe.wavecal import WaveCalibrator



class ReductionPipeline:
    """
    Main controller for specpipe reduction.
    """



    def __init__(self, night, instrument):

        self.night = Path(night)

        self.instrument = instrument

        self.bias = []
        self.flats = []
        self.arcs = []
        self.objects = []


        self.ccd = CCDProcessor(
            instrument
        )


        # Lazy loading for IRAF-dependent modules

        self.apertures = None
        self.wavecal = None





    def classify_files(self):

        """
        Classify FITS files from observing night.
        """

        files = sorted(
            list(self.night.glob("*.fits")) +
            list(self.night.glob("*.fits.gz"))
        )


        for filename in files:

            name = filename.name.lower()


            if name.endswith("b.fits") or name.endswith("b.fits.gz"):

                self.bias.append(filename)


            elif name.endswith("f.fits") or name.endswith("f.fits.gz"):

                self.flats.append(filename)


            elif name.endswith("a.fits") or name.endswith("a.fits.gz"):

                self.arcs.append(filename)


            elif name.endswith("o.fits") or name.endswith("o.fits.gz"):

                self.objects.append(filename)



        print(f"Bias: {len(self.bias)}")
        print(f"Flat: {len(self.flats)}")
        print(f"Arc: {len(self.arcs)}")
        print(f"Objects: {len(self.objects)}")






    def organize_files(self):

        """
        Create reduction folders inside night directory.
        """

        folders = [

            "bias",
            "flat",
            "arc",
            "objects",
            "final_spectra"

        ]


        for folder in folders:

            Path(
                self.night / folder
            ).mkdir(
                exist_ok=True
            )



        for item in self.bias:

            shutil.copy(
                item,
                self.night / "bias"
            )


        for item in self.flats:

            shutil.copy(
                item,
                self.night / "flat"
            )


        for item in self.arcs:

            shutil.copy(
                item,
                self.night / "arc"
            )


        for item in self.objects:

            shutil.copy(
                item,
                self.night / "objects"
            )







    def process_ccd(self):

        """
        Apply CCD corrections to all images.
        """

        folders = [

            "bias",
            "flat",
            "arc",
            "objects"

        ]


        output_base = self.night / "processed"



        for folder in folders:


            input_dir = self.night / folder

            output_dir = output_base / folder


            output_dir.mkdir(
                parents=True,
                exist_ok=True
            )



            files = sorted(
                list(input_dir.glob("*.fits")) +
                list(input_dir.glob("*.fits.gz"))
            )


            print(
                f"{folder}: {len(files)} files"
            )



            for filename in files:


                output = output_dir / filename.name.replace(
                    ".gz",
                    ""
                )


                print(
                    f"Processing {filename}"
                )


                self.ccd.process(
                    filename,
                    output
                )








    def _load_apertures(self):

        if self.apertures is None:

            self.apertures = ApertureProcessor()






    def _load_wavecal(self):

        if self.wavecal is None:

            self.wavecal = WaveCalibrator()






    def run_apertures(self):

        """
        Extract apertures.
        """

        self._load_apertures()

        self.apertures.process()






    def run_wavecal(self):

        """
        Perform wavelength calibration.
        """

        self._load_wavecal()

        self.wavecal.process()
