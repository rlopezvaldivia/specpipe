# Spectroscopic Reduction Pipeline

A modular pipeline for the reduction of astronomical spectroscopic observations.

The pipeline integrates and extends reduction routines originally developed by several colleagues into a single automated workflow. The code has been refactored and improved to provide a modular, reproducible, and easy-to-maintain reduction pipeline.

## Current Capabilities

The pipeline currently supports:

* CAnHiS spectra.
* Long-slit spectra.
* Modular execution of the reduction process.
* Automatic generation of intermediate and final data products.

## Running the Pipeline

The pipeline can be executed using

```bash
python run_pip.py
```

Configuration files and examples are provided in the repository.

## Plotting spectra

The utility `plot_spectrum.py` can display both 1D extracted spectra and
2D wavelength-calibrated images.

### Plot a 1D spectrum

```bash
python plot_spectrum.py \
    20260326/wavecal_spectra/20260326_0044o.fits
```

### Plot a 2D spectrum

If the input image is 2D, the program automatically extracts a spectrum
using the central rows.

```bash
python plot_spectrum.py \
    20260326/wavecal_2d/20260326_0044o.fits
```

### Extract around a different spatial position

```bash
python plot_spectrum.py \
    20260326/wavecal_2d/20260326_0044o.fits \
    --center 140 \
    --width 15
```

where:

- `center` is the spatial pixel used as the extraction center.
- `width` is the half-width of the extraction aperture in pixels.

The extracted spectrum is displayed either in wavelength (if WCS keywords
are present) or in detector pixels.

## Documentation

Additional documentation can be found in the `docs/` directory.

* `pipeline.md` – General description of the pipeline.
* `canhis.md` – CAnHiS reduction.
* `longslit.md` – Long-slit reduction.
* `echelle.md` – Echelle module (under development).
* `caveats.md` – Current limitations and assumptions.

## Caveats

At the moment, the pipeline has been tested only for:

* CanHiS observations.
* Long-slit observations.
* Spectra with the dispersion axis aligned with the detector **Y-axis**.

Support for additional observing modes and detector configurations will be added in future releases.

## Roadmap

Planned developments include:

* Echelle reduction module.
* Support for additional detector orientations.
* Improved diagnostics and logging.
* Expanded instrument support.

## Acknowledgements

This pipeline is based on reduction routines developed by several collaborators and has been integrated, refactored, and improved into a unified workflow. Documentation, testing, debugging, and code organization were further enhanced during the development of this repository with the assistance of AI-based programming tools.
