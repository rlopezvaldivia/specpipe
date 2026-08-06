#!/usr/bin/env python3
from specpipe.extraction import ExtractionProcessor
from specpipe.pipeline import ReductionPipeline
from specpipe.config import get_instrument


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
    inst
)


#
# File classification
#
pipe.classify_files()


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
# Calibrate science frames
#
pipe.calibrate_science()


#
# Extract 1D spectra
#
pipe.extract_spectra()

pipe.extract_arcs()
print("\nReduction completed successfully.")
