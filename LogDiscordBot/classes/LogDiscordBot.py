# Log Bot
# Description: A discord bot showing your recent logs, profile page and team matches. You can create teams,
#              fill them with players and get recent matches of the teams. You can also search for other
#              persons logs and logs.tf profile's.
#
# creator: callFEELD
#          Website: https://callfeeld.jimdo.com/
#          Steam:   http://steamcommunity.com/id/callFEELD/
#          GitHub:  https://github.com/callFEELD
# Thank you Matthew (GitHub: https://github.com/Matthew-The-Mighty-Mouse-Madge) for the support
# last edit: 02.01.2017 (callFEELD)


# Import statements
import discord                      # accessing the discord.py library
import urllib.request, json         # used to handle separate json files and the logs.tf api
import datetime                     # used to convert timestamps
from collections import Counter     # used in the match searching algorithm

# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for teams
class LogBotTeams:
    # CONFIG
    # The databse file containing the users, moderators and teams
    teamfile = "users.json"
    teamlist = open(teamfile, "r").read()
    teamlist = json.loads(teamlist)

    def __init__(self):
        self.loadteams()

    # Loads the member list as json format and converts it into an object
    def loadteams(self):
        # opens file and load as json
        self.teamlist = open(self.teamfile, "r").read()
        self.teamlist = json.loads(self.teamlist)

    # Updates(reloads) the user file
    def update(self):
        self.loadteams()

    # saves the userlist to the users file
    def save(self):
        file = open(self.teamfile, "w")
        file.write(json.dumps(self.teamlist))

    # returns all teams in a list
    def getteams(self):
        self.update()
        return self.teamlist["teams"]

    # Adds a user to a team
    def add_team(self, teamname, discordid, playername):
        # Updates File to be perfectly save
        self.update()

        # add user with discordid and steamid to the teamlist
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1
        self.teamlist["teams"][arrayposition][teamname][1]["players"].update({discordid: playername})

        # save the new teamlist into the user file
        self.save()

    # remove a user of a team
    def remove_team(self, teamname, discordid):
        # Updates File to be perfectly save
        self.update()

        # remove user from a team
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1
        del self.teamlist["teams"][arrayposition][teamname][1]["players"][discordid]

        # save the updated teamlist into the user file
        self.save()

    # creates a team
    def create_team(self, teamname, type):
        # Updates File to be perfectly save
        self.update()

        # add team with name and type to the team list
        newteam = {teamname: [{"type": type}, {"players": {}}]}
        self.teamlist["teams"].append(newteam)

        # save the new team into the user file
        self.save()

    # deletes a team
    def delete_team(self, teamname):
        # Updates File to be perfectly save
        self.update()

        # deletes the team
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1

        del self.teamlist["teams"][arrayposition]

        # save the updated teamlist into the user file
        self.save()


# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for users and moderators
class LogBotUsers:
    # CONFIG
    # The databse file containing the users, moderators and teams
    userfile = "users.json"
    userlist = open(userfile, "r").read()
    userlist = json.loads(userlist)

    def __init__(self):
        self.loadusers()

    # Loads the member list as json format and converts it into an object
    def loadusers(self):
        # opens file and load as json
        self.userlist = open(self.userfile, "r").read()
        self.userlist = json.loads(self.userlist)

    # Updates(reloads) the user file
    def update(self):
        self.loadusers()

    # saves the userlist to the users file
    def save(self):
        file = open(self.userfile, "w")
        file.write(json.dumps(self.userlist))

    # returns all moderators in a list
    def getmoderators(self):
        self.update()
        return self.userlist["moderators"]

    # returns all players in a list
    def getplayers(self):
        self.update()
        return self.userlist["users"]

    def getplayers_steamid(self, discordid):
        # grabs playerlist
        playerlist = self.getplayers()
        return playerlist[discordid]

    # Adds a user
    def add_user(self, discordid, steamid):
        # Updates File to be perfectly save
        self.update()

        # add user with discordid and steamid to the userlist
        self.userlist["users"].update({discordid: steamid})

        # save the new userlist into the user file
        self.save()

    # remove a user
    def remove_user(self, discordid):
        # Updates File to be perfectly save
        self.update()

        # remove user from userlist
        del self.userlist["users"][discordid]

        # save the new userlist into the user file
        self.save()


# This Class containing important functions that will be used in other Classes
class LogBotEssentials:
    client = discord.Client()

    # Load the CONFIG
    config = open("config.json", "r").read()
    config = json.loads(config)
    # version number of the bot
    version = config["version"]
    # nickname of the bot
    USERNAME = config["username"]
    # Playing/Game Status
    PLAYING_STATUS = config["playing_status"]

    # Minimum amount of players that a match is defined as a match
    # 6s
    sixes_min_players = config["sixes_min_players"]
    # Highlander
    hl_min_players = config["hl_min_players"]
    # 4s
    fours_min_players = config["fours_min_players"]
    # Ultiduo
    duo_min_players = config["duo_min_players"]
    # Amount of logs of a player that will be scanned to get a match
    AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER = config["amount_of_logs_searched_per_player"]


    #Variables
    userlist = LogBotUsers().getplayers()
    moderators = LogBotUsers().getmoderators()

    def update(self):
        self.userlist = LogBotUsers().getplayers()
        self.moderators = LogBotUsers().getmoderators()


    #Returning Logdetails of an player from a logid
    def LogIDdetails(self, logid, steamid3):
        #going on the Logs.tf APi and search for the logid
        with urllib.request.urlopen("http://logs.tf/json/" + str(logid)) as url:
            data = json.loads(url.read().decode())

            # when player is in the log output his performance
            if steamid3 in data["players"]:

                # get the classes the player played and sort them after playtime
                classes_data = {}
                for class_stat in data["players"][steamid3]["class_stats"]:
                    class_name = class_stat["type"]
                    playtime = class_stat["total_time"]

                    classes_data[class_name] = playtime

                #sort the classes after playtime
                sorted(classes_data.keys())

                # get stats
                kills = str(data["players"][steamid3]["kills"])
                deaths = str(data["players"][steamid3]["deaths"])
                assists = str(data["players"][steamid3]["assists"])
                kpd = str(data["players"][steamid3]["kpd"])
                kapd = str(data["players"][steamid3]["kapd"])
                dpm = str(data["players"][steamid3]["dapm"])
                dmg = str(data["players"][steamid3]["dmg"])
                dt = str(data["players"][steamid3]["dt"])
                hr = str(data["players"][steamid3]["hr"])
                airs = str(data["players"][steamid3]["as"])

                #med stats if he is medic
                #wip

                #get heals percentage
                team_of_player = str(data["players"][steamid3]["team"]) #get players team
                sum_of_heals = 0
                for player in data["players"]:
                    if data["players"][player]["team"] == team_of_player:
                        sum_of_heals = sum_of_heals + data["players"][player]["hr"]

                heal_perc = round((int(hr)/sum_of_heals) * 100, 2)
                heal_perc = str(heal_perc)

                returnobject = {"kills": kills, "deaths": deaths, "kd": kpd, "dpm": dpm, "dt": dt, "hr": hr,
                                "assists": assists, "kapd": kapd, "dmg": dmg, "as": airs, "heal_perc": heal_perc, \
                                "classes": classes_data, "playerinlog": True}
                return returnobject
            else:
                returnobject = {"playerinlog": False}
                return returnobject


    #Retruns a Player Log.tf search, by inputting steamid64 and a log limit
    def LogPlayerSearch(self, steamid64, limit):
        # going on the Logs.tf APi and search for the player with a limit
        with urllib.request.urlopen("http://logs.tf/json_search?player=" + steamid64 + "&limit=" + str(limit)) as url:
            data = json.loads(url.read().decode())
        return data


    #Returns String with performance details
    def PerformanceDisplay(self, yourorplayer, statsobject):
        #Variables
        returnvar = ""

        if yourorplayer == 0:
            title = "Your performance"
        elif yourorplayer == 1:
            title = "Player's performance"
        else:
            title = "Performance"


        #Only shows performance details if plaer is in the log
        if statsobject["playerinlog"]:

            # show played classes (sorted after playtime)
            played_classes_msg = ""
            for played_class in statsobject["classes"].keys():
                played_classes_msg = played_classes_msg + str(played_class) + "  "

            returnvar = "```classes played: " +played_classes_msg + "\n\n"\
                        "kills: " + statsobject["kills"] + ",   deaths: " + statsobject["deaths"] + ",   assists: " + statsobject["assists"] +"\n\n" \
                        "k/d: " + statsobject["kd"] + ",   ka/d: " + statsobject["kapd"] + "\n\n" \
                        "dpm: " + statsobject["dpm"] + ",   dmg: " + statsobject["dmg"] + "\n\n" \
                        "heals: " + statsobject["heal_perc"] + "%,   as: " + statsobject["as"] + "```"
        #Returning
        return returnvar


    #find the newsest team match
    def findMatch(self, minplayers, numoflogs, format, team, message):
        #update the database
        self.update()

        # minplayers: minimal amount of players to be a match
        # numoflogs: amount of logs that should be checked for each player
        # fomrat: either 6 or 9 to represent 6s or HL
        checklogs = {}
        checklogstitle = {}
        checklogids = []

        # mention statement for the name of the user that is accessing the bot
        mentionuserid = "<@" + str(message.author.id) + ">"

        # Steam ID64 and Steam ID3 of the author
        steamid64 = LogBotUsers().getplayers_steamid(message.author.id)
        steamid3 = LogBotEssentials().tosteamid3(steamid64)

        # Go trough all Players of the Team
        for player in team.keys():
            playersteamid = self.userlist[player]

            data = self.LogPlayerSearch(playersteamid, str(numoflogs))
            logids = data["logs"]

            for logid in logids:
                checklogs.update({logid["id"]: logid["date"]})
                checklogstitle.update({logid["id"]: logid["title"]})
                checklogids.append(logid["id"])


        sortedlogidsbyamount = Counter(checklogids)
        print(sortedlogidsbyamount)
        sortedlogsbytime = sorted(checklogs.keys(), reverse=True)
        print(sortedlogsbytime)

        # Get the log with the most amount and the highest time
        for i in sortedlogsbytime:
            # if log is above minplayers and not higher than 9
            if (sortedlogidsbyamount[i] >= minplayers and sortedlogidsbyamount[i] <= int(format)):
                matchid = i
                logtime = LogBotEssentials().totime(checklogs[matchid])

                logdetails = self.LogIDdetails(matchid, steamid3)
                performance = self.PerformanceDisplay(0, logdetails)

                return ":trophy: match found\n**" + str(checklogstitle[matchid]) + "**\n" + str(logtime) + "\n\n<http://logs.tf/" + str(matchid) + ">" + performance

                LogBotEssentials().consoleOutput(self.message.author.id, self.message, messagetosend)
                break


    # Converts the SteamID64 into a SteamID3 (as a string)
    def tosteamid3(self, id):
        y = int(id) - 76561197960265728
        x = y % 2
        if len(id) == 17:
            id32 = int(id[3:]) - 61197960265728
            return "[U:1:" + str(id32) + "]"
        else:
            return False


    # Makes a timestamp better readable
    def totime(self, timestamp):
        return str(datetime.datetime.fromtimestamp(int(str(timestamp))).strftime('%d-%m-%Y %H:%M:%S'))


    # Console output of the users id that was accessing the bot and the bots output
    def consoleOutput(self, userid, message, outputmessage):
        print("[+]  [command]       " + message.content.lower())
        print("     [author]        " + str(message.author.id))
        print("     [output]        " + str(outputmessage.split(" ")))
        print("\n")


# This Class handles and contain every command.
class LogBotCommands:
    message = {}
    message_content = []
    message_author_id = []
    userlist = []
    teamlist = []
    moderators = LogBotUsers().getmoderators()
    client = discord.Client()

    def update(self):
        # loading users and teams of the files
        self.teamlist = LogBotTeams().getteams()
        self.userlist = LogBotUsers().getplayers()
        self.moderators = LogBotUsers().getmoderators()


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
            self.userlist = LogBotUsers().getplayers()
            self.moderators = LogBotUsers().getmoderators()
            self.teamlist = LogBotTeams().getteams()

            if message.author.id in self.userlist:
                # Steam ID64 and Steam ID3 of the author
                steamid64 = LogBotUsers().getplayers_steamid(message.author.id)
                steamid3 = LogBotEssentials().tosteamid3(steamid64)

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

        #If user is mod, show that command !logs modhelp exists
        if self.message.author.id in self.moderators:
           modhelp = "\nYou are a Moderator, type `!logs modhelp` to get moderator commands"

        #Message that will be sended
        messagetosend = ":information_source:  __**Commands**__" + modhelp+ \
        "\n\n`!logs`\nshows your last played match with details about your performance" \
        "\n`!logs profile`\nshows your logs.tf profile" \
        "\n\n`!logs <@name>`\nshows the last log of the player you looked for" \
        "\n`!logs <@name> profile`\nshows the logs.tf profile of the player you looked for" \
        "\n\n`!logs match <teamname>`\nshows the latest match (scrim, lobby, official) of a team with details " \
        "about your performance" \
        "\n`!logs teams`\nshows the available teams" \
        "\n`!logs teams <teamname> players`\nshows the players in the team" \
        "\n\n`version: "+LogBotEssentials.version+"`"

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
                            "\n\n`version: " + LogBotEssentials.version + "`"
        #Output
        return messagetosend


    # COMMAND: !logs version
    def command_version(self):
        messagetosend = "`" + LogBotEssentials.version + "`"
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
                        minplayer = LogBotEssentials().sixes_min_players
                    #HL
                    elif team[teamname][0]["type"] == "9":
                        minplayer = LogBotEssentials().hl_min_players
                    #4s
                    elif team[teamname][0]["type"] == "4":
                        minplayer = LogBotEssentials().fours_min_players
                    #Duo
                    elif team[teamname][0]["type"] == "2":
                        minplayer = LogBotEssentials().duo_min_players

                    #check if the team has the minumum of players
                    #get the amount of players
                    team_player_amount = 0
                    for player in team[teamname][1]["players"].values():
                        team_player_amount += 1

                    if team_player_amount >= minplayer:
                        #Search for the newest match of the team
                        messagetosend = LogBotEssentials().findMatch(minplayer, LogBotEssentials().AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER, team[teamname][0]["type"], team[teamname][1]["players"], self.message)
                        if(messagetosend==None):
                            messagetosend=":hushed:  I cloudn't find any matches of the team **'"+teamname+"'**\n" \
                                          "Probably your team didn't played together for quite some time.\n\n" \
                                          "__**Background information**__\n" \
                                          "It depends on the amount of logs that going to be scanned by me. __Maybe my" \
                                          " config should be adjusted a little bit. Contact the admin for that.__\n" \
                                          "Currently I am checking the latest `"+str(LogBotEssentials().AMOUNT_OF_LOGS_SEARCHED_PER_PLAYER)+"`" \
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
            if len(self.teamlist) > 0:
                messagetosend = messagetosend + "Here are all teams I stored:\n"
                for team in self.teamlist:
                    messagetosend = messagetosend +"`"+ str(team.keys()).split("'")[1]+"`   "
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
                                        LogBotTeams().add_team(messagesplit[3], self.message.mentions[0].id, messagesplit[5])

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
                                        LogBotTeams().remove_team(messagesplit[3], self.message.mentions[0].id)

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
                messagetosend = ":warning:  " + self.message.author.name + " you don't have permissions."
                messagesplit = self.message.content.lower().split(' ')

                #check if author is moderator
                if self.message.author.id in self.moderators:
                    #if only typed: !logs teams create
                    if self.message.content.lower() == '!logs teams create':
                        messagetosend = ":information_source:  You can create a team by typing `!logs teams create` <teamname> <format>"

                    #check if team already exists
                    # Checks to see if the provided team name already exists
                    elif len(self.teamlist) == 0:
                        # No teams exist, name is original
                        notexisting = True
                    else:
                        # Compare provided name with all stored names
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                messagetosend = ":warning:  This team already exists."
                                notexisting = False
                                break
                            else:
                                notexisting = True

                    if 'notexisting' in locals():
                        #if its not existing, create one
                        if notexisting and len(messagesplit) >= 5:
                            # Check if last value is an int
                            try:
                                format = int(messagesplit[4])

                                # create a new team (teamname, type)
                                LogBotTeams().create_team(messagesplit[3],messagesplit[4])

                                messagetosend = ":ballot_box_with_check:  created team **" + messagesplit[
                                                3] + "** with the format: " + messagesplit[4]

                            except ValueError:
                                #If type isn't a number
                                messagetosend = ":no_entry_sign:  format has to be a integer (6 = 6v6, 9 = 9v9 and so on)"

                        elif len(messagesplit) <= 5 and notexisting:
                            messagetosend = ":information_source:  You have to add the teams format (6 = 6v6, 9 = 9v9 and so on) after `!logs teams create " + \
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
                            LogBotTeams().delete_team(messagesplit[3])

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
                        LogBotUsers().add_user(self.message.mentions[0].id, addusersteamid64)

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
                        LogBotUsers().remove_user(self.message.mentions[0].id)

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
            if self.message.author.id in self.userlist:
                # Then grab data of the player
                # Get the newest log of the player
                data = LogBotEssentials().LogPlayerSearch(self.userlist[self.message.author.id], 1)
                # Getting data of the log
                logid = str(data["logs"][0]["id"]) #Logid
                logtitle = str(data["logs"][0]["title"]) #Title of the log
                logtime = LogBotEssentials().totime(data["logs"][0]["date"]) # date and time of the log
                steamid3 = LogBotEssentials().tosteamid3(self.userlist[self.message.author.id])

                #Grabbing player performance
                logiddetails = LogBotEssentials().LogIDdetails(logid, steamid3)
                performance = LogBotEssentials().PerformanceDisplay(0, logiddetails)

                #Message content
                messagetosend = ":dart: " + self.message.author.name + "'s Log found\n\n**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n" + performance

        # Check if command: !logs profile is called
        if self.message.content.lower() == '!logs profile':
            #vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find you in my data."


            #check if user is in userdata
            if self.message.author.id in self.userlist:

                stored_data_msg = ":card_box:  __**"+ self.message.author.name +"**__\n\n**SteamID64:**  `" \
                                  + self.userlist[self.message.author.id] + "`\n**Steam:**  <http://steamcommunity.com/profiles/"+ self.userlist[self.message.author.id] +">\n"

                # Getting newest 3 logs
                data = LogBotEssentials().LogPlayerSearch(self.userlist[self.message.author.id], 3)

                #check if this is a real valid user
                if data["results"] != 0:
                    #building message
                    messagetosend2 = "\n\nLast 3 logs\n"
                    # looping 3 logs with id, link, title, time and date
                    for log in data["logs"]:
                        logid = str(log["id"])
                        logtitle = str(log["title"])
                        logtime = LogBotEssentials().totime(log["date"])
                        messagetosend2 = messagetosend2 + "**" + logtitle +"**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n\n"

                    #building message
                    messagetosend2 = messagetosend2 + ""
                    messagetosend = stored_data_msg + "**logs.tf profile:**  <http://logs.tf/profile/" + \
                                        self.userlist[self.message.author.id] + ">" + messagetosend2
                else:
                    messagetosend = stored_data_msg + ":warning:  Looks like that this steamid does not exits, change it by type `!logs addme <steamid>`"



        # Check if command: !logs @mention is called
        elif len(self.message.mentions) != 0 and not self.message.content.lower().endswith('profile') and not len(splitmessage) >= 3:
            #vars
            mentionuser = str(self.message.mentions[0].name)
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find **" + mentionuser + "** in my data."

            # Checks if called player is in userdata
            if self.message.mentions[0].id in self.userlist:

                # grabbing steam ids of the player
                steamid64 = self.userlist[self.message.mentions[0].id]
                steamid3 = LogBotEssentials().tosteamid3(steamid64)

                # grabbing newst log of the player
                data = LogBotEssentials().LogPlayerSearch(self.userlist[self.message.mentions[0].id], 1)
                # Getting log details
                logid = str(data["logs"][0]["id"]) #logid
                logtitle = str(data["logs"][0]["title"]) # log title
                logtime = LogBotEssentials().totime(data["logs"][0]["date"]) # date and time of the log
                # getting player performance
                logiddetails = LogBotEssentials().LogIDdetails(logid, steamid3)
                performance = LogBotEssentials().PerformanceDisplay(1, logiddetails)

                # Message content
                messagetosend = ":mag_right: **" + mentionuser + "**'s Log found\n\n**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n" + performance


        # Checking for command: !logs @mention profile
        elif not len(self.message.mentions) == 0 and len(splitmessage) >= 3 and self.message.content.lower().endswith('profile'):
            #Vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find **" + str(
            self.message.mentions[0].name) + "** in my data."

            #checks if mentioned player is in the user data
            if self.message.mentions[0].id in self.userlist:
                # Grabbing steam ids and name
                steamid64 = self.userlist[self.message.mentions[0].id]
                steamid3 = LogBotEssentials().tosteamid3(steamid64)
                mentionuser = str(self.message.mentions[0].name)

                stored_data_msg = ":credit_card:  __**" + mentionuser + "**__\n\n**SteamID64:**  `" \
                                  + self.userlist[self.message.mentions[0].id] + "`\n**Steam:**  <http://steamcommunity.com/profiles/" + \
                                  self.userlist[self.message.mentions[0].id] + ">\n"

                # Getting newest 3 logs
                data = LogBotEssentials().LogPlayerSearch(self.userlist[self.message.mentions[0].id], 3)

                # check if this is a real valid user
                if data["results"] != 0:
                    # Building message
                    messagetosend2 = "\n\nLast 3 logs\n"
                    #inserting logs with link, title, date and time
                    for log in data["logs"]:
                        logid = str(log["id"])
                        logtitle = str(log["title"])
                        logtime = LogBotEssentials().totime(log["date"])
                        messagetosend2 = messagetosend2 + "**" + logtitle + "**\n<http://logs.tf/" + logid + ">\n`" + logtime + "`\n\n"

                    #Building rest of the message
                    messagetosend2 = messagetosend2 + ""
                    messagetosend = stored_data_msg + "**logs.tf profile:**  <http://logs.tf/profile/" + \
                                    self.userlist[self.message.mentions[0].id] + ">" + messagetosend2
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
            if self.message.author.id in self.userlist:
                addorupdate = "Updated"

            else:
                addorupdate = "Added"

            # grabs users (that has to be added) steam id 64
            addusersteamid64 = splitmessage[2]

            # adds user with discord id and steam id 64
            LogBotUsers().add_user(self.message.author.id, addusersteamid64)

            # Outputs Successfull Message
            messagetosend = ":ballot_box_with_check:  " + addorupdate + " yourself with the SteamID64: " \
                                "" + addusersteamid64

        return messagetosend
