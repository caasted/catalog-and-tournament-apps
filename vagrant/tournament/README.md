# Tournament Project

This project was developed as part of Udacity's Full Stack Web Developer Nanodegree. The project uses postgresql and python to pair competitors and keep match records for a Swiss Style Tournament.

## Quickstart

After cloning the repository to your local machine, connect to your postgresql server by typing `psql` in your terminal. Next, run the tournament.sql file (`\i tournament.sql`) to create the required database and tables, then exit postgresql by entering `\q`. Once you are back on the command line, the test and demonstration files can be ran through python (e.g. `python tournament_test.py`) to validate the tournament database is running and calls to the `tournament.py` functions are working correctly.

## Files:

`tournament.sql` contains the SQL commands to create the database 'tournament' and the two tables required to run the Swiss-style tournament.

`tournament.py` contains functions to access the tournament tables and determine pairings for each round of the tournament.

Running `tournament_test.py` will validate that the tournament tables are setup correctly and the tournament.py functions perform the correct operations.

A demonstration of a full Swiss-style tournament can be launched by running `tournament_demo.py`.

## License

The **/tournament** portion of this repository is free software, and may be redistributed under the terms specified in the [LICENSE](https://github.com/caasted/catalog-and-tournament-apps/blob/master/vagrant/tournament/LICENSE) file.
