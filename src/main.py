import asyncio
import uvicorn

from account_service.database import *
from account_service.app import *


async def pre_launch():
    #primary_account = await create_primary_account(
    #    account_id="discord_id",
    #    account_type=PlatformAccountType.DISCORD_ACCOUNT
    #)
    
    #await create_platform_account(
    #    primary_account,
    #    account_id="playfab_id",
    #    account_name="mordhau_name",
    #    account_type=PlatformAccountType.MORDHAU_ACCOUNT
    #)
    pass
    


app = FastAPI()

load_tables_to_database()
hook_api_endpoints(app)

asyncio.run(pre_launch())
uvicorn.run(app, host="127.0.0.1", port=5000)
    
    #primary_account = await get_primary_account(
    #    "playfab_id",
    #    account_type=PlatformAccountType.MORDHAU_ACCOUNT
    #) 
    
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
    
    #print(primary_account)

    # new_primary_account = PeeweePrimaryAccount.create(
    #    authority_account_id="hello_id",
    #    authority_account_type=PlatformAccountType.DISCORD_ACCOUNT
    #)
    
    #database_connection.commit()
