import pandas as pd
from datetime import datetime

# Load and rename CSV
df = pd.read_csv("datasets/MEGAFRAME_CLEANEDV2.csv")
df = df.rename(columns={
  "TIME_PERIOD": "Time_period",
  "Reference area": "Reference_area",
  "REF_AREA": "Country_code",
  "Population, total": "Population",
  "GDP per capita (current US$)": "GDP_per_capita",
  "Trade union density": "Trade_union_density",
  "UNEMP": "Unemployment_rate",
  "Health spending": "Health",
  "Education spending": "Education",
  "Housing spending": "Housing",
  "Community development spending": "Community_development",
  "Combined corporate income tax rate": "Corporate_tax_rate",
  "Inflation, consumer prices (annual %)": "Inflation",
  "IRLT": "IRLT",
  "Gini index": "Gini",
  "Region": "Region"
})


# Create insert statement list
insert_statements = []

for _, row in df.iterrows():
  values = (
    int(row["Time_period"]),
    row["Reference_area"].replace("'", "''"),
    row["Country_code"],
    float(row["Population"]),
    float(row["GDP_per_capita"]),
    float(row["Trade_union_density"]),
    float(row["Unemployment_rate"]),
    float(row["Health"]),
    float(row["Education"]),
    float(row["Housing"]),
    float(row["Community_development"]),
    float(row["Corporate_tax_rate"]),
    float(row["Inflation"]),
    float(row["IRLT"]),
    float(row["Gini"]),
    row["Region"].replace("'", "''")
  )

  insert = f"""INSERT INTO TrainingData (
    Time_period, Reference_area, Country_code, Population, GDP_per_capita,
    Trade_union_density, Unemployment_rate, Health, Education, Housing,
    Community_development, Corporate_tax_rate, Inflation, IRLT, Gini,
    Region
  ) VALUES (
    {values[0]}, '{values[1]}', '{values[2]}', {values[3]}, {values[4]},
    {values[5]}, {values[6]}, {values[7]}, {values[8]}, {values[9]},
    {values[10]}, {values[11]}, {values[12]}, {values[13]}, {values[14]},
    '{values[15]}'
  );"""
  
  insert_statements.append(insert)

# Write to file
with open("database-files/07_insert_data_rows.sql", "w") as f:
  f.write("USE Consensus_DB; \n")
  f.write("\n".join(insert_statements))