INSERT INTO Users(Name, PoliticalParty, Bio)
        VALUES
        ("Prince Maximilian William-Lancelot Robertson III", "People's Party of Europe", "I'm British."),
        ("JT Nance", "Democrat Party", "I did NOT kill the pope"),
        ("Emeka Okonkwo", "Green Party", "Hello! I love the economy.")

INSERT INTO Roles(RoleType)
        VALUES
        ("Politician"),
        ("Voter"),
        ("Economist")

INSERT INTO RolesUsers(RoleID, UserID)
        VALUES
        (1, 1),
        (2, 2),
        (3, 3)

INSERT INTO Graphs (
        XAxis, XMin, XMax, XStep,
        Population, GDP_per_capita, Trade_union_density, Unemployment_rate,
        Health, Education, Housing, Community_development,
        Real_interest_rates, Productivity, Corporate_tax_rate, Inflation, Personal_property_tax
        )
        VALUES
        ('GDP per Capita', 0, 100000, 1000, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ('Unemployment Rate', 0, 50, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ('Inflation', 0, 20, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);

INSERT INTO Posts (Title, Description, UserID, GraphID)
        VALUES
        ('Post 1 Title', 'This is the description of Post 1.', 1, 1),
        ('Post 2 Title', 'This is the description of Post 2.', 2, 2),
        ('Post 3 Title', 'This is the description of Post 3.', 3, 3);
