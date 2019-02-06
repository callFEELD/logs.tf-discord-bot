![](https://image.jimcdn.com/app/cms/image/transf/none/path/s7a796ecadbf7bd45/image/i971200078c801228/version/1518474229/image.png)

A discord bot showing your recent logs, profile page and team matches based on the website http://logs.tf. You can create teams, fill them with players and get recent matches of the teams. You can also search for other persons logs and logs.tf profile's.

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/7bdca2c5c8ae4568924f7d0814364ffa)](https://app.codacy.com/app/callfeeld/logs.tf-discord-bot?utm_source=github.com&utm_medium=referral&utm_content=callFEELD/logs.tf-discord-bot&utm_campaign=Badge_Grade_Dashboard)


[![](https://image.jimcdn.com/app/cms/image/transf/dimension=234x10000:format=png/path/s7a796ecadbf7bd45/image/i0cec09af71753cd0/version/1518475074/image.png)](https://callfeeld.jimdo.com/logs-tf-discord-bot/commands/)
[![](https://image.jimcdn.com/app/cms/image/transf/dimension=230x10000:format=png/path/s7a796ecadbf7bd45/image/i9e494036347e1de1/version/1518475106/image.png)](https://github.com/callFEELD/logs.tf-discord-bot/wiki)
[![](https://image.jimcdn.com/app/cms/image/transf/dimension=225x10000:format=png/path/s7a796ecadbf7bd45/image/i49fc7bd83a4ac903/version/1518475082/image.png)](https://callfeeld.jimdo.com/logs-tf-discord-bot/)



Don't want to have a hard time installing?

![](https://image.jimcdn.com/app/cms/image/transf/dimension=500x10000:format=png/path/s7a796ecadbf7bd45/image/i26e3855a94297c9f/version/1530651637/image.png)

comming soon...

An official bot is under development right now. If you want to take part of beta [contact me](https://steamcommunity.com/id/callFEELD). During the beta phase be warned that the bot could be offline for troubleshooting for a few minutes. Also data can be lost during processes.


## Install instructions
You can set up a raspberry pi to have a small "server" running this bot in the background. Here are various types how you can install the discord bot.

![](https://cdn1.iconfinder.com/data/icons/logos-brands-1/24/logo_brand_brands_logos_microsoft_windows-48.png)
and 
![](https://cdn1.iconfinder.com/data/icons/logos-brands-1/24/logo_brand_brands_logos_linux-48.png) were successfully tested.

dependencies:
- [Python 3.6 or higher](https://www.python.org/)
- [discord.py libary](https://github.com/Rapptz/discord.py)


### Linux
[![](https://image.jimcdn.com/app/cms/image/transf/dimension=230x10000:format=png/path/s7a796ecadbf7bd45/image/i830d15d81ecbc750/version/1518475078/image.png)](https://callfeeld.jimdo.com/logs-tf-discord-bot/install-guide-linux/)


### Docker
First download the git repository
```bash
git clone https://github.com/callFEELD/logs.tf-discord-bot
```

Next hop into the folder `logs.tf-discord-bot/LogDiscordBot/data/cfg/` and add your discord bot token
```bash
cd logs.tf-discord-bot/
nano LogDiscordBot/data/cfg/token.json
```

Then create a docker volume to access the database for backup purposes
```bash
docker volume create LogDiscordBot
```

After that you can build the docker iamge
```bash
docker build . -t logdiscordbot
```

Now you can run the bot. In this run command we connect our created Docker Volume `LogDiscordBot` with the location of the database and the config in the Docker Container `/logdiscordbot/data`.
```bash
docker run -d --name logdiscordbot -v LogDiscordBot:/logdiscordbot/data logdiscordbot
```
A good addition for this command is to automatically let the docker container restart on close:
```bash
docker run --restart always -d --name logdiscordbot -v LogDiscordBot:/logdiscordbot/data logdiscordbot
```
You can start and stop the bot with:
```bash
docker start logdiscordbot
```
```bash
docker stop logdiscordbot
```

### Manual install
1. install [Python3](https://www.python.org/downloads/) with pip

Note For POSIX users (including Mac OS X and Linux users), the examples in this guide assume the use of a virtual environment.
For Windows users, the examples in this guide assume that the option to adjust the system PATH environment variable was selected when installing Python.

2. go to your CMD and type "python3 -m pip install discord.py" and after that "python3 -m pip install asyncio"

3. download this code

4. insert the code into your python3 folder

5. Create a Discord Bot (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Create-a-DiscordBOT) and let the bot join your server (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Let-the-Discord-Bot-join-your-server)

6. fill the token inside the token.json file (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-the-token-to-the-token.json-file)

7. get your Discord ID (enable the developer mode in discord (Settings -> Appearance; scroll down and check "Developer Mode") after that you can rightclick on your profile in a server member list and hit "copy id") and SteamID64 and fill them into the users.json file inside the moderators object. (tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-your-Discord-ID-and-Steam-ID-into-the-users.json-file)

8. run the python script "bot.py" with "python3 bot.py"
