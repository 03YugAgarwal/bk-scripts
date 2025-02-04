import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Paths to NDVI TIFF files
ndvi_python_tif = "E:/BrahmaKamal/Sat/script/CHLOROPHYLL_PYTHON.TIF"
ndvi_qgis_tif = "E:/BrahmaKamal/Sat/script/CHLOROPHYLL_QGIS.tif"

topic = "NDTI"

# Open Python-generated NDVI
with rasterio.open(ndvi_python_tif) as src:
    ndvi_python = src.read(1).astype(np.float32)
    python_meta = src.meta.copy()

# Open QGIS-generated NDVI
with rasterio.open(ndvi_qgis_tif) as src:
    ndvi_qgis = src.read(1).astype(np.float32)
    qgis_meta = src.meta.copy()

# Check if both files have the same shape
if ndvi_python.shape != ndvi_qgis.shape:
    raise ValueError("⚠️ NDVI images from Python and QGIS have different dimensions. They must match!")

# Check if both files have the same georeferencing
if python_meta['crs'] != qgis_meta['crs']:
    print("⚠️ Warning: CRS (Coordinate Reference System) differs between Python and QGIS NDVI files.")
    print(f"Python CRS: {python_meta['crs']}")
    print(f"QGIS CRS: {qgis_meta['crs']}")

if python_meta['transform'] != qgis_meta['transform']:
    print("⚠️ Warning: Geotransform differs between Python and QGIS NDVI files.")
    print(f"Python Transform: {python_meta['transform']}")
    print(f"QGIS Transform: {qgis_meta['transform']}")

# Compute the difference between Python and QGIS NDVI
ndvi_diff = ndvi_python - ndvi_qgis

# Compute statistics on the difference
mean_diff = np.mean(ndvi_diff)
std_diff = np.std(ndvi_diff)
min_diff = np.min(ndvi_diff)
max_diff = np.max(ndvi_diff)

# Print comparison statistics
print("\n📊 NDVI Comparison Statistics:")
print(f"Mean Difference: {mean_diff:.6f}")
print(f"Standard Deviation: {std_diff:.6f}")
print(f"Min Difference: {min_diff:.6f}")
print(f"Max Difference: {max_diff:.6f}")

# Display NDVI maps and their differences
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Python NDVI
ax[0].imshow(ndvi_python, cmap='RdYlGn', vmin=-1, vmax=1)
ax[0].set_title("NDVI (Python)")
ax[0].axis("off")

# QGIS NDVI
ax[1].imshow(ndvi_qgis, cmap='RdYlGn', vmin=-1, vmax=1)
ax[1].set_title("NDVI (QGIS)")
ax[1].axis("off")

# Difference Map
diff_map = ax[2].imshow(ndvi_diff, cmap="coolwarm", vmin=-0.2, vmax=0.2)
ax[2].set_title("NDVI Difference (Python - QGIS)")
ax[2].axis("off")

# Add colorbar for difference map
fig.colorbar(diff_map, ax=ax[2], shrink=0.6, label="Difference")

plt.tight_layout()
plt.show()

# Plot histogram of differences using Matplotlib (No Seaborn)
plt.figure(figsize=(8, 5))
plt.hist(ndvi_diff.flatten(), bins=50, color="blue", alpha=0.7, edgecolor="black")
plt.axvline(0, color='red', linestyle="dashed", linewidth=1.5)
plt.title("Histogram of NDVI Differences (Python - QGIS)")
plt.xlabel("NDVI Difference")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()
