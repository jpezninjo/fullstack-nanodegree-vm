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

insert into players (name) values ('chuck'), ('norris'),('garbage');

insert into Matches (Player1, Player2, winner) values (1, 2, 1), (1, 2, 1);