# Manual install


## 1. Install the dependencies
You need [Python 3.6 or higher](https://www.python.org/) and [git](https://git-scm.com/). If they not already installed please make sure you install them. Also make sure that the python packet manager pip is installed aswell. 


Note For POSIX users (including Mac OS X and Linux users), the examples in this guide assume the use of a virtual environment.
For Windows users, the examples in this guide assume that the option to adjust the system PATH environment variable was selected when installing Python.

### 1.1 Python dependencies
This software relies on [discord.py libary](https://github.com/Rapptz/discord.py) and therefore also on `asyncio`.

Therefore install both libaries with pip
```bash
python3 pip install discord.py
```
```bash
python3 pip install asyncio
```

## 2. Download this code
You can either click the download button on the github page or use git.
Git: 
```bash
git clone https://github.com/callFEELD/logs.tf-discord-bot.git
```

## 3. Create a Discord Bot 
(tutorial: https://github.com/callFEELD/logs.tf-discord-bot/wiki/Create-a-DiscordBOT)

## 4. Adding the discord token
Now you have to get your discord bot token and add it to the file `LogDiscordBot/cfg/token.json`. Here is a [guideline](https://github.com/callFEELD/logs.tf-discord-bot/wiki/insert-the-token-to-the-token.json-file) of how the token is added, if you don't know json.

## 5. Let the bot join your server
let the bot join your server [how to]( https://github.com/callFEELD/logs.tf-discord-bot/wiki/Let-the-Discord-Bot-join-your-server)

## 6. Run the bot 
Either double click on the file `run.py` in the `LogDiscordBot` dir or use the command line:
```bash
python3 LogDiscordBot/run.py
```