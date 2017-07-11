import mysql.connector


class MysqlConn:

    def __init__(self, database, user, password):
        config = {'host': 'localhost', 'database': database, 'user': user, 'password': password}
        self.__conn = mysql.connector.connect(**config)
        self.__cur = self.__conn.cursor()

    def cursor(self):
        return self.__cur

    def commit(self):
        self.__conn.commit()

    def close(self):
        self.__cur.close()
        self.__conn.close()
