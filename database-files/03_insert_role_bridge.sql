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
  -- Add User role (RoleID = 4) for all Voters (7–12)
  (4, 1),
  (4, 2),
  (4, 3),
  (4, 4),
  (4, 5),
  (4, 6),
  -- Add User role (RoleID = 4) for all Politicians (7–12)
  (4, 7),
  (4, 8),
  (4, 9),
  (4, 10),
  (4, 11),
  (4, 12),
  -- Add Voter role (RoleID = 4) for all Economists (13–18)
  (4, 13),
  (4, 14),
  (4, 15),
  (4, 16),
  (4, 17),
  (4, 18);
