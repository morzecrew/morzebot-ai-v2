import os

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from endpoints.users import users_router
from endpoints.intents import intents_router
from endpoints.settings import settings_router
import uvicorn


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api"

api_router_v1 = APIRouter(
    prefix="/v1",
    tags=["v1"],
)

api_router_v1.include_router(users_router)
api_router_v1.include_router(intents_router)
api_router_v1.include_router(settings_router)
app.include_router(api_router_v1, prefix=API_PREFIX, tags=["api"])

if __name__ == "__main__":
    uvicorn.run("server:app", host='0.0.0.0', port=os.getenv("PORT", default=8000), log_level="info")
