# ndvi_script.py
import sys
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show

def calculate_ndvi(red_tif, nir_tif, output_ndvi_tif):
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
    plt.title("NDVI Calculation from Red and NIR Bands")
    plt.show()

if __name__ == "__main__":
    # Get the file paths from the command-line arguments
    red_tif, nir_tif, band3_tif, band4_tif = sys.argv[1:5]  # Collect all file paths passed as arguments

    # Generate output NDVI file names based on order
    output_files = []
    for i, band_pair in enumerate([(red_tif, nir_tif), (band3_tif, band4_tif)], start=1):
        red, nir = band_pair
        output_ndvi_tif = f"{i}_PYTHON_NDVI.tif"  # Naming convention: 1_PYTHON_NDVI.tif, 2_PYTHON_NDVI.tif
        output_files.append(output_ndvi_tif)
        
        calculate_ndvi(red, nir, output_ndvi_tif)
    
    print(f"NDVI files saved as: {', '.join(output_files)}")
