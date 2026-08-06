from astropy.io import fits
import numpy as np

spec=fits.getdata(
"20260326/final_spectra/20260326_0044o.fits"
)

print(spec.shape)
print(spec[:10])
print(spec[-10:])
