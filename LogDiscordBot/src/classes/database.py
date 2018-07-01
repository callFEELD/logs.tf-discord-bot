import sqlite3
import os

class DB():
    DATABASEDIR = "data/database.db"

    # create the database if it does not exists
    def __init__(self):
        self.conn = sqlite3.connect(self.DATABASEDIR)
        self.c = self.conn.cursor()

        try:
            self.c.execute('''CREATE TABLE servers
                                (serverid TEXT PRIMARY KEY, region TEXT)''')
            print("Created table: servers...")

            self.c.execute('''CREATE TABLE users 
                                (discordid TEXT PRIMARY KEY, 
                                steamid TEXT, time)''')
            print("Created table: users...")

            self.c.execute('''CREATE TABLE moderators 
                                (discordid TEXT, serverid TEXT,
                                FOREIGN KEY(discordid) REFERENCES users(discordid),
                                FOREIGN KEY(serverid) REFERENCES servers(serverid))''')
            print("Created table: moderators...")

            self.c.execute('''CREATE TABLE teams 
                                (name TEXT, serverid TEXT, type, creator INTEGER,
                                FOREIGN KEY(creator) REFERENCES users(discordid),
                                FOREIGN KEY(serverid) REFERENCES servers(serverid))''')
            print("Created table: teams...")

            self.c.execute('''CREATE TABLE playersinteams 
                                (discordid TEXT, serverid TEXT, tname INTEGER,
                                FOREIGN KEY(tname) REFERENCES teams(name),
                                FOREIGN KEY(discordid) REFERENCES users(discordid),
                                FOREIGN KEY(serverid) REFERENCES servers(serverid))''')
            print("Created table: playersinteams...")

        except Exception as e:
            print(str(e))
            #pass

    def insertServer(self, serverid, region):
        try:
            va = tuple([serverid] + [region])
            self.c.execute('INSERT INTO servers VALUES (?,?)', va)
            self.conn.commit()
            return True
        except Exception:
            return False

    def findServer(self, serverid):
        try:
            va = tuple([serverid])
            self.c.execute('SELECT serverid FROM servers WHERE serverid=?', va)
            result = self.c.fetchall()
            if len(result) > 0:
                return True
            return False
        except Exception:
            return False

    def selectServers(self):
        self.c.execute("SELECT * FROM servers")
        result = self.c.fetchall()
        ret = {}
        for id,r in result:
            ret.update({id: r})
        return ret

    def selectUsers(self):
        self.c.execute("SELECT * FROM users")
        result = self.c.fetchall()
        ret = {}
        for d,s,t in result:
            ret.update({"discord_id": d, "steam_id": s})
        return ret

    def findUser(self, discordid):
        try:
            va = tuple([discordid])
            self.c.execute('SELECT * FROM users WHERE discordid=?', va)
            result = self.c.fetchall()
            if len(result) > 0:
                ret = {}
                for d, s, t in result:
                    ret.update({"discord_id": d, "steam_id": s})
                return ret
            return False
        except Exception:
            return False

    def selectModerators(self):
        self.c.execute("SELECT * FROM moderators")
        result = self.c.fetchall()
        ret = {}
        for d,s in result:
            ret.update({d: s})
        return ret

    def insertUser(self, discordid, steamid):
        try:
            va = tuple([discordid] + [steamid])
            self.c.execute('INSERT INTO users VALUES (?,?, null)', va)
            self.conn.commit()
            return True
        except Exception:
            return False

    def deleteUser(self, discordid):
        try:
            va = tuple([discordid])
            self.c.execute('DELETE FROM users users WHERE (discordid == ?)', va)
            self.conn.commit()
            return True
        except Exception:
            return False


    def findTeams(self, server_id):
        try:
            va = tuple([server_id])
            self.c.execute('SELECT name, type, creator FROM teams WHERE serverid=?', va)
            result = self.c.fetchall()
            if len(result) > 0:
                ret = []
                for n, t, c in result:
                    ret.append({"name": n, "type": t, "creator": c})
                return ret
            return False
        except Exception:
            return False

    def findTeam(self, server_id, name):
        try:
            va = tuple([server_id] + [name])
            self.c.execute('SELECT name, type, creator FROM teams WHERE serverid=? AND name=?', va)
            result = self.c.fetchone()
            if len(result) > 0:
                name, type, creator = result
                self.c.execute('SELECT users.discordid, users.steamid FROM playersinteams INNER JOIN users \
                               on playersinteams.discordid = users.discordid WHERE serverid=? AND tname=?', va)
                result = self.c.fetchall()
                players = []
                for d, s in result:
                    players.append({"discord_id": d, "steam_id": s})
                ret = {"name": name, "type": type, "creator": creator, "players": players}
                print(ret)
                return ret
            return False
        except Exception:
            return False


    def insertTeam(self, server_id , name, type, creator_did):
        va = tuple([name] + [server_id] + [type] + [creator_did])
        self.c.execute('INSERT INTO teams VALUES (?,?,?,?)', va)
        self.conn.commit()

    def deleteTeam(self, server_id, name):
        try:
            va = tuple([server_id] + [name])
            self.c.execute('DELETE FROM teams WHERE serverid=? AND name=?', va)
            self.conn.commit()
            return True
        except Exception:
            return False


    def close(self):
        self.conn.commit()
        self.conn.close()