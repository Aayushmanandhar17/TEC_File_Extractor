import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from dateutil import parser
import datetime
from dateutil import parser


class tec_plot:
    def __init__(self):
        self.df=None
        self.day_tec=[]
    def set_df(self, df):
        self.df=df

    def convert_datetime(self):
        date_list=np.array(self.df["DATE"])
        Date=[]
        for date in date_list:
            datetime_object = parser.parse(date)
            Date.append(datetime_object)
        self.df['DATE']=Date
    def plot(self):
        plt.figure(figsize=(12,8))
        plt.title("Total Electorn Content (TEC) with respect to time", size=15, color='r')
        plt.xlabel("Date",size=10)
        plt.ylabel("TEC",size=10)
        ax=plt.gca()
        self.df.plot(kind='line', x='DATE', y='TEC',ax=ax)
        plt.show()

    def basic_plot(self):
        if self.df is None:
            print("Enter the DataFrame first")
        else:
            self.convert_datetime()
            self.plot()
