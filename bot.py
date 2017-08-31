import discord
import asyncio
import urllib.request, json
import datetime
from collections import Counter

client = discord.Client()
user = discord.User()

version = "1.0"

tokenfile = open("token.json", "r").read()
tokenjson = json.loads(tokenfile)

#INSTALL
TOKEN = tokenjson["token"]
USERNAME = "logs.tf"
PLAYING_STATUS = "type !logs help"



def loaduserfile():
    # Loads the member list as json format and converts it into an object
    memberlist = open("users.json", "r").read()
    memberlistjson = json.loads(memberlist)
    return memberlistjson


# Converts the SteamID64 into a SteamID3 (as a string)
def tosteamid3(id):
    y = int(id) - 76561197960265728
    x = y % 2
    if len(id) == 17:
        id32 = int(id[3:]) - 61197960265728
        return "[U:1:" + str(id32) + "]"
    else:
        return False


def LogIDdetails(logid, steamid3):
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


def LogPlayerSearch(steamid64, limit):
    with urllib.request.urlopen("http://logs.tf/json_search?player=" + steamid64 + "&limit=" + str(limit)) as url:
        data = json.loads(url.read().decode())
    return data


def totime(timestamp):
    return str(datetime.datetime.fromtimestamp(int(str(timestamp))).strftime('%d-%m-%Y\n%H:%M:%S'))

# Console output of the users id that was accessing the bot and the bots output
def consoleOutput(userid, message, outputmessage):
    print("Incomming commands from id (" + str(userid) + "): " + message.content.lower())
    print("Output: " + outputmessage)
    print("____________________________________________________________________________________\n\n")


def PerformanceDisplay(yourorplayer, statsobject):

    if yourorplayer == 0:
        title = "Your performance"
    elif yourorplayer == 1:
        title = "Player's performance"
    else:
        title = "Performance"

    if statsobject["playerinlog"]:

        returnvar = "```"+title+"\n" \
        "----------------\n" \
        "kills: " + statsobject["kills"] + "\n" \
        "deaths: " + statsobject["deaths"] + "\n" \
        "k/d: " + statsobject["kd"] + "\n" \
        "dpm: " + statsobject["dpm"] + "```"
    else:
        returnvar = ""

    return returnvar




@client.event
async def on_ready():
    print('Started Logs.tf bot (v.'+version+'):')
    print("Bot's username : " + client.user.name)
    print("Bot's discordid: " + client.user.id)
    print('------------------------------------')

    #shows the 'playing' status
    await client.change_presence(game=discord.Game(name=PLAYING_STATUS))

@client.event
async def on_message(message):

    # load the users data if a message hits and contains commands
    if(message.content.lower().find("!logs") != -1):
        # Loads the member list as json format and converts it into an object
        memberlist = open("users.json", "r").read()
        memberlistjson = json.loads(memberlist)

        # loading users of the members list
        discordtosteam = memberlistjson["users"]
        moderators = memberlistjson["moderators"]

        if message.author.id in discordtosteam:
            #Steam ID64 and Steam ID3 of the author
            steamid64 = discordtosteam[message.author.id]
            steamid3 = tosteamid3(steamid64)


    def findMatch(minplayers, numoflogs, format, team, message):
        # minplayers: minimal amount of players to be a match
        # numoflogs: amount of logs that should be checked for each player
        # fomrat: either 6 or 9 to represent 6s or HL
        checklogs = {}
        checklogstitle = {}
        checklogids = []

        # mention statement for the name of the user that is accessing the bot
        mentionuserid = "<@" + str(message.author.id) + ">"
        # Steam ID64 and Steam ID3 of the author
        steamid64 = discordtosteam[message.author.id]
        steamid3 = tosteamid3(steamid64)

        # Go trough all Players of the Team
        for player in team.keys():
            playersteamid = discordtosteam[player]

            data = LogPlayerSearch(playersteamid, str(numoflogs))
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
                logtime = totime(checklogs[matchid])

                logdetails = LogIDdetails(matchid, steamid3)
                performance = PerformanceDisplay(0, logdetails)

                return ":trophy: match found\n**" + str(checklogstitle[matchid]) + "**\n" + str(logtime) + "\n\n<http://logs.tf/" + str(matchid) + ">" + performance

                consoleOutput(message.author.id, message, messagetosend)
                break

    async def sendMessage(message, messagetosend):
        await client.send_message(message.channel, messagetosend)
        consoleOutput(message.author.id, message, messagetosend)

    # mention statement for the name of the user that is accessing the bot
    mentionuserid = "<@" + str(message.author.id) + ">"


    #COMMAND: !logs help
    if message.content.lower() == "!logs help":

        if message.author.id in moderators:
            modhelp = "\nYou are a Moderator, type `!logs modhelp` to get moderator commands"
        else:
            modhelp = ""

        messagetosend = ":grey_question: Need some help "+message.author.name+" ?" + modhelp+ \
        "\n\n`!logs`\nshows your last played match with details about your performance" \
        "\n`!logs profile`\nshows your logs.tf profile" \
        "\n\n`!logs @<name>`\nshows the last log of the player you looked for" \
        "\n`!logs @<name> profile`\nshows the logs.tf profile of the player you looked for" \
        "\n\n`!logs match <teamname>`\nshows the latest match (scrim, lobby, official) of a team with details about your performance" \
        "\n`!logs teams`\nshows the available teams" \
        "\n`!logs teams <teamname> players`\nshows the players in the team" \
        "\n\n`version: "+version+"`"
        await sendMessage(message, messagetosend)


    # COMMAND: !logs version
    if message.content.lower() == '!logs version':
        messagetosend = "`"+version+"`"
        await sendMessage(message, messagetosend)


    # COMMAND: !logs profile
    if message.content.lower() == '!logs profile':
        if message.author.id in discordtosteam:

            data = LogPlayerSearch(discordtosteam[message.author.id], 3)
            messagetosend2 = "\n\n__**Last 3 logs**__\n"
            for log in data["logs"]:
                logid = str(log["id"])
                logtitle = str(log["title"])
                logtime = totime(log["date"])
                messagetosend2 = messagetosend2 + "<http://logs.tf/" + logid + ">\n" + "```" + logtitle + "\n" + logtime + "```\n"

            messagetosend2 = messagetosend2 + ""
            messagetosend = ":card_box: "+message.author.name+"'s profile found\n**Your profile on logs.tf**\n<http://logs.tf/profile/" + discordtosteam[message.author.id]+">" + messagetosend2

        else:
            messagetosend = "Sorry "+message.author.name+" :confused:  but i didn't find you in my data."

        await sendMessage(message, messagetosend)


    # COMMAND: !logs
    if message.content.lower().startswith('!logs'):
        splitmessage = message.content.lower().split(" ")

        if message.content.lower() == '!logs':

            if message.author.id in discordtosteam:

                data = LogPlayerSearch(discordtosteam[message.author.id], 1)
                logid = str(data["logs"][0]["id"])
                logtitle = str(data["logs"][0]["title"])
                logtime = totime(data["logs"][0]["date"])
                steamid3 = tosteamid3(discordtosteam[message.author.id])
                logiddetails = LogIDdetails(logid, steamid3)
                performance = PerformanceDisplay(0, logiddetails)

                messagetosend = ":dart: "+message.author.name+"'s Log found\n**" + logtitle + "**\n" + logtime + "\n\n<http://logs.tf/" + logid + ">" + performance

            else:
                messagetosend = "Sorry "+message.author.name+" :confused:  but i didn't find you in my data."

            await sendMessage(message, messagetosend)

        elif len(message.mentions) != 0 and not message.content.lower().endswith('profile') and not len(splitmessage) >= 3:
            mentionuser = str(message.mentions[0].name)
            if message.mentions[0].id in discordtosteam:

                steamid64 = discordtosteam[message.mentions[0].id]
                steamid3 = tosteamid3(steamid64)

                data = LogPlayerSearch(discordtosteam[message.mentions[0].id], 1)

                logid = str(data["logs"][0]["id"])
                logtitle = str(data["logs"][0]["title"])
                logtime = totime(data["logs"][0]["date"])
                logiddetails = LogIDdetails(logid, steamid3)
                performance = PerformanceDisplay(1, logiddetails)

                if logiddetails["playerinlog"]:
                    messagetosend = ":mag_right: Log of **" + mentionuser + "** found\n**" + logtitle + "**\n" + logtime + "\n\n<http://logs.tf/" + logid + ">" + performance
                    await sendMessage(message, messagetosend)

                else:
                    messagetosend = ":mag_right: Log of **" + mentionuser + "** found\n**" + logtitle + "**\n" + logtime + "\n\n<http://logs.tf/" + logid + ">"
                    await sendMessage(message, messagetosend)

            else:
                messagetosend = "Sorry " + message.author.name + " :confused:  but i didn't find **" + mentionuser + "** in my data."
                await sendMessage(message, messagetosend)


        elif not len(message.mentions) == 0 and len(splitmessage) >= 3 and message.content.lower().endswith('profile'):
            if message.mentions[0].id in discordtosteam:
                steamid64 = discordtosteam[message.mentions[0].id]
                steamid3 = tosteamid3(steamid64)
                mentionuser = str(message.mentions[0].name)

                data = LogPlayerSearch(discordtosteam[message.mentions[0].id], 3)

                messagetosend2 = "\n\n__**Last 3 logs**__\n"

                for log in data["logs"]:
                    logid = str(log["id"])
                    logtitle = str(log["title"])
                    logtime = totime(log["date"])
                    messagetosend2 = messagetosend2 + "<http://logs.tf/" + logid + ">\n" + "```" + logtitle + "\n" + logtime + "```\n"

                messagetosend2 = messagetosend2 + ""
                messagetosend = ":credit_card: Profile found\n**"+ mentionuser +"**'s profile on logs.tf\n<http://logs.tf/profile/" + discordtosteam[message.mentions[0].id] + ">"+ messagetosend2

            else:
                messagetosend = "Sorry " + message.author.name + " :confused:  but i didn't find **" + str(message.mentions[0].name) + "** in my data."

            await sendMessage(message, messagetosend)


    # COMMAND: !logs match
    if message.content.lower().startswith('!logs match'):
        splitmessage = message.content.lower().split(" ")

        if message.content.lower() == '!logs match':
            messagetosend = ":information_source: You can get information from a team.\n" \
            "`!logs teams` shows you the teams that are available."
            await sendMessage(message, messagetosend)

        elif len(splitmessage) >= 3:

            for team in memberlistjson["teams"]:
                if splitmessage[2] in team:
                    teamname = splitmessage[2]
                    await client.send_message(message.channel, "*wait a bit I am processing...*")

                    if team[teamname][0]["type"] == 6:
                        minplayer = 5
                    elif team[teamname][0]["type"] == 9:
                        minplayer = 7
                    elif team[teamname][0]["type"] == 4:
                        minplayer = 3
                    elif team[teamname][0]["type"] == 2:
                        minplayer = 2

                    messagetosend = findMatch(minplayer, 25, team[teamname][0]["type"], team[teamname][1]["players"], message)

                    notexisting = False
                    break

                else:
                    notexisting = True

            if notexisting:
                messagetosend = "This team does not exist. Check available teams with `!logs teams`"
                notexisting = False

            await sendMessage(message, messagetosend)


    #COMMAND: !logs teams
    if message.content.lower() == "!logs teams":
        messagetosend = ":busts_in_silhouette: **Teams**\n I stored these teams:"
        await sendMessage(message, messagetosend)

        for team in memberlistjson["teams"]:
            messagetosend = ":heavy_minus_sign: " + str(team.keys()).split("'")[1]
            await sendMessage(message, messagetosend)


    #COMMAND: !logs teams <teamname> players
    if message.content.lower().startswith('!logs teams'):
        messagesplit = message.content.lower().split(' ')

        if message.content.lower().endswith('players') and len(messagesplit) == 4:
            for team in memberlistjson["teams"]:
                if messagesplit[2] in team:

                    messagetosend = "**"+messagesplit[2]+" player's**\n"
                    num = 0
                    for player in team[messagesplit[2]][1]["players"].values():
                        messagetosend += player +"; "
                        num += 1

                    messagetosend += "(amount: "+str(num)+")"
                    notexisting = False

                    await sendMessage(message, messagetosend)
                    break
                else:
                    notexisting = True

            if notexisting:
                messagetosend = "This team does not exist"
                await sendMessage(message, messagetosend)


    # MODERATOR COMMANDS________________________________________________________________________________________________

    #COMMAND: !logs modhelp
    if message.content.lower() == '!logs modhelp':
        if message.author.id in moderators:
            messagetosend = "`!logs user add @<name> <SteamID64>`\nto add a player to the system with his/her SteamID64. This command can also be used to update a player's SteamID64." \
                            "\n`!logs user remove @<name>`\nremoves the player from the system." \
                            "\n\n`!logs teams create <teamname> <format>`\nCreates a new team. Format is the type of the team (6 = 6v6, 9 = Highlander, 4 = 4v4 and so on)." \
                            "\n`!logs teams delete <teamname>`\nRemoves a team from the system." \
                            "\n\n`!logs teams add <teamname> @<name> <name>`\nStores a player with a specific name into a team." \
                            "\n`!logs teams remove <teamname> @<name>`\nRemoves a player from a team." \
                            "\n\n`version: " + version + "`"
        else:
            messagetosend = "You don't have permission."

        await sendMessage(message, messagetosend)


    #COMMAND: !logs user add
    if message.content.lower().startswith('!logs user add'):
        if message.author.id in moderators:
            if message.content.lower() == '!logs  user add':
                messagetosend = ":information_source: "+message.author.name+",\nYou can get add or update players.\nJust type after `!logs user add` @<name> <SteamID64>"
                await sendMessage(message, messagetosend)

            else:
                splitmessage = message.content.lower().split(' ')
                if not len(splitmessage) == 5:
                    messagetosend = ":information_source: add the SteamID64 after the mention statement `"+message.content.lower()+"` <SteamID64>"
                    await sendMessage(message, messagetosend)

                else:
                    if message.mentions[0].id in discordtosteam:
                        addorupdate = "Updated"

                    else:
                        addorupdate = "Added"

                    addusersteamid64 = splitmessage[4]

                    newmemberlist = open("users.json", "r").read()
                    newmemberlistjson = json.loads(newmemberlist)

                    newmemberlistjson["users"].update({message.mentions[0].id: addusersteamid64})

                    data = open("users.json", "w")
                    data.write(json.dumps(newmemberlistjson))

                    messagetosend = ":ballot_box_with_check: "+addorupdate+" user **"+message.mentions[0].name+"** with the SteamID64: "+addusersteamid64
                    await sendMessage(message, messagetosend)

        else:
            messagetosend = message.author.name + " you don't have permissions."
            await sendMessage(message, messagetosend)


    # COMMAND: !logs user remove
    if message.content.lower().startswith('!logs user remove'):
        if message.author.id in moderators:
            if message.content.lower() == '!logs user remove':
                messagetosend = ":information_source: You can remove players.\nJust type after `!logs user remove` @<name> <SteamID64>"
                await sendMessage(message, messagetosend)

            else:
                splitmessage = message.content.lower().split(' ')
                if len(splitmessage) == 4:
                    newmemberlist = open("users.json", "r").read()
                    newmemberlistjson = json.loads(newmemberlist)

                    del newmemberlistjson["users"][message.mentions[0].id]

                    data = open("users.json", "w")
                    data.write(json.dumps(newmemberlistjson))

                    messagetosend = ":ballot_box_with_check: removed user " + message.mentions[
                        0].name
                    await sendMessage(message, messagetosend)


        else:
            messagetosend = message.author.name + " you don't have permissions."
            await sendMessage(message, messagetosend)


    # COMMANDS !logs teams add
    if message.content.lower().startswith('!logs teams add'):
        # Separates message into parts, separated by a space. Put into an array
        messagesplit = message.content.lower().split(' ')

        # Is the sending user a moderator?
        if message.author.id in moderators:
            if message.content.lower() == '!logs teams add':
                messagetosend = ":information_source: You can add or update a player to/of a team by typing `!logs teams add` <teamname> @<player> <Name>"
                await sendMessage(message, messagetosend)

            else:
                for team in memberlistjson["teams"]:
                    if messagesplit[3] in team:
                        if not len(messagesplit) >= 6:
                            if len(messagesplit) == 5:
                                messagetosend = ":information_source: add the name after your command `" + message.content.lower() + "`  <Name>"

                            else:
                                messagetosend = ":information_source: add the user and the name after your command `" + message.content.lower() + "` @<player> <Name>"
                            notexisting = False
                            break

                        elif len(message.mentions) != 0 and len(messagesplit) >=6:
                            if message.mentions[0].id in discordtosteam:
                                if message.mentions[0].id in team[messagesplit[3]][1]["players"].values():
                                    addorupdate = "Updated"

                                else:
                                    addorupdate = "Added"

                                newmemberlist = open("users.json", "r").read()
                                newmemberlistjson = json.loads(newmemberlist)

                                for team in newmemberlistjson["teams"]:
                                    if messagesplit[3] in team:
                                        team[messagesplit[3]][1]["players"].update({message.mentions[0].id: messagesplit[5]})
                                        notexisting = False
                                        break

                                data = open("users.json", "w")
                                data.write(json.dumps(newmemberlistjson))

                                messagetosend = ":ballot_box_with_check: " + addorupdate + " user **" + message.mentions[0].name+ "** with the name: " + messagesplit[5]
                                notexisting = False
                                break
                            else:
                                messagetosend = message.mentions[0].name + " isn't stored in my data.\nFirst you have to add him with the command: `!logs user edit @<mention> <SteamID64>`"
                                notexisting = False
                                break

                    else:
                        notexisting = True

                if notexisting:
                    messagetosend = "This team does not exist"

                await sendMessage(message, messagetosend)

        else:
            messagetosend = message.author.name + " you don't have permissions."
            await sendMessage(message, messagetosend)


    # COMMANDS !logs teams remove
    if message.content.lower().startswith('!logs teams remove'):
        messagesplit = message.content.lower().split(' ')

        if message.author.id in moderators:
            if message.content.lower() == '!logs teams remove':
                messagetosend = ":information_source: You can remove a player of a team by typing `!logs teams remove` <teamname> @<player>"
                await sendMessage(message, messagetosend)

            else:
                for team in memberlistjson["teams"]:
                    if messagesplit[3] in team:
                        if not len(messagesplit) >= 5:
                            if len(messagesplit) == 4:
                                messagetosend = ":information_source: add the player after your command `" + message.content.lower() + "`  @<player>"

                            notexisting = False
                            break

                        elif len(message.mentions) != 0 and len(messagesplit) >=5:
                            if message.mentions[0].id in discordtosteam:
                                newmemberlist = open("users.json", "r").read()
                                newmemberlistjson = json.loads(newmemberlist)

                                for team in newmemberlistjson["teams"]:
                                    if messagesplit[3] in team:
                                        del team[messagesplit[3]][1]["players"][message.mentions[0].id]
                                        notexisting = False
                                        break

                                data = open("users.json", "w")
                                data.write(json.dumps(newmemberlistjson))

                                messagetosend = ":ballot_box_with_check: removed user **" + message.mentions[0].name+ "** from the team: " + messagesplit[3]
                                notexisting = False
                                break
                            else:
                                messagetosend = message.mentions[0].name + " isn't stored in my data."
                                notexisting = False
                                break

                    else:
                        notexisting = True

                if notexisting:
                    messagetosend = "This team does not exist"

                await sendMessage(message, messagetosend)

        else:
            messagetosend = message.author.name + " you don't have permissions."
            await sendMessage(message, messagetosend)


    # COMMANDS !logs teams create
    if message.content.lower().startswith('!logs teams create'):
        # Separates message into parts, separated by a space. Put into an array
        messagesplit = message.content.lower().split(' ')

        # Is the sending user a moderator?
        if message.author.id in moderators:
            # Check if there's no arguments, and tell the user to put arguments
            if message.content.lower() == '!logs teams create':
                messagetosend = ":information_source: You can create a team by typing `!logs teams create` <teamname> <format>"
                await sendMessage(message, messagetosend)

            # Command has arguments, proceeding...
            else:
                notexisting = False
                # Checks to see if the provided team name already exists
                if len(memberlistjson["teams"]) == 0:
                    # No teams exist, name is original
                    notexisting = True
                else:
                    # Compare provided name with all stored names
                    for team in memberlistjson["teams"]:
                        if messagesplit[3] in team:
                            messagetosend = "This team already exists."
                            notexisting = False
                            break
                        else:
                            notexisting = True


                if notexisting and len(messagesplit) >=5:
                    # Check if last message part is an int
                    try:
                        # Int Test
                        format = int(splitmessage[4])

                        newmemberlist = open("users.json", "r").read()
                        newmemberlistjson = json.loads(newmemberlist)
                        newteam = {messagesplit[3]: [{"type": messagesplit[4]}, {"players": {}}]}
                        newmemberlistjson["teams"].append(newteam)

                        data = open("users.json", "w")
                        data.write(json.dumps(newmemberlistjson))

                        messagetosend = ":ballot_box_with_check: created team **" + splitmessage[
                            3] + "** with the format: " + messagesplit[4]

                    except ValueError:
                        messagetosend = ":no_entry_sign: format has to be a integer (6 = 6v6, 9 = 9v9 and so on)"

                elif len(messagesplit) <= 5 and notexisting:
                    messagetosend = ":information_source: You have to add the teams format (6 = 6v6, 9 = 9v9 and so on) after `!logs teams create " + \
                                    splitmessage[3] + "` <format>"

                await sendMessage(message, messagetosend)

        else:
            messagetosend = message.author.name + " you don't have permissions."
            await sendMessage(message, messagetosend)



    # COMMANDS !logs teams delete
    if message.content.lower().startswith('!logs teams delete'):
        messagesplit = message.content.lower().split(' ')

        if message.author.id in moderators:
            if message.content.lower() == '!logs teams delete':
                messagetosend = ":information_source: You can delete a team by typing `!logs teams delete` <teamname>"
                await sendMessage(message, messagetosend)

            else:
                notexisting = False
                for team in memberlistjson["teams"]:
                    if messagesplit[3] in team:
                        notexisting = False
                        break

                    else:
                        messagetosend = "This team does not exist."
                        notexisting = True

                if not notexisting and len(messagesplit) >=4:

                    newmemberlist = open("users.json", "r").read()
                    newmemberlistjson = json.loads(newmemberlist)

                    arrayposition = 0
                    for team in newmemberlistjson["teams"]:
                        if splitmessage[3] in team:
                            break
                        arrayposition += 1

                    del newmemberlistjson["teams"][arrayposition]

                    data = open("users.json", "w")
                    data.write(json.dumps(newmemberlistjson))

                    messagetosend = ":ballot_box_with_check: deleted team **" + splitmessage[
                            3] + "**"


                elif len(messagesplit)<= 4 and not notexisting:
                    messagetosend = ":information_source: You have to add the teamname"

                await sendMessage(message, messagetosend)

        else:
            messagetosend = message.author.name + " you don't have permissions."
            await sendMessage(message, messagetosend)

client.run(TOKEN)
