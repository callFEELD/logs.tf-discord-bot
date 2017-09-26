import discord
import urllib.request, json
import datetime
from collections import Counter

class LogBotTeams:
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
        self.teamlist.append(newteam)

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



class LogBotUsers:
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
        return self.userlist["moderators"]

    # returns all players in a list
    def getplayers(self):
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
        self.userlist["players"].update({discordid: steamid})

        # save the new userlist into the user file
        self.save()

    # remove a user
    def remove_user(self, discordid):
        # Updates File to be perfectly save
        self.update()

        # remove user from userlist
        del self.userlist["players"][discordid]

        # save the new userlist into the user file
        self.save()


class LogBotEssentials:
    client = discord.Client()

    version = "1.1"
    USERNAME = "logs.tf"
    PLAYING_STATUS = "type !logs help"

    sixes_min_players = 5
    hl_min_players = 7
    fours_min_players = 3
    duo_min_players = 2


    #Variables
    userlist = LogBotUsers().getplayers()
    moderators = LogBotUsers().getmoderators()


    #Returning Logdetails of an player from a logid
    def LogIDdetails(self, logid, steamid3):
        #going on the Logs.tf APi and search for the logid
        with urllib.request.urlopen("http://logs.tf/json/" + str(logid)) as url:
            data = json.loads(url.read().decode())

            # when player is in the log output his performance
            if steamid3 in data["players"]:
                kills = str(data["players"][steamid3]["kills"])
                deaths = str(data["players"][steamid3]["deaths"])
                kpd = str(data["players"][steamid3]["kpd"])
                dpm = str(data["players"][steamid3]["dapm"])

                returnobject = {"kills": kills, "deaths": deaths, "kd": kpd, "dpm": dpm, "playerinlog": True}
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

            returnvar = "```" + title + "\n" \
                        "----------------\n" \
                        "kills: " + statsobject["kills"] + "\n" \
                        "deaths: " + statsobject["deaths"] + "\n" \
                        "k/d: " + statsobject["kd"] + "\n" \
                        "dpm: " + statsobject["dpm"] + "```"
        #Returning
        return returnvar


    #find the newsest team match
    def findMatch(self, minplayers, numoflogs, format, team, message):
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
            if (sortedlogidsbyamount[i] >= minplayers and sortedlogidsbyamount[i] <= format):
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
        return str(datetime.datetime.fromtimestamp(int(str(timestamp))).strftime('%d-%m-%Y\n%H:%M:%S'))


    # Console output of the users id that was accessing the bot and the bots output
    def consoleOutput(self, userid, message, outputmessage):
        print("[+]  [command]       " + message.content.lower())
        print("     [author]        " + str(message.author.id))
        print("     [output]        " + str(outputmessage.split(" ")))
        print("\n")


class LogBotCommands:
    message = {}
    message_content = []
    message_author_id = []
    userlist = []
    teamlist = []
    moderators = LogBotUsers().getmoderators()
    client = discord.Client()

    def scan(self, message):
        #Grab important informations of message
        #self.message_content = message.content.lower()
        #self.message_author_id = message.author.id()
        self.message = message

        # load the users data if a message hits and contains LDB commands
        if (message.content.lower().find("!logs") != -1):

            # Loads the member list as json format and converts it into an object
            LogBotUsers().update()

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

            # COMMAND: !logs
            if message.content.lower().startswith('!logs'):
               return self.command_logs()


    # COMMAND: !logs help
    def command_help(self):
        #Variables
        modhelp = ""

        #If user is mod, show that command !logs modhelp exists
        #if self.message.author.id() in self.moderators:
           #modhelp = "\nYou are a Moderator, type `!logs modhelp` to get moderator commands"

        #Message that will be sended
        messagetosend = ":grey_question: Need some help "+self.message.author.name+" ?" + modhelp+ \
        "\n\n`!logs`\nshows your last played match with details about your performance" \
        "\n`!logs profile`\nshows your logs.tf profile" \
        "\n\n`!logs @<name>`\nshows the last log of the player you looked for" \
        "\n`!logs @<name> profile`\nshows the logs.tf profile of the player you looked for" \
        "\n\n`!logs match <teamname>`\nshows the latest match (scrim, lobby, official) of a team with details about your performance" \
        "\n`!logs teams`\nshows the available teams" \
        "\n`!logs teams <teamname> players`\nshows the players in the team" \
        "\n\n`version: "+LogBotEssentials.version+"`"

        #sending message
        return messagetosend


    # COMMAND: !logs modhelp
    def command_modhelp(self):
        #Variables
        messagetosend = "You don't have permission."

        #Check if message author is a moderator
        if self.message.author.id in self.moderators:
            messagetosend = "`!logs user add @<name> <SteamID64>`\nto add a player to the system with his/her SteamID64. This command can also be used to update a player's SteamID64." \
                            "\n`!logs user remove @<name>`\nremoves the player from the system." \
                            "\n\n`!logs teams create <teamname> <format>`\nCreates a new team. Format is the type of the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on). WIP" \
                            "\n`!logs teams delete <teamname>`\nRemoves a team from the system. WIP" \
                            "\n\n`!logs teams add <teamname> @<name> <name>`\nStores a player with a specific name into a team." \
                            "\n`!logs teams remove <teamname> @<name>`\nRemoves a player from a team." \
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
            messagetosend = ":information_source: You can get information from a team.\n" \
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
                    if team[teamname][0]["type"] == 6:
                        minplayer = LogBotEssentials().sixes_min_players
                    #HL
                    elif team[teamname][0]["type"] == 9:
                        minplayer = LogBotEssentials().hl_min_players
                    #4s
                    elif team[teamname][0]["type"] == 4:
                        minplayer = LogBotEssentials().fours_min_players
                    #Duo
                    elif team[teamname][0]["type"] == 2:
                        minplayer = LogBotEssentials().duo_min_players

                    #Search for the newest match of the team
                    messagetosend = LogBotEssentials().findMatch(minplayer, 25, team[teamname][0]["type"], team[teamname][1]["players"], self.message)
                    if(messagetosend==None):
                        messagetosend=":frowning: cloudn't find any matches"
                    break

        # Output
        return messagetosend


    # Command: !logs teams
    def command_teams(self):
        if self.message.content.lower() == "!logs teams":
            #vars
            messagetosend = ":busts_in_silhouette: **Teams**\n I stored these teams:\n"
            for team in self.teamlist:
                messagetosend = messagetosend +":heavy_minus_sign: " + str(team.keys()).split("'")[1]+"\n"

        if self.message.content.lower().startswith('!logs teams'):
            # split message to get all parts
            messagesplit = self.message.content.lower().split(' ')

            # check if command: !logs teams <teamname> players
            if self.message.content.lower().endswith('players') and len(messagesplit) == 4:
                #vars
                messagetosend = "This team does not exist"

                for team in self.teamlist:
                    if messagesplit[2] in team:

                        messagetosend = "**" + messagesplit[2] + " player's**\n"
                        num = 0
                        for player in team[messagesplit[2]][1]["players"].values():
                            messagetosend += player + "; "
                            num += 1

                        messagetosend += "(amount: " + str(num) + ")"
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
                        messagetosend = ":information_source: You can add or update a player to/of a team by typing `!logs teams add` <teamname> @<player> <Name>"

                    else:
                        #check if 4th position is not a team
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                if not len(messagesplit) >= 6:
                                    if len(messagesplit) == 5:
                                        messagetosend = ":information_source: add the name after your command `" + self.message.content.lower() + "`  <Name>"

                                    else:
                                        messagetosend = ":information_source: add the user and the name after your command `" + self.message.content.lower() + "` @<player> <Name>"
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
                                        messagetosend = self.message.mentions[0].name + " isn't stored in my data.\nFirst you have to add him with the command: `!logs user edit @<mention> <SteamID64>`"
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
                        messagetosend = ":information_source: You can remove a player of a team by typing `!logs teams remove` <teamname> @<player>"

                    else:
                        #else find the team name and if the team exists
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                if not len(messagesplit) >= 5:
                                    # check if enough inputs are granted
                                    if len(messagesplit) == 4:
                                        messagetosend = ":information_source: add the player after your command `" + self.message.content.lower() + "`  @<player>"

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
                            messagetosend = "This team does not exist"


            # COMMANDS !logs teams create
            if self.message.content.lower().startswith('!logs teams create'):
                #vars
                messagetosend = self.message.author.name + " you don't have permissions."
                messagesplit = self.message.content.lower().split(' ')

                #check if author is moderator
                if self.message.author.id in self.moderators:
                    #if only typed: !logs teams create
                    if self.message.content.lower() == '!logs teams create':
                        messagetosend = ":information_source: You can create a team by typing `!logs teams create` <teamname> <format>"

                    #check if team already exists
                    # Checks to see if the provided team name already exists
                    if len(self.teamlist) == 0:
                        # No teams exist, name is original
                        notexisting = True
                    else:
                        # Compare provided name with all stored names
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                messagetosend = "This team already exists."
                                notexisting = False
                                break
                            else:
                                notexisting = True

                        #if its not existing, create one
                        if notexisting and len(messagesplit) >= 5:
                            # Check if last value is an int
                            try:
                                fomrat = int(messagesplit[4])

                                # create a new team (teamname, type)
                                LogBotTeams().create_team(messagesplit[3],messagesplit[4])

                                messagetosend = ":ballot_box_with_check: created team **" + messagesplit[
                                            3] + "** with the format: " + messagesplit[4]

                            except ValueError:
                                #If type isn't a number
                                messagetosend = ":no_entry_sign: format has to be a integer (6 = 6v6, 9 = 9v9 and so on)"

                        elif len(messagesplit) <= 5 and notexisting:
                            messagetosend = ":information_source: You have to add the teams format (6 = 6v6, 9 = 9v9 and so on) after `!logs teams create " + \
                                            messagesplit[3] + "` <format>"


            # COMMANDS !logs teams delete
            if self.message.content.lower().startswith('!logs teams delete'):
                #vars
                messagetosend = self.message.author.name + " you don't have permissions."
                messagesplit = self.message.content.lower().split(' ')

                #check if author is mod
                if self.message.author.id in self.moderators:
                    #check if only !logs teams delete was typed
                    if self.message.content.lower() == '!logs teams delete':
                        messagetosend = ":information_source: You can delete a team by typing `!logs teams delete` <teamname>"

                    else:
                        #Check if team even exists
                        notexisting = False
                        for team in self.teamlist:
                            if messagesplit[3] in team:
                                notexisting = False
                                break

                            else:
                                messagetosend = "This team does not exist."
                                notexisting = True

                        #if its existing, delete it
                        if not notexisting and len(messagesplit) >= 4:

                            #deletes team (teamname)
                            LogBotTeams().delete_team(messagesplit[3])

                            messagetosend = ":ballot_box_with_check: deleted team **" + messagesplit[
                                        3] + "**"

                        #if teamname is missing
                        elif len(messagesplit) <= 4 and not notexisting:
                            messagetosend = ":information_source: You have to add the teamname"


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
                    messagetosend = ":information_source: " + self.message.author.name + ",\nYou can get add or update players.\nJust type after `!logs user add` @<name> <SteamID64>"

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


        # check for COMMAND: !logs user remove
        if self.message.content.lower().startswith('!logs user remove'):
            #vars
            splitmessage = self.message.content.lower().split(' ')
            messagetosend = self.message.author.name + " you don't have permissions."

            #check if author is mod
            if self.message.author.id in self.moderators:
                #check if only typed: !Logs user remove
                if self.message.content.lower() == '!logs user remove':
                    messagetosend = ":information_source: You can remove players.\nJust type after `!logs user remove` @<name> <SteamID64>"

                else:
                    # remove user
                    if len(splitmessage) == 4:
                        # removes user with discord id (message.mentions[0].id)
                        LogBotUsers().remove_user(self.message.mentions[0].id)

                        # Outputs Succsessfully message
                        messagetosend = ":ballot_box_with_check: removed user " + self.message.mentions[
                            0].name


    # Command: !logs
    def command_logs(self):
        #splits message to get every input
        splitmessage = self.message.content.lower().split(" ")

        #checks if only command: !logs is needed
        if self.message.content.lower() == '!logs':
            #initilaize vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find you in my data."

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
                messagetosend = ":dart: " + self.message.author.name + "'s Log found\n**" + logtitle + "**\n" + logtime + "\n\n<http://logs.tf/" + logid + ">" + performance

        # Check if command: !logs profile is called
        if self.message.content.lower() == '!logs profile':
            #vars
            messagetosend = "Sorry " + self.message.author.name + " :confused:  but i didn't find you in my data."

            #check if user is in userdata
            if self.message.author.id in self.userlist:
                # Getting newest 3 logs
                data = LogBotEssentials().LogPlayerSearch(self.userlist[self.message.author.id], 3)
                #building message
                messagetosend2 = "\n\n__**Last 3 logs**__\n"
                # looping 3 logs with id, link, title, time and date
                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = LogBotEssentials().totime(log["date"])
                    messagetosend2 = messagetosend2 + "<http://logs.tf/" + logid + ">\n" + "```" + logtitle + "\n" + logtime + "```\n"
                #building message
                messagetosend2 = messagetosend2 + ""
                messagetosend = ":card_box: " + self.message.author.name + "'s profile found\n**Your profile on logs.tf**\n<http://logs.tf/profile/" + \
                                    self.userlist[self.message.author.id] + ">" + messagetosend2


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
                messagetosend = ":mag_right: Log of **" + mentionuser + "** found\n**" + logtitle + "**\n" + logtime + "\n\n<http://logs.tf/" + logid + ">" + performance


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

                # Getting newest 3 logs
                data = LogBotEssentials().LogPlayerSearch(self.userlist[self.message.mentions[0].id], 3)

                # Building message
                messagetosend2 = "\n\n__**Last 3 logs**__\n"
                #inserting logs with link, title, date and time
                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = LogBotEssentials().totime(log["date"])
                    messagetosend2 = messagetosend2 + "<http://logs.tf/" + logid + ">\n" + "```" + logtitle + "\n" + logtime + "```\n"

                #Building rest of the message
                messagetosend2 = messagetosend2 + ""
                messagetosend = ":credit_card: Profile found\n**" + mentionuser + "**'s profile on logs.tf\n<http://logs.tf/profile/" + \
                                self.userlist[self.message.mentions[0].id] + ">" + messagetosend2

        # sending result
        return messagetosend