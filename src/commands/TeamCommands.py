from src.commands import Command, ActivatorType, CommandActivator, CommandPriority
import src.teams as LDBT
import src.users as LDBU
from src import findMatch


class Teams(Command):
    activator = CommandActivator(ActivatorType.equals, '!logs teams')

    async def logic(self, message):
        teams = await LDBT.get_teams(message.guild.id)
        if teams:
            all_teams_str = ""
            for team in teams:
                all_teams_str += f"{team['name']} | `{team['type']}`\t\t"

            return f":busts_in_silhouette:\t**Teams**\n" \
                   f"Here are all teams I stored on this Discord server:\n\n" \
                   f"{all_teams_str}", None
        else:
            return f":busts_in_silhouette:\t**Teams**\n" \
                   "There aren't any teams at the moment. You can create one with the " \
                   "command `!logs teams create <teamname> <format>`", None


class TeamsPlayers(Command):
    activator = CommandActivator(ActivatorType.starts_with, '!logs teams')
    priority = CommandPriority.medium_low

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        team = await LDBT.get_team(message.guild.id, split_msg[2])
        if team:
            # check if the teams have players, else create a tip to add them
            player_str = ""
            if len(team["players"]) > 0:
                for player in team["players"]:
                    player_str += f"{player['name']} | `{player['class']}`\t\t"
            else:
                player_str = \
                    f"No players inside the team.\n" \
                    f":bulb:\tYou can add players to the team with the command\t\t" \
                    f"`!logs teams add {split_msg[2]} <@name> <name> <class>`"

            return f":space_invader:\t**Team: '{team['name']}' player's**\n" \
                   f"(amount: {len(team['players'])})\n\n" \
                   f"{player_str}", None

        return ":warning:\tThis team does not exist", None


class TeamsCreate(Command):
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs teams create'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        # if only typed: !logs teams create
        if message.content.lower() == '!logs teams create':
            return ":incoming_envelope:\tYou can create a team by typing:\t\t" \
                   "`!logs teams create` <teamname> <format>", None

        # check if the command is correct
        if len(split_msg) >= 5:
            name = split_msg[3]
            c_type = split_msg[4]
            creator = message.author.id
            # check if the teamname already exists
            team = await LDBT.get_team(message.guild.id, name)
            if team is None:
                # Check if last value is an int
                try:
                    _ = int(c_type)
                    # create a new team (teamname, type)
                    await LDBT.create_team(
                        message.guild.id, name, c_type, creator
                    )

                    return \
                        f":sparkles:\tSuccessfully created the team **{name}**"\
                        f" with the format: {c_type}", None
                except ValueError:
                    # If type isn't a number
                    return ":no_entry_sign:\tThe format has to be a integer "\
                            "(6 = 6v6, 9 = 9v9 and so on)", None

            else:
                return ":warning:\tThis team already exists.", None

        return ":bulb:\tYou have to add the teams format " \
                "(6 = 6v6, 9 = 9v9 and so on) after\t\t" \
                "`!logs teams create <teamname> <format>`", None


class TeamsDelete(Command):
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs teams delete'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        # check if only !logs teams delete was typed
        if message.content.lower() == '!logs teams delete':
            return ":incoming_envelope:\tYou can delete a team by typing\t\t`" \
                   "!logs teams delete` <teamname>", None

        # if teamname is missing
        elif len(split_msg) < 4:
            return ":bulb:\tYou have to add the teamname", None

        elif len(split_msg) >= 4:
            # Check if team even exists
            team = await LDBT.get_team(message.guild.id, split_msg[3])

            if team:
                if str(team["creator"]) == str(message.author.id):
                    # deletes team (teamname)
                    await LDBT.delete_team(
                        message.guild.id,
                        split_msg[3]
                    )
                    return \
                        ":new_moon_with_face:\t"\
                        f"Deleted your team **{split_msg[3]}**", None
                else:
                    return ":warning:\tThis isn't your team.", None

            return ":warning:\tThis team does not exist.", None


class TeamsAddPlayer(Command):
    """
    This command adds a user into a team.

    Example:
        !logs teams add @callFEELD <teamname>
    Result:
        @callFEELD is now part of the team called <teamname>
    """
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs teams add'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        # check if he only typed: !logs teams add
        if message.content.lower() == '!logs teams add':
            return ":bulb:\tYou can add or update a player to/of a team by typing " \
                    "`!logs teams add <@player> <teamname>`", None

        team = await LDBT.get_team(message.guild.id, split_msg[4])
        if team is None:
            return ":warning:\tThis team does not exist.", None

        # check if the message author is not the team creator
        if str(message.author.id) != str(team["creator"]):
            return ":warning:\tYou are not the creator of the team.", None

        # check if a user is mention, to be added
        if len(message.mentions) <= 0:
            return ":bulb:\tYou need to mention the user you want to add to the team." \
                   "Example: `!logs teams add @callFEELD <teamname>`", None

        # check if user that should be added is in userdata
        # is stored
        user_to_add = await LDBU.get_player(message.mentions[0].id)
        if user_to_add is None:
            return f":warning:\tI don't have any data of this user.\n" \
                   f"First <@{message.mentions[0].id}> has to add himself" \
                   "with the command: `!logs addme <SteamID64>`", None

        # check if the user is already in the team
        team_players = []
        for player in team["players"]:
            team_players.append(player["discord_id"])

        if str(user_to_add["discord_id"]) in team_players:
            return ":zzz: Nothing to do, the user is already " \
                    "part of the team.", None

        # adding player with to team: serverid, teamname,
        # playerdiscordid, playername, playerclass
        await LDBT.add_teamroster(
            message.guild.id,
            team["name"],
            user_to_add["discord_id"],
            None,
            None
        )

        return f":sparkles::busts_in_silhouette:\tThe team **{team['name']}**" \
               f" has added **{message.mentions[0].name}** to their " \
               "roster", None


class TeamsRemovePlayer(Command):
    """
    This command removes a user from a team.

    Example:
        !logs teams remove @callFEELD <teamname>
    Result:
        @callFEELD is now no longer part of the team called <teamname>
    """
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs teams remove'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        if message.content.lower() == '!logs teams remove':
            return ":bulb:\tYou can remove a player of a team by typing\t\t" \
                   "`!logs teams remove` <teamname> <@player>", None

        # find the team name and if the team exists
        team = await LDBT.get_team(message.guild.id, split_msg[4])

        if team is None:
            return ":warning:\tThis team does not exist", None

        # check if the user is the team creator
        if str(message.author.id) != str(team["creator"]):
            return ":warning:\tYou are not the creator of the team.", None

        if len(message.mentions) == 0:
            return ":bulb:\tYou need to mention the user, you want to remove.\n" \
                   "Example: `!logs teams remove @callFEELD <teamname>`"
        # check if mentioned player is already in user data
        user_to_remove = await LDBU.get_player(
            message.mentions[0].id
        )

        if user_to_remove is None:
            return f":warning:\t{message.mentions[0].name} isn't stored in my data.", None

        # check if the user is part of the team
        team_players = []
        for player in team["players"]:
            team_players.append(player["discord_id"])

        if user_to_remove["discord_id"] in team_players:
            await LDBT.remove_teamroster(
                message.guild.id,
                team["name"],
                user_to_remove["discord_id"]
            )
            return f":sparkles:\t Successfully removed user **{message.mentions[0].name}**" \
                   " from the team: **{split_msg[4]}**", None
        else:
            return ":warning:\tThis player is not on your team.", None


class TeamsMatch(Command):
    """
    This command shows the logs of a team.

    Example:
        !logs match <teamname>
    Result:
        Logs.tf log with all players inside the team.
    """
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs match'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        if message.content.lower() == '!logs match':
            return ":bulb:\tYou can search for a match of a team. Append the teamname " \
                   " after the command\t\t`!logs match <teamname>`\n" \
                   "\t\t  `!logs teams` shows you the teams that are available.", None

        team = await LDBT.get_team(message.guild.id, split_msg[2])

        if team is None:
            return ":warning:\tThis team does not exist. Check available teams" \
                   " with\t\t`!logs teams`", None

        if len(team["players"]) == 0:
            return \
                ":warning:\tThis team has no players. Please add at least one first.", None

        # Search for the newest match of the team
        msg = await findMatch(message, team)
        return msg, None
