import MySQLdb
import random


class DataBase:
    """
    Create database connection.

    """
    SERVER = "localhost"
    USER = "wfm"
    PASSWORD = "wfm"
    DB = "wfm"
    _db_connection = None
    _db_cur = None

    def __init__(self):
        self._db_connection = MySQLdb.connect(self.SERVER, self.USER, self.PASSWORD, self.DB)
        self._db_cur = self._db_connection.cursor()

    def query(self, query):
        return self._db_cur.execute(query)  # Returns long integer rows affected, if any

    def fetch(self, nr=0):
        if nr==0:
            return self._db_cur.fetchall()
        else:
            return self._db_cur.fetchmany(nr)

    def get_random_eng(self, job_id):
        """
        Get a random engineer for job.

        :param job_id: job id to search for engineers
        :return: random choice of engineer
        """
        # sql = "SELECT job_eng_eid FROM job_engineers WHERE job_eng_jid=%s"
        sql = "SELECT job_eng_eid FROM job_engineers WHERE job_eng_jid=" + str(job_id)
        # self._db_cur.execute(sql, job_id)  # Returns long integer rows affected, if any
        self._db_cur.execute(sql)  # Returns long integer rows affected, if any
        data = self._db_cur.fetchall()
        data = [x[0] for x in data]
        return random.choice(data)

    '''
    def get_job_duration(self, id):
        """

        :param id:
        :return:
        """
        sql = "SELECT duration FROM job WHERE job_id=%s"
        self._db_cur.execute(sql, id)  # Returns long integer rows affected, if any
        data = self._db_cur.fetchone()
        return data[0]
    '''

    def __del__(self):
        self._db_connection.close()
