#!/usr/bin/env python
#
# Demonstration for tournament.py
#

from tournament import *

def start_tournament():
    """
    Initializes a Swiss-style tournament demonstration. Largely based on the provided tournament_test.py file.
    """
    deleteMatches()
    deletePlayers()
    registerPlayer("Twilight Sparkle")
    registerPlayer("Fluttershy")
    registerPlayer("Applejack")
    registerPlayer("Pinkie Pie")
    registerPlayer("Rarity")
    registerPlayer("Rainbow Dash")
    registerPlayer("Princess Celestia")
    registerPlayer("Princess Luna")

def play_round(round_num):
    """
    Continues an existing Swiss-style tournament.
    """
    standings = playerStandings()
    # print standings
    [id1, id2, id3, id4, id5, id6, id7, id8] = [row[0] for row in standings]
    pairings = swissPairings()
    print '\nRound {0} pairings (Player A ID, Player A Name, Player B ID, Player B Name):'.format(round_num)
    print pairings
    reportMatch(id1, id2)
    reportMatch(id3, id4)
    reportMatch(id5, id6)
    reportMatch(id7, id8)

if __name__ == '__main__':
    start_tournament()
    for round_number in range(1, 4):
        play_round(round_number)
    print "\nTournament finished! Final standings (Player ID, Name, Wins, Total Matches):"
    print playerStandings()
