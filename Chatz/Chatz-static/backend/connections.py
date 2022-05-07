import psycopg2

conn = psycopg2.connect("dbname=chatzdb user=chatz password=chatz")
conn.set_session(autocommit=True)


def joinGuild(guildId, userId):
    cur = conn.cursor()

    cur.execute("INSERT INTO guildconnections VALUES(%(userid)s, %(guildid)s)", {
                "userid": userId, "guildid": guildId})
    
    return True


def getGuildsOfUser(userId):
    cur = conn.cursor()
    cur.execute("SELECT guildid FROM guildconnections WHERE userid=%(userid)s", {
                "userid": userId})

    rows = cur.fetchall()
    data = []

    for row in rows:
        data.append(row[0])

    return data

def getGuildMembers(guildId):
    cur = conn.cursor()

    cur.execute("SELECT userid FROM guildconnections WHERE guildid=%(guildid)s", {"guildid": guildId})
    
    rows = cur.fetchall()
    data = []
    
    for row in rows:
        data.append(row[0])

    return data

def getAllMembers():
    cur = conn.cursor()

    cur.execute("SELECT userid, username FROM credentials")
    
    rows = cur.fetchall()
    data = {}
    
    for row in rows:
        if row[0] not in data:
            data[row[0]] = row[1]

    return data

