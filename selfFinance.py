# 2023-10-06 Initiated a py file

# import
import configparser
import os
from datetime import datetime
import openpyxl
import locale
from openpyxl import Workbook
from openpyxl.styles import PatternFill

# import - Own utils
from utility import SFUtil

# read configs
config = configparser.ConfigParser()        # instance
configFile = SFUtil.initiate_env_var('ConfigFile')
config.read(configFile)

def read_excel(file_path, pRow, pCol):
    # workbook = openpyxl.load_workbook(file_path)
    # sheet = workbook.active  # Assuming you want to read from the active sheet

    # Reading data from the first row and first column
    data = sheet.cell(row=pRow, column=pCol).value

    return data

intend = '      '
current_filename = os.path.basename(__file__)

print('['+datetime.now().strftime("%Y-%m-%d %H:%M:%S")+'] [' + current_filename  + "] Started - Considering config: ["
      + configFile + "]")
print('Note: Exit Code 0 means Success')

# Variables assigning [common variables]
sourcePath = config['SelfFinance']['sourcepath']
filePrefix = config['SelfFinance']['statementprefix']

# Get a list of files in the specified directory
files = os.listdir(sourcePath)

# Filter files that start with 'HDFC'
hdfc_files = [file for file in files if file.startswith(filePrefix)]

# Print the list of files
for file in hdfc_files:
    file_path = os.path.join(sourcePath, file)
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active  # Assuming you want to read from the active sheet

    # Get the total number of rows
    total_rows = sheet.max_row

    result = read_excel(file_path, 6, 1)
    print('Name: ' + result[:])