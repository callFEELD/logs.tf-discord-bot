# last edit: 20.02.2019 (callFEELD)
import logging
from databases import Database
from src.config import DATABASE_DIR

print("reading database")

database = Database(DATABASE_DIR)


async def init_db():
    await database.connect()
    logging.info("Initialize Database...")
    try:
        # create the database if it does not exists
        await database.execute('''CREATE TABLE servers
                            (serverid TEXT PRIMARY KEY, region TEXT)''')
        logging.info("[DB] Created table: servers...")

        await database.execute(
            "CREATE TABLE users "
            "(discordid TEXT PRIMARY KEY, steamid TEXT, time)"
        )
        logging.info("[DB] Created table: users...")

        await database.execute(
            "CREATE TABLE moderators "
            "(discordid TEXT, serverid TEXT, FOREIGN KEY(discordid)"
            "REFERENCES users(discordid),"
            "FOREIGN KEY(serverid) REFERENCES servers(serverid))")
        logging.info("[DB] Created table: moderators...")

        await database.execute(
            "CREATE TABLE teams"
            "(name TEXT, serverid TEXT, type, creator INTEGER,"
            "FOREIGN KEY(creator) REFERENCES users(discordid),"
            "FOREIGN KEY(serverid) REFERENCES servers(serverid))"
        )
        logging.info("[DB] Created table: teams...")

        await database.execute(
            "CREATE TABLE playersinteams "
            "(discordid TEXT, uname TEXT, class TEXT, serverid TEXT,"
            "tname INTEGER, FOREIGN KEY(tname) REFERENCES teams(name),"
            "FOREIGN KEY(discordid) REFERENCES users(discordid),"
            "FOREIGN KEY(serverid) REFERENCES servers(serverid))"
        )
        logging.info("[DB] Created table: playersinteams...")

    except Exception as e:
        logging.error(e)


async def insertServer(serverid, region):
    try:
        va = {"server_id": serverid, "region": region}
        await database.execute('INSERT INTO servers VALUES (:server_id, :region)', va)
        return True
    except Exception:
        return False


async def delete_server(serverid):
    try:
        # get all teams of a server
        teams = await findTeams(serverid)
        for team in teams:
            #remove them
            await deleteTeam(serverid, team["name"])

        #then remove the server
        va = {"server_id": serverid}
        await database.execute('DELETE FROM server WHERE (serverid = :server_id)', va)
        return True
    except Exception:
        return False


async def findServer(serverid):
    try:
        va = {"server_id": serverid}
        result = await database.fetch_all('SELECT serverid FROM servers WHERE serverid=:server_id', va)
        if len(result) > 0:
            return True
        return False
    except Exception:
        return False


async def selectServers():
    result = await database.fetch_all("SELECT * FROM servers")
    ret = {}
    for sid,r in result:
        ret.update({sid: r})
    return ret


async def selectUsers():
    result = await database.fetch_all("SELECT * FROM users")
    ret = {}
    for d, s, _ in result:
        ret.update({"discord_id": d, "steam_id": s})
    return ret


async def findUser(discordid):
    try:
        va = {"discordid": discordid}
        result = await database.fetch_all('SELECT * FROM users WHERE discordid=:discordid', va)
        if len(result) > 0:
            ret = {}
            for d, s, _ in result:
                ret.update({"discord_id": d, "steam_id": s})
            return ret
    except Exception as e:
        logging.error(e)


async def selectModerators():
    await database.execute("SELECT * FROM moderators")
    result = await database.fetchall()
    ret = {}
    for d,s in result:
        ret.update({d: s})
    return ret


async def insertUser(discordid, steamid):
    va = {"discordid": discordid, "steamid": steamid}
    await database.execute('INSERT INTO users VALUES (:discordid, :steamid, null)', va)


async def updateUser(discordid, steamid):
    va = {"steamid": steamid, "discordid": discordid}
    await database.execute('UPDATE users SET steamid=:steamid WHERE discordid=:discordid', va)


async def deleteUser(discordid):
    try:
        va = {"discordid": discordid}
        await database.execute('DELETE FROM users users WHERE (discordid == :discordid)', va)
        return True
    except Exception:
        return False


async def findTeams(server_id):
    try:
        va = {"server_id": server_id}
        result = await database.fetch_all('SELECT name, type, creator FROM teams WHERE serverid=:server_id', va)
        if len(result) > 0:
            ret = []
            for n, t, c in result:
                ret.append({"name": n, "type": t, "creator": c})
            return ret
        return False
    except Exception:
        return False


async def findTeam(server_id, name):
    va = {"server_id": server_id, "name": name}
    result = await database.fetch_one(
        "SELECT name, type, creator FROM teams WHERE serverid=:server_id AND name=:name",
        va
    )
    if result is not None and len(result) > 0:
        name, t_type, creator = result
        result = await database.fetch_all(
            "SELECT playersinteams.uname, playersinteams.class, users.discordid, users.steamid FROM playersinteams INNER JOIN users \
            on playersinteams.discordid = users.discordid WHERE serverid=:server_id AND tname=:name", va
        )
        players = []
        for n, c, d, s in result:
            players.append({
                "name": n,
                "class": c,
                "discord_id": d,
                "steam_id": s
            })
        ret = {
            "name": name,
            "type": t_type,
            "creator": creator,
            "players": players
        }
        return ret


async def insertTeam(server_id , name, t_type, creator_did):
    va = {
        "name": name,
        "server_id": server_id,
        "t_type": t_type,
        "creator_did": creator_did
    }
    await database.execute('INSERT INTO teams VALUES (:name, :server_id, :t_type, :creator_did)', va)


async def insertPlayerToTeam(server_id, teamname, discordid, playername, class_type):
    va = {
        "discordid": discordid,
        "playername": playername,
        "class_type": class_type,
        "server_id": server_id,
        "teamname": teamname
    }
    await database.execute('INSERT INTO playersinteams VALUES (:discordid, :playername, :class_type, :server_id, :teamname)', va)


async def updatePlayerToTeam(server_id, teamname, discordid, playername, class_type):
    va = {
        "discordid": discordid,
        "playername": playername,
        "class_type": class_type,
        "server_id": server_id,
        "teamname": teamname
    }
    await database.execute('UPDATE playersinteams SET uname=:playername, class=:class_type WHERE discordid=:discordid and serverid=:server_id and tname=:teamname', va)


async def removePlayerOfTeam(server_id, teamname, discordid):
    va = {
        "server_id": server_id,
        "teamname": teamname,
        "discordid": discordid
    }
    await database.execute('DELETE FROM playersinteams WHERE serverid=:server_id AND tname=:teamname AND discordid=:discordid', va)


async def deleteTeam(server_id, name):
    try:
        va = {"server_id": server_id, "name": name}
        await database.execute('DELETE FROM teams WHERE serverid=:server_id AND name=:name', va)
        return True
    except Exception:
        return False


async def close():
    await database.commit()
    await database.close()
