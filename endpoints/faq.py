from fastapi import APIRouter, File, UploadFile
from db.repository.faq_repository import insert_faq_dataset, get_faq_dataset_by_uuid, is_faq_dataset_exists

faq_router = APIRouter(
    prefix="/faq",
    tags=["faq"],
)


@faq_router.post("/")
async def upload_dataset(uuid: str, file: UploadFile):
    if file.content_type != 'text/csv':
        return {'code': 200, 'status': 'wrong file format'}

    content = await file.read()
    insert_faq_dataset(uuid, content)
    return {'code': 200, 'status': 'ok'}


@faq_router.get("/")
async def get_settings(uuid: str):
    faq_dataset = get_faq_dataset_by_uuid(uuid)
    if faq_dataset:
        del faq_dataset["_id"]
        return faq_dataset
    return {'code': 404, 'status': 'not found', 'error': f'settings not found by this uuid: {uuid}'}
