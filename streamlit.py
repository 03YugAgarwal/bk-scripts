# import streamlit as st
# import subprocess
# import os

# # Ensure directories exist
# save_dir = "uploaded_tifs"
# output_dir = "generated_tifs"
# os.makedirs(save_dir, exist_ok=True)
# os.makedirs(output_dir, exist_ok=True)

# # Function to run processing scripts
# def run_script(script, file_paths, output_tif):
#     result = subprocess.run(["python", script] + file_paths + [output_tif], capture_output=True, text=True)
#     return result.stdout, result.stderr, output_tif

# st.title("TIF File Processing & Download")

# # File uploaders
# file1 = st.file_uploader("Upload NIR Band TIF File", type=["tif"])
# file2 = st.file_uploader("Upload Red Band TIF File", type=["tif"])
# file3 = st.file_uploader("Upload Green Band TIF File", type=["tif"])
# file4 = st.file_uploader("Upload Red Edge (RE) Band TIF File", type=["tif"])

# if file1 and file2 and file3 and file4:
#     st.success("✅ All files uploaded successfully!")

#     # Save uploaded files
#     band_names = ["NIR", "Red", "Green", "RE"]
#     file_paths = []
#     for file, band in zip([file1, file2, file3, file4], band_names):
#         file_path = os.path.join(save_dir, f"{band}.tif")
#         with open(file_path, "wb") as f:
#             f.write(file.getbuffer())
#         file_paths.append(file_path)

#     # Run NDVI
#     ndvi_tif = os.path.join(output_dir, "NDVI_PYTHON.TIF")
#     ndvi_png = os.path.join(output_dir, "NDVI_PYTHON.png")
#     if st.button("Run NDVI"):
#         stdout, stderr, _ = run_script("ndvi_script.py", [file_paths[0], file_paths[1]], ndvi_tif)
#         if stderr:
#             st.error(f"NDVI Error: {stderr}")
#         else:
#             st.success(stdout)
#         if os.path.exists(ndvi_tif):
#             with open(ndvi_tif, "rb") as f:
#                 st.download_button("Download NDVI TIF", f, file_name="NDVI_PYTHON.TIF")
#         if os.path.exists(ndvi_png):
#             st.image(ndvi_png, caption="NDVI", use_column_width=True)

#     # Run NDTI
#     ndti_tif = os.path.join(output_dir, "NDTI_PYTHON.TIF")
#     ndti_png = os.path.join(output_dir, "NDTI_PYTHON.png")
#     if st.button("Run NDTI"):
#         stdout, stderr, _ = run_script("ndti_script.py", [file_paths[0], file_paths[3]], ndti_tif)
#         if stderr:
#             st.error(f"NDTI Error: {stderr}")
#         else:
#             st.success(stdout)
#         if os.path.exists(ndti_tif):
#             with open(ndti_tif, "rb") as f:
#                 st.download_button("Download NDTI TIF", f, file_name="NDTI_PYTHON.TIF")
#         if os.path.exists(ndti_png):
#             st.image(ndti_png, caption="NDTI", use_column_width=True)

#     # Run Chlorophyll Index
#     chlorophyll_tif = os.path.join(output_dir, "CHLOROPHYLL_PYTHON.TIF")
#     chlorophyll_png = os.path.join(output_dir, "CHLOROPHYLL_PYTHON.png")
#     if st.button("Run Chlorophyll Index"):
#         stdout, stderr, _ = run_script("chlorophyll_script.py", [file_paths[0], file_paths[2]], chlorophyll_tif)
#         if stderr:
#             st.error(f"Chlorophyll Error: {stderr}")
#         else:
#             st.success(stdout)
#         if os.path.exists(chlorophyll_tif):
#             with open(chlorophyll_tif, "rb") as f:
#                 st.download_button("Download Chlorophyll Index TIF", f, file_name="CHLOROPHYLL_PYTHON.TIF")
#         if os.path.exists(chlorophyll_png):
#             st.image(chlorophyll_png, caption="Chlorophyll Index", use_column_width=True)

# else:
#     st.warning("⚠️ Please upload all four files to process the data.")
import streamlit as st
import subprocess
import os
import numpy as np
import rasterio
import matplotlib.pyplot as plt

# Ensure directories exist
save_dir = "uploaded_tifs"
output_dir = "generated_tifs"
os.makedirs(save_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Function to run processing scripts
def run_script(script, file_paths, output_tif):
    result = subprocess.run(["python", script] + file_paths + [output_tif], capture_output=True, text=True)
    return result.stdout, result.stderr, output_tif

st.title("TIF File Processing & Download")

# File uploaders
file1 = st.file_uploader("Upload NIR Band TIF File", type=["tif"])
file2 = st.file_uploader("Upload Red Band TIF File", type=["tif"])
file3 = st.file_uploader("Upload Green Band TIF File", type=["tif"])
file4 = st.file_uploader("Upload Red Edge (RE) Band TIF File", type=["tif"])

if file1 and file2 and file3 and file4:
    st.success("✅ All files uploaded successfully!")

    # Save uploaded files
    band_names = ["NIR", "Red", "Green", "RE"]
    file_paths = []
    for file, band in zip([file1, file2, file3, file4], band_names):
        file_path = os.path.join(save_dir, f"{band}.tif")
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        file_paths.append(file_path)

    # Run NDVI
    ndvi_tif = os.path.join(output_dir, "NDVI_PYTHON.TIF")
    ndvi_png = os.path.join(output_dir, "NDVI_PYTHON.png")
    if st.button("Run NDVI"):
        stdout, stderr, _ = run_script("ndvi_script.py", [file_paths[0], file_paths[1]], ndvi_tif)
        if stderr:
            st.error(f"NDVI Error: {stderr}")
        else:
            st.success(stdout)
        if os.path.exists(ndvi_tif):
            with open(ndvi_tif, "rb") as f:
                st.download_button("Download NDVI TIF", f, file_name="NDVI_PYTHON.TIF")
        if os.path.exists(ndvi_png):
            st.image(ndvi_png, caption="NDVI", use_column_width=True)

    # Run NDTI
    ndti_tif = os.path.join(output_dir, "NDTI_PYTHON.TIF")
    ndti_png = os.path.join(output_dir, "NDTI_PYTHON.png")
    if st.button("Run NDTI"):
        stdout, stderr, _ = run_script("ndti_script.py", [file_paths[0], file_paths[3]], ndti_tif)
        if stderr:
            st.error(f"NDTI Error: {stderr}")
        else:
            st.success(stdout)
        if os.path.exists(ndti_tif):
            with open(ndti_tif, "rb") as f:
                st.download_button("Download NDTI TIF", f, file_name="NDTI_PYTHON.TIF")
        if os.path.exists(ndti_png):
            st.image(ndti_png, caption="NDTI", use_column_width=True)

    # Run Chlorophyll Index
    chlorophyll_tif = os.path.join(output_dir, "CHLOROPHYLL_PYTHON.TIF")
    chlorophyll_png = os.path.join(output_dir, "CHLOROPHYLL_PYTHON.png")
    if st.button("Run Chlorophyll Index"):
        stdout, stderr, _ = run_script("chlorophyll_script.py", [file_paths[0], file_paths[2]], chlorophyll_tif)
        if stderr:
            st.error(f"Chlorophyll Error: {stderr}")
        else:
            st.success(stdout)
        if os.path.exists(chlorophyll_tif):
            with open(chlorophyll_tif, "rb") as f:
                st.download_button("Download Chlorophyll Index TIF", f, file_name="CHLOROPHYLL_PYTHON.TIF")
        if os.path.exists(chlorophyll_png):
            st.image(chlorophyll_png, caption="Chlorophyll Index", use_column_width=True)

    # Run Salinity Index
    salinity_tif = os.path.join(output_dir, "SALINITY_INDEX.TIF")
    salinity_png = os.path.join(output_dir, "SALINITY_INDEX.png")
    if st.button("Run Salinity Index"):
        try:
            # Open the Red and Green band TIF files
            with rasterio.open(file_paths[1]) as red_src, rasterio.open(file_paths[2]) as green_src:
                red = red_src.read(1).astype(np.float32)
                green = green_src.read(1).astype(np.float32)
                
                # Calculate Salinity Index = sqrt(Green * Red)
                salinity_index = np.sqrt(green * red)
                
                # Update metadata for output file
                profile = red_src.profile
                profile.update(dtype=rasterio.float32)
                
                # Save the Salinity Index TIF file
                with rasterio.open(salinity_tif, "w", **profile) as dst:
                    dst.write(salinity_index.astype(np.float32), 1)
            
            # Plot and save the PNG image
            plt.figure()
            plt.imshow(salinity_index, cmap="viridis")
            plt.colorbar()
            plt.title("Salinity Index")
            plt.savefig(salinity_png, bbox_inches="tight")
            plt.close()
            
            st.success("Salinity Index calculated successfully!")
        except Exception as e:
            st.error(f"Error calculating Salinity Index: {e}")
        
        if os.path.exists(salinity_tif):
            with open(salinity_tif, "rb") as f:
                st.download_button("Download Salinity Index TIF", f, file_name="SALINITY_INDEX.TIF")
        if os.path.exists(salinity_png):
            st.image(salinity_png, caption="Salinity Index", use_column_width=True)

else:
    st.warning("⚠️ Please upload all four files to process the data.")
