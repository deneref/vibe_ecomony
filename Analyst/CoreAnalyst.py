import pandas as pd
from prophet import Prophet

from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric

import os


class CoreAnalyst():
    def __init__(self):
        '''
        sales:
            - 'supply_id'
            - 'product_nm'
            - 'channel'
            - 'item_amt'
            - 'sale_date'
        '''
        pass

    def allocateSpendings(self, opEx: pd.DataFrame, supply: pd.DataFrame) -> pd.DataFrame:
        opEx = opEx.groupby(['supply_id', 'category'], as_index=False)[
            'item_amt'].sum()

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

    def countMarketingMetrics(self, campaign: pd.DataFrame, campaign_x_product: pd.DataFrame, sales: pd.DataFrame) -> pd.DataFrame:
        # Ensure date columns are in datetime format
        campaign['start_dt'] = pd.to_datetime(campaign['start_dt'])
        campaign['end_dt'] = pd.to_datetime(campaign['end_dt'])
        sales['sale_date'] = pd.to_datetime(sales['sale_date'])

        # Merge campaign_x_product with campaigns to get campaign and product details together
        campaign_details = pd.merge(
            campaign_x_product, campaign, on='campaign_id', how='left')

        # Merge campaign_details with sales to get the sales data aligned with the campaigns and products
        merged_data = pd.merge(campaign_details, sales, on=[
                               'product_nm', 'channel'], how='left')

        # Filter the merged data to only include sales that happened during the campaign period
        merged_data = merged_data[(merged_data['sale_date'] >= merged_data['start_dt']) & (
            merged_data['sale_date'] <= merged_data['end_dt'])]

        # Group by campaign and compute the metrics
        campaign_metrics = merged_data.groupby('campaign_id').agg(
            # 'item_amt' from sales dataframe
            total_revenue=pd.NamedAgg(column='item_amt_y', aggfunc='sum'),
            total_customers=pd.NamedAgg(column='supply_id', aggfunc='nunique')
        ).reset_index()

        # Calculate ARPU
        campaign_metrics['ARPU'] = campaign_metrics['total_revenue'] / \
            campaign_metrics['total_customers']

        return campaign_metrics

    def calculate_roi(self, opEx: pd.DataFrame, sales: pd.DataFrame, supply: pd.DataFrame) -> pd.DataFrame:
        # Ensure date columns are in datetime format
        sales['sale_date'] = pd.to_datetime(sales['sale_date'])

        # TODO: тут надо перейти на pivoted_allocated

        # Calculate total expenses by supply_id
        total_expenses = opEx.groupby('supply_id')['item_amt'].sum(
        ).reset_index().rename(columns={'item_amt': 'total_expenditures'})

        # Calculate total sales by supply_id
        total_sales = sales.groupby('supply_id')['item_amt'].sum(
        ).reset_index().rename(columns={'item_amt': 'total_gains'})

        total_supply = supply.groupby('supply_id')['supply_amt'].sum(
        ).reset_index().rename(columns={'supply_amt': 'total_supply_amt'})

        # Merge the expenditures and sales data
        merged_data = pd.merge(total_expenses, total_sales,
                               on='supply_id', how='outer').fillna(0)

        # Calculate total difference (gains - expenditures)
        merged_data['total_difference'] = merged_data['total_gains'] - \
            merged_data['total_expenditures']

        avg_product_price = sales.groupby('supply_id')['item_amt'].mean(
        ).reset_index().rename(columns={'item_amt': 'avg_product_price'})

        avg_product_price = pd.merge(
            total_supply, avg_product_price, on='supply_id', how='left').fillna(0)

        merged_data = pd.merge(
            merged_data, avg_product_price, on='supply_id', how='left').fillna(0)

        # Calculate products needed to break even
        merged_data['avg_products_left_to_breakeven'] = merged_data['total_difference'] / \
            merged_data['avg_product_price'] * -1

        merged_data['expected_gain'] = merged_data['avg_product_price'] * \
            merged_data['total_supply_amt']
        merged_data['expected_return'] = merged_data['avg_product_price'] * \
            merged_data['total_supply_amt'] - merged_data['total_expenditures']

        # Handling infinite values and NaNs when dividing by zero
        merged_data['avg_products_left_to_breakeven'].replace(
            [float('inf'), - float('inf'), pd.NA], 0, inplace=True)

        return merged_data

    def calculate_income_by_product(self, sales: pd.DataFrame, allocated: pd.DataFrame) -> pd.DataFrame:
        # Ensure date columns in sales_df are in datetime format
        sales['sale_date'] = pd.to_datetime(sales['sale_date'])

        # Group by product_nm to sum up the total income for each product
        total_income_by_product = sales.groupby('product_nm')['item_amt'].sum(
        ).reset_index().rename(columns={'item_amt': 'total_income'})

        # Merge with cost_df to maintain the product list and include total_item_cost - though it's not strictly needed for this specific request
        merged_data = pd.merge(allocated[[
                               'product_nm']], total_income_by_product, on='product_nm', how='left').fillna(0)

        # Sort products by total_income for better visualization (optional)
        merged_data = merged_data.sort_values(
            by='total_income', ascending=False)

        return merged_data

    def get_avg_value_by_product(self, sales: pd.DataFrame, pivoted_allocated: pd.DataFrame) -> pd.DataFrame:
        '''
        Расчет средней чистой прибыли, которую принес продукт

        DF: product_nm  net_income
        '''
        # print(sales, pivoted_allocated)
        allocated = pivoted_allocated[['product_nm', 'total_item_cost']]
        # Merge the two DataFrames on 'supply_id' and 'product_nm'
        merged_df = pd.merge(sales, allocated, on=['product_nm'])

        # print(merged_df)

        # Calculate the net income for each sale
        merged_df['net_income'] = merged_df['item_amt'] - \
            merged_df['total_item_cost']

        # Calculate the average net income per product for returning
        avg_net_income_per_product = merged_df.groupby(
            'product_nm')['net_income'].mean().reset_index()

        return avg_net_income_per_product

    def get_russian_holidays(self) -> pd.DataFrame:
        holidays = pd.DataFrame({
            'holiday': ['National Unity Day', 'Constitution Day', 'Christmas Day', 'New Year\'s Eve'],
            'ds': pd.to_datetime([
                '2024-11-04',  # National Unity Day
                '2024-12-12',  # Constitution Day
                '2024-12-25',  # Christmas Day
                '2024-12-31',  # New Year's Eve
            ]),
            'lower_window': 0,
            'upper_window': 1
        })

        return holidays

    def get_moscow_weather(self) -> pd.DataFrame:
        '''
        weather_data.csv
        date,temperature,rainfall
        '''

        weather_df = pd.read_csv('weather.csv')
        weather_df['date'] = pd.to_datetime(
            weather_df['date'])

        return weather_df

    def get_future_moscow_weather(self) -> pd.DataFrame:
        '''
        future_weather.csv
        date,temperature,rainfall
        '''

        weather_df = pd.read_csv('future_weather.csv')
        weather_df['date'] = pd.to_datetime(weather_df['date'])

        return weather_df

    def forecats(self, sales) -> pd.DataFrame:
        # Convert the date column to datetime
        sales['sale_date'] = pd.to_datetime(
            sales['sale_date'])

        # Aggregate the sales data by date
        daily_sales = sales.groupby('sale_date')[
            'item_amt'].sum().reset_index()

        # Rename columns to be compatible with Prophet
        daily_sales.columns = ['ds', 'y']

        # Create additional features
        daily_sales['day_of_week'] = daily_sales['ds'].dt.dayofweek
        daily_sales['is_weekend'] = daily_sales['day_of_week'].apply(
            lambda x: 1 if x >= 5 else 0)

        # Initialize Prophet model
        holidays = self.get_russian_holidays()
        weather = self.get_moscow_weather()
        weather.columns = ['ds', 'temperature', 'rainfall']

        daily_sales = pd.merge(daily_sales, weather, on='ds', how='left')
        daily_sales.fillna(0, inplace=True)

        model = Prophet(holidays=holidays, yearly_seasonality=False,
                        weekly_seasonality=True, daily_seasonality=False)
        model.add_regressor('is_weekend')
        model.add_regressor('temperature')
        model.add_regressor('rainfall')

        # Fit the model with the data
        model.fit(daily_sales)

        # Create a dataframe with future dates
        future_dates = model.make_future_dataframe(
            periods=7)  # Predicting 7 days into the future
        future_dates['is_weekend'] = future_dates['ds'].dt.dayofweek.apply(
            lambda x: 1 if x >= 5 else 0)

        future_weather = self.get_future_moscow_weather()
        future_weather.columns = ['ds', 'temperature', 'rainfall']

        future = pd.merge(future_dates, future_weather, on='ds', how='left')
        future.fillna(0, inplace=True)

        # Make predictions
        forecast = model.predict(future)

        return model, forecast

    def forecats_metrics(self, model):
        # Perform cross-validation
        df_cv = cross_validation(
            model, initial='20 days', period='4 days', horizon='6 days')

        # Calculate performance metrics
        df_p = performance_metrics(df_cv)
        print(df_p.head())

        # Plot cross-validation metrics
        fig2 = plot_cross_validation_metric(df_cv, metric='mape')
        fig2.show()
