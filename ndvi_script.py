import rasterio
import numpy as np
import matplotlib.pyplot as plt
import sys

# Get file paths from command line arguments
if len(sys.argv) < 3:
    raise ValueError("Usage: python ndvi_script.py <NIR_TIF> <RED_TIF>")

nir_tif = sys.argv[1]
red_tif = sys.argv[2]
output_ndvi_tif = "NDVI_PYTHON.TIF"
output_plot = "ndvi_plot.png"

# Open Red and NIR bands
with rasterio.open(red_tif) as red_src, rasterio.open(nir_tif) as nir_src:
    red = red_src.read(1).astype(np.float32)
    nir = nir_src.read(1).astype(np.float32)
    meta = nir_src.meta.copy()

    if red.shape != nir.shape:
        raise ValueError("Red and NIR bands have different dimensions!")

# Compute NDVI
ndvi = (nir - red) / (nir + red + 1e-10)
ndvi = np.clip(ndvi, -1, 1)

# Save NDVI GeoTIFF
meta.update(dtype=rasterio.float32, count=1)
with rasterio.open(output_ndvi_tif, "w", **meta) as dst:
    dst.write(ndvi, 1)

# Save NDVI Plot
plt.figure(figsize=(10, 6))
plt.imshow(ndvi, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(label="NDVI Value")
plt.title("NDVI Calculation")
plt.savefig(output_plot, dpi=150, bbox_inches="tight")
plt.close()

print(f"NDVI saved as {output_ndvi_tif}, plot saved as {output_plot}.")
