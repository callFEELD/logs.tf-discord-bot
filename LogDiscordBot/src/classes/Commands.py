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
    message_content = []
    message_author_id = []
    userlist = []
    teamlist = []
    moderators = LBU.getmoderators()
    client = discord.Client()

    def update(self):
        # loading users and teams of the files
        self.teamlist = None
        self.userlist = LBU.getplayers()
        self.moderators = LBU.getmoderators()


    def scan(self, message):
        #Grab important informations of message
        #self.message_content = message.content.lower()
        #self.message_author_id = message.author.id()
        self.message = message

        # load the users data if a message hits and contains LDB commands
        if (message.content.lower().find("!logs") != -1):

            # Loads the member list as json format and converts it into an object
            self.update()

            # loading users of the members list
            self.userlist = LBU.getplayers()
            self.moderators = LBU.getmoderators()

            if message.author.id in self.userlist:
                # Steam ID64 and Steam ID3 of the author
                steamid64 = LBU.getplayers_steamid(message.author.id)
                steamid3 = LBE.tosteamid3(steamid64)

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
                return self.command_teams()

            # COMMAND: !logs user
            if message.content.lower().startswith('!logs user'):
                return self.command_user()

            # COMMAND: !logs addme
            if message.content.lower().startswith('!logs addme'):
                return self.command_logs_addme()

            # Only use for dev
            # COMMAND: !logs debug
            #if message.content.lower().startswith('!logs debug'):
                #return self.command_debug()

            # COMMAND: !logs
            # IMPORTANT: THIS COMMAND HAS THE BE THE LAST ONE, IF NOT IT CREATES ERRORS
            if message.content.lower().startswith('!logs'):
                return self.command_logs()


    # COMMAND: !logs help
    def command_debug(self):
        # Message that will be sended
        messagetosend = ":information_source:  __**Debug Console**__\n\n"

        messagetosend = messagetosend + "Your Discord ID: " + str(self.message.author.id) + "\n\n"

        messagetosend = messagetosend + "Teamlist: " + str(self.teamlist) + "\n\n"

        messagetosend = messagetosend + "Userlist: " + str(self.userlist) + "\n\n"

        messagetosend = messagetosend + "Modlist: " + str(self.moderators) + ""

        # sending message
        return messagetosend


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
        #sending message
        #messagetosend = str()

        return messagetosend


    # COMMAND: !logs modhelp
    def command_modhelp(self):
        #Variables
        messagetosend = "You don't have permission."

        #Check if message author is a moderator
        if self.message.author.id in self.moderators:
            messagetosend = ":information_source:  __**Moderator commands**__\n\n`!logs user add <@name> <SteamID64>`\nto add a player to the system with his/her " \
                            "SteamID64. This command can also be used to update a player's SteamID64." \
                            "\n`!logs user remove <@name>`\nremoves the player from the system." \
                            "\n\n`!logs teams create <teamname> <format>`\nCreates a new team. Format is the type of " \
                            "the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on). WIP" \
                            "\n`!logs teams delete <teamname>`\nRemoves a team from the system. WIP" \
                            "\n\n`!logs teams add <teamname> <@name> <name>`\nStores a player with a specific name " \
                            "into a team." \
                            "\n`!logs teams remove <teamname> <@name>`\nRemoves a player from a team." \
                            "\n\n`version: " + LBE.version + "`"
        #Output
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


    # Command: !logs teams
    def command_teams(self):
        if self.message.content.lower() == "!logs teams":
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

        if self.message.content.lower().startswith('!logs teams'):
            # split message to get all parts
            messagesplit = self.message.content.lower().split(' ')

            # check if command: !logs teams <teamname> players
            if self.message.content.lower().endswith('players') and len(messagesplit) == 4:
                #vars
                messagetosend = ":warning:  This team does not exist"

                for team in self.teamlist:
                    if messagesplit[2] in team:

                        messagetosend = ":space_invader:  **Team: '" + messagesplit[2] + "' player's**\n"
                        num = 0
                        for player in team[messagesplit[2]][1]["players"].values():
                            messagetosend += "`"+player + "`   "
                            num += 1

                        messagetosend += "(amount: " + str(num) + ")"

                        # if the teams dont have players, create a tip to add them
                        if num == 0:
                            messagetosend += "\n\nYou can add players to the team with the command `!logs teams add "+messagesplit[2]+" <@name> <name>`"

                        notexisting = False

            # check for COMMANDS !logs teams add
            if self.message.content.lower().startswith('!logs teams add'):
                #vars
                messagetosend = self.message.author.name + " you don't have permissions."
                messagesplit = self.message.content.lower().split(' ')

                #check if author is moderator
                if self.message.author.id in self.moderators:
                    #check if he only typed: !logs teams add
                    if self.message.content.lower() == '!logs teams add':
                        messagetosend = ":information_source: You can add or update a player to/of a team by typing `!logs teams add` <teamname> <@player> <Name>"

                    else:
                        #check if 4th position is not a team
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                if not len(messagesplit) >= 6:
                                    if len(messagesplit) == 5:
                                        messagetosend = ":information_source: add the name after your command `" + self.message.content.lower() + "`  <Name>"

                                    else:
                                        messagetosend = ":information_source: add the user and the name after your command `" + self.message.content.lower() + "` <@player> <Name>"
                                    notexisting = False
                                    break

                                #if its a team
                                elif len(self.message.mentions) != 0 and len(messagesplit) >= 6:
                                    #check if user that should be added is in userdata
                                    if self.message.mentions[0].id in self.userlist:
                                        #check if mention player is already in the team
                                        if self.message.mentions[0].id in team[messagesplit[3]][1]["players"].values():
                                            addorupdate = "Updated"

                                        else:
                                            addorupdate = "Added"

                                        # adding player with to team: teamname, discordid, playername
                                        LBT.add_team(messagesplit[3], self.message.mentions[0].id, messagesplit[5])

                                        messagetosend = ":ballot_box_with_check: " + addorupdate + " user **" + \
                                                                    self.message.mentions[0].name + "** with the name: " + \
                                                                    messagesplit[5]
                                        notexisting = False
                                        break
                                    else:
                                        messagetosend = ":warning:  "+self.message.mentions[0].name + " isn't stored in my data.\nFirst you have to add him with the command: `!logs user add <@user> <SteamID64>`"
                                        notexisting = False
                                        break

                            else:
                                notexisting = True

                        if notexisting:
                            messagetosend = "This team does not exist"

                else:
                    messagetosend = self.message.author.name + " you don't have permissions."


            # COMMANDS !logs teams remove
            if self.message.content.lower().startswith('!logs teams remove'):
                #vars
                messagetosend = self.message.author.name + " you don't have permissions."
                messagesplit = self.message.content.lower().split(' ')

                # check if author is moderator
                if self.message.author.id in self.moderators:
                    # check if only: !logs teams remove is called
                    if self.message.content.lower() == '!logs teams remove':
                        messagetosend = ":information_source: You can remove a player of a team by typing `!logs teams remove` <teamname> <@player>"

                    else:
                        #else find the team name and if the team exists
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                if not len(messagesplit) >= 5:
                                    # check if enough inputs are granted
                                    if len(messagesplit) == 4:
                                        messagetosend = ":information_source: add the player after your command `" + self.message.content.lower() + "`  <@player>"

                                    notexisting = False
                                    break

                                # if it has enough data
                                elif len(self.message.mentions) != 0 and len(messagesplit) >= 5:
                                    #check if mentioned player is already in user data
                                    if self.message.mentions[0].id in self.userlist:

                                        #removing player (teamname, discordid)
                                        LBT.remove_team(messagesplit[3], self.message.mentions[0].id)

                                        messagetosend = ":ballot_box_with_check: removed user **" + \
                                                                self.message.mentions[0].name + "** from the team: " + \
                                                                messagesplit[3]
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


            # COMMANDS !logs teams create
            if self.message.content.lower().startswith('!logs teams create'):
                #vars
                messagetosend = ":warning:  " + self.message.author.name + " you don't have permissions. Add yourself "\
                                "first my database with `!logs addme <SteamID64>`"
                messagesplit = self.message.content.lower().split(' ')

                #check if author is in system
                user = LBU.get_player(self.message.author.id)
                if user:
                    #if only typed: !logs teams create
                    if self.message.content.lower() == '!logs teams create':
                        messagetosend = ":information_source:  You can create a team by typing "\
                                        "`!logs teams create` <teamname> <format>"

                    # check if the command is correct
                    elif len(messagesplit) >= 5:
                        name = messagesplit[3]
                        type = messagesplit[4]
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

                    elif len(messagesplit) < 5:
                        messagetosend = ":information_source:  You have to add the teams format "\
                                        "(6 = 6v6, 9 = 9v9 and so on) after `!logs teams create " + \
                                            messagesplit[3] + "` <format>"



            # COMMANDS !logs teams delete
            if self.message.content.lower().startswith('!logs teams delete'):
                #vars
                messagetosend = ":warning:  " + self.message.author.name + " you don't have permissions."
                messagesplit = self.message.content.lower().split(' ')

                #check if author is mod
                if self.message.author.id in self.moderators:
                    #check if only !logs teams delete was typed
                    if self.message.content.lower() == '!logs teams delete':
                        messagetosend = ":information_source:  You can delete a team by typing `!logs teams delete` <teamname>"

                    else:
                        #Check if team even exists
                        notexisting = False
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                notexisting = False
                                break

                            else:
                                messagetosend = ":warning:  This team does not exist."
                                notexisting = True

                        #if its existing, delete it
                        if not notexisting and len(messagesplit) >= 4:

                            #deletes team (teamname)
                            LBT.delete_team(messagesplit[3])

                            messagetosend = ":ballot_box_with_check:  deleted team **" + messagesplit[
                                        3] + "**"

                        #if teamname is missing
                        elif len(messagesplit) <= 4 and not notexisting:
                            messagetosend = ":information_source:  You have to add the teamname"


        #sending message
        return messagetosend


    # COMMAND: !logs user
    def command_user(self):
        #check if its !logs user add
        if self.message.content.lower().startswith('!logs user add'):
            #vars
            splitmessage = self.message.content.lower().split(' ')
            messagetosend = self.message.author.name + " you don't have permissions."

            #check if author is mod
            if self.message.author.id in self.moderators:

                #check if only typed: !Logs user add
                if self.message.content.lower() == '!logs user add':
                    messagetosend = ":information_source:  You can get add or update players. Just type after `!logs user add` <@name> <SteamID64>"

                else:
                    #check if steamid missing
                    if not len(splitmessage) == 5:
                        messagetosend = ":information_source: add the SteamID64 after the mention statement `" + self.message.content.lower() + "` <SteamID64>"

                    else:
                        # check if user already exist and rewrite or add user
                        if self.message.mentions[0].id in self.userlist:
                            addorupdate = "Updated"

                        else:
                            addorupdate = "Added"

                        # grabs users (that has to be added) steam id 64
                        addusersteamid64 = splitmessage[4]

                        # adds user with discord id and steam id 64
                        LBU.add_user(self.message.mentions[0].id, addusersteamid64)

                        # Outputs Successfull Message
                        messagetosend = ":ballot_box_with_check: " + addorupdate + " user **" + self.message.mentions[
                            0].name + "** with the SteamID64: " + addusersteamid64

            return messagetosend


        # check for COMMAND: !logs user remove
        if self.message.content.lower().startswith('!logs user remove'):
            #vars
            splitmessage = self.message.content.lower().split(' ')
            messagetosend = self.message.author.name + " you don't have permissions."

            #check if author is mod
            if self.message.author.id in self.moderators:
                #check if only typed: !Logs user remove
                if self.message.content.lower() == '!logs user remove':
                    messagetosend = ":information_source: You can remove players.\nJust type after `!logs user remove` <@name> <SteamID64>"

                else:
                    # remove user
                    if len(splitmessage) == 4:
                        # removes user with discord id (message.mentions[0].id)
                        LBU.remove_user(self.message.mentions[0].id)

                        # Outputs Succsessfully message
                        messagetosend = ":ballot_box_with_check:  removed user " + self.message.mentions[
                            0].name

            return messagetosend


    # Command: !logs
    def command_logs(self):
        #splits message to get every input
        splitmessage = self.message.content.lower().split(" ")

        #checks if only command: !logs is needed
        if self.message.content.lower() == '!logs':
            #initilaize vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but I didn't find you in my data.\n" \
                            "But you can add yourself to the system by adding your Steam ID 64.\n" \
                            "use the command `!logs addme <SteamID64>`"

            #checks if author is registerd in the user file
            user = LBU.get_player(self.message.author.id)
            if user:
                # Then grab data of the player
                # Get the newest log of the player
                data = LBE.LogPlayerSearch(user["steam_id"], 1)
                # Getting data of the log
                logid = str(data["logs"][0]["id"]) #Logid
                logtitle = str(data["logs"][0]["title"]) #Title of the log
                logtime = LBE.totime(data["logs"][0]["date"]) # date and time of the log
                steamid3 = LBE.tosteamid3(user["steam_id"])

                #Grabbing player performance
                logiddetails = LBE.LogIDdetails(logid, steamid3)
                performance = LBE.PerformanceDisplay(0, logiddetails)

                #Message content
                messagetosend = ":dart: " + self.message.author.name + "'s Log found\n\n**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n" + performance

        # Check if command: !logs profile is called
        if self.message.content.lower() == '!logs profile':
            #vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find you in my data."


            #check if user is in userdata
            user = LBU.get_player(self.message.author.id)
            if user:
                stored_data_msg = ":card_box:  __**"+ self.message.author.name +"**__\n\n**SteamID64:**  `" \
                                  + user["steam_id"] + "`\n**Steam:**  <http://steamcommunity.com/profiles/"+ user["steam_id"] +">\n"

                # Getting newest 3 logs
                data = LBE.LogPlayerSearch(user["steam_id"], 3)

                #check if this is a real valid user
                if data["results"] != 0:
                    #building message
                    messagetosend2 = "\n\nLast 3 logs\n"
                    # looping 3 logs with id, link, title, time and date
                    for log in data["logs"]:
                        logid = str(log["id"])
                        logtitle = str(log["title"])
                        logtime = LBE.totime(log["date"])
                        messagetosend2 = messagetosend2 + "**" + logtitle +"**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n\n"

                    #building message
                    messagetosend2 = messagetosend2 + ""
                    messagetosend = stored_data_msg + "**logs.tf profile:**  <http://logs.tf/profile/" + \
                                        user["steam_id"] + ">" + messagetosend2
                else:
                    messagetosend = stored_data_msg + ":warning:  Looks like that this steamid does not exits, change it by type `!logs addme <steamid>`"



        # Check if command: !logs @mention is called
        elif len(self.message.mentions) != 0 and not self.message.content.lower().endswith('profile') and not len(splitmessage) >= 3:
            #vars
            mentionuser = str(self.message.mentions[0].name)
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find **" + mentionuser + "** in my data."

            # Checks if called player is in userdata
            user = LBU.get_player(self.message.mentions[0].id)
            if user:
                # grabbing steam ids of the player
                steamid64 = user["steam_id"]
                steamid3 = LBE.tosteamid3(steamid64)

                # grabbing newst log of the player
                data = LBE.LogPlayerSearch(self.userlist[self.message.mentions[0].id], 1)
                # Getting log details
                logid = str(data["logs"][0]["id"]) #logid
                logtitle = str(data["logs"][0]["title"]) # log title
                logtime = LBE.totime(data["logs"][0]["date"]) # date and time of the log
                # getting player performance
                logiddetails = LBE.LogIDdetails(logid, steamid3)
                performance = LBE.PerformanceDisplay(1, logiddetails)

                # Message content
                messagetosend = ":mag_right: **" + mentionuser + "**'s Log found\n\n**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n" + performance


        # Checking for command: !logs @mention profile
        elif not len(self.message.mentions) == 0 and len(splitmessage) >= 3 and self.message.content.lower().endswith('profile'):
            #Vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find **" + str(
            self.message.mentions[0].name) + "** in my data."

            #checks if mentioned player is in the user data
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
                    #inserting logs with link, title, date and time
                    for log in data["logs"]:
                        logid = str(log["id"])
                        logtitle = str(log["title"])
                        logtime = LBE.totime(log["date"])
                        messagetosend2 = messagetosend2 + "**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n\n"

                    #Building rest of the message
                    messagetosend2 = messagetosend2 + ""
                    messagetosend = stored_data_msg + "**logs.tf profile:**  <http://logs.tf/profile/" + \
                                    user["steam_id"] + ">" + messagetosend2
                else:
                    messagetosend = stored_data_msg + ":warning:  Looks like that this steamid does not exits."

        # sending result
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
