from fastapi import APIRouter
from fastapi.responses import JSONResponse

intents_router = APIRouter(
    prefix="/intents",
    tags=["intents"],
)


@intents_router.get("/{ws_token}")
async def send_intent():
    return {"get": "get request"}
