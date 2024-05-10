from Battery import dataPreparation
from Data_Collection import matToDataframe
import os
from Battery.logger_code.logger import logging
from Battery.exception_code.exception import BatteryException

# from from_root import from_root

# from os.path import dirname, join as pjoin
# from scipy.io import sio


# File path where the .mat file is stored
# mat_file_name = "Oxford_Battery_Degradation_Dataset_1"

# Get the path to the parent directory
parent_dir_path = os.path.dirname(os.getcwd())


MAT_FILE_PATH: str = os.path.join(
    parent_dir_path,
    "Battery-Degradation-Analysis",
    "Data",
    "Oxford_Battery_Degradation_Dataset_1",
)


CSV_FILE_PATH: str = os.path.join(
    parent_dir_path,
    "Battery-Degradation-Analysis",
    "Data",
    "Battery_Degradation_Dataset.csv",
)


def run_data_conversion():

    # Class instance
    data_file_converter = matToDataframe.DataFileConverter(MAT_FILE_PATH)
    logging.info(
        "Going to load mat file by calling load_mat_file function from DataFileConverter class"
    )

    # Load the .mat file
    mat_data = data_file_converter.load_mat_file()
    logging.info("Loaded mat file")
    print("Loaded mat file")

    # Get the cell names
    cell_names = data_file_converter.find_cell_names(mat_data)

    logging.info(f"Found cell names: {cell_names}")

    # Convert the .mat file to a dataframe
    battery_data_df = data_file_converter.convert_to_dataframe(mat_data, cell_names)

    # Save the dataframe to a .csv file
    battery_data_df.to_csv(CSV_FILE_PATH, index=False)
    logging.info("Data saved to CSV file")


if __name__ == "__main__":

    # Conver the .mat file to .csv file
    run_data_conversion()

    # test if the csv file is created by loading it and printing the first 10 rows
    dataPreparation.test_dataPreparation(CSV_FILE_PATH)
    logging.info("Data Preparation Done")
