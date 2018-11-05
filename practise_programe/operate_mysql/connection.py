import MySQLdb
import logging
import csv


class Database:
    def __init__(self, host='127.0.0.1', user='root', passwd='root', db='test', port=3306, autocommit=True):
        self.conn = MySQLdb.Connection(host=host, user=user, passwd=passwd, db=db, port=port, autocommit=autocommit)
        self.uri = f'{user}:{passwd}@{host}:{port}/{db}'

    def close(self):
        self.conn.close()

    def _execute(self, query: str, raw=True, *args, **kwargs):
        print(query)
        cursor_cls = None if raw else MySQLdb.cursors.DictCursor
        cursor = self.conn.cursor(cursorclass=cursor_cls)
        try:
            cursor.execute(query, *args, **kwargs)
        except MySQLdb.IntegrityError as e:
            err = e
            logging.error('Dumplicate Key:', e)
        except MySQLdb.DatabaseError as e:
            err = e
            logging.error(e)
        else:
            return cursor
        self.close()
        raise err

    def insert(self, table: str, data: dict):
        keys = ','.join(data)
        values = ','.join(['%s'] * len(data))
        sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        cursor = self._execute(sql, True, data.values())
        return cursor.lastrowid

    def insert_many(self, table: str, key: list, many):
        cursor = self.conn.cursor()
        keys = ','.join(key)
        values = ','.join(['%s'] * len(key))
        sql = f'INSERT INTO {table} ({keys}) VALUES ({values})'
        try:
            cursor.executemany(sql, many)
        except MySQLdb.DatabaseError as e:
            logging.error(e)
            raise e
        else:
            return cursor.rowcount

    def select(self, table: str, fields: list = '*', where: dict = None):
        sql = f'SELECT {fields} FROM {table}'
        if where:
            where = ' AND '.join([f"{k}='{v}'" for k, v in where.items()])
            sql = f"{sql} where {where}"
        cursor = self._execute(sql, raw=False)
        return (Row(row) for row in cursor)

    def create_table(self, table: str, fields: list):
        sql = f'CREATE TABLE {table} ({", ".join(fields)})'
        cursor = self._execute(sql)
        return cursor.description


class Row(dict):
    def __init__(self, data):
        super().__init__(data)

    def __getattr__(self, item):
        return self.__getitem__(item)


def gen_item(many):
    for line in many:
        line[-1] = line[-1] or 0
        yield line


d = Database()
# d.create_table('tags', ['id INT AUTO_INCREMENT PRIMARY KEY','userId INT', 'movieId INT', 'tag VARCHAR(255)', 'timestamp VARCHAR(255)'])
# with open('ml/ratings.csv', encoding='utf8') as data:
#     many = csv.reader(data, quoting=csv.QUOTE_MINIMAL)
#     key = next(many)
#     res = d.insert_many('ratings', key, many)
#     print(res)
# d.create_table('links', ['id INT AUTO_INCREMENT PRIMARY KEY','movieId INT', 'imdbId INT', 'tmdbId INT'])
# d.create_table('movies', ['id INT AUTO_INCREMENT PRIMARY KEY','movieId INT', 'title VARCHAR(255)', 'genres VARCHAR(255)'])
# d.create_table('ratings', ['id INT AUTO_INCREMENT PRIMARY KEY','userId INT','movieId INT', 'rating FLOAT', 'timestamp VARCHAR(255)'])
# 1. 电影id 1129 的评分人数
# res = d._execute("SELECT * FROM ratings where movieId='1129'").rowcount
# print(res)
#
# 2. 电影id 161155 的imdbId和标题
# res = d._execute("SELECT links.imdbId,movies.title  FROM links,movies where links.movieId='161155'").fetchone()
# print(res)
# 3. 电影id 6365 的平均分数
# cursor = d._execute("SELECT rating  FROM ratings where movieId='6365'")
# sum = 0
# for item in cursor.fetchall():
#     sum += item[0]
# print(sum / cursor.rowcount)
#
# 4. 用户id 624 在2011年到2012年之间评价的电影数量

# 5. 用户id 660 标记的电影的标题和标签

d.close()
