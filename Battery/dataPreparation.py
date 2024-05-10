from Battery import dataPreparation
import pandas as pd
from Battery.logger_code.logger import logging
from Battery.exception_code.exception import BatteryException


def test_dataPreparation(csv_file_path):
    dataset = pd.read_csv(csv_file_path)
    print(dataset.head(10))
