# This Class is there to handle actions that contain changing the database (users.json) file
# It only handles the actions for teams
# last edit: 20.02.2019 (callFEELD)
import src.database as DB


# returns the team with the name or False
async def get_team(server_id, name):
    return await DB.findTeam(server_id, name)


# returns all teams in a list
async def get_teams(server_id):
    return await DB.findTeams(server_id)


# Adds a user to a team
async def add_teamroster(server_id, teamname, discordid, playername, class_type):
    # add user with discordid and steamid to the teamlist
    await DB.insertPlayerToTeam(
        server_id, teamname, discordid, playername, class_type
    )


# Updates a user in a team
async def update_teamroster(server_id, teamname, discordid, playername, class_type):
    # updates user with discordid and steamid to the teamlist
    await DB.updatePlayerToTeam(
        server_id, teamname, discordid, playername, class_type
    )


# remove a user of a team
async def remove_teamroster(server_id, teamname, discordid):
    await DB.removePlayerOfTeam(server_id, teamname, discordid)


# creates a team
async def create_team(server_id, teamname, team_format, creator):
    await DB.insertTeam(server_id, teamname, team_format, creator)


# deletes a team
async def delete_team(server_id, teamname):
    await DB.deleteTeam(server_id, teamname)
