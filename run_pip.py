#!/usr/bin/env python3
from specpipe.extraction import ExtractionProcessor
from specpipe.pipeline import ReductionPipeline
from specpipe.config import get_instrument
from specpipe.observation_list import ObservationList


obs_list = ObservationList(
    "observation_list.txt"
)



obs_list = ObservationList(
    "observation_list.txt"
)


#
# Select instrument
#
inst = get_instrument(
    "canhis"
)


#
# Create pipeline
#

pipe = ReductionPipeline(
    "20260326",
    inst,
    obs_list
)


#
# File classification
#
pipe.classify_files()

#print(self.objects)
#print(self.arcs)



#
# Organize files
#
pipe.organize_files()


#
# CCD processing
#
pipe.process_ccd()


#
# Create calibration frames
#
pipe.create_calibrations()

#
#Create the trace
pipe.trace_aperture()

#
# Calibrate science frames
#
pipe.calibrate_science()


#
# Extract 1D spectra
#
pipe.extract_spectra()

pipe.extract_arcs()

pipe.calibrate_wavelength("specpipe/data/test.dat")

pipe.calibrate_wavelength_2d()

print("\nReduction completed successfully.")


