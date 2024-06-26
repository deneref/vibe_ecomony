from pprint import pprint

from ApiClient.SheetReader import SheetReader
from ApiClient.SheetWriter import SheetWriter
import SheetNames
from ApiClient.ApiService import ApiService
import CoreAnalyst as ca
import Visualiser as vision

import pandas as pd


ApiService = ApiService()

sheetReader = SheetReader(
    ApiService.getGcService(), ApiService.getWorksheet())

sheetWriter = SheetWriter(
    ApiService.getGcService(), ApiService.getWorksheet())

sn = SheetNames.SheetNames
analyst = ca.CoreAnalyst()
vision = vision.Visualiser()


opEx = sheetReader.readSheet(sn.opEx)
opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')
# print(opEx)

supply = sheetReader.readSheet(sn.supply)
supply = sheetReader.renameDataframeColumns(supply, 'supply')
# print(supply)

df = analyst.allocateSpendings(opEx=opEx, supply=supply)
df = analyst.pivot_category(df)
print(df)
sheetWriter.writeToSheet(sn.allocatedSpending, df, True)

vision.visualize_category_distribution(df)

'''
sales = sheetReader.readSheet(sn.sales)
sales = sheetReader.renameDataframeColumns(sales, 'sales')
print(sales)

supply = sheetReader.readSheet(sn.supply)
supply = sheetReader.renameDataframeColumns(supply, 'supply')
print(supply)

df = analyst.countRemains(sales, supply)
print(df)
'''
