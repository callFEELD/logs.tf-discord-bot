# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for teams
# last edit: 21.04.2018 (callFEELD)

# imports
import json

class LogBotTeams:
    # CONFIG
    # The databse file containing the users, moderators and teams
    teamfile = "data/users.json"
    teamlist = open(teamfile, "r").read()
    teamlist = json.loads(teamlist)

    def __init__(self):
        self.loadteams()

    # Loads the member list as json format and converts it into an object
    def loadteams(self):
        # opens file and load as json
        self.teamlist = open(self.teamfile, "r").read()
        self.teamlist = json.loads(self.teamlist)

    # Updates(reloads) the user file
    def update(self):
        self.loadteams()

    # saves the userlist to the users file
    def save(self):
        file = open(self.teamfile, "w")
        file.write(json.dumps(self.teamlist))

    # returns all teams in a list
    def getteams(self):
        self.update()
        return self.teamlist["teams"]

    # Adds a user to a team
    def add_team(self, teamname, discordid, playername):
        # Updates File to be perfectly save
        self.update()

        # add user with discordid and steamid to the teamlist
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1
        self.teamlist["teams"][arrayposition][teamname][1]["players"].update({discordid: playername})

        # save the new teamlist into the user file
        self.save()

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
    def create_team(self, teamname, type):
        # Updates File to be perfectly save
        self.update()

        # add team with name and type to the team list
        newteam = {teamname: [{"type": type}, {"players": {}}]}
        self.teamlist["teams"].append(newteam)

        # save the new team into the user file
        self.save()

    # deletes a team
    def delete_team(self, teamname):
        # Updates File to be perfectly save
        self.update()

        # deletes the team
        arrayposition = 0
        for team in self.teamlist["teams"]:
            if teamname in team:
                break
            arrayposition += 1

        del self.teamlist["teams"][arrayposition]

        # save the updated teamlist into the user file
        self.save()