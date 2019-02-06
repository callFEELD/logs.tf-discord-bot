# Linux Install Guide

! Disclaimer ! This was tested on a `Raspberrry Pi` running `Rasbian` and on a root server with `Ubuntu 16 Server`.

## dependencies
You need [Python 3.6 or higher](https://www.python.org/) and [git](https://git-scm.com/). If they not already installed please make sure you install them. Also make sure that the python packet manager pip is installed aswell. 

### python dependencies
This software relies on [discord.py libary](https://github.com/Rapptz/discord.py) and therefore also on `asyncio`.

Therefore install both libaries with pip
```bash
python3 pip install discord.py
```
```bash
python3 pip install asyncio
```

## [Optional] Using the install script
If you want to make it a bit easier you can use the install script.
This means you don't need to install the `python dependencies`. It also removes the step `2. Adding the discord token`.


First follow step `1. Downloading the code`. Then execute the install script
```bash
python3 install.py
```
Here just follow the console instructions.

After end of the script you only need to start the bot. Here follow the step `3. Run the bot`.

Reminder: If the install script fails, follow the other instructions and ignore the `[Optional]` steps.


## install instructions
If you got every dependencies listed above we can start with the installation process.

### 1. Downloading the code
Clone the files of the GitHub repo to your linux machine and hop into the downloaded folder.
```bash
git clone https://github.com/callFEELD/logs.tf-discord-bot.git
cd logs.tf-discord-bot/LogDiscordBot
```

### 2. Adding the discord token
Now you have to get your discord bot token and add it to the file `LogDiscordBot/cfg/token.json`. Here is a [guideline](https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-the-token-to-the-token.json-file) of how the token is added, if you don't know json.


### 3. Let the bot join your server
let the bot join your server [how to]( https://github.com/callFEELD/logs.tf-discord-bot/wiki/Let-the-Discord-Bot-join-your-server)


### 4. Run the bot
```bash
python3 run.py
```

#### Tip to run the bot in the background
You can easily let the bot run in the background so you dont have to let the script running in your console or ssh console. Just use this command line.
```bash
nohup python3 bot.py &
```