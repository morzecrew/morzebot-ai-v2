from fastapi import APIRouter


users_router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@users_router.post("/")
async def send_sentence(sentence: str):
    pass
