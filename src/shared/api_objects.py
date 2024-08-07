from pydantic import BaseModel, Field


from shared.variables import *


class PrimaryAccountObject(BaseModel):
    authority_account_id: str
    authority_account_type: PlatformAccountType


class MordhauAccountObject(BaseModel):
    primary_account: PrimaryAccountObject
    
    account_id: str 
    account_name: str | None = Field(
        default=DB_ACCOUNT_NAME_MISSING_REPLACEMENT
    )
    
    account_type: PlatformAccountType = Field(
        default=PlatformAccountType.MORDHAU_ACCOUNT
    )


class DiscordAccountObject(BaseModel):
    primary_account: PrimaryAccountObject
    
    account_id: str 
    account_name: str | None = Field(
        default=DB_ACCOUNT_NAME_MISSING_REPLACEMENT
    )
    
    account_type: PlatformAccountType = Field(
        default=PlatformAccountType.DISCORD_ACCOUNT
    )

