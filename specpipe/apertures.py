"""
Aperture extraction utilities for specpipe.

Replacement of IRAF apall/apscatter workflow.
"""

from pathlib import Path
import shutil

from specpipe.iraf_tasks import IRAFTasks


class ApertureProcessor:
    """
    Handle aperture tracing and scattered light removal.
    """

    def __init__(self, workdir="."):
        self.workdir = Path(workdir)
        self.iraf = IRAFTasks()


    def trace_object_apertures(self, input_file):
        """
        Trace object apertures using reference spectrum trz.fits.
        """

        self.iraf.apall(
            input=input_file,
            output="",
            reference="trz.fits",
            interactive="yes",
            find="no",
            recenter="yes",
            resize="yes",
            edit="yes",
            trace="yes",
            fittrace="yes",
            extract="yes",
            t_order=3,
            t_niterate=5
        )


    def remove_scattered_light(self, input_file):
        """
        Remove scattered light using IRAF apscatter.
        """

        self.iraf.apscatter(
            input=input_file,
            output="",
            interactive="yes",
            find="no",
            recenter="no",
            resize="no",
            edit="no",
            trace="no",
            fittrace="no",
            subtract="yes",
            smooth="yes",
            fitscatter="yes",
            fitsmooth="yes",
            line="INDEF",
            nsum=10,
            buffer=1.0
        )


    def retrace_apertures(self, input_file):
        """
        Retrace and widen apertures to maximize SNR.
        """

        self.iraf.apall(
            input=input_file,
            interactive="yes",
            find="yes",
            recenter="yes",
            resize="yes",
            edit="yes",
            trace="yes",
            fittrace="yes",
            extract="no",
            line=945,
            nsum=10,
            width=15.0,
            radius=15.0,
            threshold=0.0,
            minsep=17,
            maxsep=45,
            shift="no",
            avglimits="yes",
            t_order=3,
            t_niterate=5,
            ylevel=0.02
        )


    def prepare_backup(self, source, destination):
        """
        Copy files before interactive operations.
        """

        source = Path(source)
        destination = Path(destination)

        destination.mkdir(
            parents=True,
            exist_ok=True
        )

        for file in source.glob("*.fits"):
            shutil.copy2(
                file,
                destination / file.name
            )


    def process(
        self,
        spectra_list,
        backup_dir="backup/objects",
        retry=True
    ):
        """
        Complete aperture processing.

        Steps:

        1. Trace apertures
        2. Remove scattered light
        3. Retrace apertures
        """

        self.prepare_backup(
            Path(spectra_list).parent,
            backup_dir
        )


        # Step 1
        self.trace_object_apertures(
            spectra_list
        )


        # Step 2
        self.remove_scattered_light(
            spectra_list
        )


        # Step 3
        self.retrace_apertures(
            spectra_list
        )
