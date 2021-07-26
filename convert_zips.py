#!/usr/bin/env python
# coding: utf-8

# In[3]:


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


# In[4]:


crash_data = pd.read_csv('Motor_Vehicle_Collisions_-_Crashes.csv')
bike_data_or = crash_data[((crash_data['VEHICLE TYPE CODE 1'] == 'Bike')
                       |
                       (crash_data['VEHICLE TYPE CODE 2'] == 'Bike'))] #(31782, 29), bike_data_or


# In[62]:


geolocator = geopy.Nominatim(user_agent = "bike_accidents")
clean_bike_data = bike_data_or[['LATITUDE', 'LONGITUDE']].dropna()  #29465 without NA, 31782 with
clean_bike_data_nodups = bike_data_or[['LATITUDE', 'LONGITUDE']].drop_duplicates()
clean_bike_data_nodups  #16928 rows


# In[63]:


tester_df = clean_bike_data
address1 = []

thing = tester_df[0:500]
address1.extend(thing.apply(latlong_to_zip, axis=1, geolocator=geolocator, lat = 'LATITUDE', lon = 'LONGITUDE'))
add_df = pd.DataFrame(address1)

add_df.to_csv('address1.csv')


# In[17]:


## ALL TESTING - Can delete
# test_tup0 = (1.23, 2.34)
# test_tup1 = (1.11, 3.45)
# test_tup2 = (1.11, 5.67)
# test_tup3 = (1.23, 2.34)
# test_list = [test_tup0, test_tup1, test_tup2, test_tup3]
# dict_ = {}
# for item in test_list:
#     if item in dict_:
#         pass
#     else:
#         dict_[item] = item[1]
# dict_        


# index = 50
# clean_bike_data.loc[53]
# # clean_bike_data.head()

# zip_code = latlong_to_zip(clean_bike_data, geolocator = geolocator, lat = 'LATITUDE', lon = 'LONGITUDE') 
# # zip_code = latlong_to_zip(clean_bike_data.loc[index], geolocator = geolocator, lat = 'LATITUDE', lon = 'LONGITUDE') 


# In[19]:


# ## Attempt using dictionary

# zip_codes = {}
# for index, row in clean_bike_data.head(20).iterrows():
#     print(index)
# #     print(row['LATITUDE'], row['LONGITUDE'])
#     combo = (row['LATITUDE'], row['LONGITUDE'])
#     print(type(combo))
#     if combo in zip_codes:
#         pass
#     else:
#         zip_codes[combo] = latlong_to_zip(clean_bike_data, geolocator = geolocator, lat = 'LATITUDE', lon = 'LONGITUDE')

#         zip_codes[combo] = latlong_to_zip(clean_bike_data.loc[index], geolocator = geolocator, lat = 'LATITUDE', lon = 'LONGITUDE')
    
# #     latlong_to_zip(clean_bike_data, geolocator = geolocator, lat = 'LATITUDE', lon = 'LONGITUDE')
# # addresses = clean_bike_data.apply(latlong_to_zip, axis=1, geolocator=geolocator, lat = 'LATITUDE', lon = 'LONGITUDE')


# In[ ]:




