"""This file will call ExcelParser.py and pass its outputs to Calculations.py. This is the main script"""
import pandas as pd
import numpy as np
import csv

# Uses OpenPyXL engine to parse the workbook into a dictionary/dataframe where the keys are the individual sheet names
parse = pd.read_excel("Powertrain Simulation Data.xlsx", engine="openpyxl",
                      sheet_name=["Motors", "Motor_Controllers", "Batteries"])
# Breaks the parse into individual sheets. The sheet types are dataframes
motors = parse["Motors"].values
motor_controllers = parse["Motor_Controllers"].values
batteries = parse["Batteries"].values


def all_batt_configs(v_min, i_min, v_max, i_max):
    """ Takes a minimum and maximum voltage and current, parses the batteries spreadsheet, and generates the minimum
        viable pack for the required voltage and current
        Battery, Nominal Voltage (V), Nominal Capacity (Ah), Cell Weight (g), Internal Resistance (Ohms), Cost (USD)"""
    packs = []
    for battery in batteries:
        nom_voltage = battery[1]
        nom_capacity = battery[2]
        for v in np.arange(v_min, v_max, 1):
            for i in np.arange(i_min, i_max, 1):
                cells_series = np.ceil(v / nom_voltage)
                cells_parallel = np.ceil(i / nom_capacity)
                total_cells = cells_series * cells_parallel
                pack = {"cell_type": str(battery[0]),
                        "cells_total": total_cells,
                        "cells_series": cells_series,
                        "cells_parallel": cells_parallel,
                        "pack_voltage": v,
                        "pack_current": i,
                        "capacity (kWh)": np.round(
                            (cells_series * nom_voltage) * (cells_parallel * nom_capacity) / 1000, 2),
                        "resistance_total": np.round((cells_series * battery[4]) / cells_parallel, 2),
                        "weight (lbs)": np.round((total_cells * battery[3]) / 1000 * 2.2, 2),
                        "cost (USD)": total_cells * battery[5] if battery[5] else "N/A"}
                packs.append(pack)
        with open("packs.csv", 'w', newline='') as packs_csv:
            fieldnames = ["cell_type", "cells_total", "cells_series", "cells_parallel", "pack_voltage",
                          "pack_current", "capacity (kWh)", "resistance_total", "weight (lbs)", "cost (USD)"]
            writer = csv.DictWriter(packs_csv, fieldnames=fieldnames)
            writer.writeheader()
            for pack in packs:
                writer.writerow(pack)


def main():
    all_batt_configs(100, 100, 105, 110)  # Dummy test


if __name__ == "__main__":
    main()
