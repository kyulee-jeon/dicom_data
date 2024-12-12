# cdm_extension.py

def match_personid(df, df_person):
    if ("person_id" in df.columns) and ("person_source_value" not in df.columns):
        df = df.rename(columns={"person_id": "person_source_value"})
        df = df.merge(df_person[["person_id", "person_source_value"]], on="person_source_value", how="left")
        return df
    else:
        print("There's no person_id or already have person_source_value")