# csv-controller
Used to control a Simumatik model through read data in a CSV-file.

The script operates as follows: 
* Opens a csv-file with the Panda library, sorts and cleans the data. 
* Starts a UDP Server, connecting to the Simumatik Gateway
* Adds variables to be read from csv file to the gateway (the variable represent a named column in the csv file).
* Waits until A simumatik model connects to the server. 
* Sends the data from columns defined in config.json to the simulation model, based on time_relation setting recieved from Simumatik model and the date time column.

## Set-up
Install the needed libraries:
```terminal
pip install -r requirements
```
The script is developed and tested in Python 3.10.9 64-Bit

## Configurations
Edit the config.json to include different csv columns, edit which column includes a timestamp or add more variables to be read from Simumatik.
```json
{
    "FILENAME" : "example_data.csv", 
    "COLUMN_NAME_FOR_DATETIME" : "Timestamp",
    "COLUMNS_TO_SIMUMATIK" : ["Timestamp", "Set Point A", "Process Value A"],
    "VARIABLES_FROM_SIMUMATIK" : ["emulation_time", "time_relation"],   
    "DROP_QUERYS" : [" `Machine`!='A' "]
}
```