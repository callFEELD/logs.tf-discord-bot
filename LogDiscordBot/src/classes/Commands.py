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
        if (message.content.lower().find("!logs") != -1):

            # Grab important informations of message
            self.message = message
            self.message_split = self.message.content.lower().split(' ')


            #Checking message after all available commands
            # COMMAND: !logs help
            if message.content.lower() == "!logs help":
                return self.command_help()

            # COMMAND: !logs modhelp
            if message.content.lower() == '!logs modhelp':
                return self.command_modhelp()

            # COMMAND: !logs version
            if message.content.lower() == '!logs version':
                return self.command_version()

            # COMMAND: !logs match
            if message.content.lower().startswith('!logs match'):
                return self.command_match()

            # COMMAND: !logs teams
            if message.content.lower().startswith('!logs teams'):
                return self.command_handler_teams()

            # COMMAND: !logs user
            if message.content.lower().startswith('!logs user'):
                return self.command_handler_user()

            # COMMAND: !logs addme
            if message.content.lower().startswith('!logs addme'):
                return self.command_logs_addme()

            # COMMAND: !logs
            # IMPORTANT: THIS COMMAND HAS THE BE THE LAST ONE, IF NOT IT CREATES ERRORS
            if message.content.lower().startswith('!logs'):
                return self.command_handler_logs()


    # COMMAND: !logs help
    def command_help(self):
        #Variables
        modhelp = ""
        tip = ""

        #If user is mod, show that command !logs modhelp exists
        if self.message.author.id in self.moderators:
           modhelp = "\nYou are a Moderator, type `!logs modhelp` to get moderator commands"

        # if the user is not in the database, advice him to join
        user = LBU.get_player(self.message.author.id)
        if not user:
            tip = ":incoming_envelope: "\
                  "Seems like you are fresh meat. You can level up with `!logs addme <SteamID64>` to add yourself to "\
                  "my database.\n\n"

        #Message that will be sended
        messagetosend = tip + ":information_source:  __**Commands**__" + modhelp+ \
                        "\n\n`!logs`\nshows your last played match with details about your performance" \
                        "\n`!logs profile`\nshows your logs.tf profile" \
                        "\n\n`!logs <@name>`\nshows the last log of the player you looked for" \
                        "\n`!logs <@name> profile`\nshows the logs.tf profile of the player you looked for" \
                        "\n\n`!logs match <teamname>`\nshows the latest match (scrim, lobby, official) of a team with details " \
                        "about your performance" \
                        "\n`!logs teams`\nshows the available teams" \
                        "\n`!logs teams <teamname> players`\nshows the players in the team" \
                        "\n\n`version: "+LBE.version+"`"

        return messagetosend


    # COMMAND: !logs modhelp
    def command_modhelp(self):
        #Variables
        messagetosend = "You don't have permission."

        #Check if message author is a moderator
        if self.message.author.id in self.moderators:
            messagetosend = ":information_source:  __**Moderator commands**__\n\n`!logs user add <@name> <SteamID64>`" \
                            "\nto add a player to the system with his/her " \
                            "SteamID64. This command can also be used to update a player's SteamID64." \
                            "\n`!logs user remove <@name>`\nremoves the player from the system." \
                            "\n\n`!logs teams create <teamname> <format>`\nCreates a new team. Format is the type of " \
                            "the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on). WIP" \
                            "\n`!logs teams delete <teamname>`\nRemoves a team from the system. WIP" \
                            "\n\n`!logs teams add <teamname> <@name> <name>`\nStores a player with a specific name " \
                            "into a team." \
                            "\n`!logs teams remove <teamname> <@name>`\nRemoves a player from a team." \
                            "\n\n`version: " + LBE.version + "`"

        return messagetosend


    # COMMAND: !logs version
    def command_version(self):
        messagetosend = "`" + LBE.version + "`"
        return messagetosend


    # COMMAND: !logs match
    def command_match(self):
        #Variables
        splitmessage = self.message.content.lower().split(" ")
        messagetosend = "Error"

        #Check if addition "match" was choosen
        if self.message.content.lower() == '!logs match':
            messagetosend = ":information_source:  You can search for a match of a team. Append the teamname after the command (`!logs match <teamname>`)\n" \
            "`!logs teams` shows you the teams that are available."

        #if an teamname has been added
        elif len(splitmessage) >= 3:
            #Variables
            messagetosend = "This team does not exist. Check available teams with `!logs teams`"

            #Check every team
            for team in self.teamlist:

                #if team was founded
                if splitmessage[2] in team:
                    #get teamname
                    teamname = splitmessage[2]

                    #output loading message
                    self.client.send_message(self.message.channel, "*wait a bit I am processing...*")

                    #check what format the team has
                    #and use then the minplayer options
                    minplayer =0
                    #6s
                    if team[teamname][0]["type"] == "6":
                        minplayer = LBE.sixes_min_players
                    #HL
                    elif team[teamname][0]["type"] == "9":
                        minplayer = LBE.hl_min_players
                    #4s
                    elif team[teamname][0]["type"] == "4":
                        minplayer = LBE.fours_min_players
                    #Duo
                    elif team[teamname][0]["type"] == "2":
                        minplayer = LBE.duo_min_players

                    #check if the team has the minumum of players
                    #get the amount of players
                    team_player_amount = 0
                    for player in team[teamname][1]["players"].values():
                        team_player_amount += 1

                    if team_player_amount >= minplayer:
                        #Search for the newest match of the team
                        messagetosend = LBE.findMatch(minplayer, LBE.AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER, team[teamname][0]["type"], team[teamname][1]["players"], self.message)
                        if(messagetosend==None):
                            messagetosend=":hushed:  I cloudn't find any matches of the team **'"+teamname+"'**\n" \
                                          "Probably your team didn't played together for quite some time.\n\n" \
                                          "__**Background information**__\n" \
                                          "It depends on the amount of logs that going to be scanned by me. __Maybe my" \
                                          " config should be adjusted a little bit. Contact the admin for that.__\n" \
                                          "Currently I am checking the latest `"+str(LBE.AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER)+"`" \
                                          " logs of each person in the team and " \
                                          "look for logs where at least `" + str(minplayer) + "` of the team members played " \
                                          "together."
                    else:
                        # not enough players in the team to search for a match
                        messagetosend = ":information_source:  This team needs at least " + str(minplayer) + " to search" \
                                        " for a match. Currently there are only " +str(team_player_amount)+ " players in " \
                                        "the team."

        # Output
        return messagetosend


    # handles the various !logs teams ... commands
    def command_handler_teams(self):
        if self.message.content.lower() == "!logs teams":
            return self.command_teams()

        # !logs teams <teamname> players
        if self.message.content.lower().endswith('players') and len(self.message_split) >= 4:
            return self.command_teams_players()

        # !logs teams add <player> <teamname> <playername>
        if self.message.content.lower().startswith('!logs teams add'):
            return self.command_teams_add()

        if self.message.content.lower().startswith('!logs teams remove'):
            return self.command_teams_remove()

        if self.message.content.lower().startswith('!logs teams create'):
            return self.command_teams_create()

        if self.message.content.lower().startswith('!logs teams delete'):
            return self.command_teams_delete()

    # Command: !logs teams
    def command_teams(self):
        #vars
        messagetosend = ":busts_in_silhouette: **Teams**\n"

        #check if teams exists
        teams = LBT.get_teams(self.message.server.id)
        if teams:
            messagetosend = messagetosend + "Here are all teams I stored:\n"
            for team in teams:
                messagetosend = messagetosend +"`"+ team["name"] +"`   "
        else:
             messagetosend = messagetosend + "There aren't any teams at the moment. You can create one with the " \
                                                "command `!logs teams create <teamname> <format>`"

        return messagetosend

    def command_teams_players(self):
        # vars
        messagetosend = ":warning:  This team does not exist"

        team = LBT.get_team(self.message_split[2])
        # HIER WEITER ARBEITEN
        '''
            Datenbank playersinteam muss Spielernamen und Klasse speicher
            - ? oder players speichert schon den namen?

            die neuen Sachen müssen in DB findTeam übergeben werden
        '''
        if team:
            messagetosend = ":space_invader:  **Team: '" + team["name"] + "' player's**\n"
            num = 0
            for player in team["players"]:
                messagetosend += "`" + player + "`   "
                num += 1

                messagetosend += "(amount: " + str(num) + ")"

                # if the teams dont have players, create a tip to add them
                if num == 0:
                    messagetosend += "\n\nYou can add players to the team with the command `!logs teams add " + \
                                     self.message_split[2] + " <@name> <name>`"

                notexisting = False

        return messagetosend

    def command_teams_add(self):
        # vars
        messagetosend = self.message.author.name + " you don't have permissions."

        # check if author is moderator
        if self.message.author.id in self.moderators:
            # check if he only typed: !logs teams add
            if self.message.content.lower() == '!logs teams add':
                messagetosend = ":information_source: You can add or update a player to/of a team by typing `!logs teams add` <teamname> <@player> <Name>"

            else:
                # check if 4th position is not a team
                for team in self.teamlist:
                    if self.message_split[3] in team:
                        if not len(self.message_split) >= 6:
                            if len(self.message_split) == 5:
                                messagetosend = ":information_source: add the name after your command `" + self.message.content.lower() + "`  <Name>"

                            else:
                                messagetosend = ":information_source: add the user and the name after your command `" + self.message.content.lower() + "` <@player> <Name>"
                            notexisting = False
                            break

                        # if its a team
                        elif len(self.message.mentions) != 0 and len(self.message_split) >= 6:
                            # check if user that should be added is in userdata
                            if self.message.mentions[0].id in self.userlist:
                                # check if mention player is already in the team
                                if self.message.mentions[0].id in team[self.message_split[3]][1]["players"].values():
                                    addorupdate = "Updated"

                                else:
                                    addorupdate = "Added"

                                # adding player with to team: teamname, discordid, playername
                                LBT.add_team(self.message_split[3], self.message.mentions[0].id, self.message_split[5])

                                messagetosend = ":ballot_box_with_check: " + addorupdate + " user **" + \
                                                self.message.mentions[0].name + "** with the name: " + \
                                                self.message_split[5]
                                notexisting = False
                                break
                            else:
                                messagetosend = ":warning:  " + self.message.mentions[
                                    0].name + " isn't stored in my data.\nFirst you have to add him with the command: `!logs user add <@user> <SteamID64>`"
                                notexisting = False
                                break

                    else:
                        notexisting = True

                if notexisting:
                    messagetosend = "This team does not exist"

        else:
            messagetosend = self.message.author.name + " you don't have permissions."

        return messagetosend

    def command_teams_remove(self):
        # vars
        messagetosend = self.message.author.name + " you don't have permissions."

        # check if author is moderator
        if self.message.author.id in self.moderators:
            # check if only: !logs teams remove is called
            if self.message.content.lower() == '!logs teams remove':
                messagetosend = ":information_source: You can remove a player of a team by typing `!logs teams remove` <teamname> <@player>"

            else:
                # else find the team name and if the team exists
                for team in self.teamlist:
                    if self.message_split[3] in team:
                        if not len(self.message_split) >= 5:
                            # check if enough inputs are granted
                            if len(self.message_split) == 4:
                                messagetosend = ":information_source: add the player after your command `" + self.message.content.lower() + "`  <@player>"

                            notexisting = False
                            break

                        # if it has enough data
                        elif len(self.message.mentions) != 0 and len(self.message_split) >= 5:
                            # check if mentioned player is already in user data
                            if self.message.mentions[0].id in self.userlist:

                                # removing player (teamname, discordid)
                                LBT.remove_team(self.message_split[3], self.message.mentions[0].id)

                                messagetosend = ":ballot_box_with_check: removed user **" + \
                                                self.message.mentions[0].name + "** from the team: " + \
                                                self.message_split[3]
                                notexisting = False
                                break
                            else:
                                messagetosend = self.message.mentions[0].name + " isn't stored in my data."
                                notexisting = False
                                break

                    else:
                        notexisting = True

                if notexisting:
                    messagetosend = ":warning:  This team does not exist"

        return messagetosend

    def command_teams_create(self):
        # vars
        messagetosend = ":warning:  " + self.message.author.name + " you don't have permissions. Add yourself " \
                                                                   "first my database with `!logs addme <SteamID64>`"

        # check if author is in system
        user = LBU.get_player(self.message.author.id)
        if user:
            # if only typed: !logs teams create
            if self.message.content.lower() == '!logs teams create':
                messagetosend = ":information_source:  You can create a team by typing " \
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

                        messagetosend = ":ballot_box_with_check:  created team **" + name \
                                        + "** with the format: " + type
                    except ValueError:
                        # If type isn't a number
                        messagetosend = ":no_entry_sign:  format has to be a integer (6 = 6v6, 9 = 9v9 and so on)"

                else:
                    messagetosend = ":warning:  This team already exists."

            elif len(self.message_split) < 5:
                messagetosend = ":information_source:  You have to add the teams format " \
                                "(6 = 6v6, 9 = 9v9 and so on) after `!logs teams create " + \
                                self.message_split[3] + "` <format>"

        return messagetosend

    def command_teams_delete(self):
        # vars
        messagetosend = ":warning:  " + self.message.author.name + " you don't have permissions. Add yourself " \
                                                                   "first my database with `!logs addme <SteamID64>`"

        user = LBU.get_player(self.message.author.id)
        if user:
            # check if only !logs teams delete was typed
            if self.message.content.lower() == '!logs teams delete':
                messagetosend = ":information_source:  You can delete a team by typing `!logs teams delete` <teamname>"

            # if teamname is missing
            elif len(self.message_split) < 4:
                messagetosend = ":information_source:  You have to add the teamname"

            elif len(self.message_split) >= 4:
                messagetosend = ":warning: This team does not exist."

                # Check if team even exists
                teamname = self.message_split[3]
                team = LBT.get_team(self.message.server.id, teamname)

                if team:
                    if str(team["creator"]) == str(user["discord_id"]):
                        # deletes team (teamname)
                        LBT.delete_team(self.message.server.id, teamname)
                        messagetosend = ":ballot_box_with_check:  deleted team **" + teamname + "**"
                    else:
                        messagetosend = ":warning: This isn't your team."



        return messagetosend


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
            messagetosend = ":dart: " + self.message.author.name + "'s Log found\n\n**" + logtitle + \
                            "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n" + performance

        return messagetosend

    def command_logs_profile(self):
        # vars
        messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find you in my data."

        # check if user is in userdata
        user = LBU.get_player(self.message.author.id)
        if user:
            stored_data_msg = ":card_box:  __**" + self.message.author.name + "**__\n\n**SteamID64:**  `" \
                              + user["steam_id"] + "`\n**Steam:**  <http://steamcommunity.com/profiles/" + user[
                                  "steam_id"] + ">\n"

            # Getting newest 3 logs
            data = LBE.LogPlayerSearch(user["steam_id"], 3)

            # check if this is a real valid user
            if data["results"] != 0:
                # building message
                messagetosend2 = "\n\nLast 3 logs\n"
                # looping 3 logs with id, link, title, time and date
                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = LBE.totime(log["date"])
                    messagetosend2 = messagetosend2 + "**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + \
                                     logtime + "`\n\n"

                # building message
                messagetosend2 = messagetosend2 + ""
                messagetosend = stored_data_msg + "**logs.tf profile:**  <http://logs.tf/profile/" + \
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
            data = LBE.LogPlayerSearch(self.userlist[self.message.mentions[0].id], 1)
            # Getting log details
            logid = str(data["logs"][0]["id"])  # logid
            logtitle = str(data["logs"][0]["title"])  # log title
            logtime = LBE.totime(data["logs"][0]["date"])  # date and time of the log
            # getting player performance
            logiddetails = LBE.LogIDdetails(logid, steamid3)
            performance = LBE.PerformanceDisplay(1, logiddetails)

            # Message content
            messagetosend = ":mag_right: **" + mentionuser + "**'s Log found\n\n**" + logtitle\
                            + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n" + performance

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

            stored_data_msg = ":credit_card:  __**" + mentionuser + "**__\n\n**SteamID64:**  `" \
                              + user["steam_id"] + "`\n**Steam:**  <http://steamcommunity.com/profiles/" + \
                              user["steam_id"] + ">\n"

            # Getting newest 3 logs
            data = LBE.LogPlayerSearch(user["steam_id"], 3)

            # check if this is a real valid user
            if data["results"] != 0:
                # Building message
                messagetosend2 = "\n\nLast 3 logs\n"
                # inserting logs with link, title, date and time
                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = LBE.totime(log["date"])
                    messagetosend2 = messagetosend2 + "**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + \
                                     logtime + "`\n\n"

                # Building rest of the message
                messagetosend2 = messagetosend2 + ""
                messagetosend = stored_data_msg + "**logs.tf profile:**  <http://logs.tf/profile/" + \
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
            messagetosend = ":information_source:  You can get add or update your data. Just type after `!logs addme` <SteamID64>"

        else:
            # check if user already exist and rewrite or add user
            user = LBU.get_player(self.message.author.id)
            if user:
                addorupdate = "Updated"

            else:
                addorupdate = "Added"

            # grabs users (that has to be added) steam id 64
            addusersteamid64 = splitmessage[2]

            # adds user with discord id and steam id 64
            LBU.add_user(self.message.author.id, addusersteamid64)

            # Outputs Successfull Message
            messagetosend = ":ballot_box_with_check:  " + addorupdate + " yourself with the SteamID64: " \
                                "" + addusersteamid64

        return messagetosend
