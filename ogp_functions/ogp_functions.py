# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:16:59 2023

@author: cvskf
"""

import urllib.request
import json
import os
import zipfile


#%% data folder

_default_data_folder='_data'  # the default


def get_latest_data_file_info():
    """
    #%% download the latest data file information from GitHub

    # - the file on GitHub can be updated as new data files are released
    #   on the Open Geography Portal website.
    
    """
    
    download_url=r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/latest_data_file_info.json'

    with urllib.request.urlopen(download_url) as url:
        latest_data_file_info=json.load(url)

    return latest_data_file_info

    
    
def download_latest_data_files(
        data_folder=_default_data_folder
        ):
    """
    """
    
    # get latest data file into from GitHub
    latest_data_file_info=get_latest_data_file_info()
    
    # create the data folder if it doesn't exist
    if not os.path.exists(data_folder):
        
        os.makedirs(data_folder)
        
    # save latest data file info
    with open(os.path.join(data_folder,'latest_data_file_info.json'),'w') as f:
        
        json.dump(latest_data_file_info,f,indent=4)
        
    # download files
    for file_info in latest_data_file_info:
        
        download_url = file_info['download_url']  # str
        zip_file = file_info.get('zip_file',False)  # boolean
        
        if zip_file:
            
            data_files = file_info['data_files']  # a list
            
            # download zip file
            urllib.request.urlretrieve(
                url=download_url, 
                filename='_temp.zip'
                )
            
            # extract single files from zip file
            with zipfile.ZipFile('_temp.zip') as z:
                
                for data_file in data_files:
                
                    with open(os.path.join(data_folder,data_file), 'wb') as f:
                        
                        f.write(z.read(data_file))
            
            # remove temporary zip file
            os.remove('_temp.zip')
            
        else:
            
            # download single files
            
            data_file = file_info['data_file']
            
            urllib.request.urlretrieve(
                url=download_url, 
                filename=data_file
                )
            
    
#%% main functions

def get_replacement_code(code):
    """
    """
    
    
    










