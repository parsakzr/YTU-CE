import hashlib
import time
import psycopg2

conn = psycopg2.connect("dbname=chatzdb user=chatz password=chatz")
conn.set_session(autocommit=True)


def createUser(username, password):
    hashedPass = hashlib.sha256(password.encode("utf-8")).hexdigest()
    token = hashlib.sha256(
        (username + str(int(time.time())) + password).encode("utf-8")).hexdigest()

    cur = conn.cursor()
    cur.execute("SELECT MAX(userid) FROM credentials LIMIT 1")

    row = cur.fetchone()
    if row:
        max = row[0]
    else:
        max = 0

    cur.execute("INSERT INTO credentials VALUES(%(userid)s, %(passhash)s, %(token)s, %(username)s)", {
                "userid": max + 1, "passhash": str(hashedPass), "token": str(token), "username": username})

    return str(token)

def login(username, password):
    hashedPass = hashlib.sha256(password.encode("utf-8")).hexdigest()
    cur = conn.cursor()
    cur.execute("SELECT passhash FROM credentials WHERE username=%(username)s", {
                "username": username})
    row = cur.fetchone()
    dbHash = row[0]
    if dbHash == hashedPass:
        cur.execute("SELECT token FROM credentials WHERE username=%(username)s", {
                    "username": username})
        row = cur.fetchone()
        token = row[0]
        return token
    return -1


def getUserId(token):
    cur = conn.cursor()
    cur.execute("SELECT userid from credentials WHERE token=%(token)s", {
                "token": token})
    row = cur.fetchone()
    if row[0]:
        return row[0]
    return -1

def getUsername(id):
    cur = conn.cursor()
    cur.execute("SELECT username from credentials where userid=%(id)s", {"id": id})
    row = cur.fetchone()
    if row[0]:
        return row[0]
    return -1