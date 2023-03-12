from fastapi import APIRouter
from chit_chat.chit_chat import ChitChat
from chit_chat.t5_ru.t5_ru import T5ChitChat, DO_SAMPLE, TOP_P, NUM_RETURN_SEQUENCES, REPETITION_PENALTY, MAX_LENGTH, \
    TASK_PREFIX
from random import choice

chitchat_router = APIRouter(
    prefix="/chitchat",
    tags=["chitchat"],
)


@chitchat_router.get("/")
async def send_sentence(sentence: str):
    model: ChitChat = T5ChitChat()
    result = model.response(sentence, do_sample=DO_SAMPLE,
                            top_p=TOP_P,
                            num_return_sequences=NUM_RETURN_SEQUENCES,
                            repetition_penalty=REPETITION_PENALTY,
                            max_length=MAX_LENGTH)
    return choice(result)
