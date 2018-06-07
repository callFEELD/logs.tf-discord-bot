# Handles essentials to be able to start the bot
# last edit: 21.04.2018 (callFEELD)

from src.classes import ErrorHandler
from src.classes import Commands
from src.classes import Essentials

# Importing third party libraries
import discord                      # accessing the discord.py library
import json                         # used to access the token.json file
import time

LBC = Commands.LogBotCommands()
LBE = Essentials.LogBotEssentials()

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
    time.sleep(0.5)
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