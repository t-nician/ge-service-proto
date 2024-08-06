from fastapi import FastAPI

from grand_eco.api_objects.account_object import *
from grand_eco.database_models.account_model import *

from grand_eco.service_apps.account_service.account_database import *


async def account_type_to_api_model(
    account_type: PlatformAccountType
):
    match account_type:
        case PlatformAccountType.DISCORD_ACCOUNT:
            return DiscordAccountObject
        case PlatformAccountType.MORDHAU_ACCOUNT:
            return MordhauAccountObject
    return None


async def api_create_primary_account(
    primary_account: PrimaryAccountObject
) -> PrimaryAccountObject:
    primary_account_model = await create_primary_account(
        account_id=primary_account.authority_account_id,
        account_type=primary_account.authority_account_type
    )
    
    return PrimaryAccountObject(
        authority_account_id=primary_account_model.authority_account_id,
        authority_account_type=primary_account_model.authority_account_type
    )
    

async def api_create_platform_account(
    platform_account: MordhauAccountObject | DiscordAccountObject
) -> MordhauAccountObject | DiscordAccountObject:
    platform_account_model = await create_platform_account(
        primary_account=await get_primary_account(
            account_id=platform_account.primary_account.authority_account_id,
            account_type=platform_account.primary_account.authority_account_type
        ),
        
        account_id=platform_account.account_id,
        account_type=platform_account.account_type,
        account_name=platform_account.account_name
    )
    
    platform_account_class = await account_type_to_api_model(
        account_type=platform_account.account_type
    )
    
    return platform_account_class(
        primary_account=PrimaryAccountObject(
            authority_account_id=platform_account_model.primary_account.authority_account_id,
            authority_account_type=platform_account_model.primary_account.authority_account_type
        ),
        
        account_id=platform_account.account_id,
        account_type=platform_account.account_type,
        account_name=platform_account.account_name
    )


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


def load_service_endpoints(app: FastAPI):
    app.add_api_route(
        "/account-service/primary-account",
        response_model=PrimaryAccountObject,
        endpoint=api_create_primary_account,
        methods=["POST"]
    )
    
    app.add_api_route(
        "/account-service/primary-account",
        response_model=PrimaryAccountObject,
        endpoint=api_get_primary_account,
        methods=["GET"]
    )
    
    app.add_api_route(
        "/account-service/platform-account",
        response_model=DiscordAccountObject | MordhauAccountObject,
        endpoint=api_create_platform_account,
        methods=["POST"]
    )
    
    app.add_api_route(
        "/account-service/platform-account",
        response_model=DiscordAccountObject | MordhauAccountObject,
        endpoint=api_get_platform_account,
        methods=["GET"]
    )