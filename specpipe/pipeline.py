"""
Main reduction pipeline controller.

specpipe pipeline.

"""

from pathlib import Path
import shutil


from specpipe.ccd import CCDProcessor
from specpipe.calibration import Calibration
from specpipe.science import ScienceProcessor
from specpipe.extraction import ExtractionProcessor



class ReductionPipeline:

    """
    Main controller for spectral reduction.
    """



    def __init__(

        self,

        night,

        instrument

    ):


        self.night = Path(

            night

        )


        self.instrument = instrument



        #
        # File containers
        #

        self.bias = []

        self.flats = []

        self.arcs = []

        self.objects = []



        #
        # Processing modules
        #

        self.ccd = CCDProcessor(

            instrument

        )


        self.calibration = Calibration()


        self.science = ScienceProcessor()


        self.extractor = ExtractionProcessor(

            instrument

        )





    ####################################################################
    #
    # File classification
    #
    ####################################################################


    def classify_files(self):

        """
        Identify raw FITS files.
        """

        files = sorted(

            list(
                self.night.glob(
                    "*.fits"
                )
            )

            +

            list(
                self.night.glob(
                    "*.fits.gz"
                )
            )

        )


        for filename in files:


            name = filename.name.lower()



            if name.endswith(

                "b.fits"

            ) or name.endswith(

                "b.fits.gz"

            ):

                self.bias.append(

                    filename

                )


            elif name.endswith(

                "f.fits"

            ) or name.endswith(

                "f.fits.gz"

            ):

                self.flats.append(

                    filename

                )


            elif name.endswith(

                "a.fits"

            ) or name.endswith(

                "a.fits.gz"

            ):

                self.arcs.append(

                    filename

                )


            elif name.endswith(

                "o.fits"

            ) or name.endswith(

                "o.fits.gz"

            ):

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


    ####################################################################
    #
    # Organize files
    #
    ####################################################################


    def organize_files(self):

        """
        Create reduction folders.
        """


        folders = [

            "bias",
            "flat",
            "arc",
            "objects",
            "processed",
            "calibrated",
            "final_spectra"

        ]


        for folder in folders:

            Path(

                self.night / folder

            ).mkdir(

                exist_ok=True

            )



        groups = [

            (
                self.bias,
                "bias"
            ),

            (
                self.flats,
                "flat"
            ),

            (
                self.arcs,
                "arc"
            ),

            (
                self.objects,
                "objects"
            )

        ]


        for files, folder in groups:


            for item in files:

                shutil.copy(

                    item,

                    self.night / folder / item.name

                )



    ####################################################################
    #
    # CCD processing
    #
    ####################################################################


    def process_ccd(self):

        """
        Apply CCD corrections
        to raw frames.
        """


        print(

            "Processing CCD frames"

        )


        input_groups = [

            "bias",

            "flat",

            "arc",

            "objects"

        ]


        for group in input_groups:


            input_dir = self.night / group


            output_dir = (

                self.night /

                "processed" /

                group

            )


            output_dir.mkdir(

                parents=True,

                exist_ok=True

            )


            files = sorted(

                list(
                    input_dir.glob(
                        "*.fits"
                    )
                )

                +

                list(
                    input_dir.glob(
                        "*.fits.gz"
                    )
                )

            )


            for file in files:


                output = (

                    output_dir /

                    file.with_suffix(
                        ""
                    ).name

                )


                if output.suffix != ".fits":

                    output = output.with_suffix(
                        ".fits"
                    )



                print(

                    f"Processing {file}"

                )


                self.ccd.process(

                    file,

                    output

                )

    def create_calibrations(self):

        """
        Create master calibration frames.
        """

        print(
            "Creating calibration frames"
        )


        processed = (

            self.night /

            "processed"

        )


        bias_files = sorted(

            processed.joinpath("bias").glob(

                "*.fits"

            )

        )


        flat_files = sorted(

            processed.joinpath("flat").glob(

                "*.fits"

            )

        )


        arc_files = sorted(

            processed.joinpath("arc").glob(

                "*.fits"

            )

        )


        self.calibration.create_master_bias(

            bias_files,

            processed / "master_bias.fits"

        )


        self.calibration.create_master_flat(
            
            flat_files,

            processed / "master_bias.fits",

            processed / "master_flat.fits"

        )



       # self.calibration.create_master_arc(

#            arc_files,

 #           processed / "master_arc.fits"

 #       )


        print(

            "Calibration frames created"

        )
    ####################################################################
    #
    # Science calibration
    #
    ####################################################################


    def calibrate_science(self):

        """
        Apply bias/flat calibration
        to science frames.
        """


        processed = (

            self.night /

            "processed" /

            "objects"

        )


        output = (

            self.night /

            "calibrated"

        )


        output.mkdir(

            parents=True,

            exist_ok=True

        )


        files = sorted(

            processed.glob(

                "*.fits"

            )

        )


        print(

            f"Calibrating {len(files)} science frames"

        )


        for file in files:


            outfile = (

                output /

                file.name

            )


            self.science.calibrate_object(

                file,
                
                self.night / "processed" / "master_bias.fits",

                self.night / "processed" / "master_flat.fits",


                outfile

            )



    ####################################################################
    #
    # Trace creation
    #
    ####################################################################


    def trace_aperture(self):

        """
        Create aperture trace
        from master flat.
        """


        flat = (

            self.night /

            "processed" /

            "master_flat.fits"

        )


        trace = (

            self.night /

            "processed" /

            "trace.fits"

        )


        self.extractor.create_trace(

            flat,

            trace

        )



    ####################################################################
    #
    # Spectrum extraction
    #
    ####################################################################


    def extract_spectra(self):

        """
        Extract 1D spectra
        from calibrated science frames.
        """


        trace = (

            self.night /

            "processed" /

            "trace.fits"

        )


        science = (

            self.night /

            "calibrated"

        )


        output = (

            self.night /

            "final_spectra"

        )


        self.extractor.process(

            self.night /

            "processed" /

            "master_flat.fits",

            science,

            output,

            trace

        )


        ####################################################################
    #
    # Extract arc spectra
    #
    ####################################################################

    def extract_arcs(self):

        """
        Extract arc lamp spectra
        using the science trace.
        """


        arc_dir = (

            self.night /

            "processed" /

            "arc"

        )


        output = (

            self.night /

            "arc_spectra"

        )


        trace = (

            self.night /

            "processed" /

            "trace.fits"

        )


        self.extractor.process(

            self.night /

            "processed" /

            "master_flat.fits",

            arc_dir,

            output,

            trace

        )
