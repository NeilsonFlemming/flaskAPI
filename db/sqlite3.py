import sqlite3

def db_setup():
    conn = sqlite3.connect('db/app.db')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS request_log
                             (endpoint TEXT,
                              zip INT,
                              response BLOB)''')

def dict_factory(cursor, row):
    d = {}
    for index, col_name in enumerate(cursor.description):
        d[col_name[0]] = row[index]
    return d

def api_query(query):
    conn = sqlite3.connect('db/app.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    result = cur.execute(query).fetchall()
    return result


def api_log(endpoint,zip,json):
    conn = sqlite3.connect('db/app.db')
    cur = conn.cursor()
    cur.execute('''INSERT INTO request_log VALUES (?,?,?)''',(endpoint,zip,json))
    cur.execute('''COMMIT''')
    conn.close()