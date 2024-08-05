import fastapi
import asyncio


from account_service.objects import *
from account_service.procedures import (
    create_primary_account, 
    get_primary_account,
)


async def main():
    ref_primary_account = PrimaryAccount(
        authority_account=DiscordAccount(
            account_id=100,
            account_name="discord"
        ),
        
        platform_accounts=[
            MordhauAccount(
                account_id="playfab",
                account_name="mordhau"
            )
        ]
    )
    
    create_result: PrimaryAccount | dict = await create_primary_account(
        primary_account=ref_primary_account
    )
    
    get_result: PrimaryAccount | dict = await get_primary_account(
        platform_account_type=PlatformAccountType.DISCORD_ACCOUNT,
        account_id=100
    )
    
    get_platform_result: PrimaryAccount | dict = await get_primary_account(
        platform_account_type=PlatformAccountType.MORDHAU_ACCOUNT,
        account_id="playfab"
    )
    
    print("create account", create_result)
    print("get account by primary", get_result)
    print("get account by platform", get_platform_result)
    
    

asyncio.run(main())