# ndti_script.py
import sys
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show

def calculate_ndti(re_tif, nir_tif, output_ndti_tif):
    # Open the Red Edge band (extract metadata)
    with rasterio.open(re_tif) as re_src:
        re = re_src.read(1).astype(np.float32)
        transform = re_src.transform  # Preserve georeferencing
        crs = re_src.crs  # Preserve coordinate reference system

    # Open the NIR band
    with rasterio.open(nir_tif) as nir_src:
        nir = nir_src.read(1).astype(np.float32)

        # Ensure both bands have the same shape
        if re.shape != nir.shape:
            raise ValueError("Red Edge (RE) and NIR bands have different dimensions. They must be resampled.")

        # Copy metadata from one of the bands (e.g., RE) to maintain georeferencing
        meta = nir_src.meta.copy()

    # Avoid division by zero errors
    np.seterr(divide='ignore', invalid='ignore')

    # Compute NDTI: (RE - NIR) / (RE + NIR)
    ndti = (re - nir) / (re + nir + 1e-10)  # Adding a small epsilon to avoid division by zero

    # Normalize NDTI values between -1 and 1
    ndti = np.clip(ndti, -1, 1)

    # Ensure the output file retains georeferencing
    meta.update(dtype=rasterio.float32, count=1, transform=transform, crs=crs)

    # Save NDTI as a new GeoTIFF file
    with rasterio.open(output_ndti_tif, "w", **meta) as dst:
        dst.write(ndti, 1)

    # Display NDTI
    plt.figure(figsize=(10, 6))
    plt.imshow(ndti, cmap='RdYlGn')  # Red to Green colormap
    plt.colorbar(label="NDTI Value")
    plt.title("NDTI Calculation from Red Edge and NIR Bands")
    plt.show()

if __name__ == "__main__":
    # Get the file paths from the command-line arguments
    re_tif, nir_tif, band3_tif, band4_tif = sys.argv[1:5]  # Collect all file paths passed as arguments

    # Generate output NDTI file names based on order
    output_files = []
    for i, band_pair in enumerate([(re_tif, nir_tif), (band3_tif, band4_tif)], start=1):
        re, nir = band_pair
        output_ndti_tif = f"{i}_PYTHON_NDTI.tif"  # Naming convention: 1_PYTHON_NDTI.tif, 2_PYTHON_NDTI.tif
        output_files.append(output_ndti_tif)
        
        calculate_ndti(re, nir, output_ndti_tif)
    
    print(f"NDTI files saved as: {', '.join(output_files)}")
