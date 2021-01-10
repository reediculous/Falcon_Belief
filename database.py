import mysql.connector as sql


class sqlInterface():
    def __init__(self, config):
        self.cnx = sql.connect(**config)
        self.cursor = self.cnx.cursor(buffered=True)

    def pull(self, table):
        """
        Возвращает список ссылок из указанной таблицы с ссылками
        """
        self.cursor.execute("select * from " + table + ";")
        data = self.cursor.fetchall()
        links = []
        for d in data:
            links.append(d[0])
        return links

    def push(self, table, url):
        """
        Добавляет в указанную таблицу ссылок указанную ссылку
        """
        self.cursor.execute("insert into " + table + " values ('%s')" % url)
        self.cnx.commit()
