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
    DB = connect()
    s = DB.cursor()
    s.execute("select games_played from players")
    dele = DB.cursor()
    sector = s.fetchall()
    for rows in sector:
#        print 'the row is ', rows[0]
        dele.execute("update players set games_played = (%s)",(0,))
        dele.execute("update players set wins = (%s)",(0,))
    DB.commit()
    DB.close()    

def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()        
    c.execute("delete from players")
    DB.commit()
    DB.close() 

def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()        
    c.execute("select count(*) from players;")
    result = c.fetchone()[0]
    DB.close()
    return result

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()        
    c.execute("insert into players (player_name,wins,games_played) values (%s,0,0)",(name,))
    DB.commit()
    DB.close()

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
    DB = connect()
    c = DB.cursor()        
    c.execute("select* from rank;")
    result = c.fetchall()
    DB.close()
    return result
    

def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    played = DB.cursor()
    played.execute("select games_played from players where player_id = (%s);", (winner,))
    new_played = played.fetchone()[0] + 1
#    print "Games_played : ", new_played
    winning = DB.cursor()
    winning.execute("select wins from players where player_id = (%s);", (winner,))
    new_winning = winning.fetchone()[0] + 1
#    print "Player wins : ", new_winning    
    c.execute("update players set games_played = (%s) where player_id = (%s);", (new_played, winner,))
    c.execute("update players set games_played = (%s) where player_id = (%s);", (new_played, loser,))
    c.execute("update players set wins = (%s) where player_id = (%s);", (new_winning, winner,))
    DB.commit()
    DB.close()
 
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
    pairings = []
    DB = connect()
    p = DB.cursor()
    p.execute("select count(*) from players;")
    totalplayers = p.fetchone()[0]
    print "TOTAL PLAYERS ARE: ", totalplayers
    person1 = 0
    person2 = person1 + 1
    while person2 < totalplayers:
        roundtup = ()
        p.execute("select player_id, player_name from rank;")
        p1tup = p.fetchall()[person1]
#        print "p1tup = ", p1tup
        p.execute("select player_id, player_name from rank;")        
        p2tup = p.fetchall()[person2]
#        print "p2tup = ", p2tup        
        roundtup = p1tup + p2tup
#        print "ROUNDTUP IS : ", roundtup
        person1 +=2
        person2 +=2
        pairings.append(roundtup)
#    print pairings
    return pairings

