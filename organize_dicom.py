# organize_dicom.py

import os
import pandas as pd
import shutil
import argparse

def organize_dicom_files(base_folder, metatable_path):
    """
    Usage in Terminal:
    python organize_dicom.py /path/to/base_folders /path/to/metatable.csv
    """
    
    # Output folder를 base_folder로 설정 (같은 폴더 내에서 이동)
    output_folder = base_folder
    os.makedirs(output_folder, exist_ok=True)

    #1. 메타테이블 로드
    print(f"Loading metatable from {metatable_path}...")
    df = pd.read_csv(metatable_path)

    #2. 필요한 컬럼 확인
    required_columns = ["dcm_fpath", "Study UID", "Series UID"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV 파일에 필요한 컬럼이 없습니다: {required_columns}")
    
    #3. Series Instance UID를 기준으로 파일 이동
    print("Organizing files into Series-level folders...")
    for study_uid, group in df.groupby("Study UID"):
        study_folder = os.path.dirname(group["dcm_fpath"].iloc[0])# Study-level 폴더
        
        for series_uid, series_group in group.groupby("Series UID"):
            series_folder = os.path.join(study_folder, series_uid) # Series-level 하위 폴더
            os.makedirs(series_folder, exist_ok=True)

            # 각 Series UID의 파일들을 해당 폴더로 이동
            for _, row in series_group.iterrows():
                src_path = row["dcm_fpath"]
                if os.path.exists(src_path):
                    dest_path = os.path.join(series_folder, os.path.basename(src_path))
                    shutil.move(src_path, dest_path) # 파일 이동
                else:
                    print(f"File not found: {src_path}")
    print("Series-level 하위 폴더로 그룹핑 및 파일 이동 완료!")


if __name__ =="__main__":
    parser = argparse.ArgumentParser(description="Organize DICOM files into Series-level folders")
    parser.add_argument("base_folder", type=str, help = "Path to the base Study-level folder")
    parser.add_argument("metatable_path", type=str, help= "Path to the metatable CSV files")
    args = parser.parse_args()

    organize_dicom_files(args.base_folder, args.metatable_path)


"""
# 잘 만들어졌나 보기 (Series-folders로 안묶이는 .dcm 들도 있나 보기) 
def find_remaining_dcm_files(base_folder):
    remaining_files = []

    # base_folder의 study-level 폴더만 탐색 =
    for root, dirs, files in os.walk(base_folder):
        if root == base_folder:
            for study_folder in dirs:
                study_path = os.path.join(root, study_folder)
                # study-level 폴더의 하위 파일 및 디렉토리 확인
                for sub_root, sub_dirs, sub_files in os.walk(study_path):
                    if sub_root == study_path: # Series-level 폴더가 아닌 경우만
                        for file in sub_files:
                            if file.endswith(".dcm"):
                                remaining_files.append(os.path.join(root, file))
    return remaining_files

# base_folder path
base_folder = '/home/yuhsuser/workspace/DICOM/(2023300243)1~200_CT/'

remaining_dcm_files = find_remaining_dcm_files(base_folder)
if remaining_dcm_files:
    print(f"남아 있는 .dcm 파일 {len(remaining_dcm_files)}개 발견:")
    #for file in remaining_dcm_files:
        #print(file)
else:
    print("모든 .dcm 파일이 Series-level 폴더로 이동되었습니다!")
"""



"""
# 메타데이터도 업데이트
def update_file_path(row):
    # 기존 file_path에서 Study-level 폴더를 추출
    study_folder = os.path.dirname(row["dcm_fpath"])
    # 새 경로 생성: Study-level 폴더 아래에 Series-level 폴더 추가
    series_path = os.path.join(study_folder, row["Series UID"])
    # 파일 이름 유지
    dcm_fname = os.path.basename(row["dcm_fpath"])
    # Series-level 파일 경로 생성
    updated_path = os.path.join(series_path, dcm_fname) 
    return series_path, dcm_fname, updated_path

# 각 행에 대해 새로운 경로 및 파일 이름 생성
df_series["series_path"], df_series["dcm_fname"], df_series["updated_fpath"] = zip(*df_series.apply(update_file_path, axis=1))
print(df_series.shape)
df_series.head(1)
"""