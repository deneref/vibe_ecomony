from pprint import pprint

from ApiClient.SheetReader import SheetReader
from ApiClient.SheetWriter import SheetWriter
import SheetNames
from ApiClient.ApiService import ApiService
import CoreAnalyst as ca


ApiService = ApiService()

sheetReader = SheetReader(
    ApiService.getGcService(), ApiService.getWorksheet())

sheetWriter = SheetWriter(
    ApiService.getGcService(), ApiService.getWorksheet())

sn = SheetNames.SheetNames
analyst = ca.CoreAnalyst()

opEx = sheetReader.readSheet(sn.opEx)
opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')
print(opEx)

supply = sheetReader.readSheet(sn.supply)
supply = sheetReader.renameDataframeColumns(supply, 'supply')
print(supply)

df = analyst.allocateSpendings(opEx=opEx, supply=supply)
print(df)
sheetWriter.writeToSheet(sn.result, df)

df = analyst.countTotalProductCost(df)
print(df)
print(list(df.columns.values))
sheetWriter.writeToSheet(sn.total_product_cost, df)
