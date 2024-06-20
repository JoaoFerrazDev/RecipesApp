# models/database.py
import sqlite3


class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._connection = sqlite3.connect('recipes.db')
            cls._instance._cursor = cls._instance._connection.cursor()
            cls._instance._initialize_db()
        return cls._instance

    def _initialize_db(self):
        self._cursor.execute('''
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NULL,
                image TEXT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                user_id INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        self._cursor.execute('''
              CREATE TABLE IF NOT EXISTS users (
                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  email TEXT NOT NULL UNIQUE,
                  password TEXT NOT NULL,
                  date_of_birth TEXT NOT NULL,
                  state TEXT NOT NULL DEFAULT 'public'
              )
          ''')

        self._cursor.execute('''
                      CREATE TABLE IF NOT EXISTS followers (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          follower int NOT NULL,
                          following int NOT NULL
                      )
                  ''')

        self._cursor.execute('''
                              CREATE TABLE IF NOT EXISTS notifications (
                                  id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  notification TEXT NOT NULL,
                                  user_id INT NOT NULL
                              )
                          ''')

        self._connection.commit()

    def get_cursor(self):
        return self._cursor

    def commit(self):
        self._connection.commit()


def _query(query, params=None):
    db_path = './recipes.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result
