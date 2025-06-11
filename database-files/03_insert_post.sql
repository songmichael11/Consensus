Use Consensus_DB

INSERT INTO RolesUsers (RoleID, UserID) VALUES
  -- Voters (initial 6 users)
  (1, 1),
  (1, 2),
  (1, 3),
  (1, 4),
  (1, 5),
  (1, 6),
  -- Politicians (7–12)
  (2, 7),
  (2, 8),
  (2, 9),
  (2, 10),
  (2, 11),
  (2, 12),
  -- Economists (13–18)
  (3, 13),
  (3, 14),
  (3, 15),
  (3, 16),
  (3, 17),
  (3, 18),
  -- Add Voter role (RoleID = 1) for all Politicians (7–12)
  (1, 7),
  (1, 8),
  (1, 9),
  (1, 10),
  (1, 11),
  (1, 12),
  -- Add Voter role (RoleID = 1) for all Economists (13–18)
  (1, 13),
  (1, 14),
  (1, 15),
  (1, 16),
  (1, 17),
  (1, 18);

-- INSERT INTO UpvotesUsers (UserID, PostID)
-- VALUES
--     (1, 1),
--     (2, 1),
--     (3, 1),  -- Post 1 → 3 upvotes    

--     (1, 2),
--     (3, 2),  -- Post 2 → 2 upvotes

--     (2, 3),  -- Post 3 → 1 upvote

--     (1, 4),  -- Post 4 → 1 upvote

--     (2, 5), (3, 5),  -- Post 5 → 2 upvotes

--     (1, 6), (2, 6), (3, 6),  -- Post 6 → 3 upvotes

--     (1, 7),  -- Post 7 → 1 upvote

--     (3, 8),  -- Post 8 → 1 upvote

--     (1, 9), (2, 9);  -- Post 9 → 2 upvotes

-- INSERT INTO DownvotesUsers (UserID, PostID)
-- VALUES
--     (2, 1),  -- Post 1 → 1 downvote

--     (1, 2), (3, 2),  -- Post 2 → 2 downvotes

--     (1, 3), (2, 3),  -- Post 3 → 2 downvotes

--     (3, 4),  -- Post 4 → 1 downvote

--     (2, 5),  -- Post 5 → 1 downvote

--     (1, 6),  -- Post 6 → 1 downvote

--     (2, 7), (3, 7),  -- Post 7 → 2 downvotes

--     (1, 8), (2, 8), (3, 8),  -- Post 8 → 3 downvotes

--     (3, 9);  -- Post 9 → 1 downvote


-- INSERT INTO BookmarkedUsers (UserID, PostID)
-- VALUES
--     (1, 1),  -- Prince bookmarked Post 1
--     (1, 4),  -- Prince bookmarked Post 4
--     (1, 6),  -- Prince bookmarked Post 6

--     (2, 2),  -- JT bookmarked Post 2
--     (2, 5),  -- JT bookmarked Post 5
--     (2, 9),  -- JT bookmarked Post 9

--     (3, 3),  -- Emeka bookmarked Post 3
--     (3, 7),  -- Emeka bookmarked Post 7
--     (3, 8);  -- Emeka bookmarked Post 8

