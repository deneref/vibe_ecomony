import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe


class SheetReader():
    def __init__(self, gc, sh):
        self.gc = gc
        self.sh = sh  # Opened worksheet

    def readSheet(self, sheet_name: str) -> pd.DataFrame:
        worksheet = self.sh.worksheet(sheet_name)

        dataframe = pd.DataFrame(worksheet.get_all_records())

        return dataframe

    def readSheet_test(self, sheet_name: str) -> pd.DataFrame:
        worksheet = self.sh.worksheet(sheet_name)

        dataframe = get_as_dataframe(
            worksheet, usecols=[0, 1, 2], skip_blank_lines=True).dropna()

        return dataframe
