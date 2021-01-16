import psycopg2

# connect to the Postgres DB
conn = psycopg2.connect(
    host="localhost",
    database="",  # enter your DB credentials here
    user="",  # enter your user credentials here
    password=""
)

print("DB connected successfully")

# Relevant Table Models: players, teams and games
commands = ("""CREATE TABLE games
(
    table_id INT PRIMARY KEY NOT NULL,
    game_id INT NOT NULL,
    player_names TEXT NOT NULL,
    winners TEXT NOT NULL,
    game_start BIGINT default 0,
    game_end BIGINT default 0
)
""",
            """CREATE TABLE players
(
    player_id INT NOT NULL,
    player_name TEXT NOT NULL,
    team_id INT NOT NULL,
    PRIMARY KEY (player_id, team_id)
)
""",
            """CREATE TABLE teams
(
    team_id INT PRIMARY KEY NOT NULL,
    team_name TEXT NOT NULL,
    score INT DEFAULT 0
)
""")

cur = conn.cursor()

for command in commands:
    cur.execute(command)

cur.close()
conn.commit()
conn.close()
