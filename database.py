import mysql.connector as sql

class sqlInterface():
    def __init__(self, config):
        self.cnx = sql.connect(**config)
        self.cursor = self.cnx.cursor(buffered=True)

    def pull(self, table):
        self.cursor.execute("select * from " + table + ";")
        data = self.cursor.fetchall()
        links = []
        for d in data:
            links.append(d[0])
        return links

    def push(self, table, url):
        self.cursor.execute("insert into " + table + " values ('%s')" % url)
        self.cnx.commit()
