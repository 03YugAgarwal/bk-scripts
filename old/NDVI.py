import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show

# Paths to input Red & NIR band TIFF files
red_tif = "E:/BrahmaKamal/Sat/script/R.TIF"
nir_tif = "E:/BrahmaKamal/Sat/script/NIR.TIF"  # FIXED: Use correct NIR file
output_ndvi_tif = "E:/BrahmaKamal/Sat/script/NDVI_PYTHON.TIF"

# Open the Red band (extract metadata)
with rasterio.open(red_tif) as red_src:
    red = red_src.read(1).astype(np.float32)
    transform = red_src.transform  # Preserve georeferencing
    crs = red_src.crs  # Preserve coordinate reference system

# Open the NIR band
with rasterio.open(nir_tif) as nir_src:
    nir = nir_src.read(1).astype(np.float32)

    # Ensure both bands have the same shape
    if red.shape != nir.shape:
        raise ValueError("Red and NIR bands have different dimensions. They must be resampled.")

    # Copy metadata from one of the bands (e.g., Red) to maintain georeferencing
    meta = nir_src.meta.copy()

# Avoid division by zero errors
np.seterr(divide='ignore', invalid='ignore')

# Compute NDVI: (NIR - Red) / (NIR + Red)
ndvi = (nir - red) / (nir + red + 1e-10)  # Adding a small epsilon to avoid division by zero

# Normalize NDVI values between -1 and 1
ndvi = np.clip(ndvi, -1, 1)

# Ensure the output file retains georeferencing
meta.update(dtype=rasterio.float32, count=1, transform=transform, crs=crs)

# Save NDVI as a new GeoTIFF file
with rasterio.open(output_ndvi_tif, "w", **meta) as dst:
    dst.write(ndvi, 1)

# Display NDVI
plt.figure(figsize=(10, 6))
plt.imshow(ndvi, cmap='RdYlGn')  # Red to Green colormap
plt.colorbar(label="NDVI Value")
plt.title("NDVI Calculation from DJI M3M")
plt.show()
