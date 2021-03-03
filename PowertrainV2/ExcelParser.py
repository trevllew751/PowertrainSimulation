"""This file will parse the excel workbook and return it to PowertrainSim.py for use in Calculations.py"""
import pandas as pd


# Uses OpenPyXL engine to parse the workbook into a dictionary/dataframe where the keys are the individual sheet names
parse = pd.read_excel("Powertrain Simulation Data.xlsx", engine="openpyxl",
                      sheet_name=["Motors", "Motor_Controllers", "Battery_Packs"])
# Breaks the parse into individual sheets. The sheet types are dataframes
motors = parse["Motors"]
motor_controllers = parse["Motor_Controllers"]
battery_packs = parse["Battery_Packs"]
