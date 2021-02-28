<b>bgaGames.py</b>

This runs for all the relevant games of the mentioned players and calculates the score. Team Poseidon starts with 1 additional point because of an uncalculated game in BGA.

<b>bga.py</b>

This saves the games, teams and players in a Postgres DB whose table model is present in bga_tables.py


Weighted Score in a Game where team A has won = w(A,gi) = n(gi)/n(A), where gi = game i, n(g) = number of total players in the game, n(A) = number of players of Team A who played

Final Score for Team A = sum (gi) where i=games where team A has won

Weighted final score for Team A = sum(gi)/n(gA) where n(gA) = Total games played by Team A
