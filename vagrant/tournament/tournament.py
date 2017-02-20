#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
import bleach

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def showPlayers():
    conn = connect()
    cur = connect().cursor()
    cur.execute("SELECT * FROM Players;")
    print(cur.fetchall())
    conn.close()
    
def showMatches():
    conn = connect()
    cur = connect().cursor()
    cur.execute("SELECT * FROM Matches;")
    print(cur.fetchall())
    conn.close()
    
def deleteMatches():
    """Remove all the match records from the database."""
    conn = connect()
    cur = conn.cursor()    
    cur.execute("DROP TABLE IF EXISTS Matches;")
    cur.execute("""CREATE TABLE Matches(
        M_Id  SERIAL PRIMARY KEY,
        Player1   INT NOT NULL,
        Player2   INT NOT NULL,
        Winner   INT
    );""")
    conn.commit()

def deletePlayers():
    """Remove all the player records from the database."""
    conn = connect()
    cur = conn.cursor()    
    cur.execute("DROP TABLE IF EXISTS Players;") 
    cur.execute("""CREATE TABLE Players(
        P_Id  SERIAL PRIMARY KEY,
        Name   varchar(255)
    );""")
    conn.commit()
    
def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cur = connect().cursor()
    cur.execute("SELECT COUNT(*) FROM Players;")
    t = cur.fetchall()[0][0]
    conn.close()
    return t

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    name = bleach.clean(name)
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Players (Name) values (%s);", (name,))
    conn.commit()

def totalMatchesForPlayer(player_id):
    conn = connect()
    cur = connect().cursor()
    cur.execute("select count(m_id) from matches where player1 = %s or player2 = %s;", (player_id, player_id,));
    t = cur.fetchone()[0]
    conn.close()
    return t
    
def totalWins(player_id):
    conn = connect()
    cur = connect().cursor()
    cur.execute("SELECT count(m_id) FROM Matches where winner = %s;", (player_id,));
    t = cur.fetchone()[0]
    conn.close()
    return t
    
def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    conn = connect()
    cur = connect().cursor()

#    cur.execute("""
#        SELECT table1.*, table2.count from
#        (SELECT Players.*, COALESCE(NumberOfMatchesWon, 0) as MatchesWon
#        FROM Players
#        LEFT OUTER JOIN (
#            SELECT Winner AS P_Id, COUNT(*) AS NumberOfMatchesWon
#            FROM Matches
#            GROUP BY Winner
#        ) AS NumberOfMatchesWonByPlayer USING (P_Id)
#        ORDER BY MatchesWon DESC) as table1
#        INNER JOIN
#        (SELECT p_id as player_id, name as player_name, count(p_id)
#        FROM Players
#        LEFT OUTER JOIN matches
#        ON Players.p_id = matches.player1 or Players.p_id = matches.player2
#        group by p_id order by p_id) as table2
#        on table1.p_id = table2.player_id
#        ;             
#        """)
    cur.execute("""
        select foo.*, bar.total from
        (select p_id, name, count(m_id) as won from players left join matches on players.p_id = matches.winner group by p_id order by won desc) as foo
        left outer join
        (select p_id, count(m_id) as total from players left join matches on players.p_id = matches.player1 or players.p_id = matches.player2 group by p_id order by total desc) as bar
        on foo.p_id = bar.p_id;
    """)
    standings = cur.fetchall()
    
    conn.close()
    return standings

    
def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner = bleach.clean(winner)
    loser = bleach.clean(loser)
    
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO Matches (Player1, Player2, Winner) VALUES (%s, %s, %s);", (winner, loser, winner,))
    conn.commit()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn = connect()
    cur = connect().cursor()
    conn.close()
    
    l = []
    id1 = None
    name1 = None
    standings = playerStandings()
    for i in range(len(standings)):
        player = standings[i]
        if i % 2:
            l.append((id1, name1, player[0], player[1]))
        else:
            id1 = player[0]    
            name1 = player[1]
    return l


