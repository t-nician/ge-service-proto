from peewee import (
    ForeignKeyField, TextField, IntegerField, TimestampField
)


from grand_eco.database_models.account_model import *
from grand_eco.database_models.moderation_model.moderation_model_variable import *


class PeeweeModerationHistory(PeeweeBaseModel):
    account_id = TextField(primary_key=True)
    account_type = AccountTypeField()
    
    history_id = TextField()
    
    class Meta:
        table_name = DB_MODERATION_HISTORY_TABLE_NAME


class PeeweeBanLog(PeeweeBaseModel):
    moderation_history = ForeignKeyField(
        PeeweeModerationHistory,
        backref=DB_BAN_LOG_BACKREF,
        primary_key=True
    )
    
    from_account_id = TextField()
    from_account_type = TextField()
    
    target_account_id = TextField()
    target_account_type = TextField()
    
    ban_reason = TextField()
    ban_length = IntegerField()
    
    time_of_ban = TimestampField()

    class Meta:
        table_name = DB_BAN_LOG_TABLE_NAME


class PeeweeWarnLog(PeeweeBaseModel):
    moderation_history = ForeignKeyField(
        PeeweeModerationHistory,
        backref=DB_WARN_LOG_BACKREF,
        primary_key=True
    )
    
    from_account_id = TextField()
    from_account_type = TextField()
    
    target_account_id = TextField()
    target_account_type = TextField()
    
    warn_reason = TextField()
    
    time_of_warn = TimestampField()
    
    class Meta:
        table_name = DB_WARN_LOG_TABLE_NAME
        

AVAILABLE_MODERATION_SERVICE_TABLES = [
    PeeweeModerationHistory, PeeweeBanLog, PeeweeWarnLog
]