# logs.tf discord bot (Log Bot)

A discord bot showing your recent logs, profile page and team matches. You can create teams, fill them with players and get recent matches of the teams. You can also search for other persons logs and logs.tf profile's.

### ![](https://cdn1.iconfinder.com/data/icons/hawcons/32/698552-icon-40-clipboard-list-32.png)[commands](https://github.com/callFEELD/logs.tf-discord-bot/wiki/Commands)

![image](https://image.jimcdn.com/app/cms/image/transf/dimension=441x10000:format=png/path/s7a796ecadbf7bd45/image/i81d0cdc47ad5fe02/version/1514911419/image.png)

### ![](https://cdn1.iconfinder.com/data/icons/hawcons/32/698436-icon-31-book-bookmark-32.png)[Wiki on GitHub](https://github.com/callFEELD/logs.tf-discord-bot/wiki)

### ![](https://cdn1.iconfinder.com/data/icons/hawcons/32/698436-icon-31-book-bookmark-32.png)[Wiki on my Website (WIP)](https://callfeeld.jimdo.com/projects/logs-tf-discord-bot/)

## requirements
### Operatring systems:
![](https://cdn1.iconfinder.com/data/icons/logos-brands-1/24/logo_brand_brands_logos_microsoft_windows-48.png)
or
![](https://cdn1.iconfinder.com/data/icons/logos-brands-1/24/logo_brand_brands_logos_linux-48.png)

This script was tested on Linux and Windows.
### programs
- [Python 3.6 or higher](https://www.python.org/)
- [discord.py libary](https://github.com/Rapptz/discord.py)

## installing
TIP: you can set up a raspberry pi to have a small "server" running this bot in the background

### ![](https://cdn1.iconfinder.com/data/icons/logos-brands-1/24/logo_brand_brands_logos_linux-24.png)[Linux installguide](https://callfeeld.jimdo.com/projects/logs-tf-discord-bot/install-guide-linux/)

### manual installing guide:
1. install [Python3](https://www.python.org/downloads/) with pip

Note For POSIX users (including Mac OS X and Linux users), the examples in this guide assume the use of a virtual environment.
For Windows users, the examples in this guide assume that the option to adjust the system PATH environment variable was selected when installing Python.

2. go to your CMD and type "python3 -m pip install discord.py" and after that "python pip install asyncio"

3. download this code

4. insert the code into your python3 folder

5. Create a Discord Bot (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Create-a-DiscordBOT) and let the bot join your server (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Let-the-Discord-Bot-join-your-server)

6. fill the token inside the token.json file (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-the-token-to-the-token.json-file)

7. get your Discord ID (enable the developer mode in discord (Settings -> Appearance; scroll down and check "Developer Mode") after that you can rightclick on your profile in a server member list and hit "copy id") and SteamID64 and fill them into the users.json file inside the moderators object. (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-your-Discord-ID-and-Steam-ID-into-the-users.json-file)

8. run the python script "bot.py" with "python3 bot.py"
