import discord
import logging
import time
import operator
from src.config import VERSION, PLAYING_STATUS, ADMIN_USER, TOKEN
import src.database as DB

from src.commands.BasicCommands import *
from src.commands.LogsCommands import *
from src.commands import Command


class LogsDiscordBot(discord.Client):
    def set_commands(self, cmds: list):
        self.commands = cmds

    async def sendAdmin(self, message):
        try:
            admin = await self.fetch_user(ADMIN_USER)
            await admin.send(message)
        except Exception as e:
            logging.error(e)
            logging.error("Probably wrong admin id.")

    async def update_playing_status(self):
        # shows the 'playing' status
        game = discord.Activity(
            name=f"{PLAYING_STATUS} | {len(self.guilds)} servers",
            type=discord.ActivityType.listening
        )
        await self.change_presence(status=discord.Status.online, activity=game)

    async def admin_stats(self):
        serverlist = ""
        for server in self.guilds:
            serverlist += f"**{server.name}** `{server.id}` from `{server.region}`"\
                f" with `{len(server.members)}` members.\n"

        stored_users = len(await DB.selectUsers())
        message = f"**Bot online and running.**\n\n Running on `{len(self.guilds)}` servers.\n\n" \
                f"I have `{stored_users}` stored users in my database.\n\n" \
                f"Here is the server list:\n {serverlist}"
        await self.sendAdmin(message)

    async def on_ready(self):
        await DB.init_db()
        logging.info(f'Bot is up and running on version {VERSION}')
        logging.debug(
            f'Bot has the username {self.user.display_name} and the discord id {self.user.id}'
        )

        # showing the UP and RUNNING screen after the bot is ready
        logging.info("[i]  [status] up and running")
        logging.info(f"Running on [version] {VERSION}")
        logging.info(f"Connected as [username] {self.user.display_name}")
        logging.info(f"Bot's [discordid] {self.user.id}")

        # shows the 'playing' status
        await self.update_playing_status()

        # go search if every server is in the database, if not add the server
        for server in self.guilds:
            if not await DB.findServer(server.id):
                await DB.insertServer(server.id, None)
                logging.info('Added server {}, that invited the bot during offtime'.format(server.id))

        await self.admin_stats()

    async def on_guild_join(self, server):
        # save the new server to the database
        logging.info("Bot joined a new server ({})".format(server.id))
        if await DB.insertServer(server.id, None):
            logging.info("Added new server ({}) to the database".format(server.id))

        await self.update_playing_status()

    async def on_guild_remove(self, server):
        logging.info("The server ({}) removed the bot".format(server.id))
        if await DB.delete_server(server.id):
            logging.info("Removed the server ({}) from the database".format(server.id))
        else:
            logging.error("Could not remove the server ({}) from the database".format(server.id))

        await self.update_playing_status()

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return
        for cmd in self.commands:
            if cmd.activator.check(message):
                start = time.time()
                await cmd.handle(message)
                break
                print(time.time() - start)


client = LogsDiscordBot()

print("Gathering commands...")
cmds = Command.__subclasses__()
print(f"Found the following commands: {cmds}")
print("Initializing commands...")
commands = []
for cmd in cmds:
    commands.append(cmd())

commands.sort(key=operator.attrgetter('priority'))
print(commands)
print("Initializing commands [complete]")

client.set_commands(commands)
client.run(TOKEN)
