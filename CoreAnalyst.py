import pandas as pd


class CoreAnalyst():
    def __init__(self):
        pass

    def allocateSpendings(self, opEx: pd.DataFrame, supply: pd.DataFrame) -> pd.DataFrame:
        opEx = opEx.groupby(['supply_id', 'category'], as_index=False)[
            'item_amt'].sum()
        print(opEx)

        supply['total_supply_amt'] = supply.groupby(
            'supply_id')['supply_amt'].transform('sum')

        supply['supply_fraction'] = supply['supply_amt'] / \
            supply['total_supply_amt']

        allocated = supply.merge(opEx, how='inner', on='supply_id')
        # print(allocated)

        allocated['item_cost'] = allocated['item_amt'] * allocated['supply_fraction'] / \
            allocated['supply_amt']

        return allocated

    def countTotalProductCost(self, allocated: pd.DataFrame) -> pd.DataFrame:
        allocated = allocated.groupby(['supply_id', 'product_nm'])[
            'item_cost'].sum().reset_index()

        return allocated

    def countRemains(self, sales: pd.DataFrame, supply: pd.DataFrame) -> pd.DataFrame:
        sales['sold_amt'] = sales.groupby(
            'supply_id')['product_nm'].transform('count')

        remains = supply.merge(sales, how='inner', on=[
                               'supply_id', 'product_nm'])

        remains['remains'] = remains['supply_amt'] - sales['sold_amt']

        return remains

    def pivot_category(self, allocated: pd.DataFrame) -> pd.DataFrame:
        # Group by product and category to sum the item_cost
        grouped = allocated.groupby(['product_nm', 'category'], as_index=False)[
            'item_cost'].sum()

        # Pivot the DataFrame - categories become columns, products become index
        pivot_table = grouped.pivot(
            index='product_nm', columns='category', values='item_cost')

        # Reset the index to make 'product' a column and fill NaN values with 0 or any other fill value
        pivot_table.reset_index(inplace=True)
        pivot_table.fillna(0, inplace=True)

        # pivot_table.drop(columns=['item_amt', 'item_cost'])
        pivot_table['total_item_cost'] = pivot_table.loc[:,
                                                         pivot_table.columns != 'product_nm'].sum(axis=1)

        return pivot_table
