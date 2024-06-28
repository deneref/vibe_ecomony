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
