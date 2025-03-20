import rasterio
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

# Get file paths from command line arguments
if len(sys.argv) < 4:
    raise ValueError("Usage: python ndti_script.py <NIR_TIF> <RE_TIF> <OUTPUT_TIF>")

nir_tif = sys.argv[1]
rededge_tif = sys.argv[2]
output_ndti_tif = sys.argv[3]
output_plot = output_ndti_tif.replace(".TIF", ".png")

# Open NIR and Red Edge bands
with rasterio.open(nir_tif) as nir_src, rasterio.open(rededge_tif) as re_src:
    nir = nir_src.read(1).astype(np.float32)
    re = re_src.read(1).astype(np.float32)
    meta = nir_src.meta.copy()

    if nir.shape != re.shape:
        raise ValueError("NIR and Red Edge bands have different dimensions!")

# Compute NDTI
ndti = (nir - re) / (nir + re + 1e-10)
ndti = np.clip(ndti, -1, 1)

# Save NDTI GeoTIFF
meta.update(dtype=rasterio.float32, count=1)
with rasterio.open(output_ndti_tif, "w", **meta) as dst:
    dst.write(ndti, 1)

# Save NDTI Plot
plt.figure(figsize=(10, 6))
plt.imshow(ndti, cmap='RdYlGn', vmin=-1, vmax=1)
plt.colorbar(label="NDTI Value")
plt.title("NDTI Calculation")
plt.savefig(output_plot, dpi=150, bbox_inches="tight")
plt.close()

print(f"NDTI saved as {output_ndti_tif}, plot saved as {output_plot}.")
