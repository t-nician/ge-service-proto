from peewee import SqliteDatabase, DoesNotExist

from grand_eco.database_models.account_model import *
from grand_eco.service_apps.database_service.database_variable import *

from grand_eco.database_models.moderation_model import *


database_object = SqliteDatabase(DB_SQLITE_ACCOUNT_SERVICE)


async def account_type_to_peewee_model(
    account_type: PlatformAccountType
) -> PeeweeDiscordAccount | PeeweeMordhauAccount | None:
    match account_type:
        case PlatformAccountType.DISCORD_ACCOUNT:
            return PeeweeDiscordAccount
        case PlatformAccountType.MORDHAU_ACCOUNT:
            return PeeweeMordhauAccount
    return None


def load_tables_to_database():
    database_connection.initialize(database_object)

    for table_model in AVAILABLE_ACCOUNT_SERVICE_TABLES:
        if not database_connection.table_exists(table_model):
            database_connection.create_tables([table_model])
            database_connection.commit()
    
    for table_model in AVAILABLE_MODERATION_SERVICE_TABLES:
        if not database_connection.table_exists(table_model):
            database_connection.create_tables([table_model])
            database_connection.commit()


#########################
# Get Account Functions # -----------------------------------------------------
#########################


async def get_platform_account(
    account_id: str | int,
    account_type: PlatformAccountType
) -> PeeweeDiscordAccount | PeeweeMordhauAccount | None:
    database_connection.initialize(database_object)
    
    if type(account_id) is int:
        account_id = str(account_id)
    
    target_peewee_model = await account_type_to_peewee_model(
        account_type=account_type
    )
    
    try:
        if target_peewee_model is None:
            raise Exception(DB_GET_PLATFORM_ACCOUNT_INVALID_TYPE)
        
        return target_peewee_model.get(
            target_peewee_model.account_id==account_id
        )
        
    except DoesNotExist:
        return None


async def get_primary_account(
    primary_or_authority_or_platform_account_id: str | int, 
    account_type: PlatformAccountType | None = None
) -> PeeweePrimaryAccount | None:
    account_id = primary_or_authority_or_platform_account_id
    
    database_connection.initialize(database_object)
    
    if type(account_id) is int:
        try:        
            return PeeweePrimaryAccount.get(
                PeeweePrimaryAccount.id==int(account_id)
            )
        except DoesNotExist:
            pass
    
        account_id = str(account_id)
    
    try:
        primary_account: PeeweePrimaryAccount = PeeweePrimaryAccount.get(
            PeeweePrimaryAccount.authority_account_id==account_id
        )
        
        if account_type:
            if primary_account.authority_account_type is account_type:
                return primary_account
            else:
                raise Exception(DB_GET_PRIMARY_ACCOUNT_ID_MATCH_TYPE_MISMATCH)
        else:
            return primary_account
        
    except DoesNotExist:
        if account_type:
            platform_account = await get_platform_account(
                account_id=account_id,
                account_type=account_type
            )
            
            if platform_account:
                return platform_account.primary_account


############################
# Create Account Functions # --------------------------------------------------
############################


async def create_platform_account(
    primary_account: PeeweePrimaryAccount, 
    account_id: int | str,
    account_type: PlatformAccountType,
    account_name: str | None = None,
) -> PeeweeMordhauAccount | PeeweeDiscordAccount:
    database_connection.initialize(database_object)
    
    if type(account_id) is int:
        account_id = str(account_id)
        
    assert await get_platform_account(
        account_id=account_id,
        account_type=account_type
    ) is None, DB_CREATE_PLATFORM_ACCOUNT_ALREADY_EXISTS
    
    return (
        await account_type_to_peewee_model(
            account_type=account_type
        )
    ).create(
        account_id=account_id,
        account_name=account_name or DB_ACCOUNT_NAME_MISSING_REPLACEMENT,
        primary_account=primary_account
    )
        

async def create_primary_account(
    authority_account_id: str | int,
    authority_account_type: PlatformAccountType,
    
    platform_account_name: str | None = None
) -> PeeweePrimaryAccount:
    database_connection.initialize(database_object)
    
    if type(authority_account_id) is int:
        authority_account_id = str(authority_account_id)
        
    assert await get_primary_account(
        primary_or_authority_or_platform_account_id=authority_account_id,
        account_type=authority_account_type
    ) is None, DB_CREATE_PRIMARY_ACCOUNT_ALREADY_EXISTS
    
    primary_account = PeeweePrimaryAccount.create(
        authority_account_id=authority_account_id,
        authority_account_type=authority_account_type
    )
    
    await create_platform_account(
        primary_account=primary_account,
    
        account_id=authority_account_id,
        account_type=authority_account_type,
    
        account_name=platform_account_name
    )
    
    return primary_account
    
