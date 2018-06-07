# This Class containing important functions that will be used in other Classes
# last edit: 21.04.2018 (callFEELD)

# third party imports
import urllib.request, json         # used to handle separate json files and the logs.tf api
import datetime                     # used to convert timestamps
from collections import Counter     # used in the match searching algorithm

# own imports
from src.classes import Teams
from src.classes import Users


class LogBotEssentials:
    # Load the CONFIG
    config = open("data/cfg/config.json", "r").read()
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
    userlist = Users.LogBotUsers().getplayers()
    moderators = Users.LogBotUsers().getmoderators()

    def update(self):
        self.userlist = Users.LogBotUsers().getplayers()
        self.moderators = Users.LogBotUsers().getmoderators()


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
        steamid64 = Users.LogBotUsers().getplayers_steamid(message.author.id)
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
        print("     [output]        " + str(outputmessage.split()))
        print("\n")