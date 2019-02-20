# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for teams
# last edit: 20.02.2019 (callFEELD)

class LogBotTeams:
    
    def __init__(self, database):
        self.db = database

    # returns the team with the name or False
    def get_team(self, server_id, name):
        return self.db.findTeam(server_id, name)

    # returns all teams in a list
    def get_teams(self, server_id):
        return self.db.findTeams(server_id)

    # Adds a user to a team
    def add_teamroster(self, server_id, teamname, discordid, playername, class_type):
        # add user with discordid and steamid to the teamlist
        self.db.insertPlayerToTeam(server_id, teamname, discordid, playername, class_type)

    # Updates a user in a team
    def update_teamroster(self, server_id, teamname, discordid, playername, class_type):
        # updates user with discordid and steamid to the teamlist
        self.db.updatePlayerToTeam(server_id, teamname, discordid, playername, class_type)

    # remove a user of a team
    def remove_teamroster(self, server_id, teamname, discordid):
        self.db.removePlayerOfTeam(server_id, teamname, discordid)

    # creates a team
    def create_team(self, server_id, teamname, team_format, creator):
        self.db.insertTeam(server_id, teamname, team_format, creator)

    # deletes a team
    def delete_team(self, server_id, teamname):
        self.db.deleteTeam(server_id, teamname)