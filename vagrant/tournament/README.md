#TOURNAMENT DOCUMENTATION
##Instructions:

To use the files contained in this archive, first connect to your postgresql server by typing 'psql' in your terminal. Second, run the tournament.sql file (e.g. '\i tournament.sql') to create the required database and tables, then exit postgresql by entering '\q'. Once you are back on the command line, the test and demonstration files can be ran through python (e.g. 'python tournament_test.py') to validate the tournament database is running and calls to the tournament.py functions are working correctly.

##File Descriptions:

tournament.sql contains the SQL commands to create the database 'tournament' and the two tables required to run the Swiss-style tournament.

tournament.py contains functions to access the tournament tables and determine pairings for each round of the tournament.

Running tournament_test.py will validate that the tournament tables are setup correctly and the tournament.py functions perform the correct operations.

A demonstration of a full Swiss-style tournament can be launched by running tournament_demo.py.

