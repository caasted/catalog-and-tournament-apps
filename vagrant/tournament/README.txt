TOURNAMENT DOCUMENTATION
########################
Instructions:

To use the files contained in this archive your postgresql server must first be running a database named "tournament". Then you must connect to your tournament database and run the tournament.sql file (e.g. '\i tournament.sql') to create the appropriate tables. After the tables have been created, the test and demonstration files can be ran through python (e.g. 'python tournament_test.py').

########################
File Descriptions:

tournament.sql contains the SQL commands to create the two tables required to run the Swiss-style tournament.

tournament.py contains functions to access the tournament tables and determine pairings for each round of the tournament.

Running tournament_test.py will validate that the tournament tables are setup correctly and the tournament.py functions perform the correct operations.

A demonstration of a full Swiss-style tournament can be launched by running tournament_demo.py.

