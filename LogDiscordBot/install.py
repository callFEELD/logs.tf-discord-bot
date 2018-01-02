# IMPORTANT: THIS SCRIPT IS MADE FOR LINUX INSTALLATION
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
# last edit: 02.01.2018 (callFEELD)

import os
import time
import json

def insertotherstuff():
    print("     [LogDiscordBot] We did it. We successfully installed")
    print("                     the Discord.py libary.")
    time.sleep(0.4)
    print("     [LogDiscordBot] Let' get started with your token,")
    print("                     insert the token WITHOUT ANY SPACES.")
    token = input("     [place the token here]")
    time.sleep(0.4)
    print("     [LogDiscordBot] Good Job")
    time.sleep(1)
    print("     [LogDiscordBot] I am currently placing the token in the")
    print("                     right file.")
    tokenfile = open("token.json", "r").read()
    tokenjson = json.loads(tokenfile)
    tokenjson["token"] = str(token)
    file = open("token.json", "w")
    file.write(json.dumps(tokenjson))
    time.sleep(0.4)
    print("     [LogDiscordBot] Now I need your discordid and steamid64,")
    print("                     so I can make you moderator.")
    discordid = input("     [place your DiscordID here]")
    time.sleep(0.4)
    print("     [LogDiscordBot] Nice")
    time.sleep(0.4)
    steamid64 = input("     [place your SteamID64 here]")
    time.sleep(0.4)
    print("     [LogDiscordBot] Awesome")
    time.sleep(0.5)
    print("     [LogDiscordBot] Now in just a few second are you the")
    print("                     moderator.")
    tokenfile = open("users.json", "r").read()
    tokenjson = json.loads(tokenfile)
    tokenjson["moderators"].update({discordid: steamid64})
    file = open("users.json", "w")
    file.write(json.dumps(tokenjson))
    time.sleep(0.5)
    print("     [LogDiscordBot] There you go, everything finished.")
    time.sleep(1)

def installing():
    print("     [LogDiscordBot] So I am asking you: Do You wanna")
    print("                     install the Discord.py libary?")
    answer = input("     [question]    (y/n)")
    if answer == "y":
        time.sleep(0.4)
        print("     [LogDiscordBot] Let's begin the installing")
        print("                      process...")
        time.sleep(0.4)

        os.system('python3 -m pip install discord.py')
        os.system('pip install asyncio')

        insertotherstuff()

    elif answer=="n":
        time.sleep(0.4)
        print("     [LogDiscordBot] Ok! I will then shut down the")
        print("                     installing process...")
        time.sleep(0.4)
        print("     [LogDiscordBot] Byeeeeeee")
        time.sleep(2)
    else:
        time.sleep(0.4)
        print("     [LogDiscordBot] I guess you typed something wrong")
        print("                     here, lets try it again...")
        time.sleep(0.4)
        installing()

time.sleep(0.5)
print("[i]  [status]        asking to install important parts")
time.sleep(0.4)
print("     [LogDiscordBot] The LogDiscordBot folder should be now in")
print("                     the python3 directory, right?")
time.sleep(2)
print("     [LogDiscordBot] And you also installed Python3 with 'pip'?")
time.sleep(2)
print("     [LogDiscordBot] Then I need the Discord.py libary")
print("                     to function correctly.")
time.sleep(1)
installing()
