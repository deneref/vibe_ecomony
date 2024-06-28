from pprint import pprint

from ApiClient.SheetReader import SheetReader
from ApiClient.SheetWriter import SheetWriter
import SheetTuning.SheetNames as SheetNames
from ApiClient.ApiService import ApiService
import Analyst.CoreAnalyst as ca
import Analyst.Visualiser as vision


class TestingScenarios:
    '''
    Это просто сценарии, которые я хочу тестить вручную, не нормальные тесты
    '''

    def __init__(self, sheetReader, sheetWriter, sn, analyst, vision):
        self.sheetReader = sheetReader
        self.sheetWriter = sheetWriter
        self.sn = sn  # sheetNames
        self.analyst = analyst
        self.vision = vision

    def test_countMarketing(self):
        sheetReader, sn, analyst = self.sheetReader, self.sn, self.analyst

        marketing = sheetReader.readSheetMultipule(sn.marketing)

        marketing = list(
            map(lambda x: sheetReader.renameDataframeColumns(x, 'marketing'), marketing))

        campaign = marketing[0]
        campaign_x_product = marketing[1]

        print(campaign)
        print(campaign_x_product)

        sales = sheetReader.readSheet(sn.sales)
        sales = sheetReader.renameDataframeColumns(sales, 'sales')

        print(sales)

    def test_countAllocationOfExpances(self):
        sheetReader, sn, analyst = self.sheetReader, self.sn, self.analyst

        opEx = sheetReader.readSheet(sn.opEx)
        opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')
        # print(opEx)

        supply = sheetReader.readSheet(sn.supply)
        supply = sheetReader.renameDataframeColumns(supply, 'supply')
        # print(supply)

        df = analyst.allocateSpendings(opEx=opEx, supply=supply)
        print(df)
        self.sheetWriter.writeToSheet(sn.allocatedSpending, df, True)

        vision.visualize_category_distribution(df)

    def test_visualiseAllocation(self):
        sheetReader, sn, analyst = self.sheetReader, self.sn, self.analyst

        opEx = sheetReader.readSheet(sn.opEx)
        opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')
        # print(opEx)

        supply = sheetReader.readSheet(sn.supply)
        supply = sheetReader.renameDataframeColumns(supply, 'supply')
        # print(supply)

        df = analyst.allocateSpendings(opEx=opEx, supply=supply)
        df = analyst.pivot_category(df)
        print(df)
        self.sheetWriter.writeToSheet(sn.allocatedSpending, df, True)

        vision.visualize_category_distribution(df)

    def test_count_roi(self):
        '''
        Тестирует цепочку расчета окупаемости парти: сколько в среднем штук осталось до того, чтобы отбить затраты
        '''
        sheetReader, sn, analyst = self.sheetReader, self.sn, self.analyst

        opEx = sheetReader.readSheet(sn.opEx)
        opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')
        # print(opEx)

        sales = sheetReader.readSheet(sn.sales)
        sales = sheetReader.renameDataframeColumns(sales, 'sales')
        # print(sales)

        supply = sheetReader.readSheet(sn.supply)
        supply = sheetReader.renameDataframeColumns(supply, 'supply')
        # print(supply)

        df = analyst.calculate_roi(opEx, sales, supply)

        print(df)

    def test_visualise_roi(self):
        sheetReader, sn, analyst, vision = self.sheetReader, self.sn, self.analyst, self.vision

        opEx = sheetReader.readSheet(sn.opEx)
        opEx = sheetReader.renameDataframeColumns(opEx, 'opEx')
        # print(opEx)

        sales = sheetReader.readSheet(sn.sales)
        sales = sheetReader.renameDataframeColumns(sales, 'sales')
        # print(sales)

        supply = sheetReader.readSheet(sn.supply)
        supply = sheetReader.renameDataframeColumns(supply, 'supply')
        # print(supply)

        df = analyst.calculate_roi(opEx, sales, supply)

        vision.visualize_roi(df)
