# chlorophyll_script.py
import sys
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from rasterio.plot import show

def calculate_chlorophyll(red_tif, green_tif, output_chlorophyll_tif):
    # Open the Red band (extract metadata)
    with rasterio.open(red_tif) as red_src:
        red = red_src.read(1).astype(np.float32)
        transform = red_src.transform  # Preserve georeferencing
        crs = red_src.crs  # Preserve coordinate reference system

    # Open the Green band
    with rasterio.open(green_tif) as green_src:
        green = green_src.read(1).astype(np.float32)

        # Ensure both bands have the same shape
        if red.shape != green.shape:
            raise ValueError("Red and Green bands have different dimensions. They must be resampled.")

        # Copy metadata from one of the bands (e.g., Red) to maintain georeferencing
        meta = green_src.meta.copy()

    # Compute Chlorophyll Index: (Green - Red) / (Green + Red)
    chlorophyll = (green - red) / (green + red + 1e-10)  # Adding a small epsilon to avoid division by zero

    # Normalize Chlorophyll values between -1 and 1
    chlorophyll = np.clip(chlorophyll, -1, 1)

    # Ensure the output file retains georeferencing
    meta.update(dtype=rasterio.float32, count=1, transform=transform, crs=crs)

    # Save Chlorophyll Index as a new GeoTIFF file
    with rasterio.open(output_chlorophyll_tif, "w", **meta) as dst:
        dst.write(chlorophyll, 1)

    # Display Chlorophyll Index
    plt.figure(figsize=(10, 6))
    plt.imshow(chlorophyll, cmap='YlGn')  # Green to Yellow colormap
    plt.colorbar(label="Chlorophyll Index")
    plt.title("Chlorophyll Index Calculation")
    plt.show()

if __name__ == "__main__":
    # Get the file paths from the command-line arguments
    red_tif, green_tif, band3_tif, band4_tif = sys.argv[1:5]  # Collect all file paths passed as arguments

    # Generate output Chlorophyll Index file names based on order
    output_files = []
    for i, band_pair in enumerate([(red_tif, green_tif), (band3_tif, band4_tif)], start=1):
        red, green = band_pair
        output_chlorophyll_tif = f"{i}_PYTHON_CHLOROPHYLL.tif"  # Naming convention: 1_PYTHON_CHLOROPHYLL.tif
        output_files.append(output_chlorophyll_tif)
        
        calculate_chlorophyll(red, green, output_chlorophyll_tif)
    
    print(f"Chlorophyll Index files saved as: {', '.join(output_files)}")
