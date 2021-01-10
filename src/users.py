# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for users and moderators
# last edit: 20.02.2019 (callFEELD)
import src.database as DB

# CONFIG
# The databse file containing the users, moderators and teams
_moderators = None
_userlist = None


# Loads the member list as json format and converts it into an object
async def loadusers():
    global _userlist
    global _moderators
    # opens file and load as json
    _userlist = await DB.selectUsers()
    _moderators = await DB.selectModerators()


# Updates(reloads) the user file
async def update():
    await loadusers()


# returns all moderators in a list
async def getmoderators():
    await update()
    return _moderators


# returns all players in a list
async def getplayers():
    await update()
    return _userlist


# returns all players in a list
async def get_player(discordid):
    return await DB.findUser(discordid)


async def getplayers_steamid(discordid):
    # grabs playerlist
    playerlist = await getplayers()
    return playerlist[discordid]


# Adds a user
async def add_user(discordid, steamid):
    # add user with discordid and steamid to the userlist
    await DB.insertUser(discordid, steamid)


# updates a user
async def update_user(discordid, steamid):
    # add user with discordid and steamid to the userlist
    await DB.updateUser(discordid, steamid)
