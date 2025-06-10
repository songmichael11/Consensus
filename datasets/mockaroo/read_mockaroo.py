import csv
import textwrap

def generate_insert_sql(csv_path, table_name):
  with open("database-files/mockaroo/" + csv_path, newline='', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)

    values = []
    for row in reader:
      formatted_row = []
      for val in row:
        val = val.strip()
        if val == '':
          formatted_row.append('NULL')
        elif val.lower() in ('true', 'false'):
          formatted_row.append(val.lower())
        elif val.replace('.', '', 1).isdigit():
          formatted_row.append(val)
        else:
          # Escape single quotes in string values
          escaped = val.replace("'", "''")
          formatted_row.append(f"'{escaped}'")
      values.append(f"({', '.join(formatted_row)})")

    header_str = ', '.join(headers)
    values_str = ',\n  '.join(values)
    return f"INSERT INTO {table_name} ({header_str}) VALUES\n  {values_str};\n"


def insert_users():
  return generate_insert_sql("Users.csv", "Users")

def insert_posts():
  return generate_insert_sql("Posts.csv", "Posts")

def insert_graphs():
  return generate_insert_sql("Graphs.csv", "Graphs")

def insert_user_questions():
  return generate_insert_sql("UserQuestions.csv", "UserQuestions")

def insert_expert_opinions():
  return generate_insert_sql("ExpertOpinions.csv", "ExpertOpinions")

with open("database-files/02_insert.sql", "w") as f:
    f.write("USE Consensus_DB;\n")
    f.write(insert_users())
    f.write(insert_posts())
    f.write(insert_graphs())
    f.write(insert_user_questions())
    f.write(insert_expert_opinions())

