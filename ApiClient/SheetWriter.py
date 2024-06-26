from gspread_dataframe import get_as_dataframe, set_with_dataframe
from pandas import DataFrame
from gspread import exceptions


class SheetWriter():
    def __init__(self, gc, sh):
        self.gc = gc
        self.sh = sh  # Opened worksheet

    def writeToSheet(self, sheet_name: str, df: DataFrame, include_headers=False):
        worksheet = self.sh.worksheet(sheet_name)

        try:
            # Запись DataFrame в таблицу Google Sheets
            ws = set_with_dataframe(
                worksheet, df, include_column_header=include_headers)
            print("Данные успешно записаны в таблицу")
        except exceptions.APIError as e:
            print("Ошибка записи данных в таблицу:", e)
