#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 21 17:13:19 2021

@author: julie
"""

import numpy as np
import pandas as pd
import geopandas as gpd
import geopy
import re

def latlong_to_zip(df, geolocator, lat, lon):    #https://gis.stackexchange.com/questions/352961/convert-lat-lon-to-zip-postal-code-using-python
    """
    This takes in latitude and longitude coordinates and outputs city zipcode using geopy
    arguments: latitude (float), longitude(float)
    returns: Series of location objects (zipcode is a string)
    """
    location = geolocator.reverse((df[lat], df[lon]))
    try:
        return location.raw['address']['postcode']
    except:
        # location.raw['postcode'] == ['     ']    # doesn't work
        # return location.raw['address']['postcode']
        return None
    # return location.raw['address']['postcode']


#%% Read Data

## Read Collision crash_data
crash_data = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv')
vehicle_data = pd.read_csv('Motor_Vehicle_Collisions_-_Vehicles.csv')

## Find column names
crash_columns = crash_data.columns
vehicle_columns = vehicle_data.columns

#%% Find date ranges
crash_data['CRASH DATE']     # 07/05/2012 - 04/14/2021
vehicle_data['CRASH_DATE']    # 09/07/2012 - 07/10/2021


#%% Find number of entries
crash_data.shape[0]     #1801417
vehicle_data.shape[0]     #3608515

#%% Vehicle types
crash_vehicle_types1 = crash_data['VEHICLE TYPE CODE 1'].unique()    #1260 unique types
crash_vehicle_types2 = crash_data['VEHICLE TYPE CODE 2'].unique()     #1381 unique types

#%% Trim data down to bicycle only
crash_bicycle_names = [
    'E-Bike', 
    'Bike', 
    'Scooter', 
    'Dirt Bike', 
    'SCOOTER', 
    'kick scoot', 
    'MOTOR SCOO', 
    'Minibike', 
    'DIRT BIKE', 
    'Minibike'
    ]

#%% Narrowing data down to bike data

# Selecting for all bike-like vehicles but only in vehicle type 1
bike_data_any = crash_data[crash_data['VEHICLE TYPE CODE 1'].isin(crash_bicycle_names)] #(11397, 29)

bike_data_any_or = crash_data[((crash_data['VEHICLE TYPE CODE 1'].isin(crash_bicycle_names))
                       |
                       (crash_data['VEHICLE TYPE CODE 2'].isin(crash_bicycle_names)))] #(34532, 29)
bike_data_any_and = crash_data[((crash_data['VEHICLE TYPE CODE 1'].isin(crash_bicycle_names))
                       &
                       (crash_data['VEHICLE TYPE CODE 2'].isin(crash_bicycle_names)))] #(470, 29) saved as bike_on_bike...
# This data is for BICYCLE specific rows
bike_data_or = crash_data[((crash_data['VEHICLE TYPE CODE 1'] == 'Bike')
                       |
                       (crash_data['VEHICLE TYPE CODE 2'] == 'Bike'))] #(31782, 29), bike_data_or
### Check for duplicates in above:
#bike_data_or['COLLISION_ID'].duplicated().sum()     #Is 0

# Just 'bike'
bike_data_1 = crash_data[crash_data['VEHICLE TYPE CODE 1'] == 'Bike'] #(10382, 29)
bike_data_2 = crash_data[crash_data['VEHICLE TYPE CODE 2'] == 'Bike'] #(34532, 29)


bike_data_and = crash_data[((crash_data['VEHICLE TYPE CODE 1'] == 'Bike') #418, saved as bike_data_bike_on_bike
                       &
                       (crash_data['VEHICLE TYPE CODE 2'] == 'Bike'))] 


#%% By Borough
#%%% Convert latitude and longitude to zipcode
## Create geocoder
geolocator = geopy.Nominatim(user_agent = "bike_accidents")
clean_bike_data = bike_data_or[['LATITUDE', 'LONGITUDE', 'COLLISION_ID']].dropna()  #29465 without NA, 31782 with
print(type(clean_bike_data))
clean_bike_data = clean_bike_data[1000:5000,] 
print(type(clean_bike_data))
# # clean_short_list = bike_data_and[['LATITUDE', 'LONGITUDE']].dropna()     #268
# df = bike_data_and[['LATITUDE', 'LONGITUDE']].dropna()

## retrieve zipcode
addresses = clean_bike_data.apply(latlong_to_zip, axis=1, geolocator=geolocator, lat = 'LATITUDE', lon = 'LONGITUDE')



#%%
any_by_borough = bike_data_or[['BOROUGH', 'VEHICLE TYPE CODE 1', 'VEHICLE TYPE CODE 2', 'ZIP CODE', 'NUMBER OF PERSONS KILLED']]

# bike_data_trimmed = bike_data[['CRASH DATE']][['BOROUGH']]
bike_data_trimmed = bike_data['CRASH DATE', 'BOROUGH', 'ZIP CODE', 'LATITUDE', 'LONGITUDE', 'NUMBER OF CYCLIST INJURED','NUMBER OF CYCLIST KILLED','VEHICLE TYPE CODE 1']

crash_data_ebike = crash_data['VEHICLE TYPE CODE 1' == 'E-Bike']

tmp = crash_data_ebike.values == 'E-Bike'

crash_data.shape     #Shape is (1 801 417, 29)

column_names = crash_data.columns
column_names

#%% Separate date into month and year


#%% Plot total accidents over time

#%% Load Geopandas shape file
bike_lanes_2021 = gpd.read_file('Bicycle Routes 2021/')


#%% temp test
# addresses = addresses.str.slice(stop=5)
# addresses = addresses.astype('string')
print(addresses.values.dtype)
# tmp_series = addresses.dtype
# print(tmp_series)
# tmp_series2 = (addresses.dtype != 'str')
# print(tmp_series2)


for i in addresses:
    # print(type(i))
    print(i, end="\n")
    if type(i) != str:
        print(i)
        print(type(i))
        
    # if type(i) == str: 
    #     # print('string')       
    #     print(re.findall(r"\D(\d{5})\D", i))
    # else:
    #     pass

#%%