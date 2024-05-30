from pprint import pprint

from SheetReader import SheetReader
from SheetWriter import SheetWriter
import SheetNames
import ApiService


ApiService = ApiService.ApiService()

sheetReader = SheetReader(
    ApiService.getGcService(), ApiService.getWorksheet())

sheetWriter = SheetWriter(
    ApiService.getGcService(), ApiService.getWorksheet())

sn = SheetNames.SheetNames

totalSpending = sheetReader.readSheet_test(sn.totalSpending)
# opEx = sheetReader.readSheet(sn.opEx)
# supply = sheetReader.readSheet(sn.supply)

sheetWriter.writeToSheet(sn.result, totalSpending)

'''
# Пример записи в файл
values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "B3:C4",
             "majorDimension": "ROWS",
             "values": [["This is B3", "This is C3"], ["This is B4", "This is C4"]]},
            {"range": "D5:E6",
             "majorDimension": "COLUMNS",
             "values": [["This is D5", "This is D6"], ["This is E5", "=5+5"]]}
  ]
    }
).execute()
'''
