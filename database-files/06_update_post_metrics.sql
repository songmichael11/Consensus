USE Consensus_DB;

UPDATE Posts
SET NumUpvotes = (
  SELECT COUNT(*)
  FROM UpvotesUsers
  WHERE UpvotesUsers.PostID = Posts.PostID
);

UPDATE Posts
SET NumDownvotes = (
  SELECT COUNT(*)
  FROM DownvotesUsers
  WHERE DownvotesUsers.PostID = Posts.PostID
);

UPDATE Posts
SET NumEndorsements = (
  SELECT COUNT(*)
  FROM EndorsementsUsers
  WHERE EndorsementsUsers.PostID = Posts.PostID
);