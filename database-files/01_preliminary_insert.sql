Use Consensus_DB;

-- INSERT INTO Users(UserID, Name, PoliticalParty, Bio)
--         VALUES
--         (1, "Prince Maximilian William-Lancelot Robertson III", "People's Party of Europe", "I'm British."),
--         (2, "JT Nance", "Democrat Party", "I did NOT kill the pope"),
--         (3, "Emeka Okonkwo", "Green Party", "Hello! I love the economy.");


-- THE MOCK DATA WE HAVE IS FROM CHATGPT
-- WE ARE GOING TO MOCKAROO DATA AFTER THIS DELIVERABLE

-- INSERT INTO Graphs (
--     XAxis, XMin, XMax, XStep,
--     Population, GDP_per_capita, Trade_union_density, Unemployment_rate,
--     Health, Education, Housing, Community_development,
--     Corporate_tax_rate, Inflation, IRLT,
--     Region_East_Asia_and_Pacific,
--     Region_Europe_and_Central_Asia,
--     Region_Latin_America_and_Caribbean,
--     Region_Middle_East_and_North_Africa
-- )
-- VALUES
--     ('GDP_per_capita', 0, 100000, 10,
--      0, 0, 0, 0,
--      0, 0, 0, 0,
--      0, 0, 0, 
--      0, 0, 0, 0),
     
--     ('Unemployment_rate', 0, 50, 5,
--      0, 0, 0, 0,
--      0, 0, 0, 0,
--      0, 0, 0, 
--      0, 0, 0, 0),
     
--     ('Inflation', 0, 20, 20,
--      0, 0, 0, 0,
--      0, 0, 0, 0,
--      0, 0, 0, 
--      0, 0, 0, 0);


-- INSERT INTO Posts (Title, Description, UserID, GraphID, NumUpvotes, NumDownvotes)
-- VALUES
--     ('Post 1 Title', 'This is the description of Post 1.', 1, 1, 3, 1),
--     ('Post 2 Title', 'This is the description of Post 2.', 2, 2, 2, 2),
--     ('Post 3 Title', 'This is the description of Post 3.', 3, 3, 1, 2),
--     ('Post 4 Title', 'Exploring new policies in healthcare.', 1, 2, 1, 1),
--     ('Post 5 Title', 'Debate on climate change strategies.', 2, 3, 2, 1),
--     ('Post 6 Title', 'Economic impacts of tax reform.', 3, 1, 3, 1),
--     ('Post 7 Title', 'Education reforms for the next decade.', 1, 3, 1, 2),
--     ('Post 8 Title', 'Housing market trends and predictions.', 2, 1, 1, 3),
--     ('Post 9 Title', 'Community engagement and public safety.', 3, 2, 2, 1);

INSERT INTO Roles(RoleType)
        VALUES
        ("Voter"),
        ("Politician"),
        ("Economist");