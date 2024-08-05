from fastapi import FastAPI
from playhouse.shortcuts import model_to_dict, dict_to_model

from account_service.objects import *
from account_service.database import *
from account_service.variables import *

async def account_type_to_api_model(
    account_type: PlatformAccountType
):
    match account_type:
        case PlatformAccountType.DISCORD_ACCOUNT:
            return DiscordAccountObject
        case PlatformAccountType.MORDHAU_ACCOUNT:
            return MordhauAccountObject
    return None


async def api_get_primary_account(
    account_id: str,
    account_type: PlatformAccountType
) -> PrimaryAccountObject:   
    primary_account = await get_primary_account(
        account_id=account_id,
        account_type=account_type
    )
    
    return PrimaryAccountObject(
        authority_account_id=primary_account.authority_account_id,
        authority_account_type=primary_account.authority_account_type
    )


async def api_get_platform_account(
    account_id: str,
    account_type: PlatformAccountType
) -> MordhauAccountObject | DiscordAccountObject:
    platform_account = await get_platform_account(
        account_id=account_id,
        account_type=account_type
    )

    primary_account: PeeweePrimaryAccount = platform_account.primary_account
    
    primary_account_object = PrimaryAccountObject(
        authority_account_id=primary_account.authority_account_id,
        authority_account_type=primary_account.authority_account_type
    )
    
    account_object_class = await account_type_to_api_model(
        account_type=account_type
    )
    
    return account_object_class(
        primary_account=primary_account_object,
        
        account_id=platform_account.account_id,
        account_name=platform_account.account_name,
        
        account_type=account_type
    )

def hook_api_endpoints(app: FastAPI):
    app.add_api_route(
        "/account-service/get-primary-account-by",
        response_model=PrimaryAccountObject,
        endpoint=api_get_primary_account,
        methods=["GET"]
    )
    
    app.add_api_route(
        "/account-service/get-platform-account-by",
        response_model=DiscordAccountObject | MordhauAccountObject,
        endpoint=api_get_platform_account,
        methods=["GET"]
    )