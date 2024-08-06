from enum import Enum


class PlatformAccountType(str, Enum):
    DISCORD_ACCOUNT = "discord_account"
    MORDHAU_ACCOUNT = "mordhau_account"
    

ACCOUNT_NAME_MISSING_PLACEMENT = "missing name"