from enum import Enum


class PlatformAccountType(str, Enum):
    PLATFORM_ACCOUNT = "platform_account"
    DISCORD_ACCOUNT = "discord_account"
    MORDHAU_ACCOUNT = "mordhau_account"
    

MISSING_ACCOUNT_NAME_FIELD = "missing name"