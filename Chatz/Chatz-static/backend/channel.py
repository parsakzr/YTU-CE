import psycopg2

conn = psycopg2.connect("dbname=chatzdb user=chatz password=chatz")
conn.set_session(autocommit=True)


def createChannel(channelName, guildId):
    cur = conn.cursor()
    cur.execute("SELECT MAX(channelid) FROM channels LIMIT 1")

    row = cur.fetchone()
    if row[0]:
        max = row[0]
    else:
        max = 0

    cur.execute("INSERT INTO channels VALUES(%(guildid)s, %(channelname)s, %(channelid)s)", {
                "channelname": channelName, "channelid": max + 1, "guildid": guildId})

    return (max + 1)
    
def getGuildChannels(guildId):
    cur = conn.cursor()
    cur.execute("SELECT * FROM channels where guildid=%(guildid)s",
                {"guildid": guildId})

    rows = cur.fetchall()
    data = []

    for row in rows:
        data.append({"channelName": row[1], "channelId": row[2]})

    return data
