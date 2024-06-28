import pandas as pd
import matplotlib.pyplot as plt


class Visualiser():
    def __init__(self):
        pass

    def visualize_category_distribution(self, df: pd.DataFrame):
        # Ensure that the dataframe has the required structure
        if 'product_nm' not in df.columns or 'total_item_cost' not in df.columns:
            raise ValueError(
                "DataFrame must contain 'product_nm' and 'total_item_cost' columns")

        df.set_index('product_nm', inplace=True)
        # Calculate the percentage for each category
        categories = [col for col in df.columns if col not in [
            'product_nm', 'total_item_cost']]
        df_categories = df[categories]
        df_percentage = df_categories.div(df['total_item_cost'], axis=0) * 100

        # Plotting
        ax = df_percentage.plot(kind='bar', stacked=True,
                                colormap='viridis', figsize=(10, 7))

        # Adding labels and title
        plt.xlabel('Product')
        plt.ylabel('Percentage of Total Cost Amount')
        plt.title(
            'Percentage Contribution of Each Category to Total Cost Amount by Product')
        plt.legend(title='Category', bbox_to_anchor=(
            1.05, 1), loc='upper left')

        # Annotate bars
        for p in ax.patches:
            width, height = p.get_width(), p.get_height()
            x, y = p.get_xy()
            ax.annotate(f'{height:.1f}%', (x + width / 2, y + height / 2),
                        ha='center', va='center', fontsize=9, color='white', weight='bold')

        ax.set_xticklabels(df.index, rotation=0)
        # Show the plot
        plt.tight_layout()
        plt.show()

    def visualize_roi(self, roi: pd.DataFrame):
        # Visualization: Total Spend vs Total Gain vs Expected Return vs Expected Gain
        plt.figure(figsize=(14, 7))
        bar_width = 0.2  # Width of the bars
        r1 = range(len(roi['supply_id']))
        r2 = [x + bar_width for x in r1]
        r3 = [x + bar_width for x in r2]
        r4 = [x + bar_width for x in r3]

        # Create bars for total_expenditures, total_gains, expected_return, and expected_gain
        plt.bar(r1, roi['total_expenditures'], color='blue',
                width=bar_width, edgecolor='grey', label='Total Expenditures')
        plt.bar(r2, roi['total_gains'], color='green',
                width=bar_width, edgecolor='grey', label='Total Gains')
        plt.bar(r3, roi['expected_return'], color='orange',
                width=bar_width, edgecolor='grey', label='Expected Return')
        plt.bar(r4, roi['expected_gain'], color='red',
                width=bar_width, edgecolor='grey', label='Expected Gain')

        # Add labels, title, and legend
        plt.xlabel('Supply ID', fontweight='bold')
        plt.xticks(
            [r + 1.5*bar_width for r in range(len(roi['supply_id']))], roi['supply_id'])
        plt.ylabel('Amount')
        plt.title(
            'Total Expenditures vs Total Gains vs Expected Return vs Expected Gain by Supply ID')
        plt.legend()

        # Add annotations for each bar
        for i in range(len(roi)):
            # Annotations for total_expenditures
            plt.text(r1[i], roi['total_expenditures'][i] + 0.05 * roi['total_expenditures'][i],
                     f'{roi["total_expenditures"][i]:.2f}', ha='center', va='bottom')

            # Annotations for total_gains
            plt.text(r2[i], roi['total_gains'][i] + 0.05 * roi['total_gains'][i],
                     f'{roi["total_gains"][i]:.2f}', ha='center', va='bottom')

            # Annotations for expected_return
            plt.text(r3[i], roi['expected_return'][i] + 0.05 * roi['expected_return'][i],
                     f'{roi["expected_return"][i]:.2f}', ha='center', va='bottom')

            # Annotations for expected_gain
            plt.text(r4[i], roi['expected_gain'][i] + 0.05 * roi['expected_gain'][i],
                     f'{roi["expected_gain"][i]:.2f}', ha='center', va='bottom')

        # Display the plot
        plt.show()
