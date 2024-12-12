# dicom_code_sequence.py

import pydicom
import pandas as pd

def extract_code_sequence(fpath, sequence_name):
    """
    Usage:
    import sys
    sys.path.append('/home/yuhsuser/workspace/kyulee/Codes')
    
    Parameters:
    - fpath: str, path to the DICOM file.
    - sequence_name: str, name of the DICOM sequence to extract data from (e.g., 'ViewCodeSequence').
    """
    try: 
        dcm = pydicom.dcmread(fpath, stop_before_pixels = True)
        if hasattr(dcm, sequence_name) and getattr(dcm, sequence_name, None):
            sequence = getattr(dcm, sequence_name)
            return [
                {
                    "fpath": fpath,
                    "CodeValue": getattr(item, "CodeValue", "N/A"),
                    "CodeSchemeDesignator": getattr(item, "CodeSchemeDesignator", "N/A"),
                    "CodeMeaning": getattr(item, "CodeMeaning", "N/A")
                }
                for item in sequence
            ]
        else:
            return [
                {"fpath": fpath, "CodeValue": "N/A", "CodeSchemeDesignator": "N/A", "CodeMeaning": "N/A"}
            ]
    except Exception as e:
        return [
            {"fpath": fpath, "CodeValue": "N/A", "CodeSchemeDesignator": "N/A", "CodeMeaning": "N/A"}
        ]

def create_code_sequence_dataframe(fpaths, sequence_name):
    """
    Usage:
    from dicom_code_sequence import create_code_sequence_dataframe
    file_paths = ["file1.dcm", "file2.dcm"] # List of DICOM file paths
    sequence_name = "ViewCodeSequence" # Name of the sequence to extract
    df = create_code_sequence_dataframe(file_paths, sequence_name)
    """
    data = []
    for fpath in fpaths:
        data.extend(extract_code_sequence(fpath, sequence_name))
    return pd.DataFrame(data)