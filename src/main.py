import uvicorn
import fastapi
import multiprocessing

import account_service
import moderation_service


from shared import api_objects, variables


def launch_account_service():
    web_api_app = fastapi.FastAPI()
    
    account_service.database.load_tables_to_database()
    account_service.app.load_service_endpoints(web_api_app)
    
    uvicorn.run(web_api_app, host="127.0.0.1", port=5000)

def launch_moderation_service():
    web_api_app = fastapi.FastAPI()
    
    moderation_service.database.load_tables_to_database()
    moderation_service.app.load_service_endpoints(web_api_app)
    
    uvicorn.run(web_api_app, host="127.0.0.1", port=5001)


if __name__ == "__main__":
    account_service_process = multiprocessing.Process(
        target=launch_account_service,
    )
    
    moderation_service_process = multiprocessing.Process(
        target=launch_moderation_service,
    )
    
    account_service_process.start()
    moderation_service_process.start()
    
    account_service_process.join()
    
    #primary_account = await get_primary_account(
    #    "playfab_id",
    #    account_type=PlatformAccountType.MORDHAU_ACCOUNT
    #) 
    
    #if primary_account is None:
    #    primary_account = await create_primary_account(
    #        "hello_id",
    #        PlatformAccountType.DISCORD_ACCOUNT
    #    )
    
    #mordhau_account = await create_platform_account(
    #    "playfab_id",
    #    PlatformAccountType.MORDHAU_ACCOUNT,
    #    primary_account
    #)
    
    #print(mordhau_account)
    
    #print(primary_account)

    # new_primary_account = PeeweePrimaryAccount.create(
    #    authority_account_id="hello_id",
    #    authority_account_type=PlatformAccountType.DISCORD_ACCOUNT
    #)
    
    #database_connection.commit()
