# Docker Install Guide
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

Now you have to get your discord bot token and add it to the file `LogDiscordBot/cfg/token.json`. Here is a [guideline](https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-the-token-to-the-token.json-file) of how the token is added, if you don't know json.


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


Then let the bot join your server [how to]( https://github.com/callFEELD/logs.tf-discord-bot/wiki/Let-the-Discord-Bot-join-your-server)

## Server tips
Create a crontab or a autostart script that allow the bot to be started on every reboot.