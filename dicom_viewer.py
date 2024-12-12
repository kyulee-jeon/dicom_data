# dicom_viewer.py

import os
import pydicom
import matplotlib.pyplot as plt

def check_dicom_attributes(fpath, attributes):
    """
    Usage:
    import sys
    sys.path.append('/home/yuhsuser/workspace/kyulee/Codes')
    from dicom_viewer import check_dicom_attributes
    
    dicom_file_path = "example.dcm"
    attributes_to_check = [
        "StudyInstanceUID", "SeriesInstanceUID", "ProtocolName", "ViewPosition", "SeriesDescription"
    ]
    """
    try:
        dcm = pydicom.dcmread(fpath)
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


