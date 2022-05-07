import psycopg2

conn = psycopg2.connect(database="taksidb", user="postgres", password="postgres", host="localhost", port="5432")
conn.set_session(autocommit=True)

cur = conn.cursor()

def newTrip():
    cur.execute("")
