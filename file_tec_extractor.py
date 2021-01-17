import pandas as pd
import json
import numpy as np
from dateutil import parser
import cartopy.crs as ccrs
import datetime
from dateutil import parser
import matplotlib.pyplot as plt
import cartopy.feature as cf
import cartopy.io.shapereader as shpr
import os,glob
import matplotlib.pyplot as plt

class Noaa:
    ## Constructor
    ## Only takes in the name of the file
    def __init__(self,file_name):
        self.file_name=file_name
        self.list=self.open_file()
         #Using the list data the start and end date is stored in start and end variable
        self.start,self.end=self.date_time_iso()
        self.TEC_Data=self.convert_list()
        self.column=self.set_column()
        self.df=self.convert_dataframe()
        self.array=self.convert_numpyArray()
        self.json=self.convert_json()


    ## Extract the data from the file
    ## The data that is being extracted is converted into a list
    ## Returns the list
    def open_file(self):
        list=[]
        file=open(self.file_name,"r")
        for line in file:
            list.append(line)
        return list

    ## Extract the Vertical TEC data from the list
    ## The vertical TEC data is converted into integer
    ## Returns the list of vertical TEC data
    def convert_list(self):
        non_empty_string=[]
        tec_data_list=[]
        Vertical_TEC=self.list[19:70]
        for i in range(len(Vertical_TEC)):
            data_list=[]
            split=Vertical_TEC[i].split("  ")
            sorted_split=split[1:-1]
            for string in sorted_split:
                if(string!=""):
                    data_list.append(string)
            non_empty_string.append(data_list)

        #converting every element in the list to integer
        for j in range(len(non_empty_string)):
            data_list=[]
            tec_data=non_empty_string[j]
            for k in range(len(tec_data)):
                tec=int(tec_data[k])
                data_list.append(tec)
            tec_data_list.append(data_list)

        return tec_data_list

    ## Sets the longitude value
    ## column 18 from the list is the longitude value
    ## Returns the list of longitude value
    def set_column(self):
        column_list=[]
        columns=self.list[18]
        columns=columns.split(" -")
        columns=columns[:-1]
        for i in range(len(columns)):
            int_column=int(columns[i])
            column_list.append(int_column)
        return column_list

    ## Converts the list into a dataframe
    ## Returns the Dataframe
    def convert_dataframe(self):
        df=pd.DataFrame(self.TEC_Data,columns=self.column)
        df=df.set_index(self.column[0])
        return df

    ## Converts DF to numpy array
    ## Returns numpy array (2-D matrix)
    def convert_numpyArray(self):
        numpy_array=self.df.values
        return numpy_array
    ## Takes the Dataframe
    ## Converts the Dataframe into a dictionary
    ## Converts the dictionary into a Json format

    def convert_json(self):
        Dict={}
        #date=date_time_obj()
        description=" The file contains the Vertical TEC data. The TEC data is stored in 2-D matrix. Each row of the matrix represents the latitude while the column represent longitude. Example the [0][0] element of matrix represent first latitude and first longitude TEC data. [1][0] represents second latitude and first longitude TEC data "

        dictionary=self.array.tolist()
        Dict['META']={'DESCRIPTION':description,'Units':self.list[5], 'LATITUDE':np.linspace(-150, -51, self.array.shape[0]).tolist(),'LONGITUDE':np.linspace(-150, -51, self.array.shape[1]).tolist(), 'DATE':f"{self.start}-{self.end}"}
        Dict['DATA']={'TEC_DATA':dictionary}

        # Storing the data into a Json File
        with open("sample.json", "w") as outfile:
            json.dump(Dict, outfile, indent= 4)

        # Returning the Json Data
        json_object = json.dumps(Dict, indent = 4)

        return json_object

    # Generate the latitude and longiude value

    def lat_long(self):
        """Return ``lons``, ``lats`` and ``data`` """
        shape=self.array.shape
        nlats, nlons = shape
        lats = np.linspace(10, 60, nlats)
        lons = np.linspace(-150, -51, nlons)
        lons, lats = np.meshgrid(lons, lats)


        return lons, lats


    def date_time_iso(self):

        date=self.list[10].split(" ")[3:-1]
        time1=":".join([date[3][i:i+2] for i in range(0, len(date[3]), 2)])
        time2=":".join([date[5][i:i+2] for i in range(0, len(date[5]), 2)])

        date=" ".join(date)
        start_date= date[0:12]+" "+ time1
        end_date=date[0:12]+" "+time2
        ##converting string to datetime format
        start_date=parser.parse(start_date)
        end_date=parser.parse(end_date)
        ## converting to iso format
        start_date=start_date.isoformat()
        end_date=end_date.isoformat()
        return start_date,end_date
