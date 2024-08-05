from typing import Tuple, Callable
from pydantic import BaseModel, Field


from account_service.variables import *


class PlatformAccount(BaseModel):
    account_id: str | int

    account_name: str = Field(default=MISSING_ACCOUNT_NAME_FIELD)
    account_type: PlatformAccountType = Field(
        default=PlatformAccountType.PLATFORM_ACCOUNT
    )


class DiscordAccount(PlatformAccount):
    account_type: PlatformAccountType = Field(
        default=PlatformAccountType.DISCORD_ACCOUNT
    )
    

class MordhauAccount(PlatformAccount):
    account_type: PlatformAccountType = Field(
        default=PlatformAccountType.MORDHAU_ACCOUNT
    )


class PrimaryAccount(BaseModel):
    authority_account: PlatformAccount
    
    platform_accounts: list[MordhauAccount | DiscordAccount] = Field(default_factory=list)
    