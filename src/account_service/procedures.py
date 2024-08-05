from account_service.objects import *
from account_service.variables import *


available_accounts: dict[tuple[PlatformAccountType, str | int], PrimaryAccount] = {}


async def __add_primary_account_to_database(primary_account: PrimaryAccount):
    account_key = (
        primary_account.authority_account.account_type,
        primary_account.authority_account.account_id
    )
    
    available_accounts[account_key] = primary_account.model_copy()


async def __get_primary_account_from_database(
    platform_account_type: PlatformAccountType, account_id: str | int
) -> PrimaryAccount | dict:
    primary_account = available_accounts.get((platform_account_type, account_id))
    
    if primary_account:
        return primary_account
    else:
        for primary_account in available_accounts.values():
            for platform_account in primary_account.platform_accounts:
                if platform_account.account_type is platform_account_type:
                    if platform_account.account_id == account_id:
                        return primary_account
                    
    return PROC_ACC_DOES_NOT_EXIST_MSG


async def create_primary_account(
    primary_account: PrimaryAccount
) -> PrimaryAccount | dict:    
    primary_account_type = primary_account.authority_account.account_type
    primary_account_id = primary_account.authority_account.account_id
    
    existing_primary_account = await get_primary_account(
        platform_account_type=primary_account_type,
        account_id=primary_account_id
    ) 
    
    if not existing_primary_account:
        for platform_account in primary_account.platform_accounts:
            result_type = type(
                await get_primary_account(
                    platform_account_type=platform_account.account_type,
                    account_id=platform_account.account_id
                )
            )
            
            if result_type is PrimaryAccount:
                return PROC_CREATE_ACC_FAILURE_PLATFORM_ACC_TAKEN
        
        await __add_primary_account_to_database(
            primary_account=primary_account
        )

        return await get_primary_account(
            platform_account_type=primary_account_type,
            account_id=primary_account_id
        )
    else:
        return PROC_CREATE_ACC_ALREADY_EXISTS_MSG
    

async def get_primary_account(
    platform_account_type: PlatformAccountType, account_id: str | int
) -> PrimaryAccount | dict:
    return await __get_primary_account_from_database(
        platform_account_type=platform_account_type, 
        account_id=account_id
    )