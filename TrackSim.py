# this program is called by the optimization program to determine the new powertrain's track time

import numpy as np
import pandas as pd
import math
import os

# inputs: motor max torque and total bike mass

GearRatio = 4
WheelR = 0.3302  # Wheel diameter in nanometers
BikeM = 200  # mass input from optimization program in kgs
max_torque = 10  # max torque of bike motor

location = os.path.abspath('BOLT3Data.csv')  # csv file trimmed for data from when the bike is racing

# create DataFrame
data = pd.read_csv(location, names=['time start', 'high low', 'distances', 'final speed'], header=0, low_memory=False)
data_df = pd.DataFrame(data)

# torque = torque wheel = torque shaft * 4
# f*r = torque
# torque / r = f
# f = m * a
# torque_shaft * 4 / r / m = a

max_accel = max_torque * GearRatio / WheelR / BikeM
powertrain_ID = 1  # some input from Kristen's program?

segment_times = np.zeros((len(data_df['time start']) + 1) / 2)

for i in range(0, len(data_df['time start'])):
    if i % 2 is 1:  # segments bike is braking
        time = (2 * data_df['distances'[i]]) / (data_df['final speed'][i] - data_df['final speed'][i - 1])
        segment_times.put([i], time)
    else:  # segments bike is accelerating
        if i is 0:
            det = 2 * max_accel * data_df['distances'][i]
            time = math.sqrt(det) / max_accel
            segment_times.put([i], time)
        else:
            det = pow(data_df['final speed'][i - 1], 2) + 2 * max_accel * data_df['distances']
            time = (math.sqrt(det) - data_df['final speed'][i - 1]) / max_accel
            segment_times.put([i], time)

total_time = np.sum(segment_times)

print("Total time for powertrain {} is {}".format(powertrain_ID, total_time))
