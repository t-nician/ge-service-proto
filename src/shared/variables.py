from enum import Enum


class PlatformAccountType(str, Enum):
    DISCORD_ACCOUNT = "discord_account"
    MORDHAU_ACCOUNT = "mordhau_account"


DB_SQLITE_ACCOUNT_SERVICE = "./workspace/account-service.sqlite"
DB_SQLITE_MODERATION_SERVICE = "./workspace/moderation-service.sqlite"

DB_ACCOUNT_NAME_MISSING_REPLACEMENT = "missing name"

DB_ACCOUNT_TYPE_FIELD_NAME = "account_type"

DB_PRIMARY_ACCOUNT_TABLE_NAME = "primary_accounts"
DB_DISCORD_ACCOUNT_TABLE_NAME = "discord_accounts"
DB_MORDHAU_ACCOUNT_TABLE_NAME = "mordhau_accounts"

DB_DISCORD_ACCOUNT_BACKREF = "discord_accounts_ref"
DB_MORDHAU_ACCOUNT_BACKREF = "mordhau_accounts_ref"

DB_BAN_LOG_TABLE_NAME = "ban_logs"
DB_WARN_LOG_TABLE_NAME = "warn_logs"
DB_MODERATION_HISTORY_TABLE_NAME = "moderation_historys"

DB_BAN_LOG_BACKREF = "ban_logs_ref"
DB_WARN_LOG_BACKREF = "warn_logs_ref"
DB_MODERATION_HISTORY_BACKREF = "moderation_history_ref"

DB_CREATE_PRIMARY_ACCOUNT_ALREADY_EXISTS = "This platform account is already taken by a primary account!"
DB_CREATE_PLATFORM_ACCOUNT_ALREADY_EXISTS = "This platform account already exists!"

DB_GET_PRIMARY_ACCOUNT_ID_MATCH_TYPE_MISMATCH = "PrimaryAccount.authority_account_id matched, but authority_account_type do not match!"
DB_GET_PLATFORM_ACCOUNT_INVALID_TYPE = "Invalid account_type!"