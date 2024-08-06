from peewee import (
    Model, ForeignKeyField, TextField, Field, Proxy, IntegerField, TimestampField
)

from shared.variables import *


database_connection = Proxy()


class AccountTypeField(Field):
    field_type=DB_ACCOUNT_TYPE_FIELD_NAME
    
    def db_value(self, value: PlatformAccountType) -> str:
        return value.value
    
    def python_value(self, value: str) -> PlatformAccountType:
        return PlatformAccountType(value)


class PeeweeBaseModel(Model):
    class Meta:
        database = database_connection


###################
# Account Service # -----------------------------------------------------------
###################


class PeeweePrimaryAccount(PeeweeBaseModel):
    authority_account_id = TextField(primary_key=True)
    authority_account_type = AccountTypeField()
    
    class Meta:
        table_name = DB_PRIMARY_ACCOUNT_TABLE_NAME

    
class PeeweeDiscordAccount(PeeweeBaseModel):
    primary_account = ForeignKeyField(
        PeeweePrimaryAccount,
        backref=DB_DISCORD_ACCOUNT_BACKREF,
    )
    
    account_id = TextField(primary_key=True)
    account_name = TextField()
    
    class Meta:
        table_name = DB_DISCORD_ACCOUNT_TABLE_NAME


class PeeweeMordhauAccount(PeeweeBaseModel):
    primary_account = ForeignKeyField(
        PeeweePrimaryAccount,
        backref=DB_MORDHAU_ACCOUNT_BACKREF,
    )
    
    account_id = TextField(primary_key=True)
    account_name = TextField()
    
    class Meta:
        table_name = DB_MORDHAU_ACCOUNT_TABLE_NAME


AVAILABLE_ACCOUNT_SERVICE_TABLES = [
    PeeweePrimaryAccount, PeeweeDiscordAccount, PeeweeMordhauAccount
]


######################
# Moderation Service # --------------------------------------------------------
######################


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