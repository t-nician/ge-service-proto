import fastapi
import uvicorn
import asyncio


from grand_eco.service_apps import account_service, moderation_service, database_service

web_api = fastapi.FastAPI()

database_service.database_app.load_tables_to_database()
database_service.database_app.load_service_endpoints(web_api)

account_service.account_app.load_service_endpoints(web_api)
moderation_service.moderation_app.load_service_endpoints(web_api)


async def pre_launch():
    await database_service.database_function.create_primary_account(
        authority_account_id="playfab_id",
        authority_account_type=account_service.account_app.PlatformAccountType.MORDHAU_ACCOUNT
    )
    print((await database_service.database_function.get_primary_account(1)).authority_account_id)


asyncio.run(pre_launch())
#uvicorn.run(web_api, host="127.0.0.1", port=5000)