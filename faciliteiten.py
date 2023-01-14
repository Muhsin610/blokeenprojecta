import psycopg2
import atexit

hostname = 'localhost'
database = 'projectA'
username = 'postgres'
pwd = 'Trabzon6161_'
port_id = 5432
conn = psycopg2.connect(
    host=hostname,
    dbname=database,
    user=username,
    password=pwd,
    port=port_id)
cur = conn.cursor()

def exit_handler():
    conn.close()
    print('Connection has been closed!')

# Hier worden de tabellen aangemaakt waar we data in kunnen opslaan

create_script5 = """CREATE TABLE IF NOT EXISTS service(
                            id serial PRIMARY KEY,
                            naam varchar(255) NOT NULL
                            )"""

create_script0 = """ CREATE TABLE if not exists station (
                            id serial primary key,
                            naam varchar(255) not null
                            )"""
create_script1 = """ CREATE TABLE if not exists bericht (
                            bericht_id serial primary key,
                            naam varchar(255) null,
                            tekst varchar(255) null,
                            datum date not null,
                            tijd time not null,
                            goedOfAfgekeurd varchar(255) null,
                            tijdBeoordeling time null,
                            stationNaam varchar(255) not null
                            )"""

create_script2 = """ CREATE TABLE if not exists alleBericht (
                            bericht_id integer,
                            naam varchar(255) null,
                            tekst varchar(255) null,
                            datum date not null,
                            tijd time not null,
                            goedOfAfgekeurd varchar(255) null,
                            tijdBeoordeling time null,
                            stationNaam varchar(255) not null
                            )"""


create_script3 = """ CREATE TABLE if not exists moderator (
                            moderator_id serial primary key,
                            naam varchar(255) not null,
                            email varchar(255) not null,
                            wachtwoord varchar(255) not null
                            )"""

create_script4 = """ CREATE TABLE IF NOT EXISTS voorziening(
                            id serial primary key,
                            fk_station_id int NOT NULL,
                            fk_service_id int NOT NULL,
                            aantal int NOT NULL,
                            FOREIGN KEY(fk_station_id) REFERENCES station(id),
                            FOREIGN KEY(fk_service_id) REFERENCES service(id)
                            )"""



cur.execute(create_script5)
cur.execute(create_script0)
cur.execute(create_script1)
cur.execute(create_script2)
cur.execute(create_script3)
cur.execute(create_script4)


cur.execute( """INSERT INTO moderator (naam, email, wachtwoord)
                VALUES('Muhsin Kan', 'muhsinkan61@hotmail.com', '0000')""")

# Ik gebruik een drop table, want dan komt er geen dubbele data in onze datbase, want als het de programma runt de hele tijd komt er dubbele gegevens erin.

def insert_statements():
    stations = [('Utrecht'), ('Amsterdam'), ('Den Haag')]
    for station in stations:
        cur.execute("INSERT INTO station(naam) VALUES (%s)", (station,))

    voorziening = [('ov_fiets'), ('lift'), ('toilet'), ('park_and_ride')]
    for namen in voorziening:
        cur.execute("INSERT INTO service(naam) VALUES (%s)", (namen,))

    voorzieningen_script = "INSERT INTO  voorziening(fk_station_id,fk_service_id,aantal) VALUES (%s,%s,%s)"
    voorzieningen_values = [(1, 2, 5), (1, 1, 15), (1, 3, 20), (1, 4, 210),  (2, 4, 200), (2, 3, 10), (2, 1, 30), (2, 2, 0),
                            (3, 2, 4), (3, 3, 18), (3, 1, 10), (3, 4, 0)]
    for voorzieningen in voorzieningen_values:
        cur.execute(voorzieningen_script, voorzieningen)


insert_statements()

conn.commit()

print("Dit was het!")

atexit.register(exit_handler)