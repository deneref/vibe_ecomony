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
