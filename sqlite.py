import sqlite3
conn = sqlite3.connect('dojo.db')
c = conn.cursor()


def create_table():
    c.execute("CREATE TABLE IF NOT EXISTS rooms(room_name TEXT, id INTEGER AUTOINCREMENT, members TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS people(fname TEXT, lname TEXT)")