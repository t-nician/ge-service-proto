import fastapi
import uvicorn
import asyncio


from grand_eco.service_apps import account_service, moderation_service

web_api = fastapi.FastAPI()

account_service.account_database.load_tables_to_database()
moderation_service.moderation_database.load_tables_to_database()

account_service.account_app.load_service_endpoints(web_api)
moderation_service.moderation_app.load_service_endpoints(web_api)


async def pre_launch():
    pass


asyncio.run(pre_launch())
uvicorn.run(web_api, host="127.0.0.1", port=5000)