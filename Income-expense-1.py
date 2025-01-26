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

    return(df)

def plot_the_chart(df):
    # Detect all year columns dynamically (assuming numeric columns except "Category")
    year_columns = [col for col in df.columns if col != "Category"]

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


def format_the_df(dfcopy):
    dfcopy = dfcopy.drop(dfcopy[dfcopy['Category'] == 'Svigs b4 YrEXP&INV&INS'].index)
    print(dfcopy)

    # Select the rows you want to add
    us_expenditure = dfcopy[dfcopy['Category'] == 'Usual expenditure'].iloc[0]
    yearly_exp = dfcopy[dfcopy['Category'] == 'Yearly Exp'].iloc[0]

    # Sum the values for each year column (assuming they are numeric)
    summed_row = us_expenditure.copy()
    summed_row[1:] = us_expenditure[1:] + yearly_exp[1:]  # Add the values (excluding the Category column)
    # Set the 'Category' for the new row
    summed_row['Category'] = 'Total Expediture'

    # Drop the original rows
    dfcopy = dfcopy.drop(dfcopy[dfcopy['Category'] == 'Yearly Exp'].index)
    dfcopy = dfcopy.drop(dfcopy[dfcopy['Category'] == 'Usual expenditure'].index)
    dfcopy = dfcopy.drop(dfcopy[dfcopy['Category'] == 'Income'].index)

    # Use pd.concat to add the new row
    dfcopy = pd.concat([dfcopy, pd.DataFrame([summed_row])], ignore_index=True)

    # Display the updated DataFrame
    return(dfcopy)


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
    plot_the_chart(df)


    dfcopy = format_the_df(df.copy())
    plot_the_chart(dfcopy)


    print(f'\n{intend}[' + datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S") + '] [' + current_filename + "] Completed")

if __name__ == "__main__":
    main()
