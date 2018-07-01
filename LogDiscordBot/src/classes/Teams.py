# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for teams
# last edit: 21.04.2018 (callFEELD)

# imports
import json
from src.classes import database

class LogBotTeams:
    # CONFIG
    # The databse file containing the users, moderators and teams
    teamfile = "data/users.json"
    teamlist = open(teamfile, "r").read()
    teamlist = json.loads(teamlist)
    db = database.DB()

    def __init__(self):
        self.loadteams()

    # NOT NEEDED
    # Loads the member list as json format and converts it into an object
    def loadteams(self):
        # opens file and load as json
        self.teamlist = open(self.teamfile, "r").read()
        self.teamlist = json.loads(self.teamlist)

    # NOT NEEDED
    # Updates(reloads) the user file
    def update(self):
        self.loadteams()

    # NOT NEEDED
    # saves the userlist to the users file
    def save(self):
        file = open(self.teamfile, "w")
        file.write(json.dumps(self.teamlist))

    # returns the team with the name or False
    def get_team(self, server_id, name):
        return self.db.findTeam(server_id, name)

    # returns all teams in a list
    def get_teams(self, server_id):
        return self.db.findTeams(server_id)

    # Adds a user to a team
    def add_team(self, server_id, teamname, discordid, playername):
        # add user with discordid and steamid to the teamlist
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1
        self.teamlist["teams"][arrayposition][teamname][1]["players"].update({discordid: playername})


    # remove a user of a team
    def remove_team(self, teamname, discordid):
        # Updates File to be perfectly save
        self.update()

        # remove user from a team
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1
        del self.teamlist["teams"][arrayposition][teamname][1]["players"][discordid]

        # save the updated teamlist into the user file
        self.save()

    # creates a team
    def create_team(self, server_id, teamname, type, creator):
        self.db.insertTeam(server_id, teamname, type, creator)

    # deletes a team
    def delete_team(self, server_id, teamname):
        self.db.deleteTeam(server_id, teamname)