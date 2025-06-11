import random

def generate_bridge_inserts(table_name, user_range, post_range, min_votes=1, max_votes=20):
  user_ids = list(range(user_range[0], user_range[1] + 1))
  statements = [f"INSERT INTO {table_name} (UserID, PostID) VALUES"]
  values = []

  for post_id in range(post_range[0], post_range[1] + 1):
    num_votes = random.randint(min_votes, max_votes)
    voters = random.sample(user_ids, min(num_votes, len(user_ids)))
    for user_id in voters:
      values.append(f"  ({user_id}, {post_id})")

  sql = ",\n".join(values) + ";"
  statements.append(sql)
  return "\n".join(statements)

def insert_upvotes():
  return generate_bridge_inserts(table_name="UpvotesUsers",
                                 user_range=(1,18),
                                 post_range=(1,80),
                                 min_votes=0,
                                 max_votes=20
                                 )

def insert_downvotes():
  return generate_bridge_inserts(table_name="DownvotesUsers",
                                 user_range=(1,18),
                                 post_range=(1,80),
                                 min_votes=0,
                                 max_votes=10
                                 )
def insert_endorsements():
  return generate_bridge_inserts(table_name="EndorsementsUsers",
                                 user_range=(7,12),
                                 post_range=(1,80),
                                 min_votes=0,
                                 max_votes=10
                                 )
def insert_bookmarks():
  return generate_bridge_inserts(table_name="BookmarkedUsers",
                                 user_range=(1,18),
                                 post_range=(1,80),
                                 min_votes=0,
                                 max_votes=10
                                 )

with open("database-files/05_insert_bridge.sql", "w") as f:
    f.write("USE Consensus_DB;\n")
    f.write(insert_upvotes())
    f.write(insert_downvotes())
    f.write(insert_endorsements())
    f.write(insert_bookmarks())
