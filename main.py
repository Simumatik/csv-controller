COLUMN_NAME_FOR_DATETIME = "Fecha envio"
COLUMNS_TO_SIMUMATIK = ['SP_Aluminio', 'PV_Aluminio', 'Kilos total lingotes', 'Total escorias']

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
    data = read_data("data.csv", debug=True)
    
    for i in range(len(data)):
        print(f"Time : {data.loc[i][COLUMN_NAME_FOR_DATETIME]}")
        
        for col in COLUMNS_TO_SIMUMATIK:
            print(f"{col} : {data.loc[i][col]}")
        
        print()
        
        if i > 10:
            break