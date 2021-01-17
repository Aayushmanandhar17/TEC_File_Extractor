import file_tec_extractor
import earthquake_analysis as eq
import matplotlib.pyplot as plt
import pandas as pd
import os


my_analysis=eq.TEC_analysis()
# input Latitude and Longitude
my_analysis.set_lat_lon(35,-117)
#input file location where all the *TEC.txt files are located
my_analysis.set_dir_name("E:/TEC/2020TEC_ONLY/")
#Go through all the files and extract the entered location TEC DataFrame
if os.path.exists("TEC_data.csv"):
    print("Check the TEC_data.csv file in the folder ")
else:
    my_analysis.iterate_dir()
#save the TEC data into a csv files
    my_analysis.convert_csv()

df=pd.read_csv("TEC_data.csv")
plt.plot(df["TEC"])
plt.show()
