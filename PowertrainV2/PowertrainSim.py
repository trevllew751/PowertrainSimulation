"""This file will call ExcelParser.py and pass its outputs to Calculations.py. This is the main script"""
import pandas as pd
import numpy as np

# Uses OpenPyXL engine to parse the workbook into a dictionary/dataframe where the keys are the individual sheet names
parse = pd.read_excel("Powertrain Simulation Data.xlsx", engine="openpyxl",
                      sheet_name=["Motors", "Motor_Controllers", "Batteries"])
# Breaks the parse into individual sheets. The sheet types are dataframes
motors = parse["Motors"].values
motor_controllers = parse["Motor_Controllers"].values
batteries = parse["Batteries"].values


def all_batt_configs(v_min, i_min):
    """ Takes a minimum voltage and current, parses the batteries spreadsheet, and generates the minimum
        viable pack for the required voltage and current
        Battery, Nominal Voltage (V), Nominal Capacity (Ah), Cell Weight (g), Internal Resistance (Ohms), Cost (USD)"""
    packs = []
    pack_num = 1
    for battery in batteries:
        nom_voltage = battery[1]
        nom_capacity = battery[2]
        cells_series = np.ceil(v_min / nom_voltage)
        cells_parallel = np.ceil(i_min / nom_capacity)
        total_cells = cells_series * cells_parallel
        pack = {"pack": f"Pack {pack_num}",
                "cell": str(battery[0]),
                "cells_total": total_cells,
                "cells_series": cells_series,
                "cells_parallel": cells_parallel,
                "capacity (kWh)": np.round((cells_series * nom_voltage) * (cells_parallel * nom_capacity) / 1000, 2),
                "resistance_total": np.round((cells_series * battery[4]) / cells_parallel, 2),
                "weight (lbs)": np.round((total_cells * battery[3]) / 1000 * 2.2, 2)}
        packs.append(pack)
        pack_num += 1
        # print(battery)
    for pack in packs:
        print(pack)


def main():
    all_batt_configs(100, 200)  # Dummy test


if __name__ == "__main__":
    main()
