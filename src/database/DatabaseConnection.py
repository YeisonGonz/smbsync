import sqlite3
from src.Configuration import Configuration

class DatabaseConnection:
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._initialize_connection()
        return cls._instance

    def _initialize_connection(self):
        config = Configuration()
        db_path = config.config.DATABASE_FILE_PATH
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row

    def get_connection(self):
        return self._connection

    def close(self):
        if self._connection:
            self._connection.close()
            DatabaseConnection._instance = None
            DatabaseConnection._connection = None
