import discord
import urllib.request, json


#import Classes
from LogDiscordBot import LogDiscordBot
ldbcommands = LogDiscordBot.LogBotCommands()
ldbessentials = LogDiscordBot.LogBotEssentials()

client = discord.Client()
user = discord.User()

tokenfile = open("token.json", "r").read()
tokenjson = json.loads(tokenfile)

#INSTALL
TOKEN = tokenjson["token"]
USERNAME = "logs.tf"
PLAYING_STATUS = "type !logs help"

print('starting LogDiscordBot (v.'+ldbessentials.version+')...')

# sends message to the channel
# also outputs the message and answer into the console
async def sendMessage(message, messagetosend):
    await client.send_message(message.channel, messagetosend)
    ldbessentials.consoleOutput(message.author.id, message, messagetosend)

@client.event
async def on_ready():
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

client.run(TOKEN)