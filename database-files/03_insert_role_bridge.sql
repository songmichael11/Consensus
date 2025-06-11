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
