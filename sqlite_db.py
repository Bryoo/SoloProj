
def create_tables(c, conn):
    c.execute("CREATE TABLE IF NOT EXISTS offices(room_name TEXT, id INTEGER, members TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS livings(room_name TEXT, id INTEGER, members TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS people(id INTEGER, names TEXT, role TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS unallocated(id INTEGER, names TEXT, role TEXT)")

def insert_offices(c, conn, room_name, members):
    c.execute("INSERT INTO offices (room_name, members) VALUES(?, ?)",(room_name, members))
    conn.commit()

def insert_livings(c, conn, room_name, members):
    c.execute("INSERT INTO livings (room_name, members) VALUES(?, ?)",(room_name, members))
    conn.commit()

def insert_people(c, conn, id, names, role):
    c.execute("INSERT INTO people (id, names, role) VALUES(?, ?, ?)", (id, names, role))
    conn.commit()

def insert_unallocated(c, conn, id, names, role):
    c.execute("INSERT INTO unallocated (id, names, role) VALUES(?, ?, ?)", (id, names, role))
    conn.commit()

