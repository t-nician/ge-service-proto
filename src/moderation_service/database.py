from peewee import (
    Model, ForeignKeyField, TextField, Field,
    SqliteDatabase, MySQLDatabase, PostgresqlDatabase,
    DoesNotExist
)

from shared.variables import *
from shared.database_objects import *


def load_tables_to_database():
    database_connection.initialize(
        SqliteDatabase(DB_SQLITE_MODERATION_SERVICE)
    )
    
    for table_model in AVAILABLE_MODERATION_SERVICE_TABLES:
        if not database_connection.table_exists(table_model):
            database_connection.create_tables([table_model])
            database_connection.commit()
