"""
Wavelength calibration utilities.
"""

from pathlib import Path

import numpy as np

from astropy.io import fits

from scipy.signal import find_peaks



class WavelengthCalibration:


    def __init__(

        self,

        prominence_factor=3

    ):

        self.prominence_factor = prominence_factor



    def read_spectrum(

        self,

        filename

    ):

        """
        Read 1D arc spectrum.
        """

        return fits.getdata(

            filename

        )



    def find_lines(

        self,

        spectrum

    ):

        """
        Detect emission lines.
        """

        noise = np.std(

            spectrum

        )


        peaks, properties = find_peaks(

            spectrum,

            prominence=self.prominence_factor * noise,

            distance=5

        )


        return peaks, properties



    def detect_arc_lines(

        self,

        filename

    ):

        """
        Read arc and detect lines.
        """

        spectrum = self.read_spectrum(

            filename

        )


        peaks, properties = self.find_lines(

            spectrum

        )


        return peaks

    def fit_solution(

        self,

        pixels,

        wavelengths,

        degree=3

    ):

        """
        Fit wavelength solution.
        """

        coef = np.polyfit(

            pixels,

            wavelengths,

            degree

        )


        return coef



    def wavelength_array(

        self,

        npixels,

        coef

    ):

        """
        Generate wavelength array.
        """

        pixels = np.arange(

            npixels

        )


        wave = np.polyval(

            coef,

            pixels

        )


        return wave

    def apply_solution(

        self,

        input_file,

        output_file,

        coef

    ):

        """
        Apply wavelength solution to 1D spectrum.
        """


        spectrum = fits.getdata(

            input_file

        )


        wavelength = self.wavelength_array(

            len(spectrum),

            coef

        )


        hdu = fits.PrimaryHDU(

            spectrum

        )


        hdu.header["CTYPE1"] = "WAVE"

        hdu.header["CRVAL1"] = wavelength[0]

        hdu.header["CDELT1"] = (

            wavelength[-1] - wavelength[0]

        ) / (

            len(wavelength) - 1

        )

        hdu.header["CUNIT1"] = "Angstrom"


        hdu.header["HISTORY"] = (

            "specpipe: wavelength calibration"

        )


        hdu.writeto(

            output_file,

            overwrite=True

        )


    def load_solution_file(

        self,

        filename

    ):

        """
        Load pixel-wavelength identified lines.
        """

        pixels = []

        wavelengths = []


        with open(

            filename,

            "r"

        ) as f:


            for line in f:


                line = line.strip()


                if not line:

                    continue


                if line.startswith("#"):

                    continue


                pixel, wavelength = line.split()


                pixels.append(

                    float(pixel)

                )


                wavelengths.append(

                    float(wavelength)

                )


        return (

            np.array(pixels),

            np.array(wavelengths)

        )


    def save_solution(

        self,

        filename,

        coef

    ):

        """
        Save wavelength polynomial coefficients.
        """

        filename = Path(

            filename

        )


        filename.parent.mkdir(

            parents=True,

            exist_ok=True

        )


        np.savetxt(

            filename,

            coef,

            header="Wavelength solution coefficients"

        )



    def load_solution(

        self,

        filename

    ):

        """
        Load wavelength polynomial coefficients.
        """

        return np.loadtxt(

            filename

        )
