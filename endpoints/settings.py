from fastapi import APIRouter
from pydantic import BaseModel
from db.repository.settings_repository import insert_settings, get_settings_by_uuid

settings_router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)


class Settings(BaseModel):
    uuid: str
    settings: dict


@settings_router.post("/")
def set_settings(sett: Settings):
    insert_settings(sett.uuid, sett.settings)
    return {'code': 200, 'status': 'ok'}


@settings_router.get("/")
def get_settings(uuid: str):
    settings = get_settings_by_uuid(uuid)
    if settings:
        del settings["_id"]
        return settings
    return {'code': 404, 'status': 'not found', 'error': f'settings not found by this uuid: {uuid}'}
