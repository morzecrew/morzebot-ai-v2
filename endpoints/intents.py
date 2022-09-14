from fastapi import APIRouter
from intent_catcher.intent_catcher import IntentCatcher, NatashaCatcher
from morph_tagging.builder import Builder, MorphBuilder
from morph_tagging.tagger import Tools

intents_router = APIRouter(
    prefix="/intents",
    tags=["intents"],
)


@intents_router.get("/{ws_token}")
async def send_intent():
    return {"get": "get request"}


@intents_router.get("/")
async def send_sentence(sentence: str):
    tools = Tools()
    builder: Builder = MorphBuilder(tools=tools)
    normal_sentence = builder.build(sentence=sentence)

    catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    response = catcher.catch()

    return {"intent": response}
