## River masks Semi-authomatic Multi-Temporal extraction from Landsat SR images usign Google Earth Engine

Modified code from the Arctic_rivermasks branch for the use with service accounts and the auomatic dowload from drive.
For the automatic download you need to activate also the Drive API.
To authenticate the credentials are specified in the second code cell of the notebook, read below for a better understanding of the authentication process.

### Authentication process
To authenticate both Earth Engine and Drive you need to specify the name of the service account (the mail associated with it) in the ```service_account``` variable, the name of the json file where the credentials are stored in the ```credentials_file``` variable and the path of the folder where the file is stored in the ```credentials_folder```. The author used a file called ```credential_script.py``` that is placed in the same directory as the other scripts, but is not tracked on git to keep the credentials safe. In this file there is a function called ```get_credentials``` that takes no input and returns the value of this three variables. Below you will find an example of the structure.

```python
'''
script to get credentials for GEE and Google Drive
'''

def get_credentials():
    # credentials
    service_account    = 'service-account-email@project-domain.com' # service account name
    credentials_folder = '<path\\to\\folder\\with\\credentials\\file\\>' # folder where the credentials are stored
    credentials_file   = '<credential_file_name>.json' # credentials file name
    return service_account, credentials_folder, credentials_file
```

### input data import
To avoid modifying the main code every time the input data was moved to an external function that is not tracked in git, like the credentia function. The file need to be named ```input_data.py``` and contain a function ```get_input_data``` which will return data needed, below you will find an example of the structure.

```python
def get_input_data():
    # specify the input data
    river_name    = 'Kuk' # river name
    source        = 'ls'  # specify the satellite data: 'ls' for Landsat or 's2' for Sentinel-2
    scaledLS      = True  # specify if you want to analyse also the sentinel-2 data with a PM filter with a kernel equal to the Landsat one
    print_errors  = True  # specify if you want to print the errors during the mask extraction
    delete_other  = False # specify if you want to delete other folders in google drive
    download_wait = 30    # specify the time to wait for checks if task are running

    coordinates = [[[-159.2000, 70.0365],
                    [-159.0765, 70.2179],
                    [-159.6402, 70.1556],
                    [-159.7777, 70.0919],
                    [-159.2000, 70.0365]]] # coordinates of the area to investigate

    EPSG_code = 'EPSG:32604' # EPSG code for the projection of the results

    dates = [1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993,
             1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
             2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013,
             2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023] # years to be analysed
    
    return river_name, source, scaledLS, print_errors, delete_other, download_wait, coordinates, EPSG_code, dates
```