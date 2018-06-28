# Handles essentials to be able to start the bot
# last edit: 21.04.2018 (callFEELD)

from src.classes import ErrorHandler
from src.classes import Commands
from src.classes import Essentials
from src.classes import database

# Importing third party libraries
import discord                      # accessing the discord.py library
import json                         # used to access the token.json file
import time
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

LBC = Commands.LogBotCommands()
LBE = Essentials.LogBotEssentials()
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
    time.sleep(0.3)
    await discord_client.send_message(message.channel, messagetosend)
    LBE.consoleOutput(message.author.id, message, messagetosend)


@discord_client.event
async def on_ready():
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
    print('starting LogDiscordBot (v.' + LBE.version + ')...')

    # Opening config files and other files
    try:
        # Opening the token file and reading the token
        tokenfile = open("data/cfg/token.json", "r").read()
        tokenjson = json.loads(tokenfile)
        TOKEN = tokenjson["token"]

        #read the config
        configfile = open("data/cfg/config.json", "r").read()
        configjson = json.loads(configfile)
        PLAYING_STATUS = configjson["playing_status"]
    except:
        ErrorHandler.error(1)
        return

    if TOKEN == "":
        ErrorHandler.error(2)
        return

    # connecting the bot to the discord servers
    try:
        discord_client.run(TOKEN)
    except:
        ErrorHandler.error(3)
        return