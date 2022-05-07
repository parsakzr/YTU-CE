import psycopg2

conn = psycopg2.connect("dbname=chatzdb user=chatz password=chatz")
conn.set_session(autocommit=True)


def createGuild(guildName, creatorId):
    cur = conn.cursor()
    cur.execute("SELECT MAX(guildid) FROM guilds LIMIT 1")

    row = cur.fetchone()
    if row[0]:
        max = row[0]
    else:
        max = 0

    cur.execute("INSERT INTO guilds VALUES(%(guildid)s, %(guildname)s, %(creatorid)s)", {
                "guildid": max + 1, "guildname": guildName, "creatorid": str(creatorId)})

    return (max + 1)

def getGuildData(guildId):
    cur = conn.cursor()
    cur.execute("SELECT * from guilds where guildid=%(guildid)s",
                {"guildid": guildId})

    row = cur.fetchone()
    if row is not None:
        return {"guildName": row[1], "creatorId": row[2]}
    else:
        return -1
