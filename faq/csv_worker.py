import os
import pandas as pd


# DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), os.path.join("data", table_name))
class TableWorker:
    def __init__(self, table_name="faq_school.csv"):
        try:
            self.table = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), os.path.join("data", table_name)))
        except:
            self.table = None
