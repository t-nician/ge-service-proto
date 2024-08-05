import fastapi
import asyncio

from account_service.database import *
from account_service.procedures import *


load_tables_to_database()


async def main():
    primary_account = await get_primary_account(
        "playfab_id",
        account_type=PlatformAccountType.MORDHAU_ACCOUNT
    ) 
    
    #if primary_account is None:
    #    primary_account = await create_primary_account(
    #        "hello_id",
    #        PlatformAccountType.DISCORD_ACCOUNT
    #    )
    
    #mordhau_account = await create_platform_account(
    #    "playfab_id",
    #    PlatformAccountType.MORDHAU_ACCOUNT,
    #    primary_account
    #)
    
    #print(mordhau_account)
    
    print(primary_account)
    
    # new_primary_account = PeeweePrimaryAccount.create(
    #    authority_account_id="hello_id",
    #    authority_account_type=PlatformAccountType.DISCORD_ACCOUNT
    #)
    
    #database_connection.commit()


asyncio.run(main())