import os
import pandas as pd

from io import StringIO
from db.repository.faq_repository import get_faq_dataset_by_uuid


class TableWorker:
    def __init__(self, uuid: str):
        try:
            self.table = pd.read_csv(StringIO(get_faq_dataset_by_uuid(uuid)['data'].decode('utf-8')), sep=',')
        except:
            self.table = None
