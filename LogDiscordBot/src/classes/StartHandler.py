# Handles essentials to be able to start the bot
# last edit: 21.04.2018 (callFEELD)

from src.classes import ErrorHandler
from src.classes import Commands
from src.classes.Essentials import LogBotEssentials, consoleOutput
from src.classes import database

# Importing third party libraries
import discord                      # accessing the discord.py library
import json                         # used to access the token.json file
import asyncio
import logging


logging.basicConfig(level=logging.INFO,
                    format='[%(levelname)s] %(asctime)s - %(message)s',
                    filename='Log.log',
                    filemode='w')
# create logger with 'spam_application'
logger = logging.getLogger('Log-Discord-Bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('Log.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
# create formatter and add it to the handlers
formatter = logging.Formatter('[%(levelname)s] %(asctime)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)


LBC = Commands.LogBotCommands()
LBE = LogBotEssentials()
DB = database.DB()

# Defining discord.py vars
discord_client = discord.Client()
discord_user = discord.User()

PLAYING_STATUS = ""

# Message Handler
@discord_client.event
async def on_message(message):
    # Scan message for LDB commands
    messagetosend = LBC.scan(message)
    if(not messagetosend == None):
        await sendMessage(message, messagetosend)
    messagetosend = None

# sends message to the channel
# also outputs the message and answer into the console
async def sendMessage(message, messagetosend):
    await discord_client.send_typing(message.channel)
    await discord_client.send_message(message.channel, messagetosend)
    consoleOutput(message.author.id, message, messagetosend)


@discord_client.event
async def on_ready():
    logging.info('Bot is up and running on version {}'.format(LBE.version))
    logging.debug('Bot has the username {} and the discord id {}'.format(discord_client.user.name, discord_client.user.id))

    # showing the UP and RUNNING screen after the bot is ready
    print('[i]  [status]        up and running')
    print("     [version]       " + LBE.version)
    print("     [username]      " + discord_client.user.name)
    print("     [discordid]     " + discord_client.user.id + "\n\n")

    # shows the 'playing' status
    await discord_client.change_presence(game=discord.Game(name=PLAYING_STATUS))

    # go search if every server is in the database, if not add the server
    for server in discord_client.servers:
        if not DB.findServer(server.id):
            DB.insertServer(server.id, None)
            logging.info('Added server {}, that invited the bot during offtime'.format(server.id))
            print("added missing server in the database: " + server.id)

    print(DB.selectServers())

# If the bot gets connected to a new server
@discord_client.event
async def on_server_join(server):
    # save the new server to the database
    print("new server join: " + server.id)
    if DB.insertServer(server.id, None):
        print("Connected to a new server: " + server.id)

def run():
    global PLAYING_STATUS
    # Starting announcement
    logging.info('starting LogDiscordBot...')
    print('starting LogDiscordBot (v.' + LBE.version + ')...')

    # Opening config files and other files
    try:
        # Opening the token file and reading the token
        tokenfile = open("data/cfg/token.json", "r").read()
        tokenjson = json.loads(tokenfile)
        TOKEN = tokenjson["token"]
        logging.debug('read the token')

        #read the config
        configfile = open("data/cfg/config.json", "r").read()
        configjson = json.loads(configfile)
        PLAYING_STATUS = configjson["playing_status"]
        logging.debug('read the config')
    except Exception as e:
        ErrorHandler.error(1)
        logging.error('Missing files to run the bot. Make sure you installed everything correct')
        logging.error(e)
        return

    if TOKEN == "":
        ErrorHandler.error(2)
        logging.error('Couldn\'t read the token. Please insert the token into the token.json file.')
        return

    # connecting the bot to the discord servers
    try:
        discord_client.run(TOKEN)
    except:
        ErrorHandler.error(3)
        logging.error('Critical Error! Maybe wrong Token!')
        return