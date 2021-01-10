from src.commands import Command, ActivatorType, CommandActivator
from src.config import VERSION
import src.users as LDBU


class AddMe(Command):
    activator = CommandActivator(ActivatorType.starts_with, '!logs addme')

    async def logic(self, message):
        # check if only typed: !logs addme
        if message.content.lower() == '!logs addme':
            return \
                ":incoming_envelope:\tYou can get add or update your data. Just type after\t\t"\
                "`!logs addme` <SteamID64>", None
        else:
            splitmessage = message.content.lower().split(' ')
            # check if user already exist and rewrite or add user
            user = await LDBU.get_player(message.author.id)
            if user:
                # grabs users (that has to be added) steam id 64
                addusersteamid64 = splitmessage[2]

                # adds user with discord id and steam id 64
                await LDBU.update_user(message.author.id, addusersteamid64)
                return \
                    f":sparkles:\tUpdated yourself with the SteamID64: {addusersteamid64}", None
            else:
                # grabs users (that has to be added) steam id 64
                addusersteamid64 = splitmessage[2]

                # adds user with discord id and steam id 64
                await LDBU.add_user(message.author.id, addusersteamid64)

                # Outputs Successfull Message
                return \
                    f":sparkles:\tAdded yourself with the SteamID64: {addusersteamid64}", None


class Help(Command):
    activator = CommandActivator(ActivatorType.equals, '!logs help')

    async def logic(self, message):
        modhelp = "`!logs teamhelp` - for every team commands"
        tip = ""

        # if the user is not in the database, advice him to join
        user = await LDBU.get_player(message.author.id)
        if not user:
            tip = ":incoming_envelope: "\
                  "Seems like you are fresh meat. You can level up with `!logs addme <SteamID64>` to add yourself to "\
                  "my database.\n\n", None
        return \
            f"{tip}__**Commands**__" \
            "\n:information_source:\tParts of the commands have this kind of syntax `<teamname>` or `<@name>`. "\
            f"Those meant to be placeholders for your own input.\n\n{modhelp}" \
            "\n\n`!logs` - shows your las!t played match with details about your performance" \
            "\n`!logs profile` - shows your logs.tf profile" \
            "\n\n`!logs <@name>` - shows the last log of the player you looked for" \
            "\n`!logs <@name> profile` - shows the logs.tf profile of the player you looked for" \
            "\n\n`!logs match <teamname>` - shows the latest match (scrim, lobby, official) of a team with details " \
            "about your performance" \
            "\n`!logs teams` - shows the available teams" \
            "\n`!logs teams <teamname> players` - shows the players in the team" \
            f"\n\n`version: {VERSION}`", None


class TeamHelp(Command):
    activator = CommandActivator(ActivatorType.equals, '!logs teamhelp')

    async def logic(self, message):
        return \
            "__**Advanced commands**__" \
            "\n\n`!logs teams create <teamname> <format>` - Creates a new team. Format is the type of " \
            "the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on)." \
            "\n`!logs teams delete <teamname>` - Removes a team from the system." \
            "\n\n`!logs teams add <teamname> <@name> <name> <class>` - Stores a player with a specific name " \
            "into a team." \
            "\n`!logs teams remove <teamname> <@name>` - Removes a player from a team." \
            f"\n\n`version: {VERSION}`", None


class Version(Command):
    activator = CommandActivator(ActivatorType.equals, '!logs version')

    async def logic(self, message):
        return f"`{VERSION}`", None
