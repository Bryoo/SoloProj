class SaveState(object):
    def create_tables(self, c, conn):
        c.execute("CREATE TABLE IF NOT EXISTS offices(id INTEGER PRIMARY KEY, room_name TEXT, members TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS livings(id INTEGER PRIMARY KEY, room_name TEXT, members TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS people(id INTEGER, names TEXT, office_id, living_id, role TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS unallocated(id INTEGER, names TEXT, role TEXT)")

    def insert_offices(self, c, conn, room_name, members):
        c.execute("INSERT INTO offices (room_name, members) VALUES(?, ?)",(room_name, members))
        conn.commit()

    def insert_livings(self, c, conn, room_name, members):
        c.execute("INSERT INTO livings (room_name, members) VALUES(?, ?)",(room_name, members))
        conn.commit()

    def insert_people(self, c, conn, id, names, role):
        c.execute("INSERT INTO people (id, names, role) VALUES(?, ?, ?)", (id, names, role))
        conn.commit()

    def insert_unallocated(self, c, conn, id, names, role):
        c.execute("INSERT INTO unallocated (id, names, role) VALUES(?, ?, ?)", (id, names, role))
        conn.commit()


class LoadState(object):
    def load_unallocated(self, c):
        c.execute("SELECT * FROM unallocated")
        query = c.fetchall()
        return query

    def load_offices(self,c):
        c.execute("SELECT room_name, members FROM offices")
        query = c.fetchall()
        return query

    def load_livings(self,c):
        c.execute("SELECT room_name, members FROM livings")
        query = c.fetchall()
        return query
