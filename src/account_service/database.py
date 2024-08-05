from peewee import (
    Model, ForeignKeyField, TextField, Field,
    SqliteDatabase, MySQLDatabase, PostgresqlDatabase,
    DoesNotExist
)

from account_service.variables import *


database_connection = SqliteDatabase("./workspace/database.sqlite")
database_connection.connect()


class AccountTypeField(Field):
    field_type="account_type"
    
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
        table_name = "primary_accounts"

    
class PeeweeDiscordAccount(PeeweeBaseModel):
    primary_account = ForeignKeyField(
        PeeweePrimaryAccount,
        backref='discord_accounts',
    )
    
    account_id = TextField(primary_key=True)
    account_name = TextField()
    
    class Meta:
        table_name = "discord_accounts"


class PeeweeMordhauAccount(PeeweeBaseModel):
    primary_account = ForeignKeyField(
        PeeweePrimaryAccount,
        backref='mordhau_accounts',
    )
    
    account_id = TextField(primary_key=True)
    account_name = TextField()
    
    class Meta:
        table_name = "mordhau_accounts"


AVAILABLE_TABLES = [
    PeeweePrimaryAccount, PeeweeDiscordAccount, PeeweeMordhauAccount
]


def __platform_type_to_peewee_model(
    platform_type: PlatformAccountType
) -> PeeweeDiscordAccount | PeeweeMordhauAccount | None:
    match platform_type:
        case PlatformAccountType.DISCORD_ACCOUNT:
            return PeeweeDiscordAccount
        case PlatformAccountType.MORDHAU_ACCOUNT:
            return PeeweeMordhauAccount
    return None


def load_tables_to_database():
    for table_model in AVAILABLE_TABLES:
        if not database_connection.table_exists(table_model):
            database_connection.create_tables([table_model])
            database_connection.commit()


async def get_platform_account(
    account_id: str | int,
    account_type: PlatformAccountType
) -> PeeweeDiscordAccount | PeeweeMordhauAccount | None:
    if type(account_id) is int:
        account_id = str(account_id)
    
    target_peewee_model = __platform_type_to_peewee_model(
        platform_type=account_type
    )
    
    try:
        if target_peewee_model is None:
            raise Exception("failed to match account_type")
        
        return target_peewee_model.get(
            target_peewee_model.account_id==account_id
        )
    except DoesNotExist:
        return None


async def get_primary_account(
    account_id: str | int, 
    account_type: PlatformAccountType | None = None
) -> PeeweePrimaryAccount | None:
    if type(account_id) is int:
        account_id = str(account_id)
    
    try:
        if account_type:
            return PeeweePrimaryAccount.get(
                PeeweePrimaryAccount.authority_account_id==account_id,
                PeeweePrimaryAccount.authority_account_type==account_type
            )
        else:
            return PeeweePrimaryAccount.get(
                PeeweePrimaryAccount.authority_account_id==account_id
            )
            
    except DoesNotExist:
        if account_type:
            platform_account = await get_platform_account(
                account_id=account_id,
                account_type=account_type
            )
            
            return platform_account and platform_account.primary_account or None
    
    finally:
        return None


async def create_platform_account(
    account_id: int | str,
    account_type: PlatformAccountType,
    primary_account: PeeweePrimaryAccount,
    account_name: str | None = None,
) -> PeeweeMordhauAccount | PeeweeDiscordAccount:
    if type(account_id) is int:
        account_id = str(account_id)
        
    assert await get_platform_account(
        account_id=account_id,
        account_type=account_type
    ) is None, "This platform account already exists!"
    
    return __platform_type_to_peewee_model(
        platform_type=account_type
    ).create(
        account_id=account_id,
        account_name=account_name or MISSING_ACCOUNT_NAME_FIELD,
        primary_account=primary_account
    )
        

async def create_primary_account(
    account_id: str | int,
    account_type: PlatformAccountType,
    
    platform_account_name: str | None = None
) -> PeeweePrimaryAccount:
    if type(account_id) is int:
        account_id = str(account_id)
        
    assert await get_primary_account(
        account_id=account_id,
        account_type=account_type
    ) is None, "This platform account is already taken by a primary account!"
    
    primary_account = PeeweePrimaryAccount.create(
        authority_account_id=account_id,
        authority_account_type=account_type
    )
    
    await create_platform_account(
        account_id=account_id,
        account_type=account_type,
        
        primary_account=primary_account,
        account_name=platform_account_name
    )
    
    return primary_account
    
    