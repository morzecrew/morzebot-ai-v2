from fastapi import APIRouter, File, UploadFile
from db.repository.faq_repository import insert_faq_dataset, get_faq_dataset_by_uuid, is_faq_dataset_exists, insert_new_row

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
async def get_dataset(uuid: str):
    faq_dataset = get_faq_dataset_by_uuid(uuid)
    if faq_dataset:
        del faq_dataset["_id"]
        return faq_dataset
    return {'code': 404, 'status': 'not found', 'error': f'settings not found by this uuid: {uuid}'}


@faq_router.post("/add_row")
def add_new_row(uuid: str, question: str, answer: str):
    is_exist = is_faq_dataset_exists({'uuid': uuid})
    if is_exist:
        dataset = get_faq_dataset_by_uuid(uuid)['data']
        print(type(dataset))
        dataset = dataset if isinstance(dataset, str) else dataset.decode('utf-8')
    else:
        dataset = 'Question,Answer'
    new_dataset_string = question + ',' + answer + '\n'
    dataset = dataset + new_dataset_string
    insert_new_row(uuid, dataset.encode('utf-8'))
    return {'code': 200, 'status': 'ok'}
