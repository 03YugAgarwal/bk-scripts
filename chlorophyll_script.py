import rasterio
import numpy as np
import matplotlib.pyplot as plt
import sys

# Get file paths from command line arguments
if len(sys.argv) < 3:
    raise ValueError("Usage: python chlorophyll_script.py <NIR_TIF> <GREEN_TIF>")

nir_tif = sys.argv[1]
green_tif = sys.argv[2]
output_chlorophyll_tif = "CHLOROPHYLL_PYTHON.TIF"
output_plot = "chlorophyll_plot.png"

# Open Green and NIR bands
with rasterio.open(green_tif) as green_src, rasterio.open(nir_tif) as nir_src:
    green = green_src.read(1).astype(np.float32)
    nir = nir_src.read(1).astype(np.float32)
    meta = nir_src.meta.copy()

    if green.shape != nir.shape:
        raise ValueError("Green and NIR bands have different dimensions!")

# Compute Chlorophyll Index
chlorophyll_index = (nir / (green + 1e-10)) - 1

# Save Chlorophyll GeoTIFF
meta.update(dtype=rasterio.float32, count=1)
with rasterio.open(output_chlorophyll_tif, "w", **meta) as dst:
    dst.write(chlorophyll_index, 1)

# Save Chlorophyll Plot
plt.figure(figsize=(10, 6))
plt.imshow(chlorophyll_index, cmap='YlGn', vmin=0, vmax=2)
plt.colorbar(label="Chlorophyll Index")
plt.title("Chlorophyll Index Calculation")
plt.savefig(output_plot, dpi=150, bbox_inches="tight")
plt.close()

print(f"Chlorophyll Index saved as {output_chlorophyll_tif}, plot saved as {output_plot}.")
