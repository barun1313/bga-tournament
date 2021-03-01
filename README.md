<b>bgaGames.py</b>

This runs for all the relevant games of the mentioned players and calculates the score. Team Poseidon starts with 1 additional point because of an uncalculated game in BGA.

<b>bga.py</b>

This saves the games, teams and players in a Postgres DB whose table model is present in bga_tables.py



Assumptions for calculating weighted score :
1. All players are equally likely to win a game
2. All games will have a result
3. The distribution of scores of a game is even
4. Normalizing score across final number of games a team has played is possible since each team participates in a decent number of games (a maximum difference of 30 at the moment I write this)

Weighted Score in a Game where team A has won = w(A,gi) = n(gi)/n(A), where gi = game i, n(g) = number of total players in the game, n(A) = number of players of Team A who played

Final Score for Team A = sum (gi) where i=games where team A has won

**Weighted final score for Team A = sum(gi)/n(gA)** where n(gA) = Total games played by Team A

The next step would be to find out distribution of scores possible in a game, chances of draw and multiply that factor to each game to normalize across different types of games as well (for example, what are the chances of having 2 winners instead of 1 in Hearts). In the above mentioned model, we assume there will always be exactly one winner
