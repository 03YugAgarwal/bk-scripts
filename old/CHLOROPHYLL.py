import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Paths to input Green & NIR band TIFF files (For CIgreen)
green_tif = "E:/BrahmaKamal/Sat/script/G.TIF"  # Green band
nir_tif = "E:/BrahmaKamal/Sat/script/NIR.TIF"  # NIR band
output_ci_tif = "E:/BrahmaKamal/Sat/script/CHLOROPHYLL_PYTHON.TIF"

# Open the Green band (extract metadata)
with rasterio.open(green_tif) as green_src:
    green = green_src.read(1).astype(np.float32)
    transform = green_src.transform  # Preserve georeferencing
    crs = green_src.crs  # Preserve coordinate reference system

# Open the NIR band
with rasterio.open(nir_tif) as nir_src:
    nir = nir_src.read(1).astype(np.float32)

    # Ensure both bands have the same shape
    if green.shape != nir.shape:
        raise ValueError("Green and NIR bands have different dimensions. They must be resampled.")

    # Copy metadata from one of the bands (e.g., Green) to maintain georeferencing
    meta = nir_src.meta.copy()

# Avoid division by zero errors
np.seterr(divide='ignore', invalid='ignore')

# Compute Chlorophyll Index (CIgreen): (NIR / Green) - 1
chlorophyll_index = (nir / (green + 1e-10)) - 1  # Adding small epsilon to avoid division by zero

# Ensure the output file retains georeferencing
meta.update(dtype=rasterio.float32, count=1, transform=transform, crs=crs)

# Save Chlorophyll Index as a new GeoTIFF file
with rasterio.open(output_ci_tif, "w", **meta) as dst:
    dst.write(chlorophyll_index, 1)

# Display Chlorophyll Index
plt.figure(figsize=(10, 6))
plt.imshow(chlorophyll_index, cmap='YlGn')  # Yellow-Green colormap
plt.colorbar(label="Chlorophyll Index (CIgreen)")
plt.title("Chlorophyll Index (CIgreen) from DJI M3M")
plt.show()
