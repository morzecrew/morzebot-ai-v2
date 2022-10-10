from fastapi import APIRouter
from pydantic import BaseModel
from db.repository.settings_repository import insert_settings, get_settings_by_uid

settings_router = APIRouter(
    prefix="/settings",
    tags=["settings"],
)


class Settings(BaseModel):
    uuid: str
    global_: bool
    settings: dict


@settings_router.post("/set")
def set_settings(sett: Settings):
    # TODO: add logic for global_
    insert_settings(sett.uuid, sett.settings)
    return {'code': 200, 'status': 'ok'}


@settings_router.get("/get")
def get_settings(uuid: str, global_: bool):
    settings = get_settings_by_uid(uuid)
    if settings:
        return settings
    else:
        return {'code': 404, 'status': 'not found', 'error': f'settings not found by this uuid: {uuid}'}
