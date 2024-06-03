import pandas as pd


class CoreAnalyst():
    def __init__(self):
        pass

    def allocateSpendings(self, opEx: pd.DataFrame, supply: pd.DataFrame) -> pd.DataFrame:
        opEx = opEx.groupby(['supply_id', 'category']).sum()

        supply['total_supply_amt'] = supply.groupby(
            'supply_id')['supply_amt'].transform('sum')

        supply['supply_fraction'] = supply['supply_amt'] / \
            supply['total_supply_amt']

        allocated = supply.merge(opEx, how='inner', on='supply_id')

        allocated['item_cost'] = allocated['item_amt'] * allocated['supply_fraction'] / \
            allocated['supply_amt']

        return allocated

    def countTotalProductCost(self, allocated: pd.DataFrame) -> pd.DataFrame:
        allocated = allocated.groupby(['supply_id', 'product_nm'])[
            'item_cost'].sum().reset_index()

        return allocated
