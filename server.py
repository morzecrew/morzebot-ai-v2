from fastapi import FastAPI, APIRouter
from endpoints.users import users_router
from endpoints.intents import intents_router


app = FastAPI()

API_PREFIX = "/api"

api_router_v1 = APIRouter(
    prefix="/v1",
    tags=["v1"],
)


api_router_v1.include_router(users_router)
api_router_v1.include_router(intents_router)
app.include_router(api_router_v1, prefix=API_PREFIX, tags=["api"])
