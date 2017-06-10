
def create_tables(c, conn):
    c.execute("CREATE TABLE IF NOT EXISTS rooms(room_name TEXT, id INTEGER, room_type BOOLEAN, members TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS people(id INTEGER, fname TEXT, lname TEXT, role TEXT)")

def insert_rooms(c, conn, room_name, members):
    c.execute("INSERT INTO rooms (room_name, members) VALUES(?, ?)",(room_name, members))
    conn.commit()

def insert_people(c, conn, id, fname, lname, role):
    c.execute("INSERT INTO people (id, fname, lname, role) VALUES(?, ?, ?, ?)", (id, fname, lname, role))
    conn.commit()

def close_conn(c, conn):
    c.close()
    conn.close()



