import pandas as pd
import time
import json
from Controller import UDP_Controller

# Read config file
f = open('config.json')
config = json.load(f)
    
def read_data(filename='data.csv', debug:bool=False):
    global config

    # Read csv file
    start_time = time.time()
    data = pd.read_csv(filename, low_memory=False) #  index_col=0,
    if debug:
        print("--- Reading data %.2s seconds ---" % (time.time() - start_time))

    # Removing columns with NaN
    start_time = time.time()
    data.dropna(axis=1, inplace=True) 
    if debug:
        print("--- DropNA %.2s seconds ---" % (time.time() - start_time))

    # Drop Query
    for query in config["DROP_QUERYS"]:
        start_time = time.time()
        data.drop(data.query(query).index, inplace=True)
        if debug:
            print(f"--- Drop '{query}' %.2s seconds ---" % (time.time() - start_time))

    # Drop columns that is not used
    start_time = time.time()
    data = data.filter(config["COLUMNS_TO_SIMUMATIK"])
    if debug:
        print("--- Drop unused columns %.2s seconds ---" % (time.time() - start_time))

    # Convert time to datetime
    start_time = time.time()
    data[config["COLUMN_NAME_FOR_DATETIME"]] = pd.to_datetime(data[config["COLUMN_NAME_FOR_DATETIME"]], dayfirst=True)
    if debug:
        print("--- Convert time to datetime %.2s seconds ---" % (time.time() - start_time))

    # Sort on Date time
    start_time = time.time()
    data.sort_values(by=config["COLUMN_NAME_FOR_DATETIME"], inplace=True, ignore_index=True)
    if debug:
        print("--- Sort by date  %.2s seconds ---" % (time.time() - start_time))

    # Include timedelta for all lines
    start_time = time.time()
    data['time_delta'] = data[config["COLUMN_NAME_FOR_DATETIME"]] - data[config["COLUMN_NAME_FOR_DATETIME"]].shift()
    if debug:
        print("--- Calculate time_delta %.2s seconds ---" % (time.time() - start_time))

    # Determine data types
    types = data.dtypes

    if debug:
        print(data)
        
    return data, types

def connect_controller(initial_values, types):
    _controller = UDP_Controller()
    
    for variable in config["COLUMNS_TO_SIMUMATIK"]:
        if types[variable] == "float64":
            data_type = "float"
        elif types[variable] == "int64":
            data_type = "int"
        else:
            data_type = "str"
            
        _controller.addVariable(variable, data_type, 0)
    
    for variable in config["VARIABLES_FROM_SIMUMATIK"]:
        _controller.addVariable(variable, "float", 0)
    
    _controller.start()
    return _controller

if __name__ == "__main__":    
    data, types = read_data(config["FILENAME"], debug=True)

    _controller = connect_controller(data.loc[0], types)
    
    while _controller.getValue('emulation_time') == 0.0:
        print("Waiting for simulation model to connect...", end="\r")
        time.sleep(0.1)
    print("\nSimulation Model Connected")
    emulation_time = _controller.getValue('emulation_time')

    while True:
        last_pause_check = time.time()
        for i in range(len(data)-1):
            # Send values to Simumatik
            for col in config["COLUMNS_TO_SIMUMATIK"]:
                _controller.setValue(col, data.loc[i][col]) 

            # Check to see if simulation model paused.
            if time.time() - last_pause_check > 1:
                last_pause_check = time.time()
                new_time = _controller.getValue('emulation_time')
                if new_time == emulation_time:
                    while new_time == emulation_time:
                        print("---- Simulation model paused ----                     ", end="\r")
                        time.sleep(0.1)
                        new_time = _controller.getValue('emulation_time')
                    if new_time < emulation_time:
                        print("\nSimulation restarted")
                        break
                    else: 
                        print("\nSimulation resumed")
                emulation_time = new_time

            # Calculate time to sleep
            time_relation = _controller.getValue("time_relation")
            if time_relation > 0:
                delta = data.loc[i+1]['time_delta'] / time_relation
                delta = delta.seconds + delta.microseconds/1000000
                print(f"Time : {emulation_time}, line: {i}, delta: {delta}                 ", end="\r")  

                time.sleep(delta)
            else:
                print(f"Line: {i}                                                          ", end="\r")  

            if i == len(data)-1:
                print("All lines read.")
