import pandas as pd
import time
import json
from Controller import UDP_Controller

# Read config file
f = open('config.json')
config = json.load(f)
print(config)
    
def read_data(filename='data.csv', debug:bool=False):
    global config
    print(config)
    start_time = time.time()
    data = pd.read_csv(filename, low_memory=False) #  index_col=0,

    if debug:
        print("reading %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    data.dropna(axis=1, inplace=True) # Removing columns with NaN
    if debug:
        print("dropNA %s seconds ---" % (time.time() - start_time))

    start_time = time.time()
    # Convert time to datetime
    data[config["COLUMN_NAME_FOR_DATETIME"]] = pd.to_datetime(data[config["COLUMN_NAME_FOR_DATETIME"]], format='mixed')
    if debug:
        print("transform data %s seconds ---" % (time.time() - start_time))
        print(data)
    
    types = data.dtypes
    if debug:
        print(types["PV_Aluminio"])
        
    return data, types

def connect_controller(initial_values, types):
    global config
    
    _controller = UDP_Controller()
    
    for variable in config["COLUMNS_TO_SIMUMATIK"]:
        if types[variable] == "float64":
            data_type = "float"
        elif types[variable] == "int64":
            data_type = "int"
        else:
            data_type = "str"
            
        _controller.addVariable(variable, data_type, initial_values[variable])
    
    for variable in config["Variables_from_simumatik"]:
        pass
    
    _controller.start()
    
    return _controller

if __name__ == "__main__":    
    data, types = read_data("data.csv", debug=False)
    
    #controller = connect_controller(data.loc[0], types)
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
        pass
    
    _controller.start()
    
    
    for i in range(len(data)):
        print(f"Time : {i}", end="\r")
        #print(f"Time : {data.loc[i][config['COLUMN_NAME_FOR_DATETIME']]}", end="\r")
        # print(f"Time diff : {data.loc[i][config['COLUMN_NAME_FOR_DATETIME']]-data.loc[0][config['COLUMN_NAME_FOR_DATETIME']]}")
        
        # for col in config["COLUMNS_TO_SIMUMATIK"]:
        #     print(f"{col} : {type(data.loc[i][col])}")
        
        # print()
        for col in config["COLUMNS_TO_SIMUMATIK"]:
            _controller.setValue(col, data.loc[i][col])
        
        time.sleep(1e-5)
        
        # if i > 10000:
            
        #     break