# logs.tf-discord-bot
A discord bot showing your recent logs, profile page and team matches. You can create teams, fill them with players and get recent matches of the teams. You can also search for other persons logs and logs.tf profile's.

## requirements
Your System (Computer/Server) needs: 
- Python 3.6 or higher
- discord.py libary (https://github.com/Rapptz/discord.py)



You need a bit experience in JSON or general programming (so you can fill the token and your user correctly). Trust me this ins't that hard to do.

## installing
#easier installing:
- install Python3 with pip
(https://www.python.org/downloads/)
Note For POSIX users (including Mac OS X and Linux users), the examples in this guide assume the use of a virtual environment.
For Windows users, the examples in this guide assume that the option to adjust the system PATH environment variable was selected when installing Python.
- insert the folder into your python directory
- and open the file: install.py

#manual installing:
1. install Python3 with pip

2. go to your CMD and type "py -m pip install discord.py" and after that "py -m pip install asyncio"

3. download this code

4. insert the code into your python3 folder

5. Create a Discord Bot (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Create-a-DiscordBOT) and let the bot join your server (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Let-the-Discord-Bot-join-your-server)

6. fill the token inside the token.json file (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-the-token-to-the-token.json-file)

7. get your Discord ID (enable the developer mode in discord (Settings -> Appearance; scroll down and check "Developer Mode") after that you can rightclick on your profile in a server member list and hit "copy id") and SteamID64 and fill them into the users.json file inside the moderators object. (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-your-Discord-ID-and-Steam-ID-into-the-users.json-file)

8. run the python script "bot.py"
 
 btw: you can set up a raspberry pi to have a small "server" running this bot in the background
