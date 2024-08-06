from fastapi import FastAPI

from grand_eco.api_objects.account_object import *
from grand_eco.database_models.account_model import *

from grand_eco.service_apps.database_service.database_function import *

def load_service_endpoints(app: FastAPI):
    pass