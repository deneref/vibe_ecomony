import pandas as pd
from gspread_dataframe import get_as_dataframe, set_with_dataframe
import SheetTuning.ColumnMapping as cmap
import SheetTuning.SheetBoudaries as b


class SheetReader():
    def __init__(self, gc, sh):
        self.gc = gc
        self.sh = sh  # Opened worksheet

    def readSheet(self, sheet_name: str) -> pd.DataFrame:
        '''
        Прочитать весь лист в один датафрейм
        '''
        worksheet = self.sh.worksheet(sheet_name)
        dataframe = pd.DataFrame(worksheet.get_all_records())

        return dataframe

    def readSheetMultipule(self, sheet_name: str) -> list:
        '''
        Прочитать несколько датафреймов с листа
        '''
        worksheet = self.sh.worksheet(sheet_name)
        result_tables = []
        for key in b.SheetBoudaries[sheet_name]:
            df = get_as_dataframe(
                worksheet, usecols=b.SheetBoudaries[sheet_name][key], skip_blank_lines=True).dropna()
            result_tables.append(df)

        return result_tables

    def readSheet_test(self, sheet_nm: str) -> pd.DataFrame:
        worksheet = self.sh.worksheet(sheet_nm)

        dataframe = get_as_dataframe(
            worksheet, usecols=[0, 1, 2], skip_blank_lines=True).dropna()

        return dataframe

    def renameDataframeColumns(self, df: pd.DataFrame, sheet_nm: str):
        return df.rename(columns=cmap.ColumnMapping[sheet_nm])
