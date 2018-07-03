# This Class handles and contain every command.
# last edit: 21.04.2018 (callFEELD)

# imports
import discord

# own imports
from src.classes import Essentials
from src.classes import Users
from src.classes import Teams

LBU = Users.LogBotUsers()
LBE = Essentials.LogBotEssentials()
LBT = Teams.LogBotTeams()

class LogBotCommands:
    message = {}
    moderators = LBU.getmoderators()
    client = discord.Client()


    def scan(self, message):
        # load the users data if a message hits and contains LDB commands
        if (message.content.lower().startswith("!logs")):

            # Grab important informations of message
            self.message = message
            self.message_split = self.message.content.lower().split(' ')
            msg = None

            #Checking message after all available commands
            # COMMAND: !logs help
            if message.content.lower() == "!logs help":
                msg = self.command_help()

            # COMMAND: !logs modhelp
            elif message.content.lower() == '!logs teamhelp':
                msg = self.command_modhelp()

            # COMMAND: !logs version
            elif message.content.lower() == '!logs version':
                msg = self.command_version()

            # COMMAND: !logs match
            elif message.content.lower().startswith('!logs match'):
                msg = self.command_match()

            # COMMAND: !logs teams
            elif message.content.lower().startswith('!logs teams'):
                msg = self.command_handler_teams()

            # COMMAND: !logs user
            elif message.content.lower().startswith('!logs user'):
                msg = "This command is no longer supported on the Server Edition."
                    #self.command_handler_user()

            # COMMAND: !logs addme
            elif message.content.lower().startswith('!logs addme'):
                msg = self.command_logs_addme()

            # COMMAND: !logs
            # IMPORTANT: THIS COMMAND HAS THE BE THE LAST ONE, IF NOT IT CREATES ERRORS
            elif message.content.lower().startswith('!logs'):
                msg = self.command_handler_logs()

            else:
                msg = self.command_not_found()

            if msg is None:
                return self.command_not_found()
            return msg



    # Command not found error
    def command_not_found(self):
        messagetosend = "You probably mistyped something. Don't worry and try again\n" \
                        "If you need help you can type `!logs help` for the commands."
        return messagetosend

    # COMMAND: !logs help
    def command_help(self):
        #Variables
        modhelp = "`!logs teamhelp` - for every team commands"
        tip = ""

        # if the user is not in the database, advice him to join
        user = LBU.get_player(self.message.author.id)
        if not user:
            tip = ":incoming_envelope: "\
                  "Seems like you are fresh meat. You can level up with `!logs addme <SteamID64>` to add yourself to "\
                  "my database.\n\n"

        #Message that will be sended
        messagetosend = tip + "__**Commands**__\n\n" + modhelp+ \
                        "\n\n`!logs` - shows your las!t played match with details about your performance" \
                        "\n`!logs profile` - shows your logs.tf profile" \
                        "\n\n`!logs <@name>` - shows the last log of the player you looked for" \
                        "\n`!logs <@name> profile` - shows the logs.tf profile of the player you looked for" \
                        "\n\n`!logs match <teamname>` - shows the latest match (scrim, lobby, official) of a team with details " \
                        "about your performance" \
                        "\n`!logs teams` - shows the available teams" \
                        "\n`!logs teams <teamname> players` - shows the players in the team" \
                        "\n\n`version: "+LBE.version+"`"

        return messagetosend


    # COMMAND: !logs modhelp
    def command_modhelp(self):
        messagetosend = "__**Advanced commands**__" \
                        "\n\n`!logs teams create <teamname> <format>` - Creates a new team. Format is the type of " \
                        "the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on)." \
                        "\n`!logs teams delete <teamname>` - Removes a team from the system." \
                        "\n\n`!logs teams add <teamname> <@name> <name> <class>` - Stores a player with a specific name " \
                        "into a team." \
                        "\n`!logs teams remove <teamname> <@name>` - Removes a player from a team." \
                        "\n\n`version: " + LBE.version + "`"

        return messagetosend


    # COMMAND: !logs version
    def command_version(self):
        messagetosend = "`" + LBE.version + "`"
        return messagetosend


    # COMMAND: !logs match
    def command_match(self):
        #Variables
        messagetosend = "Error"

        #Check if addition "match" was choosen
        if self.message.content.lower() == '!logs match':
            messagetosend = ":incoming_envelope:\tYou can search for a match of a team. Append the teamname "\
                            " after the command\t\t`!logs match <teamname>`\n" \
                            "\t\t  `!logs teams` shows you the teams that are available."

        #if an teamname has been added
        elif len(self.message_split) >= 3:
            #Check every team
            team = LBT.get_team(self.message.server.id, self.message_split[2])

            #if team was founded
            if team:
                #check what format the team has
                #and use then the minplayer options
                minplayer = 0
                #6s
                if team["type"] == "6":
                    minplayer = LBE.sixes_min_players
                #HL
                elif team["type"] == "9":
                    minplayer = LBE.hl_min_players
                #4s
                elif team["type"] == "4":
                    minplayer = LBE.fours_min_players
                #Duo
                elif team["type"] == "2":
                    minplayer = LBE.duo_min_players

                #check if the team has the minumum of players
                if len(team["players"]) >= minplayer:
                    #Search for the newest match of the team
                    messagetosend = LBE.findMatch(minplayer, LBE.AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER, team["type"], team["players"], self.message)
                    if(messagetosend==None):
                        messagetosend = ":new_moon:\tI cloudn't find any matches of the team **'"+team["name"]+"'**\n" \
                                        "Probably your team didn't played together for quite some time.\n\n" \
                                        ":bulb:\t**Background information**\n" \
                                        "It depends on the amount of logs that going to be scanned by me."\
                                        " If that happens more often contact callFEELD for that.\n" \
                                        "Currently I am checking the latest `"+\
                                        str(LBE.AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER)+"`" \
                                        " logs of each person in the team and " \
                                        "look for logs where at least `" + \
                                        str(minplayer) + "` of the team members played together."
                else:
                    # not enough players in the team to search for a match
                    messagetosend = ":warning:\tThis team needs at least " + \
                                    str(minplayer) + " to search for a match. Currently there are only " +\
                                    str(len(team["players"]))+ " players in the team."
            else:
                messagetosend = ":warning:\tThis team does not exist. Check available teams with\t\t`!logs teams`"

        # Output
        return messagetosend


    # handles the various !logs teams ... commands
    def command_handler_teams(self):
        user = LBU.get_player(self.message.author.id)
        if self.message.content.lower() == "!logs teams":
            return self.command_teams()

        # !logs teams <teamname> players
        if self.message.content.lower().endswith('players') and len(self.message_split) >= 4:
            return self.command_teams_players()

        if user:
            # !logs teams add <player> <teamname> <playername>
            if self.message.content.lower().startswith('!logs teams add'):
                return self.command_teams_add()

            if self.message.content.lower().startswith('!logs teams remove'):
                return self.command_teams_remove()

            if self.message.content.lower().startswith('!logs teams create'):
                return self.command_teams_create()

            if self.message.content.lower().startswith('!logs teams delete'):
                return self.command_teams_delete()
        else:
            return ":warning:\t" + self.message.author.name + " you don't have permissions. Add yourself " \
                   "first my database with `!logs addme <SteamID64>`"


    # Command: !logs teams
    def command_teams(self):
        #vars
        messagetosend = ":busts_in_silhouette:\t**Teams**\n"

        #check if teams exists
        teams = LBT.get_teams(self.message.server.id)
        if teams:
            messagetosend = messagetosend + "Here are all teams I stored on this Discord server:\n\n"
            for team in teams:
                messagetosend = messagetosend + team["name"] + " | `"+ team["type"] +"`\t\t"
        else:
             messagetosend = messagetosend + "There aren't any teams at the moment. You can create one with the " \
                                                "command `!logs teams create <teamname> <format>`"

        return messagetosend

    def command_teams_players(self):
        # vars
        messagetosend = ":warning:\tThis team does not exist"

        team = LBT.get_team(self.message.server.id, self.message_split[2])
        if team:
            messagetosend = ":space_invader:\t**Team: '" + team["name"] + "' player's**\n"
            messagetosend += "(amount: " + str(len(team["players"])) + ")\n\n"
            # check if the teams have players, else create a tip to add them
            if len(team["players"]) > 0:
                for player in team["players"]:
                    messagetosend += "" + player["name"] + " | `" + player["class"] + "`\t\t"

            else:
                messagetosend += ":bulb:\tYou can add players to the team with the command\t\t`!logs teams add " + \
                                     self.message_split[2] + " <@name> <name> <class>`"
        else:
            messagetosend = ":warning:\t This team does not exist."
        return messagetosend

    def command_teams_add(self):
        # vars
        messagetosend = None

        # check if he only typed: !logs teams add
        if self.message.content.lower() == '!logs teams add':
            messagetosend = ":incoming_envelope:\tYou can add or update a player to/of a team by typing\t\t"\
                            "`!logs teams add` <teamname> <@player> <Name>"

        elif len(self.message_split)>3:
            # check if 4th position is not a team
            team = LBT.get_team(self.message.server.id, self.message_split[3])
            if team:
                if not len(self.message_split) >= 7:
                    if len(self.message_split) == 4:
                        messagetosend = ":bulb:\tYou have to mention the player, add his name and his class after your command\t\t`" \
                                        + self.message.content.lower() + "` <@player> <Name> <class>"
                    elif len(self.message_split) == 5:
                        messagetosend = ":bulb:\tAdd the players name and his class after your command\t\t`" + \
                                        self.message.content.lower() + "` <Name> <class>"
                    else:
                        messagetosend = ":bulb:\tAdd his class after your command\t\t`" + \
                                        self.message.content.lower() + "` <class>"

                # if its a team and it has the correct msg
                elif len(self.message.mentions) == 1 and len(self.message_split) >= 7:
                    # check if user that should be added is in userdata
                    user_to_add = LBU.get_player(self.message.mentions[0].id)
                    if user_to_add:
                        if str(self.message.author.id) == str(team["creator"]):
                            # check if mention player is already in the team
                            team_players = []
                            for player in team["players"]:
                                team_players.append(player["discord_id"])
                            if str(user_to_add["discord_id"]) in team_players:
                                addorupdate = "updated"
                                # adding player with to team: serverid, teamname, playerdiscordid, playername, playerclass
                                LBT.update_teamroster(self.message.server.id, team["name"], user_to_add["discord_id"],
                                             self.message_split[5], self.message_split[6])
                            else:
                                addorupdate = "increased"
                                # adding player with to team: serverid, teamname, playerdiscordid, playername, playerclass
                                LBT.add_teamroster(self.message.server.id, team["name"], user_to_add["discord_id"],
                                             self.message_split[5], self.message_split[6])

                            messagetosend = ":sparkles::busts_in_silhouette:\tThe team " + team["name"]\
                                            + " has "+ addorupdate + " their roster** " + \
                                            self.message.mentions[0].name + "** - class: " + \
                                            self.message_split[6]
                        else:
                            messagetosend = ":warning:\tYou are not the creator of the team."
                    else:
                        messagetosend = ":warning: \t" + self.message.mentions[0].name + \
                                        " isn't stored in my data. First <@"+str(self.message.mentions[0].id)+\
                                        "> has to add himself with the command:\t\t" \
                                        "`!logs addme <SteamID64>`"


            else:
                messagetosend = ":warning:\tThis team does not exist."

        else:
            messagetosend = None

        return messagetosend

    def command_teams_remove(self):
        # vars
        messagetosend = None
        if self.message.content.lower() == '!logs teams remove':
            messagetosend = ":incoming_envelope:\tYou can remove a player of a team by typing\t\t`!logs teams remove` <teamname> <@player>"

        elif len(self.message_split) > 3:
            # else find the team name and if the team exists
            team = LBT.get_team(self.message.server.id, self.message_split[3])
            if team:
                if not len(self.message_split) >= 5:
                    # check if enough inputs are granted
                    if len(self.message_split) == 4:
                        messagetosend = ":bulb:\tAdd the player after your command\t\t`" + \
                                        self.message.content.lower() + "`  <@player>"

                # if it has enough data
                elif len(self.message.mentions) == 1 and len(self.message_split) >= 5:
                    if str(self.message.author.id) == str(team["creator"]):
                        # check if mentioned player is already in user data
                        user_to_remove = LBU.get_player(self.message.mentions[0].id)
                        if user_to_remove:
                            team_players = []
                            for player in team["players"]:
                                team_players.append(player["discord_id"])
                            if user_to_remove["discord_id"] in team_players:
                                # removing player (teamname, discordid)
                                LBT.remove_teamroster(self.message.server.id, team["name"], user_to_remove["discord_id"])
                                messagetosend = ":new_moon_with_face:\t Successfully removed user **" + \
                                                            self.message.mentions[0].name + "** from the team: " + \
                                                            self.message_split[3]
                            else:
                                messagetosend = ":warning:\tThis player is not on your team."
                        else:
                            messagetosend = ":warning:\t" + self.message.mentions[0].name + " isn't stored in my data."
                    else:
                        messagetosend = ":warning:\tYou are not the creator of the team."
            else:
                messagetosend = ":warning:\tThis team does not exist"

        return messagetosend

    def command_teams_create(self):
        messagetosend = None

        # if only typed: !logs teams create
        if self.message.content.lower() == '!logs teams create':
            messagetosend = ":incoming_envelope:\tYou can create a team by typing:\t\t" \
                                "`!logs teams create` <teamname> <format>"

        # check if the command is correct
        elif len(self.message_split) >= 5:
            name = self.message_split[3]
            type = self.message_split[4]
            creator = self.message.author.id
            # check if the teamname already exists
            team = LBT.get_team(self.message.server.id, name)
            if not team:
                # Check if last value is an int
                try:
                    format = int(type)
                    # create a new team (teamname, type)
                    LBT.create_team(self.message.server.id, name, type, creator)

                    messagetosend = ":sparkles:\tSuccessfully created the team **" + name \
                                        + "** with the format: " + type
                except ValueError:
                    # If type isn't a number
                    messagetosend = ":no_entry_sign:\tThe format has to be a integer (6 = 6v6, 9 = 9v9 and so on)"

            else:
                messagetosend = ":warning:\tThis team already exists."

        elif len(self.message_split) < 5:
            messagetosend = ":bulb:\tYou have to add the teams format " \
                                "(6 = 6v6, 9 = 9v9 and so on) after\t\t`!logs teams create " + \
                                self.message_split[3] + "` <format>"

        return messagetosend

    def command_teams_delete(self):
        messagetosend = None
        # check if only !logs teams delete was typed
        if self.message.content.lower() == '!logs teams delete':
            messagetosend = ":incoming_envelope:\tYou can delete a team by typing\t\t`!logs teams delete` <teamname>"

        # if teamname is missing
        elif len(self.message_split) < 4:
            messagetosend = ":bulb:\tYou have to add the teamname"

        elif len(self.message_split) >= 4:
            messagetosend = ":warning:\tThis team does not exist."

            # Check if team even exists
            teamname = self.message_split[3]
            team = LBT.get_team(self.message.server.id, teamname)

            if team:
                if str(team["creator"]) == str(self.message.author.id):
                    # deletes team (teamname)
                    LBT.delete_team(self.message.server.id, teamname)
                    messagetosend = ":new_moon_with_face:\tDeleted your team **" + teamname + "**"
                else:
                    messagetosend = ":warning:\tThis isn't your team."

        return messagetosend

    ''' REMOVED OF THE SERVER EDITION
    def command_handler_user(self):
        if self.message.content.lower() == "!logs user":
            return self.command_user()

        if self.message.content.lower().startswith('!logs user add'):
            return self.command_user_add()

        if self.message.content.lower().startswith('!logs user remove'):
            return self.command_user_remove()

    def command_user(self):
        messagetosend = "Type `!logs user add` to add a user or type `!logs user remove` to remove one."
        return messagetosend

    def command_user_add(self):
        # vars
        messagetosend = self.message.author.name + " you don't have permissions."

        # check if author is mod
        if self.message.author.id in self.moderators:

            # check if only typed: !Logs user add
            if self.message.content.lower() == '!logs user add':
                messagetosend = ":information_source:  You can get add or update players. Just type after `!logs user add` <@name> <SteamID64>"

            else:
                # check if steamid missing
                if not len(self.message_split) == 5:
                    messagetosend = ":information_source: add the SteamID64 after the mention statement `" + self.message.content.lower() + "` <SteamID64>"

                else:
                    # check if user already exist and rewrite or add user
                    if self.message.mentions[0].id in self.userlist:
                        addorupdate = "Updated"

                    else:
                        addorupdate = "Added"

                    # grabs users (that has to be added) steam id 64
                    addusersteamid64 = self.message_split[4]

                    # adds user with discord id and steam id 64
                    LBU.add_user(self.message.mentions[0].id, addusersteamid64)

                    # Outputs Successfull Message
                    messagetosend = ":ballot_box_with_check: " + addorupdate + " user **" + self.message.mentions[
                        0].name + "** with the SteamID64: " + addusersteamid64

        return messagetosend

    def command_user_remove(self):
        # vars
        messagetosend = self.message.author.name + " you don't have permissions."

        # check if author is mod
        if self.message.author.id in self.moderators:
            # check if only typed: !Logs user remove
            if self.message.content.lower() == '!logs user remove':
                messagetosend = ":information_source: You can remove players.\nJust type after `!logs user remove` <@name> <SteamID64>"

            else:
                # remove user
                if len(self.message_split) == 4:
                    # removes user with discord id (message.mentions[0].id)
                    LBU.remove_user(self.message.mentions[0].id)

                    # Outputs Succsessfully message
                    messagetosend = ":ballot_box_with_check:  removed user " + self.message.mentions[
                        0].name


        return messagetosend
    '''


    # Command: !logs
    def command_handler_logs(self):
        if self.message.content.lower() == '!logs':
            return self.command_logs()

        if self.message.content.lower() == '!logs profile':
            return self.command_logs_profile()

        # Check if command: !logs @mention is called
        elif len(self.message.mentions) != 0 and not self.message.content.lower().endswith('profile') and not len(
                self.message_split) >= 3:
            return self.command_logs_mention()

        # Checking for command: !logs @mention profile
        elif not len(self.message.mentions) == 0 and len(
                self.message_split) >= 3 and self.message.content.lower().endswith('profile'):
            return self.command_logs_mention_profile()

    def command_logs(self):
        # initilaize vars
        messagetosend = "Sorry " + self.message.author.name + \
                        " :confused:  but I didn't find you in my data.\n" \
                        "But you can add yourself to the system by adding your Steam ID 64.\n" \
                        "use the command `!logs addme <SteamID64>`"

        # checks if author is registerd in the user file
        user = LBU.get_player(self.message.author.id)
        if user:
            # Then grab data of the player
            # Get the newest log of the player
            data = LBE.LogPlayerSearch(user["steam_id"], 1)
            # Getting data of the log
            logid = str(data["logs"][0]["id"])  # Logid
            logtitle = str(data["logs"][0]["title"])  # Title of the log
            logtime = LBE.totime(data["logs"][0]["date"])  # date and time of the log
            steamid3 = LBE.tosteamid3(user["steam_id"])

            # Grabbing player performance
            logiddetails = LBE.LogIDdetails(logid, steamid3)
            performance = LBE.PerformanceDisplay(0, logiddetails)

            # Message content
            messagetosend = ":dart:\t" + self.message.author.name + "'s Log found\n\n**" + logtitle + "**\t`" \
                             + logtime + "`\n<http://logs.tf/" + logid + ">\n" + performance

        return messagetosend

    def command_logs_profile(self):
        # vars
        messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find you in my data."

        # check if user is in userdata
        user = LBU.get_player(self.message.author.id)
        if user:
            stored_data_msg = ":card_box:\t**" + self.message.author.name + "'s profile**\n\nSteamID\t\t\t`" \
                              + user["steam_id"] + "`\nSteam:\t\t\t\t<http://steamcommunity.com/profiles/" + user[
                                  "steam_id"] + ">\n"

            # Getting newest 3 logs
            data = LBE.LogPlayerSearch(user["steam_id"], 3)

            # check if this is a real valid user
            if data["results"] != 0:
                # building message
                messagetosend2 = "\n\n__Last 3 logs__\n"
                # looping 3 logs with id, link, title, time and date
                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = LBE.totime(log["date"])
                    messagetosend2 = messagetosend2 + "**" + logtitle + "**\t`"+ logtime \
                                     +"`\n<http://logs.tf/" + logid + ">\n\n"

                # building message
                messagetosend2 = messagetosend2 + ""
                messagetosend = stored_data_msg + "logs.tf profile:\t<http://logs.tf/profile/" + \
                                user["steam_id"] + ">" + messagetosend2
            else:
                messagetosend = stored_data_msg + ":warning:  Looks like that this steamid does not exits, \
                                change it by type `!logs addme <steamid>`"

        return messagetosend

    def command_logs_mention(self):
        # vars
        mentionuser = str(self.message.mentions[0].name)
        messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find **" + \
                        mentionuser + "** in my data."

        # Checks if called player is in userdata
        user = LBU.get_player(self.message.mentions[0].id)
        if user:
            # grabbing steam ids of the player
            steamid64 = user["steam_id"]
            steamid3 = LBE.tosteamid3(steamid64)

            # grabbing newst log of the player
            data = LBE.LogPlayerSearch(user["steam_id"], 1)
            # Getting log details
            logid = str(data["logs"][0]["id"])  # logid
            logtitle = str(data["logs"][0]["title"])  # log title
            logtime = LBE.totime(data["logs"][0]["date"])  # date and time of the log
            # getting player performance
            logiddetails = LBE.LogIDdetails(logid, steamid3)
            performance = LBE.PerformanceDisplay(1, logiddetails)

            # Message content
            messagetosend = ":mag_right:\t**" + mentionuser + "**'s Log found\n\n**" + logtitle\
                            + "**\t`" + logtime + "`\n<http://logs.tf/" + logid + ">" + performance

        return messagetosend

    def command_logs_mention_profile(self):
        # Vars
        messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find **" + str(
            self.message.mentions[0].name) + "** in my data."

        # checks if mentioned player is in the user data
        user = LBU.get_player(self.message.mentions[0].id)
        if user:
            # Grabbing steam ids and name
            mentionuser = str(self.message.mentions[0].name)

            stored_data_msg = ":credit_card:\t This is **" + mentionuser + " profile**\n\nSteamID:\t\t\t`" \
                              + user["steam_id"] + "`\nSteam:\t\t\t\t<http://steamcommunity.com/profiles/" + \
                              user["steam_id"] + ">\n"

            # Getting newest 3 logs
            data = LBE.LogPlayerSearch(user["steam_id"], 3)

            # check if this is a real valid user
            if data["results"] != 0:
                # Building message
                messagetosend2 = "\n\n__Last 3 logs__\n"
                # inserting logs with link, title, date and time
                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = LBE.totime(log["date"])
                    messagetosend2 = messagetosend2 + "**" + logtitle + "**\t`" + logtime \
                                     + "`\n<http://logs.tf/" + logid + ">\n\n"

                # Building rest of the message
                messagetosend2 = messagetosend2 + ""
                messagetosend = stored_data_msg + "logs.tf profile:\t<http://logs.tf/profile/" + \
                                user["steam_id"] + ">" + messagetosend2
            else:
                messagetosend = stored_data_msg + ":warning:  Looks like that this steamid does not exits."

        return messagetosend


    # COMMAND: !logs addme
    def command_logs_addme(self):
        # vars
        messagetosend = "Error"
        splitmessage = self.message.content.lower().split(' ')

        # check if only typed: !logs addme
        if self.message.content.lower() == '!logs addme':
            messagetosend = ":incoming_envelope:\tYou can get add or update your data. Just type after\t\t"\
                            "`!logs addme` <SteamID64>"

        else:
            # check if user already exist and rewrite or add user
            user = LBU.get_player(self.message.author.id)
            if user:
                # grabs users (that has to be added) steam id 64
                addusersteamid64 = splitmessage[2]

                # adds user with discord id and steam id 64
                LBU.update_user(self.message.author.id, addusersteamid64)
                messagetosend = ":sparkles:\tUpdated yourself with the SteamID64: " + addusersteamid64

            else:
                # grabs users (that has to be added) steam id 64
                addusersteamid64 = splitmessage[2]

                # adds user with discord id and steam id 64
                LBU.add_user(self.message.author.id, addusersteamid64)

                # Outputs Successfull Message
                messagetosend = ":sparkles:\tAdded yourself with the SteamID64: " + addusersteamid64

        return messagetosend
