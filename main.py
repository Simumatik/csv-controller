import pandas as pd
import time
import json
from Controller import UDP_Controller

# Read config file
f = open('config.json')
config = json.load(f)
# print(config)
    
def read_data(filename='data.csv', debug:bool=False):
    global config

    # Read csv file
    start_time = time.time()
    data = pd.read_csv(filename, low_memory=False) #  index_col=0,
    if debug:
        print("reading %s seconds ---" % (time.time() - start_time))

    # Removing columns with NaN
    start_time = time.time()
    data.dropna(axis=1, inplace=True) 
    if debug:
        print("dropNA %s seconds ---" % (time.time() - start_time))

    # Drop columns that is not used
    start_time = time.time()
    data = data.filter(config["COLUMNS_TO_SIMUMATIK"])
    if debug:
        print("dropColumns %s seconds ---" % (time.time() - start_time))

    # Convert time to datetime
    start_time = time.time()
    data[config["COLUMN_NAME_FOR_DATETIME"]] = pd.to_datetime(data[config["COLUMN_NAME_FOR_DATETIME"]], dayfirst=True)
    if debug:
        print("transform data %s seconds ---" % (time.time() - start_time))

    # Include timedelta for all lines
    start_time = time.time()
    data['time_delta'] = data["Fecha envio"] - data["Fecha envio"].shift()
    if debug:
        print("transform data %s seconds ---" % (time.time() - start_time))

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
    
    for variable in config["Variables_from_simumatik"]:
        _controller.addVariable(variable, "float", 0)
    
    _controller.start()
    return _controller

if __name__ == "__main__":    
    data, types = read_data("data.csv", debug=True)

    _controller = connect_controller(data.loc[0], types)
    
    while _controller.getValue("emulation_time") == 0.0:
        print("Waiting for simulation model to connect...", end="\r")
        time.sleep(1)
    print()

    for i in range(len(data)-1):
        for col in config["COLUMNS_TO_SIMUMATIK"]:
            _controller.setValue(col, data.loc[i][col])
        
        # Read values from Simumatik:
        time_relation = _controller.getValue("time_relation")
        emulation_time = _controller.getValue('emulation_time')

        # calculate time to sleep
        if time_relation > 0:
            delta = data.loc[i+1]['time_delta'] / time_relation
            delta = delta.seconds + delta.microseconds/1000000
            print(f"Time : {emulation_time}, line: {i}, delta: {delta}                 ", end="\r")  
            time.sleep(delta)

    print("\nAll lines read.")
