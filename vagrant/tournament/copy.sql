-- Table definitions for the tournament project.

DROP TABLE IF EXISTS Players;
DROP TABLE IF EXISTS Matches;

CREATE TABLE Players(
    P_Id  SERIAL PRIMARY KEY,
    Name   varchar(255)
);

CREATE TABLE Matches(
    M_Id  SERIAL PRIMARY KEY,
    Player1   INT NOT NULL,
    Player2   INT NOT NULL,
    Winner   INT
);

insert into players (name) values
    ('Twilight Sparkle'),
    ('Fluttershy'),
    ('Applejack'),
    ('Pinkie Pie'),
    ('"Rarity'),
    ('Rainbow Dash'),
    ('Princess Celestia'),
    ('Princess Luna');

insert into matches (player1, player2, winner) values
(1, 2, 1),
(3, 4, 3),
(5, 6, 5),
(7, 8, 7),
(1, 3, 3),
(5, 7, 5);



SELECT Players.*, COALESCE(NumberOfMatchesWon, 0) as MatchesWon
FROM Players
LEFT OUTER JOIN (
    SELECT Winner AS P_Id, COUNT(*) AS NumberOfMatchesWon
    FROM Matches
    GROUP BY Winner
) AS NumberOfMatchesWonByPlayer USING (P_Id)
ORDER BY MatchesWon DESC;


SELECT Players.*, COALESCE(NumberOfMatchesWon, 0) as MatchesWon
FROM Players
LEFT OUTER JOIN (
    SELECT count(m_id) as P_ID
    FROM matches
    WHERE player1 = P_ID or player2 = P_ID
) AS NumberOfMatchesWonByPlayer USING (P_Id)
ORDER BY MatchesWon DESC;


SELECT Players.*, COALESCE(NumberOfMatchesWon, 0) as MatchesWon
FROM Players
LEFT OUTER JOIN (
    SELECT count(m_id) as P_ID
    FROM matches
) AS NumberOfMatchesWonByPlayer USING (P_Id)
WHERE matches.player1 = P_ID or matches.player2 = P_ID
ORDER BY MatchesWon DESC;


//Good get total matches, does not handle 0
SELECT p_id as player_id, name as player_name, count(p_id)
FROM Players
LEFT OUTER JOIN matches
ON Players.p_id = matches.player1 or Players.p_id = matches.player2
group by p_id
;

SELECT * from

(SELECT Players.*, COALESCE(NumberOfMatchesWon, 0) as MatchesWon
FROM Players
LEFT OUTER JOIN (
    SELECT Winner AS P_Id, COUNT(*) AS NumberOfMatchesWon
    FROM Matches
    GROUP BY Winner
) AS NumberOfMatchesWonByPlayer USING (P_Id)
ORDER BY MatchesWon DESC) as table1

INNER JOIN

(SELECT p_id as player_id, name as player_name, count(p_id)
FROM Players
LEFT OUTER JOIN matches
ON Players.p_id = matches.player1 or Players.p_id = matches.player2
group by p_id order by p_id) as table2
on table1.p_id = table2.player_id
;





SELECT table1.*, table2.count from

(SELECT Players.*, COALESCE(NumberOfMatchesWon, 0) as MatchesWon
FROM Players
LEFT OUTER JOIN (
    SELECT Winner AS P_Id, COUNT(*) AS NumberOfMatchesWon
    FROM Matches
    GROUP BY Winner
) AS NumberOfMatchesWonByPlayer USING (P_Id)
ORDER BY MatchesWon DESC) as table1

INNER JOIN

(SELECT p_id as player_id, name as player_name, count(p_id)
FROM Players
LEFT OUTER JOIN matches
ON Players.p_id = matches.player1 or Players.p_id = matches.player2
group by p_id order by p_id) as table2
on table1.p_id = table2.player_id
;



select p_id, name, count(m_id) as won from players left join matches on players.p_id = matches.winner group by p_id order by won desc;

select p_id, name, count(m_id) as total from players left join matches on players.p_id = matches.player1 or players.p_id = matches.player2 group by p_id order by total desc;

select foo.*, bar.total from
(select p_id, name, count(m_id) as won from players left join matches on players.p_id = matches.winner group by p_id order by won desc) as foo
left outer join
(select p_id, count(m_id) as total from players left join matches on players.p_id = matches.player1 or players.p_id = matches.player2 group by p_id order by total desc) as bar
on foo.p_id = bar.p_id;