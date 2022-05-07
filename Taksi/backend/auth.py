import psycopg2
import hashlib

conn = psycopg2.connect(database="taksidb", user="postgres", password="postgres", host="localhost", port="5432")
conn.set_session(autocommit=True)

curr = conn.cursor()

def addUser(username, password, user_type):
    if(user_type != "customer" and user_type != "manager"):
        return False
    hashedPass = hashlib.sha256(password.encode("utf-8")).hexdigest()

    try:
        curr.execute("INSERT INTO credentials VALUES(%(username)s, %(password)s, %(user_type)s)", {
                    "username": username, "password": hashedPass, "user_type": user_type})
    except:
        print("Error: username already exists")
        return False
    
    return True


def login(username, password):
    hashedPass = hashlib.sha256(password.encode("utf-8")).hexdigest()

    try:
        curr.execute("SELECT password FROM credentials WHERE username=%(username)s", {
                    "username": username})
    except:
        print("Error: could not login")
        return False
    
    row = curr.fetchone()
    db_hashedPass = row[0]
    if db_hashedPass != hashedPass:
        return False

    return True


print(addUser("test", "test", "customer"))

