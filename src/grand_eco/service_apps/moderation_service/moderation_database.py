from peewee import SqliteDatabase, DoesNotExist

from grand_eco.database_models.moderation_model import *
from grand_eco.service_apps.moderation_service.moderation_variables import *

database_object = SqliteDatabase(DB_SQLITE_MODERATION_SERVICE)





def load_tables_to_database():
    database_connection.initialize(database_object)
    
    for table_model in AVAILABLE_MODERATION_SERVICE_TABLES:
        if not database_connection.table_exists(table_model):
            database_connection.create_tables([table_model])
            database_connection.commit()


