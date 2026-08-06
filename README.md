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

## Documentation

Additional documentation can be found in the `docs/` directory.

* `pipeline.md` – General description of the pipeline.
* `canhis.md` – CAnHiS reduction.
* `longslit.md` – Long-slit reduction.
* `echelle.md` – Echelle module (under development).
* `caveats.md` – Current limitations and assumptions.

## Caveats

At the moment, the pipeline has been tested only for:

* CAnHiS observations.
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
