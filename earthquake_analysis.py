#!/usr/bin/env python
# coding: utf-8

# In[108]:


import file_tec_extractor
import os,glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
import datetime
from dateutil import parser


# In[110]:


class TEC_analysis:
    def __init__(self):
        self.dir_name=None
        self.longitude=None
        self.latitude=None
        self.new_df=pd.DataFrame(columns=["DATE","TEC"])
 #setters for latitude and longitude
    def set_lat_lon(self,lat,lon):
        self.latitude=lat
        self.longitude=lon
    def set_dir_name(self,dir_name):
        self.dir_name=dir_name
    def get_df(self):
        return self.new_df
    def print_lat_lon(self):
            print(f"Latitude--> {self.latitude} ")
            print(f"Longitude--> {self.longitude}")
    def no_dir_lat_lon(self):
        if ((self.dir_name or self.longitude or self.latitude)== None):
            return True
    def convert_csv(self):
        self.new_df.to_csv('TEC_data.csv')

    def convert_datetime(self):
        date_list=np.array(self.new_df["DATE"])
        Date=[]
        for date in date_list:
            datetime_object = parser.parse(date)
            Date.append(datetime_object)
        self.new_df['DATE']=Date

    # Takes filename as parameter
    # Extracts only interested lat and lon TEC data
    # Stores it into a df
    def get_specific_TEC(self,filename):
        obj=file_tec_extractor.Noaa(filename)
        df=obj.convert_dataframe()
        df.columns=np.linspace(-150, -51, 100)
        df.index= np.linspace(10, 60, 51)
        date=obj.date_time_iso()[0]
        TEC=df[self.longitude][self.latitude]
        a_series = pd.Series([date,TEC], index = self.new_df.columns)
        self.new_df = self.new_df.append(a_series, ignore_index=True)
        return self.new_df

    # iterates over all the txt file in the directory
    # implements get_specific_TEC
    # Appends the DF with only interested TEC
    def iterate_dir(self):
        if self.no_dir_lat_lon is True:
            print("Missing dir location or latitude or longitude")
            return
        os.chdir(self.dir_name)
        for file in glob.glob("*.txt"):
            self.new_df=self.get_specific_TEC(file)
        #converts the date of the df into a datetime format
        self.convert_datetime()



#my_analysis=TEC_analysis()
#my_analysis.set_lat_lon(35,-117)
#my_analysis.set_dir_name("E:/TEC/2020TEC_ONLY/")
#my_analysis.iterate_dir()
#my_df=my_analysis.get_df()
