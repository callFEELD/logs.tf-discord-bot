from src.commands import Command, Placeholder, ActivatorType, CommandActivator, CommandPriority
from src import tosteamid3, totime, get_logs, get_parsed_log_details, \
                get_closest_demo, PerformanceDisplay
import src.teams as LDBT


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
    activator = CommandActivator(ActivatorType.starts_with, '!logs teams create')

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
                    team_format = int(c_type)
                    # create a new team (teamname, type)
                    await LDBT.create_team(
                        message.guild.id, name, c_type, creator
                    )

                    return \
                        f":sparkles:\tSuccessfully created the team **{name}**"\
                        f"with the format: {c_type}", None
                except ValueError:
                    # If type isn't a number
                    return ":no_entry_sign:\tThe format has to be a integer "\
                            "(6 = 6v6, 9 = 9v9 and so on)", None

            else:
                return ":warning:\tThis team already exists.", None

        return ":bulb:\tYou have to add the teams format " \
                "(6 = 6v6, 9 = 9v9 and so on) after\t\t" \
                "`!logs teams create <teamname> <format>`", None
