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

