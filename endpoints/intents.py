from fastapi import APIRouter
from intent_catcher.intent_catcher_with_cos_sim import IntentCatcher
from morph_tagging.builder import Builder, MorphBuilder, EmbedderBuilder
from morph_tagging.tagger import Tools
from db.repository.settings_repository import is_uuid_exists

intents_router = APIRouter(
    prefix="/intents",
    tags=["intents"],
)


@intents_router.get("/{ws_token}")
async def send_intent():
    return {"get": "get request"}


@intents_router.get("/")
async def send_sentence(sentence: str, uuid: str):
    if uuid is not None:
        if not is_uuid_exists(uuid):
            return {'code': 404, 'status': 'uuid not found', 'error': f'settings not found by this uuid: {uuid}'}

    # tools = Tools()
    # builder: Builder = MorphBuilder(tools=tools)
    # normal_sentence = builder.build(sentence=sentence, uuid=uuid)

    # catcher: IntentCatcher = NatashaCatcher(normal_sentence)
    # response = catcher.catch()

    # variable: IdCatcher = VariableCatcher(response, normal_sentence)
    # result = variable.get_variable()

    builder = EmbedderBuilder("tiny-bert2")
    emb = builder.build()
    catcher = IntentCatcher(sentence, emb)
    result = catcher.get_intent()

    return result
