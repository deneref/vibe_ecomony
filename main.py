from pprint import pprint

from AnalystApp import AnalystApp
from bot.YourBot import YourBot

import TestingScenarios as test

analystApp = AnalystApp()
yourBot = YourBot()

yourBot.startBot()

# test.test_countMarketing()

# test.test_count_roi()
test.test_visualise_income_by_product()
