from peewee import (
    Proxy, Model, 
    ForeignKeyField, TextField, Field
)


from grand_eco.api_objects.account_object.account_object_variable import *
from grand_eco.database_models.account_model.account_model_variable import *


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
