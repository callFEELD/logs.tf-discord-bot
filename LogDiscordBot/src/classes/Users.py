# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for users and moderators

#imports
import json
from src.classes import database

class LogBotUsers:
    # CONFIG
    # The databse file containing the users, moderators and teams
    db = database.DB()
    moderators = None

    def __init__(self):
        self.loadusers()

    # Loads the member list as json format and converts it into an object
    def loadusers(self):
        # opens file and load as json
        self.userlist = self.db.selectUsers()
        self.moderators = self.db.selectModerators()

    # Updates(reloads) the user file
    def update(self):
        self.loadusers()

    # returns all moderators in a list
    def getmoderators(self):
        self.update()
        return self.moderators

    # returns all players in a list
    def getplayers(self):
        self.update()
        return self.userlist

    # returns all players in a list
    def get_player(self, discordid):
        return self.db.findUser(discordid)

    def getplayers_steamid(self, discordid):
        # grabs playerlist
        playerlist = self.getplayers()
        return playerlist[discordid]

    ''' REMOVED OF THE SERVER EDITION
    # Adds a user
    def add_user(self, discordid, steamid):
        # add user with discordid and steamid to the userlist
        self.db.insertUser(discordid, steamid)

    # remove a user
    def remove_user(self, discordid):
        # remove user from userlist
        # self.db.deleteUser(discordid)
    '''