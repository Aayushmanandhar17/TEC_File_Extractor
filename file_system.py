#!/usr/bin/env python
# coding: utf-8

# In[80]:


import glob,os
import shutil
from shutil import copyfile


# In[81]:


class file_mgmt:
    def __init__(self):
        self.file_directory=None
        self.folder_list=[]
        self.destination_dir=None

    def set_file_dir(self,path):
        self.file_directory=path

    def set_destination_folder(self,destination):
        self.destination_dir=destination

    def list_folders(self):
        if self.file_directory is None:
            print("Set the folder path first")
        else:
            os.chdir(self.file_directory)
            for file in glob.glob("*"):
                self.folder_list.append(file)
        return self.folder_list

    def print_folders(self):
        if len(self.folder_list)==0:
            print("No folder in the list")
        else:
            for file in self.folder_list:
                print(file)

    def save_only_tec(self):
        if len(self.folder_list)==0:
            print("No folder in the list")
            return
        elif self.destination_dir is None:
            print("Set the destination dir first")
            return
        else:
            for file_name in self.folder_list:
                os.chdir(f"{self.file_directory}/{file_name}")
                for file in glob.glob("*TEC.txt"):
                    newPath = shutil.copy(file,self.destination_dir)
                    print(newPath)





# In[82]:


#Setting the folder home directory
#folder=file_mgmt()
#folder.set_file_dir("E:/TEC/2020TEC/")
#number of folders in the directory
#folder.list_folders()

#setting the folder destination directory
#folder.set_destination_folder("E:/TEC/2020TEC_ONLY/")
#folder.save_only_tec()


# In[ ]:
