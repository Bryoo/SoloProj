class SaveState(object):
    def create_tables(self, c, conn):
        c.execute("CREATE TABLE IF NOT EXISTS offices(id INTEGER PRIMARY KEY, room_name TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS livings(id INTEGER PRIMARY KEY, room_name TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS people(id INTEGER, names TEXT, office_id TEXT, living_id TEXT, role TEXT)")
        c.execute("CREATE TABLE IF NOT EXISTS unallocated(id INTEGER, names TEXT, role TEXT)")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS uniq_id ON people(id)")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS uniq_name ON offices(room_name)")
        c.execute("CREATE UNIQUE INDEX IF NOT EXISTS uniq_living ON livings(room_name)")

    def insert_offices(self, c, conn, room_name):
        c.execute("INSERT OR IGNORE INTO offices (room_name) VALUES(?)",(room_name,))
        conn.commit()

    def insert_livings(self, c, conn, room_name):
        c.execute("INSERT OR IGNORE INTO livings (room_name) VALUES(?)",(room_name,))
        conn.commit()

    def insert_people_offices(self, c, conn, id, names, office, role):
        c.execute("INSERT OR IGNORE INTO people (id, names, office_id, role) VALUES(?,?,?,?)",
                  (id, names, office, role))
        conn.commit()

    def insert_people_livings(self, c, conn, identity, names, living, role):
        c.execute("SELECT office_id FROM people WHERE id= ?", (identity,))
        office = c.fetchone()
        office = office[0]
        c.execute("INSERT OR REPLACE INTO people (id, names, office_id, living_id, role) VALUES(?,?,?,?,?)",
                  (identity, names, office, living, role))
        conn.commit()

    def insert_unallocated(self, c, conn, id, names, role):
        c.execute("INSERT OR IGNORE INTO unallocated (id, names, role) VALUES(?, ?, ?)", (id, names, role))
        conn.commit()


class LoadState(object):
    def load_unallocated(self, c):
        c.execute("SELECT * FROM unallocated")
        query = c.fetchall()
        return query

    def load_offices(self,c):
        c.execute("SELECT room_name FROM offices")
        query = c.fetchall()
        return query

    def load_livings(self,c):
        c.execute("SELECT room_name FROM livings")
        query = c.fetchall()
        return query

    def load_office_alloc(self, c, room):
        c.execute("SELECT * FROM people WHERE office_id= ?", (room,))
        query = c.fetchall()
        return query

    def load_living_alloc(self, c, room):
        c.execute("SELECT * FROM people WHERE living_id= ?", (room,))
        query = c.fetchall()
        return query
