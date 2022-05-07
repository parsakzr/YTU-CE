import psycopg2
from psycopg2 import sql


conn = psycopg2.connect(database="taksidb", user="postgres", password="postgres", host="localhost", port="5432")
conn.set_session(autocommit=True)


def newCar(license_plate, car_type, c_model, prod_year, engine_spec, car_loc, base_rate):
    cur = conn.cursor()
    cur.execute("INSERT INTO car VALUES(%(license_plate)s, %(car_type)s, %(c_model)s, %(prod_year)s, %(engine_spec)s, %(car_loc)s, %(base_rate)s)", {
                "license_plate": license_plate, "car_type": car_type, "c_model": c_model, "prod_year": prod_year, "engine_spec": engine_spec, "car_loc": car_loc, "base_rate": base_rate})
    return True


def deleteCar(license_plate):
    cur = conn.cursor()
    cur.execute("DELETE FROM car WHERE license_plate=%(license_plate)s", {"license_plate": license_plate})
    return True


def getAllCars():
    cur = conn.cursor()
    cur.execute("SELECT * FROM car")
    data = cur.fetchall()
    return data


def getAvailableCars():
    cur = conn.cursor()
    cur.execute("SELECT * FROM car WHERE is_available=True")
    data = cur.fetchall()
    return data

def getOccupiedCars():
    cur = conn.cursor()
    cur.execute("SELECT * FROM car WHERE is_available=False")
    data = cur.fetchall()
    return data


def getCar(license_plate):
    cur = conn.cursor()
    cur.execute("SELECT * FROM car WHERE license_plate=%(license_plate)s", {"license_plate": license_plate})
    data = cur.fetchall()
    return data


def getCars_filtered(car_model=None, car_type=None, car_loc=None):
    queries = []
    params = {}
    if(car_model):
        params['car_model'] = car_model
    if(car_type):
        params['car_type'] = car_type
    if(car_loc):
        params['car_loc'] = car_loc

    
    for field in params.keys():
        queries.append(sql.SQL("SELECT * FROM car WHERE {}=%s").format(sql.Identifier(field)))

    query = sql.SQL("{}").format(sql.SQL(" INTERSECT ").join(queries))

    cur = conn.cursor()

    try:
        cur.execute(query, list(params.values()))
    except:
        print("Error: unable to fetch data")
        return None

    data = cur.fetchall()
    return data
