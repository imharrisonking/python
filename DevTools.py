'''
This module contains tooling classes that aid in development and testing. For example classes that handle logging.
'''

import numpy as np
import logging
import logging.config
import json
import os
import sys
from datetime import datetime

# Define file paths
LOGGING_CONFIG_FILE_PATH = './config/logging_config.json'

class Logger:
    def __init__(self, logger_type:str):
        ''' This class configures a logger using the logging_config.json file using the dictConfig method in the logging.config library. It returns a logger object based on the logger_type parameter. For example 'mainLogger' is the standard logger configuration.
        Args:
            logger_type: the logger name as defined in the logger_config.json under "loggers" (string)
        Returns:
            A logger object
        '''
        self._logger_type = logger_type
        self._script_name = os.path.splitext(os.path.basename(sys.argv[0]))[0]
        self._time_stamp = datetime.today().strftime('%Y-%m-%d--%H-%M-%S')

        with open(LOGGING_CONFIG_FILE_PATH) as file:
            config_dict = json.load(file)
            # Dynamically change the log file name by editing the dictionary
            config_dict['handlers']['file']['filename'] = f'./log/{self._script_name}--{self._time_stamp}.log'
            logging.config.dictConfig(config_dict)

        self._logger = logging.getLogger(self._logger_type)
  
    def get_Logger(self):
        return self._logger


class FileOutputter:
    def __init__(self, export_chunk_size):
        self.chunk_Size = export_chunk_size
        self._time_stamp = datetime.today().strftime('%Y-%m-%d--%H-%M-%S')

    @property
    def time_Stamp(self):
        return self._time_stamp

    def write_Bytes(self, current_hour, value, array_name, data_type):
        ''' Function creates a new binary file if one does not already exist, then appends a 'chunk' or list of data to that binary file, opening the binary file in append mode when the new chunk has been created.
        Args:
            current_hour: the counter of the current hour of data that we're processing
            value: the data for the current hour
            array_name: string value of the name to identify the binary file when saved
            data_type: the data type of value - used for deserialising the data in .read_Bytes()
        Returns:
            a .bin timestamped file with the array name and data_type stored in the filename
        '''
        # Create unique filename storing the original data type in the name
        filename = f'./outputs/{array_name}--{data_type.__name__}--{self.time_Stamp}.bin'

        # Define the index used to access the lists created below
        i = current_hour if current_hour < self.chunk_Size else current_hour % self.chunk_Size

        # Create new lists for the first hour of the simulation
        if current_hour == 0:
            self.create_New_Chunk_Lists(type(value))

        # Allocate the current iteration to the chunk list
        self.chunk_Array[i] = value

        # Append to the binary file if at the end of the chunk
        if i == self.chunk_Size - 1 and current_hour != 0:
            with open(filename, 'ab') as file:
                    self.chunk_Array.tofile(file)

            # Reset the lists of fuel and carbon prices
            self.create_New_Chunk_Lists(type(value))                
        
    def create_New_Chunk_Lists(self, data_type):
        ''' Function creates a new chunk where the chunk is an empty numpy array of a specified data type
        Args:
            data_type: the data type of the value being processed
        Returns:
            self.chunk_Array is reset when the function is called
        '''
        self.chunk_Array = np.zeros(self.chunk_Size, data_type)

    def read_Bytes(self, filename, data_type):
        ''' Function reads a binary file and deserialises it back into a numpy array
        Args:
            filename: the file path of the binary file to be deserialised
            data_type: the orignal data type of the binary file before it was serialised
        Returns:
            A deserialised numpy array
        '''
        return np.fromfile(filename, data_type)


def main():
    # Create outputter with chunk size of 48
    outputter = FileOutputter(48)
    descriptions = {'Coal_Fuel_Prices': np.float64}

    # Create fake hourly data
    np.random.seed(0)
    coal_fuel_prices = np.random.uniform(30, 100, 144)
    print(coal_fuel_prices)
    print(len(coal_fuel_prices))

    # Output to binary file
    for current_hour, coal_fuel_price in enumerate(coal_fuel_prices):
        for array_name, data_type in descriptions.items():
            outputter.write_Bytes(current_hour, coal_fuel_price, array_name, data_type)

    # Read the binary file
    for array_name, data_type in descriptions.items():
        filename = f'./outputs/{array_name}--{data_type.__name__}--{outputter.time_Stamp}.bin'
        deserialised_array = outputter.read_Bytes(filename, data_type)
        print(deserialised_array)
        print(len(deserialised_array))


if __name__ == '__main__':
    main()