import sqlite3
import os

class DB():
    DATABASEDIR = "data/database.db"

    # create the database if it does not exists
    def __init__(self):
        self.conn = sqlite3.connect(self.DATABASEDIR)
        self.c = self.conn.cursor()

        try:
            self.c.execute('''CREATE TABLE users
                              (discordid TEXT PRIMARY KEY, steamid TEXT, time)''')
            print("Created table: users...")
            self.c.execute('''CREATE TABLE moderators
                              (discordid INTEGER,
                               FOREIGN KEY(discordid) REFERENCES users(discordid))''')
            print("Created table: moderators...")
            self.c.execute('''CREATE TABLE teams
                                (name TEXT PRIMARY KEY, type,
                                 creator INTEGER,
                                 FOREIGN KEY(creator) REFERENCES users(discordid))''')
            print("Created table: teams...")
            self.c.execute('''CREATE TABLE playersinteams
                                (discordid INTEGER, tname INTEGER,
                                 FOREIGN KEY(tname) REFERENCES teams(name),
                                 FOREIGN KEY(discordid) REFERENCES users(discordid))''')
            print("Created table: playersinteams...")
        except Exception as e:
            #print(str(e))
            pass

    def selectUsers(self):
        self.c.execute("SELECT * FROM users")
        result = self.c.fetchall()
        ret = {}
        for d,s,t in result:
            ret.update({d: s})
        return ret

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
            return True
        except Exception:
            return False

    def deleteUser(self, discordid):
        try:
            va = tuple([discordid])
            self.c.execute('DELETE FROM users users WHERE (discordid == ?)', va)
            return True
        except Exception:
            return False


    def selectTeams(self):
        try:
            self.c.execute("SELECT * FROM teams")
            result = self.c.fetchall()
            ret = {}
            for n,t,d in result:
                ret.update({d: t})

            return ret
        except Exception as e:
            return False


    def insertTeam(self, name, type, creator_did):
        va = tuple([name] + [type] + [creator_did])
        self.c.execute('INSERT INTO teams VALUES (?,?,?)', va)


    def close(self):
        self.conn.commit()
        self.conn.close()