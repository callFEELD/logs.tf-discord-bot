import configparser
CONFIG_PATH = 'data/cfg/LogDiscordBot.cfg'

config = configparser.ConfigParser()
config.read(CONFIG_PATH)

VERSION = config.get("General", "version")
ADMIN_USER = config.getint("General", "admin")

USERNAME = config.get("Bot", "username")
PLAYING_STATUS = config.get("Bot", "playing_status")
TOKEN = config.get("Bot", "token")

DATABASE_DIR = config.get("Paths", "database")

# Minimum amount of players that a match is defined as a match
# 6s
SIXES_MIN_PLAYERS = config.get("Matches", "sixes_min_players")
# Highlander
HL_MIN_PLAYERS = config.get("Matches", "hl_min_players")
# 4s
FOURS_MIN_PLAYERS = config.get("Matches", "fours_min_players")
# Ultiduo
DUO_MIN_PLAYERS = config.get("Matches", "duo_min_players")
# Amount of logs of a player that will be scanned to get a match
AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER = config.get("Matches", "amount_of_logs_searched_per_player")
