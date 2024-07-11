from pprint import pprint

from AnalystApp import AnalystApp
from bot.YourBot import YourBot

import TestingScenarios as test

analystApp = AnalystApp()
yourBot = YourBot()

yourBot.startBot()

'''
print('читаем sales')
sales = analystApp.getSheetReader().readSheet(analystApp.getSn().sales)
sales = analystApp.getSheetReader().renameDataframeColumns(
    analystApp.getSn().sales, 'sales')
print(sales)
'''

# test.test_countMarketing()

# test.test_count_roi()
# analystApp.run_test('test_visualise_roi')
