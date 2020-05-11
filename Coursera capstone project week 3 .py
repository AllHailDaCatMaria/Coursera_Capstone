#!/usr/bin/env python
# coding: utf-8

# 1. Import Beautifulsoup and other libraries

# In[219]:


pip install beautifulsoup4


# In[220]:


pip install lxml


# In[221]:


pip install requests


# In[222]:


#Import libraries
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

#Import folium 
get_ipython().system('conda install -c conda-forge folium=0.5.0 --yes')
import folium

print('Folium installed and imported!')


# In[223]:


#Request for data
url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
toronto_doc = requests.get(url).text
soup = BeautifulSoup(toronto_doc,'lxml')
print(soup.prettify())


# In[224]:


#Locate the table that is stored at <table class="wikitable sortable">
wikitable = soup.find('table', class_='wikitable')
print(wikitable.prettify())


# In[225]:


#Get the column names, which are stored at <tr><th>
toronto_col = []
for tr in wikitable.find_all('tr'):
    for th in tr.find_all('th'):
        toronto_col.append(th.text)
toronto_col


# In[226]:


#Clean the column names by replacing all '\n' with ''
toronto_col_clean = []
for i in range(len(toronto_col)):
    toronto_col_clean.append(toronto_col[i].replace('\n',''))
print(toronto_col_clean)


# In[227]:


#Get the table values, which are stored at <tr><td>
toronto_pc=[]
for tr in wikitable.find_all('tr'):
    for td in tr.find_all('td'):
        toronto_pc.append(td.text)
toronto_pc


# In[228]:


#Similarly, clean the table values by replacing all '\n' with ''
toronto_pc_clean=[]
for i in range(len(toronto_pc)):
    toronto_pc_clean.append(toronto_pc[i].replace('\n',''))
print(toronto_pc_clean)


# In[229]:


#Change the list to np.array, then change the size to match the shape of the original table
toronto_pc_array = np.array(toronto_pc_clean)
toronto_pc_array.resize(int(len(toronto_pc_clean)/3),3)
toronto_pc_array


# In[230]:


#Create a DataFrame from the resized array
df = pd.DataFrame(toronto_pc_array, columns = toronto_col_clean)
df.head(20)


# In[231]:


#Select all existing Boroughs
df = df[df.Borough != 'Not assigned']
df.head(20)


# In[232]:


#Check to see if any Neighborhoods are 'Not assigned' or empty
print(df[df.Neighborhood.isin(['Not assigned',''])])


# In[233]:


#None of the Neighborhoods have missing values, but if there are any, I can use the follwing code to replace them
df['Neighborhood'] = df['Neighborhood'].replace('Not assigned', np.nan).ffill()
for row in range(df.shape[0]):
    if df.iloc[row,2] == 'NaN':
        df.iloc[row,2] = df.iloc[row,0]


# In[234]:


#Check the shape
print(df.shape)


# In[235]:


#Download coordinates
lat_lng_coords = pd.read_csv('http://cocl.us/Geospatial_data')
lat_lng_coords


# In[236]:


#merge df with coordinates
df_coord = pd.merge(df,lat_lng_coords,on='Postal Code')


# In[237]:


df_coord.head()


# In[245]:


# create map and display it
sanfran_map = folium.Map(location=[43.6532,-79.3832], zoom_start=12)

# display the map of San Francisco
sanfran_map


# In[246]:


# instantiate a feature group for the incidents in the dataframe
incidents = folium.map.FeatureGroup()

# loop through the 100 crimes and add each to the incidents feature group
for lat, lng, in zip(df_coord.Latitude, df_coord.Longitude):
    incidents.add_child(
        folium.features.CircleMarker(
            [lat, lng],
            radius=5, # define how big you want the circle markers to be
            color='yellow',
            fill=True,
            fill_color='blue',
            fill_opacity=0.6
        )
    )
 
# add incidents to map
sanfran_map.add_child(incidents)
sanfran_map


# In[ ]:




