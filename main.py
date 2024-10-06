# This is a sample Python script.

# Press Maiusc+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


# Load the CSV file using pandas
class DataMiner:
    def __init__(self, csv1, csv2):
        tmp1 = pd.read_csv(csv1)
        tmp2 = pd.read_csv(csv2)
        self.df = pd.merge(tmp1, tmp2, left_on='cyclist', right_on='_url', how='inner')
        self.delete_column("_url_y")

    def columns_names(self):
        return self.df.columns

    def delete_column(self, col):
        self.df.drop(columns=[col], inplace=True)

    def replace_NaN(self, column, value):
        self.df[column].fillna(value, inplace=True)
    # Loop through each column to get counts
    def inspect_for_missing(self):
        print(f"{'Column':<30} | {'Non-null count':<15} | {'Total count':<15} | {'Missing':<15}")
        tmp = []
        for column in self.columns_names():
            non_null_count = self.df[column].count()  # Count of non-null values
            total_count = len(self.df[column])        # Total number of values
            print(f"{column:<30} | {non_null_count:<15} | {total_count:<15} | {total_count != non_null_count}")

            if total_count != non_null_count:
                tmp.append(column)

        return tmp

    def enumerate_column_range(self, col):
        tmp = set()
        min_v = float('inf')
        max_v = float('-inf')


        if col in self.get_categorical_columns():
            for _, row in self.df.iterrows():
                tmp.add(row[col])

            return tmp

        if col in self.get_numerical_columns():
            for _, row in self.df.iterrows():
                min_v = min(min_v, row[col])
                max_v = max(max_v, row[col])

            return [min_v, max_v]

    def find_rows_with_alternatives(self, col1, col2):
        tmp = []
        for _, row in self.df.iterrows():
            if pd.isna(row[col1]) ^ pd.isna(row[col2]):
                tmp.append(row['name_x'])
        return tmp

    def check_are_alternatives(self, col1, col2):
        alternatives_rows = len(dm.find_rows_with_alternatives(col1, col2))
        print(f"Columns: {col1}, {col2} {"YES. Columns are alternatives" if alternatives_rows == self.rows_count() else "NO. Columns are not alternatives"}. It's true only for {alternatives_rows}/{dm.rows()} rows")

    def get_missing_value_rows(self, col):
        tmp = []
        for _, row in self.df.iterrows():
            if pd.isna(row[col]):
                tmp.append(row['name_x'])
        return tmp

    def get_categorical_columns(self):
        return self.df.select_dtypes(include=['object', 'category']).columns.tolist()

    def get_numerical_columns(self):
        return self.df.select_dtypes(include=['number']).columns.tolist()

    def hist_plot(self, col):
        sns.displot(self.df,
                        x=col,
                        kind="hist",
                        row_order="desc",
                        bins=15)
        plt.xticks(rotation=90, ha='right')
        plt.show()

    def scatter_plot(self, x, y):
        sns.scatterplot(self.df, x=x, y=y)
        plt.show()

    def reformat_date(self):
        for _, row in self.df.iterrows():
            tmp = datetime.strptime(row['date'], "%Y-%m-%d %H:%M:%S")
            new_tmp = tmp.replace(hour=0, minute=0, second=0)
            row['date'] = str(int(new_tmp.timestamp()))

    def rows_count(self):
        return len(self.df)

dm = DataMiner(r"./dataset/races.csv", r"./dataset/cyclists.csv")

categoricals_cols = dm.get_categorical_columns()
numericals_cols = dm.get_numerical_columns()
print(f"Categoricals columns: {categoricals_cols}")
print(f"Numerical columns: {numericals_cols}")

missing_cols = dm.inspect_for_missing()
print(f"Missing values in columns: {missing_cols}")

dm.hist_plot("nationality")
dm.scatter_plot("profile", "points")
dm.delete_column("average_temperature")

# dm.check_are_alternatives("points", "uci_points")

print("END")