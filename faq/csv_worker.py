import os
import pandas as pd

# tmp = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), os.path.join("data", "faq_school.csv")))
# print(tmp)
# DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), os.path.join("data", table_name))
class TableWorker:
    def __init__(self, table_name="faq_school.csv"):
        try:
            self.table = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), os.path.join("data", table_name)))
        except:
            self.table = None

    # def save_table(self,name):
    #     # self.table.
    #
    # def add_line(self, question, answer):
    #
    # def extract_line(self,row_num):
