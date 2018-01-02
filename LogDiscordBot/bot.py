# Log Bot
# Description: A discord bot showing your recent logs, profile page and team matches. You can create teams,
#              fill them with players and get recent matches of the teams. You can also search for other
#              persons logs and logs.tf profile's.
#
# creator: callFEELD
#          Website: https://callfeeld.jimdo.com/
#          Steam:   http://steamcommunity.com/id/callFEELD/
#          GitHub:  https://github.com/callFEELD
# Thank you Matthew (GitHub: https://github.com/Matthew-The-Mighty-Mouse-Madge) for the support
# last edit: 02.01.2017 (callFEELD)


# Importing third party libraries
import discord                      # accessing the discord.py library
import urllib.request, json         # used to access the token.json file
import sys, time                    # used to handle errors

# Importing own Classes
from classes import LogDiscordBot
ldbcommands = LogDiscordBot.LogBotCommands()
ldbessentials = LogDiscordBot.LogBotEssentials()


# Defining discord.py vars
client = discord.Client()
user = discord.User()


# function to handle errors
def error(error):
    print('[i]  [status]        ERROR')
    print("     [error type]        "+str(error))
    if error == 1:
        print("     [error msg]         Missing files to run the bot. Make sure you installed everything correct.")

    elif error == 2:
        print("     [error msg]         Couldn't read the token. Please insert the token into the token.json file.")

    elif error == 3:
        print("     [error msg]         Critical Error! Maybe wrong Token!")


    time.sleep(5)
    sys.exit()



# Opening config files and other files
try:
    # Opening the token file and reading the token
    tokenfile = open("token.json", "r").read()
    tokenjson = json.loads(tokenfile)
    TOKEN = tokenjson["token"]

    #read the config
    configfile = open("config.json", "r").read()
    configjson = json.loads(configfile)
    PLAYING_STATUS = configjson["playing_status"]
except:
    error(1)




if TOKEN == "":
    error(2)

# Starting announcement
print('starting LogDiscordBot (v.'+ldbessentials.version+')...')

# sends message to the channel
# also outputs the message and answer into the console
async def sendMessage(message, messagetosend):
    await client.send_message(message.channel, messagetosend)
    ldbessentials.consoleOutput(message.author.id, message, messagetosend)

@client.event
async def on_ready():
    # showing the UP and RUNNING screen after the bot is ready
    print('[i]  [status]        up and running')
    print("     [version]       " + ldbessentials.version)
    print("     [username]      " + client.user.name)
    print("     [discordid]     " + client.user.id + "\n\n")

    # shows the 'playing' status
    await client.change_presence(game=discord.Game(name=PLAYING_STATUS))


@client.event
async def on_message(message):
    # Scan message for LDB commands
    messagetosend = ldbcommands.scan(message)
    if(not messagetosend == None):
        await sendMessage(message, messagetosend)
    messagetosend = None


# connecting the bot to the discord servers
try:
    client.run(TOKEN)
except:
    error(3)