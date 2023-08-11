# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:16:59 2023

@author: cvskf
"""

import urllib
import urllib.request
import json
import os
import zipfile
import sqlite3
import importlib.resources as pkg_resources
import ogp_functions
import subprocess
from datetime import datetime
import pandas as pd
import csv
from lxml import etree
from bs4 import BeautifulSoup


_default_data_folder='_data'  # the default


#%% data folder


def update_data_files(
        data_folder=_default_data_folder,
        latest_data_file_info_download_url=r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/latest_data_file_info.json'
        ):
    """
    """
    
    # download latest data file info
    _update_latest_data_file_info(
        data_folder,
        latest_data_file_info_download_url
        )
    
    # open latest data file info
    latest_data_file_info=\
        _get_latest_data_file_info_json(
                data_folder
                )
    
    # update data files
    for x in latest_data_file_info:
        
        metadata_download_url=x['metadata_download_url']
        
        metadata_xml=\
            get_metadata_xml(
                metadata_download_url
                )
    
        metadata_dict=\
            parse_metadata_xml(
                metadata_xml
                )
        
        print(metadata_dict)



def _update_latest_data_file_info(
        data_folder=_default_data_folder,
        download_url=r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/latest_data_file_info.json'
        ):
    """
    # download the latest data file information from GitHub

    # - the file on GitHub can be updated as new data files are released
    #   on the Open Geography Portal website.
    
    # saves the file in the 'data_folder'
    
    
    """

    urllib.request.urlcleanup()
    
    fp=os.path.join(data_folder,'latest_data_file_info.json')

    urllib.request.urlretrieve(
        url=download_url, 
        filename=fp
        )
    

def _get_latest_data_file_info_json(
        data_folder=_default_data_folder,
        ):
    """
    # download the latest data file information from GitHub

    # - the file on GitHub can be updated as new data files are released
    #   on the Open Geography Portal website.
    
    """
    fp=os.path.join(data_folder,'latest_data_file_info.json')
    
    with open(fp) as f:
        latest_data_file_info=json.load(f)
        
    return latest_data_file_info
        


def get_metadata_xml(
        download_url
        ):
    """
    
    returns XML -> a lxml.etree root node (element)
    
    """
    
    urllib.request.urlcleanup()
    
    with urllib.request.urlopen(download_url) as url:
        print(url.read())
        root = etree.fromstring(url.read())
        
    return root
    

def parse_metadata_xml(
        root
        ):
    """
    """

    d=dict(
        title=root.xpath('dataIdInfo/idCitation/resTitle')[0].text,
        creation_date=root.xpath('dataIdInfo/idCitation/date/createDate')[0].text,
        publication_date=root.xpath('dataIdInfo/idCitation/date/pubDate')[0].text,
        id_code=root.xpath('dataIdInfo/idCitation/citId/identCode')[0].text,
        abstract=BeautifulSoup(root.xpath('dataIdInfo/idAbs')[0].text, "lxml").text,
        purpose=root.xpath('dataIdInfo/idPurp')[0].text
        )

    d['fieldnames']=[x.strip() for x in d['abstract'].split('Field Names -')[1].split('Field Types -')[0].split(',')]
    d['fieldtypes']=[x.strip() for x in d['abstract'].split('Field Types -')[1].split('Field Lengths -')[0].split(',')]
    d['description']=d['abstract'].split('(File Size -')[0].strip()


    return d
    
    
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
        
    # # download files
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
            
    # create changes table in database
    _create_changes_table(
        fp_database=_get_fp_database()
        )
    
    # create changehistory table in database
    _create_changehistory_table(
        fp_database=_get_fp_database()
        )

    




def load_data(
        data_folder=_default_data_folder
        ):
    """
    """
    d={}
    
    # Changes.csv
    
    fp=os.path.join(data_folder,'Changes.csv')
    
    with open(fp,encoding='utf-8-sig') as f:
        
        csvreader=csv.DictReader(f)
        
        for row in csvreader:
            
            geogcd=row['GEOGCD']
            geogcd_p=row['GEOGCD_P']
            
            x=d.setdefault(geogcd,{})
            y=x.setdefault('changes',[])
            y.append(row)
            
            x=d.setdefault(geogcd_p,{})
            y=x.setdefault('__next__',[])
            y.append(geogcd)
    
    # ChangeHistory.csv
    
    fp=os.path.join(data_folder,'ChangeHistory.csv')
    
    with open(fp,encoding='utf-8-sig') as f:
        
        csvreader=csv.DictReader(f)
        
        for row in csvreader:
            
            geogcd=row['GEOGCD']
            parentcd=row['PARENTCD']
            
            x=d.setdefault(geogcd,{})
            y=x.setdefault('changehistory',[])
            y.append(row)
            
            x=d.setdefault(parentcd,{})
            y=x.setdefault('__children__',[])
            y.append(geogcd)
    
    
    return d
    


def get_previous_codes(code,data):
    ""
    return [x['GEOGCD_P'] for x in data[code]['changes']]


def get_next_codes(code,data):
    ""
    return data[code].get('__next__',[])


def get_latest_codes(code,data):
    """
    """
    result=set()
    
    def _get_next_codes(
            result,
            codes,
            data):
        
        for code in codes:
            
            x=get_next_codes(code,data)  # a list of codes
            
            result.update(x)
            
            result = _get_next_codes(result,x,data)
            
        return result
    
    result =  _get_next_codes(result,[code],data)
    
    return list(result)


def get_parent_codes(
        code,
        data
        ):
    """
    """
    return [x['PARENTCD'] for x in data[code]['changehistory']
            if x['PARENTCD']!='']


def get_child_codes(code,data):
    ""
    return data[code].get('__children__',[])

def get_ancestor_codes(
        code,
        data
        ):
    """
    """
    result=set()
    
    def _get_parent_codes(
            result,
            codes,
            data
            ):
        
        for code in codes:
            
            x=get_parent_codes(code,data)  # a list of codes
            
            result.update(x)
            
            result = _get_parent_codes(result,x,data)
            
        return result
    
    result =  _get_parent_codes(result,[code],data)
    
    return list(result)


def get_descendent_codes(
        code,
        data
        ):
    """
    """
    result=set()
    
    def _get_child_codes(
            result,
            codes,
            status):
        
        for code in codes:
            
            x=get_child_codes(code,data)  # a list of codes
                            
            result.update(x)
            
            result = _get_child_codes(result,x,data)
            
        return result
    
    result =  _get_child_codes(result,[code],data)
    
    return list(result)




#%% read metadata files

# Changes-schema-metadata.json
fp=os.path.join(
    pkg_resources.files(ogp_functions),
    'Changes-schema-metadata.json'
    )
with open(fp) as f:
    changes_schema_metadata=json.load(f)

# ChangeHistory-schema-metadata.json
fp=os.path.join(
    pkg_resources.files(ogp_functions),
    'ChangeHistory-schema-metadata.json'
    )
with open(fp) as f:
    changehistory_schema_metadata=json.load(f)



class OGPdata():
    """
    """
    
    def __init__(
            self,
            data_folder='_data'
        ):
        """
        """
        self.data_folder=data_folder
        
        self.df_changes=self._load_changes_dataframe()
        #print(self._df_changes)
        
        self.df_changehistory=self._load_changehistory_dataframe()
        
        
        
        

    def _load_changes_dataframe(self):
        ""
        fp=os.path.join(self.data_folder,'Changes.csv')
        return pd.read_csv(fp)
        
    
    def _load_changehistory_dataframe(self):
        ""
        fp=os.path.join(self.data_folder,'ChangeHistory.csv')
        return pd.read_csv(fp)


    def get_previous_codes(self,code):
        """Returns the previous codes of a code change.
        """
        
        return self.df_changes[self.df_changes.GEOGCD==code].GEOGCD_P.dropna().to_list()
    
    def get_next_codes(self,code):
        """
        """
        
        return self.df_changes[self.df_changes.GEOGCD_P==code].GEOGCD.dropna().to_list()
        
        
    def get_latest_codes(self,code):
        """
        """
        result=set()
        
        def _get_next_codes(
                result,
                codes):
            
            for code in codes:
                
                x=self.get_next_codes(code)  # a list of codes
                
                result.update(x)
                
                result = _get_next_codes(result,x)
                
            return result
        
        result =  _get_next_codes(result,[code])
        
        return list(result)
    
    
    def get_parent_codes(
            self,
            code,
            status='live'  # 'live' or 'terminated' or none 
            ):
        """
        """
        
        if status is None:
            
            mask = self.df_changehistory.GEOGCD==code
            
        else:
            
            mask = (self.df_changehistory.GEOGCD==code) & (self.df_changehistory.STATUS==status)
            
        result = self.df_changehistory[mask].PARENTCD.dropna().to_list()
            
        return result
    
    
    def get_ancestor_codes(
            self,
            code,
            status='live'  # 'live' or 'terminated' or none 
            ):
        """
        """
        result=set()
        
        def _get_parent_codes(
                result,
                codes,
                status):
            
            for code in codes:
                
                x=self.get_parent_codes(code,status)  # a list of codes
                
                result.update(x)
                
                result = _get_parent_codes(result,x,status)
                
            return result
        
        result =  _get_parent_codes(result,[code],status)
        
        return list(result)
       
        
    def get_child_codes(
            self,
            code,
            status='live'  # 'live' or 'terminated' or none 
            ):
        """
        """
      
        if status is None:
            
            mask = self.df_changehistory.PARENTCD==code
            
        else:
            
            mask = (self.df_changehistory.PARENTCD==code) & (self.df_changehistory.STATUS==status)
            
        result = self.df_changehistory[mask].GEOGCD.dropna().to_list()
            
        return result
       

    def get_descendent_codes(
            self,
            code,
            status='live'  # 'live' or 'terminated' or none 
            ):
        """
        """
        result=set()
        
        def _get_child_codes(
                result,
                codes,
                status):
            
            for code in codes:
                
                if code[1:3]=='00':
                    continue
                
                x=self.get_child_codes(code,status)  # a list of codes
                                
                result.update(x)
                
                result = _get_child_codes(result,x,status)
                
            return result
        
        result =  _get_child_codes(result,[code],status)
        
        return list(result)



#%% database functions

def _get_fp_database():
    ""
    return os.path.join(_default_data_folder,'ogp.sqlite')


def _check_if_table_exists_in_database(
        fp_database,
        table_name
        ):
    ""
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query=f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        return True if c.execute(query).fetchall()[0][0] else False
    


def _create_changes_table(
        fp_database,
        verbose=True
        ):
    """Creates a changes table in the sqlite database.
    
    Replaces any existing 'changes' table.
    
    """
    
    # drop table in database
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query='DROP TABLE IF EXISTS changes;'
        c.execute(query)
        conn.commit()
    
    # create query
    datatype_map={
    'integer':'INTEGER',
    'decimal':'REAL'
    }
    query='CREATE TABLE changes ('
    for column_dict in changes_schema_metadata['columns']:
        name=column_dict['name']
        datatype=datatype_map.get(column_dict['datatype']['base'],'TEXT')
        query+=f"{name} {datatype}"
        query+=", "
    query=query[:-2]
    query+=');'
    
    if verbose:
        print('---QUERY TO CREATE TABLE---')
        print(query)
    
    # create empty table in database
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        
    # create indexes
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query="CREATE INDEX index_changes_GEOGCD ON changes(GEOGCD)"
        c.execute(query)
        query="CREATE INDEX index_changes_GEOGCD_P ON changes(GEOGCD_P)"
        c.execute(query)
        conn.commit()
        
    # import data into table
    fp_database2=fp_database.replace('\\','\\\\')
    fp_csv=os.path.join(_default_data_folder,'Changes.csv')
    fp_csv2=fp_csv.replace('\\','\\\\')
    command=f'sqlite3 {fp_database2} -cmd ".mode csv" ".import --skip 1 {fp_csv2} changes"'
    if verbose:
        print('---COMMAND LINE TO IMPORT DATA---')
        print(command)
    subprocess.run(command)
    if verbose:
        print('Number of rows after import: ', _get_row_count_in_database_table(fp_database,'changes'))
    
    
def _create_changehistory_table(
        fp_database,
        verbose=True
        ):
    """Creates a changehistory table in the sqlite database.
    
    Replaces any existing 'changehistory' table.
    
    """
    
    # drop table in database
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query='DROP TABLE IF EXISTS changehistory;'
        c.execute(query)
        conn.commit()
    
    # create query
    datatype_map={
    'integer':'INTEGER',
    'decimal':'REAL'
    }
    query='CREATE TABLE changehistory ('
    for column_dict in changehistory_schema_metadata['columns']:
        name=column_dict['name']
        datatype=datatype_map.get(column_dict['datatype']['base'],'TEXT')
        query+=f"{name} {datatype}"
        query+=", "
    query=query[:-2]
    query+=');'
    
    if verbose:
        print('---QUERY TO CREATE TABLE---')
        print(query)
    
    # create empty table in database
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        
    # create indexes
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query="CREATE INDEX index_changehistory_GEOGCD ON changehistory(GEOGCD)"
        c.execute(query)
        query="CREATE INDEX index_changehistory_PARENTCD ON changehistory(PARENTCD)"
        c.execute(query)
        query="CREATE INDEX index_changehistory_STATUS ON changehistory(STATUS)"
        c.execute(query)
        conn.commit()
        
    # import data into table
    fp_database2=fp_database.replace('\\','\\\\')
    fp_csv=os.path.join(_default_data_folder,'ChangeHistory.csv')
    fp_csv2=fp_csv.replace('\\','\\\\')
    command=f'sqlite3 {fp_database2} -cmd ".mode csv" ".import --skip 1 {fp_csv2} changehistory"'
    if verbose:
        print('---COMMAND LINE TO IMPORT DATA---')
        print(command)
    subprocess.run(command)
    if verbose:
        print('Number of rows after import: ', _get_row_count_in_database_table(fp_database,'changehistory'))
    
    
    
        
def _get_row_count_in_database_table(
        fp_database,
        table_name,
        column_name='*'
        ):
    """Gets number of rows in table
    
    """
    with sqlite3.connect(fp_database) as conn:
        c = conn.cursor()
        query=f'SELECT COUNT({column_name}) FROM {table_name}'
        return c.execute(query).fetchone()[0]
    




    
#%% main functions

# def _convert_date_string_to_python_datetime(
#         date_string
#         ):
#     ""
#     return datetime.strptime(date_string,'%d/%m/%Y')



    
# def get_next_code(code):
#     """
#     """
#     with sqlite3.connect(_get_fp_database()) as conn:
#         c = conn.cursor()
#         query=f"""
#             SELECT 
#                 GEOGCD, OPER_DATE
#             FROM
#                 changes
#             WHERE
#                 GEOGCD_P = "{code}"
#             """
            
#         result=[(x[0],_convert_date_string_to_python_datetime(x[1])) 
#                  for x in c.execute(query).fetchall()]
        
#         if len(result)==0:
            
#             raise ValueError('Code does not have a next code')
            
#         elif len(result)>1:
            
#             raise Exception('...wasnt execting a result of more that one item here...???')
            
#         else:
            
#             return result[0]
    

# def get_latest_code(code):
#     """
#     """
#     while True:
        
#         try:
            
#             next_code = get_next_code(code)
            
#         except ValueError:
            
#             return code
        
#         code = next_code


# def get_parent_codes(
#         code,
#         status='live'  # 'live' or 'terminated' or none 
#         ):
#     """
#     """
   
    
#     with sqlite3.connect(_get_fp_database()) as conn:
#         c = conn.cursor()
        
#         query=f"""
#             SELECT 
#                 PARENTCD
#             FROM
#                 changehistory
#             WHERE
#                 GEOGCD = "{code}"
#             """
                
#         if not status is None:
            
#             query+=f""" 
#                  AND STATUS="{status}"
#                 """
            
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#         return result
    
    
# def get_child_codes(
#         code,
#         status='live'  # 'live' or 'terminated' or none 
#         ):
#     """
#     """
   
    
#     with sqlite3.connect(_get_fp_database()) as conn:
#         c = conn.cursor()
        
#         query=f"""
#             SELECT 
#                 GEOGCD
#             FROM
#                 changehistory
#             WHERE
#                 PARENTCD = "{code}"
#             """
                
#         if not status is None:
            
#             query+=f""" 
#                  AND STATUS="{status}"
#                 """
            
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#         return result
    
    
# def get_ancestor_codes(
#         code,
#         status='live'  # 'live' or 'terminated' or none 
#         ):
#     """
#     """
#     result=set()
    
#     def _get_parent_codes(
#             result,
#             codes,
#             status):
        
#         for code in codes:
            
#             x=get_parent_codes(code,status)  # a list of codes
            
#             result.update(x)
            
#             result = _get_parent_codes(result,x,status)
            
#         return result
    
#     result =  _get_parent_codes(result,[code],status)
    
#     return result


# def get_descendent_codes(
#         code,
#         status='live'  # 'live' or 'terminated' or none 
#         ):
#     """
#     """
#     result=set()
    
#     def _get_child_codes(
#             result,
#             codes,
#             status):
        
#         for code in codes:
            
#             x=get_child_codes(code,status)  # a list of codes
            
#             result.update(x)
            
#             result = _get_parent_child(result,x,status)
            
#         return result
    
#     result =  _get_parent_codes(result,[code],status)
    
#     return result







