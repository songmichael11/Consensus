import pandas as pd

df = pd.read_csv("ml-src/model_weights.csv")

columns = list(df.columns)
columns_sql = ", ".join(columns)

with open("database-files/02_insert_model_weights.sql", "w") as f:
    for _, row in df.iterrows():
        values = []
        for col in columns:
            val = row[col]
            values.append(str(val))
        values_sql = ", ".join(values)
        insert_stmt = f"INSERT INTO ModelWeights ({columns_sql}) VALUES ({values_sql});\n"
        f.write(insert_stmt)
