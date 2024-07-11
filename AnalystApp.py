from pprint import pprint

from ApiClient.SheetReader import SheetReader
from ApiClient.SheetWriter import SheetWriter
import SheetTuning.SheetNames as SheetNames
from ApiClient.ApiService import ApiService
import Analyst.CoreAnalyst as ca
import Analyst.Visualiser as vision

import TestingScenarios as test


class AnalystApp():
    def __init__(self) -> None:
        self.ApiService = ApiService()

        self.sheetReader = SheetReader(
            self.ApiService.getGcService(), self.ApiService.getWorksheet())

        self.sheetWriter = SheetWriter(
            self.ApiService.getGcService(), self.ApiService.getWorksheet())

        self.sn = SheetNames.SheetNames
        self.analyst = ca.CoreAnalyst()
        self.vision = vision.Visualiser()
        self.test = test.TestingScenarios(
            self.sheetReader, self.sheetWriter, self.sn, self.analyst, self.vision)

    def getSheetReader(self):
        return self.sheetReader

    def getSn(self):
        return self.sn

    def getAllGraphs(self):
        sheetReader, sn, analyst, vision = self.sheetReader, self.sn, self.analyst, self.vision

        print('читаем opEx')
        opEx = sheetReader.readSheet(sn.opEx)
        opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')

        print('читаем supply')
        supply = sheetReader.readSheet(sn.supply)
        supply = sheetReader.renameDataframeColumns(supply, 'supply')

        print('читаем sales')
        sales = sheetReader.readSheet(sn.sales)
        sales = sheetReader.renameDataframeColumns(sales, 'sales')

        print('считаем allocated')
        allocated = analyst.allocateSpendings(opEx=opEx, supply=supply)
        pivoted_allocated = analyst.pivot_category(allocated)
        print('считаем roi')
        roi = analyst.calculate_roi(opEx, sales, supply)
        print('считаем income_by_product')
        income_by_product = analyst.calculate_income_by_product(
            sales, allocated)

        images_array = []

        images_array.append(
            vision.visualize_category_distribution(pivoted_allocated, True))

        images_array.append(vision.visualize_roi(roi, True))

        images_array.append(
            vision.visualize_income_by_product(income_by_product, True))

        print('считаем images')
        return images_array

    def run_test(self, test_name: str):
        if test_name == 'test_visualiseAllocation':
            self.test.test_visualiseAllocation()
        elif test_name == 'test_visualise_roi':
            self.test.test_visualise_roi()
