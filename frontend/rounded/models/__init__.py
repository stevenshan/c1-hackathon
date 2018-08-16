from flask_sqlalchemy import SQLAlchemy

import sqlalchemy
from sqlalchemy.exc import IntegrityError
import sqlite3

# enforce foreign keys so that secondary databases are deleted automatically
@sqlalchemy.event.listens_for(sqlalchemy.engine.Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, sqlite3.Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()

db = SQLAlchemy()

