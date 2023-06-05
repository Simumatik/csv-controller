# csv-controller
Used to control a Simumatik model through read data in a CSV-file.

The script operates as follos: 
* Opens a csv-file with the Panda library, sorts and cleans the data. 
* Starts a UDP Server, connecting to the Simumatik Gateway
* Adds variables to be read from csv file to the gateway (the variable represent a named column in the csv file).
* Waits until A simumatik model connects to the server. 
* Sends the data from columns defined in config.json to the simulation model, based on time_relation setting recieved from Simumatik model and the date time column.
* Closes UDP server when all lines in CSV has been sent.  

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
    "COLUMN_NAME_FOR_DATETIME" : "Fecha envio",
    "COLUMNS_TO_SIMUMATIK" : ["Fecha envio", "SP_Aluminio", "PV_Aluminio", "Kilos total lingotes", "Total escorias"],
    "Variables_from_simumatik" : ["emulation_time", "time_relation"]   
}
```