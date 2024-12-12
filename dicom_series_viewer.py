# dicom_series_viewer.py

import os
import pydicom
import matplotlib.pyplot as plt

def check_dicom_in_series(series_folder_path, attributes, max_files = 5):
    """
    Reads up to 'max_files' DICOM files from a given Series-level folder,
    Display attributes and the image.

    Parameters:
        - series_to_folder_path (str): Path to the SEries-level folder.
        - attribute (list): List of DICOM attributes to check.
        - max_files (int): Maximum number of files to display (default: 5)
    """
    # List all .dcm files in the series folder
    dcm_files = [f for f in os.listdir(series_folder_path) if f.endswith(".dcm")]

    if not dcm_files:
        print(f"No DICOM files found in {series_folder_path}")
        return

    # Process up to 'max_files'
    for dcm_file in dcm_files[:max_files]:
        fpath = os.path.join(series_folder_path, dcm_file)
        print(f"\nProcessing DICOM file: {fpath}")

        try:
            # Read DICOM file
            dcm = pydicom.dcmread(fpath)
            
            # Display attributes
            for attr in attributes:
                if hasattr(dcm, attr):
                    value = getattr(dcm, attr, "N/A")
                    print(f"{attr}: {value}")
                else:
                    print(f"{attr}: Attribute not found")
                    
            # Display the DICOM image 
            if hasattr(dcm, "pixel_array"):
                img = dcm.pixel_array
                plt.figure(figsize=(4,4))
                plt.imshow(img, cmap = 'gray')
                plt.title(f"DICOM Image: {os.path.basename(fpath)}")
                plt.axis('off')
                plt.show()
            else:
                print("No pixel data found in this DICOM file.")
                
        except Exception as e:
            print(f"Error reading file {fpath}: {e}")

## View Full Metadata
#dcm_path_1 = os.path.join(series_folder_path, os.listdir(series_folder_path)[0])
#pydicom.dcmread(dcm_path_1)