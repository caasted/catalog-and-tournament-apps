#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")

def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute('delete from matches;')
    cur.execute('update players set matches_played = 0')
    db.commit()
    db.close()

def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    cur = db.cursor()
    cur.execute('delete from players;')
    db.commit()
    db.close()

def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    cur = db.cursor()
    cur.execute('select count(id) from players;')
    numPlayers = cur.fetchall()
    db.close()
    return numPlayers[0][0]

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    cur = db.cursor()
    cur.execute('insert into players (name, matches_played) values (%s, 0);', (name, ))
    db.commit()
    db.close()

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
    db = connect()
    cur = db.cursor()
    cur.execute('select players.id, players.name, players.matches_played, count(matches.winner) as wins from players left join matches on players.id = matches.winner group by players.id order by wins desc;')
    standings = [(int(row[0]), str(row[1]), int(row[3]), int(row[2])) for row in cur.fetchall()]
    db.close()
    return standings

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    cur = db.cursor()
    cur.execute('insert into matches (winner, loser) values ({0}, {1});'.format(winner, loser))
    cur.execute('select matches_played from players where id = {0};'.format(winner))
    cur.execute('update players set matches_played = {0} where id = {1};'.format(int(cur.fetchall()[0][0]) + 1, winner))
    cur.execute('select matches_played from players where id = {0};'.format(loser))
    cur.execute('update players set matches_played = {0} where id = {1};'.format(int(cur.fetchall()[0][0]) + 1, loser))
    db.commit()
    db.close()
 
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
    current_record = playerStandings()
    new_pairings = []
    index = 0;
    while index < len(current_record):
        new_pairings.append((current_record[index][0], current_record[index][1], 
            current_record[index + 1][0], current_record[index + 1][1]))
        index += 2
    return new_pairings
