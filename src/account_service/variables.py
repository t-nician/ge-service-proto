from enum import Enum


class PlatformAccountType(str, Enum):
    PLATFORM_ACCOUNT = "platform_account"
    DISCORD_ACCOUNT = "discord_account"
    MORDHAU_ACCOUNT = "mordhau_account"
    

MISSING_ACCOUNT_NAME_FIELD = "missing name"


PROC_CREATE_ACC_ALREADY_EXISTS_MSG = {
    "status": 400,
    "message": "account already exists!"
}

PROC_CREATE_ACC_FAILURE_MSG = {
    "status": 400,
    "message": "failed to create account!"
}

PROC_CREATE_ACC_FAILURE_PLATFORM_ACC_TAKEN = {
    "status": 400,
    "message": "one of the platform accounts is already taken!"
}

PROC_ACC_DOES_NOT_EXIST_MSG = {
    "status": 404,
    "message": "account does not exist!"
}