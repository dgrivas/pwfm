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

    def __del__(self):
        self._db_connection.close()
