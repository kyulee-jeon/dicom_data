# search_image_occurrence.py (Only for code storage)    

def return_image_occurrence_dataframe(keyword, value_ls):
    # Measurement
    meas_condition = (measurement_staging['measurement_source_value'] == keyword) & (measurement_staging['value_source_value'].isin(value_ls))
    df_measurement = measurement_staging[meas_condition]
    measurement_ids = df_measurement['measurement_id'].unique()
    #print(len(measurement_ids))

    # Image_feature
    feature_condition = (image_feature_staging['image_feature_event_field_concept_id'] == 1147330) & (image_feature_staging['image_feature_event_id'].isin(measurement_ids))
    df_feature = image_feature_staging[feature_condition]
    occurrence_ids = df_feature['image_occurrence_id'].unique()
    #print(len(occurrence_ids))

    # Image_occurrence
    df_occurrence = image_occurrence_updated[image_occurrence_updated['image_occurrence_id'].isin(occurrence_ids)]
    print(f"df_occurrence: {df_occurrence.shape[0]} rows of {df_occurrence['image_study_uid'].nunique()} studies and {df_occurrence['image_series_uid'].nunique()} series")
    return df_occurrence[['image_occurrence_id', 'person_id', 'image_occurrence_date', 'procedure_unique_id', 'local_path']]


def return_image_occurrence_path(keyword, value):
    df_occurrence = return_image_occurrence_dataframe(keyword, value)
    return df_occurrence['local_path'].unique()


def return_measurement(keyword, value_ls):
    df_occurrence = return_image_occurrence_dataframe(keyword, value_ls)
    occurrence_ids = df_occurrence['image_occurrence_id'].unique()
    
    df_feature = image_feature_staging[image_feature_staging['image_occurrence_id'].isin(occurrence_ids)]
    feature_ids = df_feature['image_feature_event_id'].unique()

    meas_condition = (measurement_staging['measurement_id'].isin(feature_ids))
    df_measurement = measurement_staging[meas_condition]
    print(f"df_measurement: {df_measurement.shape[0]} rows of {df_measurement['person_id'].nunique()} patients")
    return df_measurement[['measurement_id', 'person_id', 'measurement_source_value', 'value_source_value']]


# 특정 key,value만 보고 싶을 때
def return_part_measurement(df_occurrence, keyword, value):
    occurrence_ids = df_occurrence['image_occurrence_id'].unique()
    
    df_feature = image_feature_staging[image_feature_staging['image_occurrence_id'].isin(occurrence_ids)]
    feature_ids = df_feature['image_feature_event_id'].unique()

    meas_condition = (measurement_staging['measurement_id'].isin(feature_ids)) & (measurement_staging['measurement_source_value'] == keyword) & (measurement_staging['value_source_value']==value)
    df_measurement = measurement_staging[meas_condition]
    return df_measurement[['measurement_id', 'person_id', 'measurement_source_value', 'value_source_value']]


def return_measurement_by_image_occurrence_id(image_occurrence_id):
    df_feature = image_feature_staging[image_feature_staging['image_occurrence_id']==image_occurrence_id]
    feature_ids = df_feature['image_feature_event_id'].unique()

    meas_condition = (measurement_staging['measurement_id'].isin(feature_ids))
    df_measurement = measurement_staging[meas_condition]
    return df_measurement[['measurement_id', 'person_id', 'measurement_source_value', 'value_source_value']]

