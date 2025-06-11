import pandas as pd

def get_presets():
    megaframe = pd.read_csv("../assets/temp_datasets/MEGAFRAME_CLEANEDV2.csv")
    idx = megaframe.groupby('REF_AREA')['TIME_PERIOD'].idxmax()
    max_rows = megaframe.loc[idx]
    max_rows = pd.get_dummies(max_rows, columns=['Region'], dtype=int)


    PRESETS = {}
    for index, row in max_rows.iterrows():
        dct = dict(row.iloc[3:])
        PRESETS[f"{row['Reference area']} ({row['TIME_PERIOD']})"] = dct
    return PRESETS