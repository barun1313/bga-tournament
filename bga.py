import requests
import psycopg2
import json
from time import sleep
from random import randint
from wappdriver import WhatsApp

# Connect to a local Postgres DB that stores the games, players info and scores
conn = psycopg2.connect(
    host="localhost",
    database="",
    user="",
    password=""
)

cur = conn.cursor()

# fetch list of all players from the DB
all_players = '''select player_id from players'''
cur.execute(all_players)
gamer_all = cur.fetchall()
gamers = [item[0] for item in gamer_all]

# check last updated game time so that script runs for games past that time
# if no data available, we set date to tournament start time
last_updated_time = cur.execute(
    '''select game_start from games order by game_start desc limit 1''')
last_time = cur.fetchall()
if cur.rowcount == 0:
    script_run_time = 1609942700
else:
    last_updated_unix = [item[0] for item in last_time]
    script_run_time = max(1610029100, last_updated_unix[0]) - 86400

# check last updated game table so that script runs for games past that table
last_updated_table = cur.execute(
    '''select table_id from games order by table_id desc limit 1''')
last_table = cur.fetchall()
if cur.rowcount == 0:
    last_updated_game = [1]
else:
    last_updated_game = [item[0] for item in last_table]

# check games of all Weekend gamers
for gamer in gamers:
    # checks total number of games of the gamer to see how many pages of games need to be fetched
    games_url = "https://boardgamearena.com/gamestats/gamestats/getGames.html?player=" + \
        str(gamer) + "&opponent_id=0&start_date=" + \
        str(script_run_time) + "&finished=1&updateStats=1"
    r = requests.get(games_url)
    games_data = json.loads(r.text)
    games_played = int(games_data['data']['stats']['general']['played'])

    # checks each table for relevance
    for i in range(games_played//10):
        games_page = requests.get(
            "https://boardgamearena.com/gamestats/gamestats/getGames.html?player=" + str(gamer) + "&opponent_id=0&start_date=" + str(script_run_time) + "&finished=1&page=" + str(i+1) + "&updateStats=0")
        page = json.loads(games_page.text)
        tables = page["data"]["tables"]
        for table in tables:
            game_start = int(table["start"])
            game_end = int(table["end"])
            table_id = int(table["table_id"])

            # checks if table exists in DB
            check_if_exists = cur.execute(
                "select table_id from games where table_id=%s", [table_id])

            # if table does not already exist in DB; exlude co-op games
            if cur.rowcount == 0:
                if game_start > script_run_time and table_id > last_updated_game[0] and table["game_id"] not in ("1015", "1181", "1224") and table["unranked"] == "0":
                    players = table["players"].split(',')
                    player_names = table["player_names"].split(',')

                    # check for playing teams
                    playing_teams = set()
                    for player in players:
                        if player in ('88473419', '88658952', '89599720'):
                            playing_teams.add('Hephaestus')
                        elif player in ('85067613', '88627921'):
                            playing_teams.add('Poseidon')
                        elif player in ('88658518', '88794406'):
                            playing_teams.add('Gaia')
                        elif player in ('88627861', '88627920'):
                            playing_teams.add('Zephyrus')

                    # check for at least 3 teams rule
                    if len(playing_teams) > 2:
                        ranks = table["ranks"]
                        count = ranks.count('1')
                        winning_team = set()

                        # check for winning teams
                        for player in players[:count]:
                            if player in ('88473419', '88658952', '89599720'):
                                winning_team.add('Hephaestus')
                            elif player in ('85067613', '88627921'):
                                winning_team.add('Poseidon')
                            elif player in ('88658518', '88794406'):
                                winning_team.add('Gaia')
                            elif player in ('88627861', '88627920'):
                                winning_team.add('Zephyrus')

                        # if there's at least one winner, insert game into DB and update team scores
                        if len(winning_team) > 0:
                            cur.execute("insert into games (table_id, game_id, player_names, winners, game_start, game_end) values (%s, %s, %s, %s, %s, %s) ON CONFLICT (table_id) DO NOTHING", (table_id,
                                                                                                                                                                                                 table["game_id"], player_names, player_names[:count], game_start, game_end))
                            for value in winning_team:
                                if value == 'Hephaestus':
                                    cur.execute(
                                        "update teams set score = score + 1 where team_id=2")
                                elif value == 'Poseidon':
                                    cur.execute(
                                        "update teams set score = score + 1 where team_id=3")
                                elif value == 'Gaia':
                                    cur.execute(
                                        "update teams set score = score + 1 where team_id=1")
                                elif value == 'Zephyrus':
                                    cur.execute(
                                        "update teams set score = score + 1 where team_id=4")
                        else:
                            continue
                    else:
                        continue
                else:
                    continue
            else:
                continue

        # limit number of requests per second
        sleep(randint(2, 3))

# fetch current scores from DB
team_scores = cur.execute(
    '''select team_name, score from teams order by score desc''')
scores = cur.fetchall()
current_score = {}

# prints the score and closes connection to the DB
for a, b in scores:
    current_score[a] = b
print(current_score)
conn.commit()
conn.close()

# opens up WhatsApp web and sends the updated score to the group
with WhatsApp() as bot:
    bot.send('Weekend Gamers',  # name of recipient
             'Here are the updated scores' + \
             str(current_score)  # message
             )

# Hope the best team wins
