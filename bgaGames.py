import requests
import json
from time import sleep
from random import randint

# Initial scores (Poseidon starts with 1 because of an abandoned game)
Hephaestus_score, Poseidon_score, Gaia_score, Zephyrus_score = 0, 1, 0, 0

# Update Valid Games in this Dict
Valid_Games = {}

# List of Gamers included
gamers = ['88473419', '88658952', '89599720', '85067613',
          '88627921', '88658518', '88794406', '88627861', '88627920']

# Tournament start time
tournament_start = 1610029100

# Go through all the games post tournament start time
for gamer in gamers:
    games_url = "https://boardgamearena.com/gamestats/gamestats/getGames.html?player=" + \
        str(gamer) + "&opponent_id=0&start_date=1609871400&finished=1&updateStats=1"
    r = requests.get(games_url)
    games_data = json.loads(r.text)
    # calculate number of games played by this gamer after tournament start time
    games_played = int(games_data['data']['stats']['general']['played'])

    # go through each page of games; each page has 10 games
    for i in range(games_played//10):
        games_page = requests.get(
            "https://boardgamearena.com/gamestats/gamestats/getGames.html?player=" + str(gamer) + "&opponent_id=0&start_date=1609871400&finished=1&page=" + str(i+1) + "&updateStats=0")
        page = json.loads(games_page.text)
        tables = page["data"]["tables"]
        for table in tables:
            game_time = int(table["start"])

            # exclude co-op games
            if game_time > tournament_start and table["game_id"] not in ("1015", "1181", "1224"):
                table_id = table["table_id"]

                # if table exists in Dict, ignore table
                if table_id in Valid_Games.keys():
                    continue
                else:
                    players = table["players"].split(',')
                    player_names = table["player_names"].split(',')
                    playing_teams = set()

                    # check which teams are playing
                    for player in players:
                        if player in ('88473419', '88658952', '89599720'):
                            playing_teams.add('Hephaestus')
                        elif player in ('85067613', '88627921'):
                            playing_teams.add('Poseidon')
                        elif player in ('88658518', '88794406'):
                            playing_teams.add('Gaia')
                        elif player in ('88627861', '88627920'):
                            playing_teams.add('Zephyrus')

                    # only consider if three or more playing teams
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

                        # update Dict if there is at least one winning team
                        if len(winning_team) > 0:
                            for player_name in player_names[:count]:
                                Valid_Games[table_id] = [table["game_name"]]
                                Valid_Games[table_id].append(player_name)

                            # add 1 score to winning team
                            for value in winning_team:
                                if value == 'Hephaestus':
                                    Hephaestus_score += 1
                                elif value == 'Poseidon':
                                    Poseidon_score += 1
                                elif value == 'Gaia':
                                    Gaia_score += 1
                                elif value == 'Zephyrus':
                                    Zephyrus_score += 1
                        else:
                            continue
            else:
                continue

        sleep(randint(2, 3))


print("Hephaestus_score", Hephaestus_score)
print("Poseidon_score", Poseidon_score)
print("Gaia_score", Gaia_score)
print("Zephyrus_score", Zephyrus_score)

print(Valid_Games)
