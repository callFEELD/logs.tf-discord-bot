# Handles essentials to be able to start the bot
# last edit: 20.02.2019 (callFEELD)

from src.classes.Commands import LogBotCommands
from src.classes.Essentials import LogBotEssentials, consoleOutput
from src.classes.Users import LogBotUsers
from src.classes.Database import DB

from src.handler.logger import logger
from src.handler.config import config

# Importing third party libraries
import discord                      # accessing the discord.py library
import asyncio

DB = DB()
LBU = LogBotUsers(DB)
LBC = LogBotCommands()
LBE = LogBotEssentials(LBU)


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

# sends the admin a private message
async def sendAdmin(message):
    try:
        admin =  await discord_client.get_user_info(config["General"]["admin"])
        await discord_client.send_message(admin, message)
    except Exception as e:
        logger.error(e)
        logger.error("Probably wrong admin id.")
    

async def update_playing_status():
    # shows the 'playing' status
    await discord_client.change_presence(game=discord.Game(name=PLAYING_STATUS + " | {} servers".format(len(discord_client.servers))))

async def admin_stats():
    serverlist = ""
    for server in discord_client.servers:
        serverlist += "**{}** `{}` from `{}` with `{}` members.\n".format(server.name, server.id, server.region, len(server.members))
    
    stored_users = len(DB.selectUsers())
    message = "**Bot online and running.**\n\n" + \
              "Running on `{}` servers.\n\n".format(len(discord_client.servers)) + \
              "I have `{}` stored users in my database.\n\n".format(stored_users) + \
              "Here is the server list:\n {}".format(serverlist)
    await sendAdmin(message)
    


@discord_client.event
async def on_ready():
    logger.info('Bot is up and running on version {}'.format(LBE.version))
    logger.debug('Bot has the username {} and the discord id {}'.format(discord_client.user.name, discord_client.user.id))

    # showing the UP and RUNNING screen after the bot is ready
    logger.info("[i]  [status] up and running")
    logger.info("Running on [version] " + LBE.version)
    logger.info("Connected as [username] " + discord_client.user.name)
    logger.info("Bot's [discordid] " + discord_client.user.id)

    # shows the 'playing' status
    await update_playing_status()

    # go search if every server is in the database, if not add the server
    for server in discord_client.servers:
        if not DB.findServer(server.id):
            DB.insertServer(server.id, None)
            logger.info('Added server {}, that invited the bot during offtime'.format(server.id))
    
    await admin_stats()
    


# If the bot gets connected to a new server
@discord_client.event
async def on_server_join(server):
    # save the new server to the database
    logger.info("Bot joined a new server ({})".format(server.id))
    if DB.insertServer(server.id, None):
        logger.info("Added new server ({}) to the database".format(server.id))
    
    await update_playing_status()
    


# If the bot was removed from a server
@discord_client.event
async def on_server_remove(server):
    logger.infologger.info("The server ({}) removed the bot".format(server.id))
    if DB.delete_server(server.id):
        logger.info("Removed the server ({}) from the database".format(server.id))
    else:
        logger.error("Could not remove the server ({}) from the database".format(server.id))
    
    await update_playing_status()


def run():
    global PLAYING_STATUS
    # Starting announcement
    logger.info('starting LogDiscordBot (v.' + LBE.version + ')...')

    # Opening config files and other files
    try:
        # Opening the token file and reading the token
        
        TOKEN = config["Bot"]["token"]
        PLAYING_STATUS = config["Bot"]["playing_status"]
        logger.debug('read the token')

    except Exception as e:
        logger.error('Missing files to run the bot. Make sure you installed everything correct')
        logger.error(e)
        return

    if TOKEN == "":
        logger.error('Couldn\'t read the token. Please insert the token into the token.json file.')
        return

    # connecting the bot to the discord servers
    try:
        discord_client.run(TOKEN)
    except Exception as e:
        logger.error('Critical Error! Maybe wrong Token!')
        logger.error(e)
        return
