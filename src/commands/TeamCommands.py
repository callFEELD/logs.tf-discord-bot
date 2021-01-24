from src.commands import Command, ActivatorType, CommandActivator, CommandPriority
import src.teams as LDBT
import src.users as LDBU


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
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs teams add'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        # check if he only typed: !logs teams add
        if message.content.lower() == '!logs teams add':
            return ":bulb:\tYou can add or update a player to/of a team by typing " \
                    "`!logs teams add <teamname> <@player> <Name>`", None

        # check if 4th position is not a team
        team = await LDBT.get_team(message.guild.id, split_msg[3])
        if team:
            if len(split_msg) == 4:
                return ":bulb:\tYou have to mention the player, add his name and "\
                        f"his class after your command\t\t`{message.content.lower()}" \
                        " <@player> <Name> <class>`", None
            elif len(split_msg) == 5:
                return ":bulb:\tAdd the players name and his class after your " \
                       f"command\t\t`{message.content.lower()} <Name> <class>`", None
            elif len(split_msg) == 6:
                return ":bulb:\tAdd his class after your command\t\t`" \
                       f"{message.content.lower()} <class>`", None
            elif len(split_msg) >= 7 and len(message.mentions) > 0:
                # check if user that should be added is in userdata
                user_to_add = await LDBU.get_player(message.mentions[0].id)
                if user_to_add:
                    if str(message.author.id) == str(team["creator"]):
                        # check if mention player is already in the team
                        team_players = []
                        for player in team["players"]:
                            team_players.append(player["discord_id"])
                        if str(user_to_add["discord_id"]) in team_players:
                            addorupdate = "updated"
                            # adding player with to team: serverid, teamname,
                            # playerdiscordid, playername, playerclass
                            await LDBT.update_teamroster(
                                message.guild.id,
                                team["name"],
                                user_to_add["discord_id"],
                                split_msg[5],
                                split_msg[6]
                            )
                        else:
                            addorupdate = "increased"
                            # adding player with to team: serverid, teamname,
                            # playerdiscordid, playername, playerclass
                            await LDBT.add_teamroster(
                                message.guild.id,
                                team["name"],
                                user_to_add["discord_id"],
                                split_msg[5],
                                split_msg[6]
                            )

                        return f":sparkles::busts_in_silhouette:\tThe team {team['name']}" \
                               f" has {addorupdate} their roster** {message.mentions[0].name}**" \
                               f"- class: {split_msg[6]}", None
                    else:
                        return \
                            ":warning:\tYou are not the creator of the team.", None
                else:
                    return f":warning: \t {message.mentions[0].name}" \
                           f" isn't stored in my data. First <@{message.mentions[0].id}" \
                            "> has to add himself with the command:\t\t" \
                            "`!logs addme <SteamID64>`", None
        else:
            return ":warning:\tThis team does not exist.", None


class TeamsRemovePlayer(Command):
    activator = CommandActivator(
        ActivatorType.starts_with, '!logs teams remove'
    )

    async def logic(self, message):
        split_msg = message.content.lower().split(" ")

        if message.content.lower() == '!logs teams remove':
            return  ":incoming_envelope:\tYou can remove a player of a team by typing\t\t" \
                    "`!logs teams remove` <teamname> <@player>", None
        elif len(split_msg) > 3:
            # else find the team name and if the team exists
            team = await LDBT.get_team(message.guild.id, split_msg[3])
            if team:
                if len(split_msg) == 4:
                    return ":bulb:\tAdd the player after your command\t\t`" \
                           f"{message.content.lower()}  <@player>`", None
                elif len(message.mentions) == 1 and len(split_msg) >= 5:
                    if str(message.author.id) == str(team["creator"]):
                        # check if mentioned player is already in user data
                        user_to_remove = await LDBU.get_player(
                            message.mentions[0].id
                        )
                        if user_to_remove:
                            team_players = []
                            for player in team["players"]:
                                team_players.append(player["discord_id"])
                            if user_to_remove["discord_id"] in team_players:
                                # removing player (teamname, discordid)
                                await LDBT.remove_teamroster(
                                    message.guild.id,
                                    team["name"],
                                    user_to_remove["discord_id"]
                                )
                                return ":new_moon_with_face:\t Successfully removed user **" \
                                       f"{message.mentions[0].name}** from the team: {split_msg[3]}", None
                            else:
                                return ":warning:\tThis player is not on your team.", None
                        else:
                            return f":warning:\t{message.mentions[0].name} isn't stored in my data.", None
                    else:
                        return ":warning:\tYou are not the creator of the team.", None
            else:
                return ":warning:\tThis team does not exist", None
