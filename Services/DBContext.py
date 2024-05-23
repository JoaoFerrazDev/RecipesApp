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
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL
            )
        ''')
        self._connection.commit()

    def get_cursor(self):
        return self._cursor

    def commit(self):
        self._connection.commit()