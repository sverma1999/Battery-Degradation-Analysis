import pandas as pd
from Battery.logger_code.logger import logging
from Battery.exception_code.exception import BatteryException
from scipy.io import loadmat

# from scipy.io import sio
import numpy as np


class DataFileConverter:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_mat_file(self):
        # Load the .mat file
        try:
            mat_data = loadmat(self.file_path)
            logging.info(
                "Inside load_mat_file function: Done loading mat file in a viariable"
            )
        except Exception as e:
            logging.error("Inside load_mat_file function: Error loading mat file")
            raise BatteryException("Error loading mat file", e)
        return mat_data

    def find_cell_names(self, mat_data):

        data_dict_keys = list(mat_data.keys())

        # Find the index of '__globals__' in the list of keys
        globals_index = data_dict_keys.index("__globals__")

        # Extract cell names after '__globals__'
        cell_names = [
            key for key in data_dict_keys[globals_index + 1 :] if key.startswith("Cell")
        ]
        return cell_names

        # print(cell_names)

    def convert_to_dataframe(self, mat_data, cell_names):
        try:
            # Define an empty DataFrame with the specified columns
            columns = [
                "Cell Name",
                "Cycle Rotation number",
                "Cycle type",
                "Time (sec)",
                "Voltage (volts)",
                "Charge (mAh)",
                "Temperature (Celcius)",
            ]
            # battery_data_df = pd.DataFrame(columns=columns)
            dfs = []
            # breake_counter = 0

            for cell in cell_names:
                print(cell)
                logging.info(f"Inside Cell: {cell}")
                cycle_number_list = list(mat_data[cell].dtype.names)
                print(cycle_number_list)
                logging.info(
                    f"Inside Cell: {cell} Entir Cycle Number List: {cycle_number_list}"
                )
                for cycle_number in cycle_number_list:
                    # print(cycle_number)
                    # logging.info(f"Inside Cycle Number: {cycle_number}")
                    # Iterate through each cycle number
                    for i in range(4):
                        if i == 0:
                            cycle_type_name = "C1ch"
                        elif i == 1:
                            cycle_type_name = "C1dc"
                        elif i == 2:
                            cycle_type_name = "OCVch"
                        elif i == 3:
                            cycle_type_name = "OCVdc"
                        cycle_type = mat_data[cell][cycle_number][0][0][0][0][i]
                        # logging.info("Inside Cycle Type: " + cycle_type_name)

                        time_data = cycle_type[0][0][0].flatten().tolist()
                        voltage_data = cycle_type[0][0][1].flatten().tolist()
                        charge_data = cycle_type[0][0][2].flatten().tolist()
                        temperature_data = cycle_type[0][0][3].flatten().tolist()

                        temp_dict = {
                            "Cell Name": [cell] * len(time_data),
                            "Cycle Rotation number": [cycle_number] * len(time_data),
                            "Cycle type": [cycle_type_name] * len(time_data),
                            "Time (sec)": time_data,
                            "Voltage (volts)": voltage_data,
                            "Charge (mAh)": charge_data,
                            "Temperature (Celcius)": temperature_data,
                        }
                        # print(temp_dict)
                        df_transposed = pd.DataFrame.from_dict(
                            temp_dict, orient="index"
                        ).transpose()

                        # Append the cycle type DataFrame to the list
                        dfs.append(df_transposed)
                        # logging.info("Done with Cycle Type: " + cycle_type_name)
                    # logging.info(f"Done with Cycle Number: {cycle_number}")
                    # logging.info("------------------------------------------------")
                logging.info(f"Done with Cell: {cell}")
                logging.info(
                    "============================================================================"
                )
            battery_data_df = pd.concat(dfs, ignore_index=True)
            logging.info("Successfully converted mat data to DataFrame")
            return battery_data_df
        except Exception as e:
            logging.error(
                "Inside convert_to_dataframe function: Error converting mat data to DataFrame"
            )
            raise BatteryException("Error converting mat data to DataFrame", e)
