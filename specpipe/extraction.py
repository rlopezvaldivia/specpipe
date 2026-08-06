"""
Spectrum extraction module.

Handles aperture tracing and
1D spectral extraction.

Instrument geometry:

    Y axis  = dispersion
    X axis  = spatial

Input image:

    (2048,256)

Output spectrum:

    (2048,)

"""

from pathlib import Path

import numpy as np

from astropy.io import fits

from scipy.signal import find_peaks



class ExtractionProcessor:


    def __init__(

        self,

        instrument

    ):

        self.instrument = instrument


        self.aperture_width = instrument.get(

            "aperture_width",

            10

        )


        self.trace_degree = instrument.get(

            "trace_degree",

            3

        )



    ####################################################################
    #
    # Collapse image spatially
    #
    ####################################################################


    def collapse_spatial(

        self,

        image

    ):

        """
        Collapse spatial direction.

        Since dispersion is vertical,
        collapse X axis.

        Returns
        -------

        profile : ndarray

            Spatial profile.

        """

        profile = np.median(

            image,

            axis=0

        )


        return profile



    ####################################################################
    #
    # Find aperture
    #
    ####################################################################


    def find_aperture(

        self,

        profile

    ):

        """
        Find stellar position
        in spatial direction.
        """


        peaks, properties = find_peaks(

            profile,

            distance=20,

            prominence=np.std(profile)

        )


        if len(peaks) == 0:

            raise RuntimeError(

                "No aperture found"

            )


        peak = peaks[

            np.argmax(

                profile[peaks]

            )

        ]


        return peak

    ####################################################################
    #
    # Trace aperture
    #
    ####################################################################


    def trace_aperture(

        self,

        image,

        center

    ):

        """
        Trace aperture position.

        Returns:

            y positions
            x positions

        """

        ny, nx = image.shape


        ypos = []

        xpos = []



        half = self.aperture_width // 2



        for y in range(ny):


            x1 = max(

                0,

                center-half

            )


            x2 = min(

                nx,

                center+half+1

            )


            section = image[

                y,

                x1:x2

            ]


            if np.sum(section) <= 0:

                continue



            xpeak = (

                np.argmax(section)

                +

                x1

            )


            ypos.append(

                y

            )


            xpos.append(

                xpeak

            )



        return (

            np.array(ypos),

            np.array(xpos)

        )



    ####################################################################
    #
    # Fit trace
    #
    ####################################################################


    def fit_trace(

        self,

        ypos,

        xpos

    ):

        """
        Fit polynomial:

            x = f(y)

        """

        coef = np.polyfit(

            ypos,

            xpos,

            self.trace_degree

        )


        poly = np.poly1d(

            coef

        )


        return coef, poly



    ####################################################################
    #
    # Save trace
    #
    ####################################################################


    def save_trace(

        self,

        coef,

        filename

    ):

        """
        Save polynomial coefficients.
        """

        fits.writeto(

            filename,

            coef,

            overwrite=True

        )



    ####################################################################
    #
    # Load trace
    #
    ####################################################################


    def load_trace(

        self,

        filename

    ):

        """
        Load trace polynomial.
        """

        coef = fits.getdata(

            filename

        )


        return np.poly1d(

            coef

        )

    def refine_trace(
        self,
        image,
        trace,
        search_width=30
    ):

        """
        Refine aperture trace using
        the science image itself.

        image shape:
            (dispersion, spatial)

        Returns:
            refined spatial position
            for each dispersion pixel.
        """


        nx, ny = image.shape


        refined = []


        for i in range(nx):

            x0 = int(
                trace(i)
            )


            xmin = max(
                0,
                x0 - search_width
            )


            xmax = min(
                ny,
                x0 + search_width
            )


            section = image[
                i,
                xmin:xmax
            ]


            peak = np.argmax(
                section
            )


            refined.append(
                xmin + peak
            )


        refined = np.array(
            refined
        )


        return refined  
    ####################################################################
    #
    # Create trace file
    #
    ####################################################################


    def create_trace(

        self,

        flat_file,

        output_file

    ):

        """
        Create aperture trace from flat.
        """


        image = fits.getdata(

            flat_file

        )


        profile = self.collapse_spatial(

            image

        )


        center = self.find_aperture(

            profile

        )


        ypos, xpos = self.trace_aperture(

            image,

            center

        )


        coef, poly = self.fit_trace(

            ypos,

            xpos

        )


        self.save_trace(

            coef,

            output_file

        )


        return coef



    ####################################################################
    #
    # Extract spectrum
    #
    ####################################################################


    def extract(

        self,

        image,

        trace

    ):

        """
        Extract spectrum.

        Dispersion axis:

            Y

        Spatial axis:

            X

        Output:

            spectrum[2048]

        """

        ny, nx = image.shape


        spectrum = np.zeros(

            ny,

            dtype=float

        )


        half = self.aperture_width // 2



        for y in range(ny):

            if callable(trace):

                xc = trace(y)

            else:

                xc = trace[y]
            


            xc = int(

                round(xc)

            )


            x1 = max(

                0,

                xc-half

            )


            x2 = min(

                nx,

                xc+half+1

            )


            spectrum[y] = np.sum(

                image[

                    y,

                    x1:x2

                ]

            )



        return spectrum

    ####################################################################
    #
    # Extract single file
    #
    ####################################################################


    def extract_file(

        self,

        input_file,

        trace_file,

        output_file

    ):

        """
        Extract one science frame.
        """


        image = fits.getdata(

            input_file

        )

        trace = self.load_trace(
            trace_file
        )
        
        trace = self.refine_trace(
            image,
            trace

        )


        spectrum = self.extract(

            image,

            trace

        )


        header = fits.Header()


        header["NAXIS"] = 1

        header["NAXIS1"] = len(

            spectrum

        )


        header["HISTORY"] = (

            "specpipe: aperture extraction "

            "vertical dispersion"

        )


        fits.writeto(

            output_file,

            spectrum,

            header,

            overwrite=True

        )



    ####################################################################
    #
    # Process all files
    #
    ####################################################################


    def process(

        self,

        master_flat,

        science,

        output,

        trace

    ):

        """
        Extract spectra.

        Parameters
        ----------
        master_flat : Path
            Master flat image used for trace creation.

        science : Path
            Directory with calibrated science images.

        output : Path
            Output directory.

        trace : Path
            Trace polynomial file.
        """


        science = Path(science)

        output = Path(output)

        trace = Path(trace)



        output.mkdir(

            parents=True,

            exist_ok=True

        )


        files = sorted(

            science.glob(

                "*.fits"

            )

        )


        for filename in files:


            outfile = (

                output /

                filename.name

            )


            print(

                "Extracting",

                filename.name

            )


            self.extract_file(

                filename,

                trace,

                outfile

            )


