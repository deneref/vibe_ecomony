import pandas as pd
import matplotlib.pyplot as plt


class Visualiser():
    def __init__(self):
        pass

    def visualize_category_distribution(self, df):
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
