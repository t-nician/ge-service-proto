from fastapi import FastAPI


async def api_create_moderation_history():
    pass


async def api_get_moderation_history():
    pass


def load_service_endpoints(app: FastAPI):
    app.add_api_route(
        "/moderation-service/moderation-history",
        response_model=None,
        endpoint=api_create_moderation_history,
        methods=["POST"]
    )
    
    app.add_api_route(
        "/moderation-service/moderation-history",
        response_model=None,
        endpoint=api_create_moderation_history,
        methods=["GET"]
    )