import streamlit as st
import subprocess
import os

# Ensure the directory exists
save_dir = os.path.join(os.getcwd(), "uploaded_tifs")
os.makedirs(save_dir, exist_ok=True)

# Function to run a Python file with multiple file paths as input
def run_python_script(script_name, file_paths):
    try:
        result = subprocess.run(
            ["python", script_name] + file_paths,  # Use "python" instead of "python3" for Windows
            capture_output=True,
            text=True
        )
        return result.stdout, result.stderr
    except Exception as e:
        return str(e), None

# Streamlit UI
st.title("TIF File Upload and Python Script Executor")

# File upload buttons for 4 bands (TIF files)
file1 = st.file_uploader("Upload NIR Band TIF File", type=["tif", "tiff"])
file2 = st.file_uploader("Upload Red Band TIF File", type=["tif", "tiff"])
file3 = st.file_uploader("Upload Green Band TIF File", type=["tif", "tiff"])
file4 = st.file_uploader("Upload Red Edge (RE) Band TIF File", type=["tif", "tiff"])

# Check if files are uploaded
if file1 and file2 and file3 and file4:
    st.write("All files uploaded successfully.")

    # Save the files to disk with new names corresponding to band names
    file_paths = []
    band_names = ["NIR", "Red", "Green", "RE"]
    for file, band in zip([file1, file2, file3, file4], band_names):
        file_path = os.path.join(save_dir, f"{band}.tif")  # Save files in the created directory
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
        file_paths.append(file_path)  # Use absolute path

    # Buttons to run each Python script for NDVI, NDTI, and Chlorophyll Index
    if st.button("Run NDVI Calculation"):
        stdout, stderr = run_python_script("ndvi_script.py", file_paths)
        if stderr:
            st.error(f"Error in NDVI Calculation Script: {stderr}")
        else:
            st.success(f"NDVI Calculation executed successfully: {stdout}")

    if st.button("Run NDTI Calculation"):
        stdout, stderr = run_python_script("ndti_script.py", file_paths)
        if stderr:
            st.error(f"Error in NDTI Calculation Script: {stderr}")
        else:
            st.success(f"NDTI Calculation executed successfully: {stdout}")

    if st.button("Run Chlorophyll Index Calculation"):
        stdout, stderr = run_python_script("chlorophyll_script.py", file_paths)
        if stderr:
            st.error(f"Error in Chlorophyll Calculation Script: {stderr}")
        else:
            st.success(f"Chlorophyll Calculation executed successfully: {stdout}")

else:
    st.warning("Please upload all four files to run the scripts.")
