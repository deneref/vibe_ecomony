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

        self.investments = None  # not yet used
        self.result = None  # not yet used
        self.remains = None  # not yet used

        self.opEx = None
        self.capEx = None
        self.supply = None
        self.sales = None
        self.marketing = None
        self.allocated = None
        self.pivoted_allocated = None

    def getSheetReader(self):
        return self.sheetReader

    def getSn(self):
        return self.sn

    def get_opEx(self):
        if not self.opEx is None:
            return self.opEx
        else:
            self.opEx = self.sheetReader.readSheet(self.sn.opEx)
            self.opEx = self.sheetReader.renameDataframeColumns(
                self.opEx, 'opEx')

            return self.opEx

    def get_capEx(self):
        if not self.capEx is None:
            return self.capEx
        else:
            self.capEx = self.sheetReader.readSheet(sn.capEx)
            self.capEx = self.sheetReader.renameDataframeColumns(
                self.capEx, 'capEx')

            return self.capEx

    def get_supply(self):
        if not self.supply is None:
            return self.supply
        else:
            self.supply = self.sheetReader.readSheet(self.sn.supply)
            self.supply = self.sheetReader.renameDataframeColumns(
                self.supply, 'supply')

            return self.supply

    def get_sales(self):
        if not self.sales is None:
            return self.sales
        else:
            self.sales = self.sheetReader.readSheet(self.sn.sales)
            self.sales = self.sheetReader.renameDataframeColumns(
                self.sales, 'sales')

            return self.sales

    def get_marketing(self):
        if not self.marketing is None:
            return self.marketing
        else:
            self.marketing = self.sheetReader.readSheet(self.sn.marketing)
            self.marketing = self.sheetReader.renameDataframeColumns(
                self.marketing, 'marketing')

            return self.marketing

    def get_allocated(self):
        if not self.allocated is None:
            return self.allocated
        else:
            opEx = self.get_opEx()
            supply = self.get_supply()
            self.allocated = self.analyst.allocateSpendings(opEx, supply)

            return self.allocated

    def get_pivoted_allocated(self):
        if not self.pivoted_allocated is None:
            return self.pivoted_allocated
        else:
            self.pivoted_allocated = self.analyst.pivot_category(
                self.get_allocated())

            return self.pivoted_allocated

    def getAllGraphs(self):
        analyst, vision = self.analyst, self.vision

        print('читаем opEx')
        opEx = self.get_opEx()

        print('читаем supply')
        supply = self.get_supply()

        print('читаем sales')
        sales = self.get_sales()

        print('считаем allocated')
        allocated = self.get_allocated()
        pivoted_allocated = self.get_pivoted_allocated()

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

    def get_avg_by_product(self):
        result = self.analyst.get_avg_value_by_product(
            self.get_sales(), self.get_pivoted_allocated())

        return result.to_string()

    def run_test(self, test_name: str):
        print("запускаем test")
        if test_name == 'test_visualiseAllocation':
            self.test.test_visualiseAllocation()
        elif test_name == 'test_visualise_roi':
            self.test.test_visualise_roi()
        elif test_name == 'test_get_avg_value_by_product':
            self.test.test_get_avg_value_by_product()
