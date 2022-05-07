import psycopg2
from time import time
conn = psycopg2.connect("dbname=chatzdb user=chatz password=chatz")
conn.set_session(autocommit=True)


def sendMessage(userId, message, channelId):
    cur = conn.cursor()
    epoch = int(time())

    cur.execute("SELECT MAX(messageid) FROM messages LIMIT 1")

    row = cur.fetchone()
    if row[0]:
        max = row[0]
    else:
        max = 0

    cur.execute("INSERT INTO messages VALUES(%(content)s, %(messageid)s, %(time)s, %(channelid)s, %(senderid)s)", {
                "content": message, "messageid": max + 1, "time": epoch, "channelid": channelId, "senderid": userId})

    return True
    
def getMessages(channelId, after=None):
    cur = conn.cursor()
    if not after:
        cur.execute(
            "SELECT * FROM messages where channelid=%(channelid)s", {"channelid": channelId})
    else:
        cur.execute("SELECT * FROM messages where channelid=%(channelid)s and time > %(after)s",
                    {"channelid": channelId, "after": after})

    rows = cur.fetchall()
    data = []
    for row in rows:
        data.append(
            {"content": row[0], "messageId": row[1], "time": row[2], "senderId": row[4]})

    return data


def deleteMessage(messageId):
    cur = conn.cursor()
    if len(str(messageId)) > 0:
        cur.execute("DELETE FROM messages where messageid=%(messageid)s", {
                    "messageid": messageId})
