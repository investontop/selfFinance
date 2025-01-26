# import - Own utils
import configparser
from utility import SFUtil
import os
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

intend = '      '

def initialize():
    # read configs
    config = configparser.ConfigParser()        # instance
    configFile = SFUtil.initiate_env_var('ConfigFile')
    config.read(configFile)

    return(config, configFile)

def read_format_excel(file_path):
    # Read the worksheet into a DataFrame
    df = pd.read_excel(file_path, sheet_name='Sheet1')  # Replace 'Sheet1' with your sheet name if required

    # Convert all columns to numeric where possible
    for col in df.columns[1:]:  # Skip the first column (non-numeric, categorical)
        df[col] = df[col].replace(",", "", regex=True).astype(float)

    # Format all numeric columns with commas
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: f"{x:,.0f}")



    return(df)

def plot_the_chart(df):
    # Detect all year columns dynamically (assuming numeric columns except "Category")
    year_columns = [col for col in df.columns if col != "Category"]

    # Convert year column values to numeric if they are strings
    for col in year_columns:
        df[col] = df[col].replace(",", "", regex=True).astype(float)

    # Plot all categories in a single chart
    plt.figure(figsize=(12, 8))

    for _, row in df.iterrows():
        # Plot each category as a separate line
        line, = plt.plot(year_columns, [row[year] for year in year_columns], marker="o", label=row["Category"])

        # Adding category name near the line
        # Adjust 'x' and 'y' offsets to fine-tune the label position
        plt.text(year_columns[-1], row[year_columns[-1]], row["Category"], color=line.get_color(),
                 verticalalignment='bottom', horizontalalignment='left', fontsize=12)

    # Customize the chart
    plt.title("Yearly Financial Data by Category", fontsize=16)
    plt.xlabel("Year", fontsize=14)
    plt.ylabel("Amount", fontsize=14)
    plt.xticks(year_columns, rotation=45)

    # Set the y-axis range and create detailed yticks
    y_min = df[year_columns].min().min()
    y_max = df[year_columns].max().max()
    yticks_range = np.arange(y_min, y_max + 1, step=(y_max - y_min) / 10)  # 10 intervals
    plt.yticks(yticks_range)  # Apply the custom yticks

    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()

    # Show the chart
    plt.show()


def main():

    config, configFile = initialize()
    base_dir = os.path.dirname(os.path.abspath(__file__))
    current_filename = os.path.basename(__file__)

    print(f'\n{intend}[' + datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S") + '] [' + current_filename + "] Started - Considering config: ["
          + configFile + "]")
    print(f'{intend}Note: Exit Code 0 means Success')

    # Variables assigning [common variables]
    sourcePath = config['Income-Expense']['sourcepath']
    fileName = config['Income-Expense']['fileName']  # sample file name: Data.xlsx
    file_path = os.path.join(sourcePath, fileName)

    df = read_format_excel(file_path)

    print(df)
    plot_the_chart(df)
    print(df)



if __name__ == "__main__":
    main()
