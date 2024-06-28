from pprint import pprint

from ApiClient.SheetReader import SheetReader
from ApiClient.SheetWriter import SheetWriter
import SheetTuning.SheetNames as SheetNames
from ApiClient.ApiService import ApiService
import Analyst.CoreAnalyst as ca
import Analyst.Visualiser as vision

import TestingScenarios as test

ApiService = ApiService()

sheetReader = SheetReader(
    ApiService.getGcService(), ApiService.getWorksheet())

sheetWriter = SheetWriter(
    ApiService.getGcService(), ApiService.getWorksheet())

sn = SheetNames.SheetNames
analyst = ca.CoreAnalyst()
vision = vision.Visualiser()

test = test.TestingScenarios(
    sheetWriter=sheetWriter, sheetReader=sheetReader, sn=sn, analyst=analyst, vision=vision)

# test.test_countMarketing()

# test.test_count_roi()
test.test_visualise_roi()
