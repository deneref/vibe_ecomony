import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import ColumnMapping as cmap


class SheetReader():
    def __init__(self, gc, sh):
        self.gc = gc
        self.sh = sh  # Opened worksheet

    def readSheet(self, sheet_name: str) -> pd.DataFrame:
        worksheet = self.sh.worksheet(sheet_name)

        dataframe = pd.DataFrame(worksheet.get_all_records())

        return dataframe

    def readSheet_test(self, sheet_nm: str) -> pd.DataFrame:
        worksheet = self.sh.worksheet(sheet_nm)

        dataframe = get_as_dataframe(
            worksheet, usecols=[0, 1, 2], skip_blank_lines=True).dropna()

        return dataframe

    def renameDataframeColumns(self, df: pd.DataFrame, sheet_nm: str):
        return df.rename(columns=cmap.ColumnMapping[sheet_nm])
