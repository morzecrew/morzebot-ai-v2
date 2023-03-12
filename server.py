import os

from morph_tagging.builder import EmbedderBuilder
from chit_chat.t5_ru.t5_ru import chat_model

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, APIRouter
from endpoints.users import users_router
from endpoints.intents import intents_router
from endpoints.settings import settings_router
from endpoints.faq import faq_router
from endpoints.chitchat import chitchat_router
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
api_router_v1.include_router(faq_router)
api_router_v1.include_router(chitchat_router)

app.include_router(api_router_v1, prefix=API_PREFIX, tags=["api"])

if __name__ == "__main__":
    # TEMPORARY
    # Download models from huggingface
    EmbedderBuilder("rubert-tiny2-tuned").build()
    chat_model.__init__()
    uvicorn.run("server:app", host='0.0.0.0', port=os.getenv("PORT", default=8000), log_level="info")
