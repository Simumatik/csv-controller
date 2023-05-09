COLUMN_NAME_FOR_DATETIME = "Fecha envio"

import pandas as pd
import time

def read_data(filename='data.csv', debug:bool=False):
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
    data[COLUMN_NAME_FOR_DATETIME] = pd.to_datetime(data[COLUMN_NAME_FOR_DATETIME], format='mixed')
    if debug:
        print("transform data %s seconds ---" % (time.time() - start_time))
        print(data)
        
    return data



if __name__ == "__main__":
    data = read_data("data.csv", debug=False)
    
    
    
    for i in range(len(data)):
        print(data.loc[10])
        print(type(data.loc[10]))
        if i > 10:
            break