import MySQLdb


class DataBase:
    """
    Create database connection
    """
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = MySQLdb.connect("localhost", "diet", "3RpMGSWGHHTNMRQP", "diet")
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        return self._db_cur.execute(query)  # Returns long integer rows affected, if any

    def fetch(self, nr=0):
        if nr==0:
            return self._db_cur.fetchall()
        else:
            return self._db_cur.fetchmany(nr)

    def get_random_eng(self, job_id):
        sql = "select .."
        self._db_cur.execute(sql)  # Returns long integer rows affected, if any
        engs = self._db_cur.fetchone()
        print("engineers: %s"% engs)

    def __del__(self):
        self._db_connection.close()
