from fastapi import APIRouter
from chit_chat.chit_chat import ChitChat
from chit_chat.t5_ru.t5_ru import T5ChitChat
from random import choice

chitchat_router = APIRouter(
    prefix="/chitchat",
    tags=["chitchat"],
)


@chitchat_router.get("/")
async def send_sentence(sentence: str):
    model: ChitChat = T5ChitChat()
    result = model.response(sentence,)
    return choice(result)
