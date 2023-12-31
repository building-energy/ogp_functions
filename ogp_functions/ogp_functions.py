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
import csvw_functions_extra
import matplotlib.pyplot as plt
import matplotlib


urllib.request.urlcleanup()

metadata_document_location = r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/ogp_tables-metadata.json'
metadata_filename = 'ogp_tables-metadata.json'

boundaries_metadata_location = r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/ogp_boundaries-metadata.json'
boundaries_metadata_filename = 'ogp_boundaries-metadata.json'

#%% data folder

def get_available_csv_file_names(
        ):
    """Returns the CSV file names of all tables in the (remote) CSVW metadata file.
    
    """
    result = \
        csvw_functions_extra.get_available_csv_file_names(
            metadata_document_location = metadata_document_location
            )
    
    return result


def download_and_import_data(
        csv_file_names = None,
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        verbose=False
        ):
    """
    """
    _download_table_group(
            data_folder = data_folder,
            csv_file_names = csv_file_names,  
            verbose = verbose
            )
    
    _import_table_group_to_sqlite(
            data_folder = data_folder,
            database_name = database_name,
            csv_file_names = csv_file_names, 
            verbose = verbose
            )
    
    
def _download_table_group(
        data_folder = '_data',
        csv_file_names = None,  
        verbose = False
        ):
    """
    """
    csvw_functions_extra.download_table_group(
        metadata_document_location = metadata_document_location,
        csv_file_names = csv_file_names,
        data_folder = data_folder,
        overwrite_existing_files = True,
        verbose = verbose
        )
        
    
def _import_table_group_to_sqlite(
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        csv_file_names = None, 
        verbose = False
        ):
    """
    """
    csvw_functions_extra.import_table_group_to_sqlite(
        metadata_filename = metadata_filename,
        csv_file_names = csv_file_names,
        data_folder = data_folder,
        database_name = database_name,
        overwrite_existing_tables = True,
        verbose = verbose
        )


def get_ogp_field_names_in_database(
        data_folder = '_data',
        database_name = 'ogp_data.sqlite'
        ):
    """
    """
    table_names = \
        get_ogp_table_names_in_database(
            data_folder = data_folder,
            database_name = database_name
            )
        
    result = {}
    for table_name in table_names:
        result[table_name] =\
            csvw_functions_extra.get_field_names(
                    table_name = table_name,
                    data_folder = data_folder,
                    database_name = database_name,
                    )
            
    return result
    
    
def get_ogp_table_names_in_database(
        data_folder = '_data',
        database_name = 'ogp_data.sqlite'
        ):
    """
    """
    
    result = \
        csvw_functions_extra.get_sql_table_names_in_database(
            data_folder = data_folder,
            database_name = database_name,
            metadata_filename = metadata_filename
            )
    
    return result


#%% boundaries data


    
def get_available_boundaries_names(
        ):
    """
    """
    request = \
        urllib.request.urlopen(
            boundaries_metadata_location
            )
    boundaries_metadata_list = json.loads(request.read().decode())
    
    names = [x['name'] for x in boundaries_metadata_list]
    
    return names
    

def download_boundaries_data(
        names = None,
        data_folder = '_data'
        ):
    """
    """
    # get names to download
    if names is None:
        names = get_available_boundaries_names()
        
    names = csvw_functions_extra.convert_to_iterator(names)
    
    # download boundaries metadata from GitHub
    fp_boundaries_metadata = \
        os.path.join(
            data_folder,
            boundaries_metadata_filename
            )
    
    urllib.request.urlretrieve(
        url = boundaries_metadata_location, 
        filename = fp_boundaries_metadata
        )
    
    # get boundaries_metadata_list
    with open(fp_boundaries_metadata) as f:
        boundaries_metadata_list = json.load(f)
    
    # download files
    for x in boundaries_metadata_list:
        
        name = x['name'] 
        
        if name in names:
            
            # geojson
            request = \
                urllib.request.urlopen(
                    x['geojson_url']
                    )
            geojson = json.loads(request.read().decode())
            
            fp_geojson = \
                os.path.join(
                    data_folder,
                    f'{name}.json'
                    )
                
            with open(fp_geojson, 'w') as f:
                json.dump(
                    geojson,
                    f,
                    indent = 4
                    )
            
            # geojson - metadata
            fp_geojson_metadata = \
                os.path.join(
                    data_folder,
                    f'{name}.json-metadata.xml'
                    )
            
            urllib.request.urlretrieve(
                url = x['metadata_url'], 
                filename = fp_geojson_metadata
                )
            
    return boundaries_metadata_list


def get_downloaded_boundaries_names(
        data_folder = '_data'
        ):
    """
    """
    boundaries_metadata_list = \
        get_boundaries_metadata_list(
            data_folder = data_folder
            )
        
    result = []
        
    for x in boundaries_metadata_list:
        
        name = x['name']
        
        fp_geojson = \
            os.path.join(
                data_folder,
                f'{name}.json'
                )
            
        if os.path.exists(fp_geojson):
            
            result.append(name)
            
    return result
    
    
def get_boundaries_metadata_list(
        data_folder = '_data'
        ):
    """
    """
    fp_boundaries_metadata = \
        os.path.join(
            data_folder,
            boundaries_metadata_filename
            )
        
    # get boundaries_metadata_list
    with open(fp_boundaries_metadata) as f:
        boundaries_metadata_list = json.load(f)
        
    return boundaries_metadata_list


def get_boundaries_geojson(
        name,
        data_folder = '_data'
        ):
    """
    """
    fp_geojson = \
        os.path.join(
            data_folder,
            f'{name}.json'
            )
    
    with open(fp_geojson) as f:
        geojson = json.load(f)
        
    return geojson


def plot_boundaries(
        name,
        cmap = None,
        color_value_map = None,
        code_name = None,
        data_folder = '_data',
        matplotlib_ax = None
        ):
    """
    """
    if cmap is None:
        cmap = matplotlib.cm.get_cmap('bone')
        
    if color_value_map is None:
        color_value_map = {}
    
    if matplotlib_ax is None:
        fig,ax=plt.subplots(1)
        ax.axis('equal')

    geojson = \
        get_boundaries_geojson(
               name = name,
               data_folder = '_data'
               )
    
    # get coordinates - as multipolygon
    for feature in geojson['features']:
        
        #print(feature['id'])
        
        if feature['geometry']['type'] == 'MultiPolygon':
            
            coordinates = feature['geometry']['coordinates']
            
        elif feature['geometry']['type'] == 'Polygon':
            
            coordinates = [feature['geometry']['coordinates']]
            
        else:
            
            raise Exception
        
        # plt coordinates
        cd = feature['properties'].get(code_name,None)
        
        for polygon in coordinates:
            
            for coordinates_list in polygon:
                
                x,y=list(zip(*coordinates_list))
                
                color_value = color_value_map.get(cd,None)
                if color_value is None:
                    color = 'white'
                else:
                    color = cmap(color)
                
                pos = ax.fill(
                    x, 
                    y,
                    color = color,
                    #color=cmap(random.uniform(0.3,1.0)),
                    edgecolor='black',
                    linewidth=0.2
                    )
            
            
        
        #break




# def get_metadata_sql_table_names(
#         data_folder=_default_data_folder
#         ):
#     """
#     """
#     return csvw_functions_extra.get_metadata_sql_table_names(
#         data_folder=data_folder,
#         metadata_filename='ogp_tables-metadata.json'
#         )


# def set_data_folder(
#         metadata_document_location=r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/ogp_tables-metadata.json', 
#         data_folder=_default_data_folder,
#         overwrite_existing_files=False,
#         database_name=_default_database_name,
#         remove_existing_tables=False,
#         csv_file_name=None,
#         verbose=False
#         ):
#     ""
    
#     # download all tables to data_folder
#     fp_metadata=\
#         csvw_functions_extra.download_table_group(
#             metadata_document_location,
#             data_folder=data_folder,
#             csv_file_name=csv_file_name,
#             overwrite_existing_files=overwrite_existing_files,
#             verbose=verbose
#             )

#     #return
        
#     # import all tables to sqlite
#     csvw_functions_extra.import_table_group_to_sqlite(
#         metadata_document_location=fp_metadata,
#         data_folder=data_folder,
#         database_name=database_name,
#         csv_file_name=csv_file_name,
#         remove_existing_tables=remove_existing_tables,
#         verbose=verbose
#         )


# def _read_metadata_table_group_dict(
#         data_folder,
#         ):
#     ""
#     fp=os.path.join(
#         data_folder,
#         'ogp_tables-metadata.json'
#         )
#     with open(fp) as f:
#         metadata_table_group_dic=json.load(f)
        
#     return metadata_table_group_dic
        

    
# #%% Local_Authority_District_to_Region functions

# def get_region_from_local_authority_district(
#         lad_code,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     table_name='Local_Authority_District_to_Region_December_2022'
    
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"""
#         SELECT
#             RGN22CD
#         FROM
#             "{table_name}"
#         WHERE
#             LAD22CD = "{lad_code}"
#         """
#         #print(query)
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#     return result


# def get_local_authority_district_from_region(
#         region_code,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     table_name='Local_Authority_District_to_Region_December_2022'
    
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"""
#         SELECT
#             LAD22CD
#         FROM
#             "{table_name}"
#         WHERE
#             RGN22CD = "{region_code}"
#         """
#         #print(query)
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#     return result
    

#%% Code_History_Database functions


def get_CHD_change_rows(
        GEOGCD = None,  # Nine digit code for the Instance (i.e. E01000001).
        GEOGNM = None,   # Name of the Instance
        GEOGNMW = None,  # Welsh name of the Instance
        GEOGCD_P = None,  # The previous nine digit code before the change.
        GEOGNM_P = None,  # The previous name before the change.
        GEOGNMW_P = None,  # The previous Welsh name before the change.
        SI_ID = None,  # Number of legislation which defines the Instance, if applicable (i.e.  Statutory Instruments)
        SI_TITLE = None,  # Name of legislation which defines the Instance, if applicable (i.e. Statutory Instruments)
        OPER_DATE = None,  # Date when the Instance came into use (usually the enforcement date of legislation which defines the instance)
        ENTITYCD = None,  # Three digit code prefix for the Entity (i.e. E01). This field is the code allocated from the Register of Geographic Codes.
        YEAR = None,  # This field refers to the year of introduction.
        table_name = 'Code_History_Database_May_2023_UK_Changes',
        fields = None,
        limit = None,
        pandas = False,
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        verbose = False
        ):
    """
    """
    
    filter_by = \
        dict(
            GEOGCD = GEOGCD,  # Nine digit code for the Instance (i.e. E01000001).
            GEOGNM = GEOGNM,   # Name of the Instance
            GEOGNMW = GEOGNMW,  # Welsh name of the Instance
            GEOGCD_P = GEOGCD_P,  # The previous nine digit code before the change.
            GEOGNM_P = GEOGNM_P,  # The previous name before the change.
            GEOGNMW_P = GEOGNMW_P,  # The previous Welsh name before the change.
            SI_ID = SI_ID,  # Number of legislation which defines the Instance, if applicable (i.e.  Statutory Instruments)
            SI_TITLE = SI_TITLE,  # Name of legislation which defines the Instance, if applicable (i.e. Statutory Instruments)
            OPER_DATE = OPER_DATE,  # Date when the Instance came into use (usually the enforcement date of legislation which defines the instance)
            ENTITYCD = ENTITYCD,  # Three digit code prefix for the Entity (i.e. E01). This field is the code allocated from the Register of Geographic Codes.
            YEAR = YEAR,  # This field refers to the year of introduction.
            )
    filter_by = {k:v for k,v in filter_by.items() if not v is None}    
    
                
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields,
            limit = limit,
            pandas = pandas,
            metadata_filename = metadata_filename,
            verbose = verbose
            )
    
    return result


def get_CHD_change_history_rows(
        GEOGCD=None,  # Nine digit code for the Instance (i.e. E01000001).
        GEOGNM=None,   # Name of the Instance
        GEOGNMW=None,  # Welsh name of the Instance
        SI_ID=None,  # Number of legislation which defines the Instance, if applicable (i.e.  Statutory Instruments)
        SI_TITLE=None,  # Name of legislation which defines the Instance, if applicable (i.e. Statutory Instruments)
        OPER_DATE=None,  # Date when the Instance came into use (usually the enforcement date of legislation which defines the instance)
        TERM_DATE=None,  # Date when the Instance was archived (usually the day before the enforcement date of legislation which defines the new instance)
        PARENTCD=None,  # Nine digit code of the parent instance in the hierarchy (if there is one).
        ENTITYCD=None,  # Three digit code prefix for the Entity (i.e. E01). This field is the code allocated from the Register of Geographic Codes.
        OWNER=None,  # Geography owner of the entity
        STATUS=None,  # States whether the Instance is live or terminated
        AREAEHECT=None,  # 'Extent of the Realm' measurement, in hectares, to 2 decimal places. 'Extent of the Realm' is typically co-incident with Mean Low Water
        AREACHECT=None,  # Area to Mean High Water, in hectares, to 2 decimal places. Measurements are limited to the Mean High Water mark and include all tracts of inland water
        AREAIHECT=None,  # Area of inland water, in hectares, to 2 decimal places. This is the surface area of inland water with a surface area measurement of more than 1km2
        AREALHECT=None,  # Area to Mean High Water excluding area of inland water (land area), in hectares, to 2 decimal places.
        table_name='Code_History_Database_May_2023_UK_ChangeHistory',
        fields = None,
        limit = None,
        pandas = False,
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        verbose=False
        ):
    """
    """
    
    filter_by = \
        dict(
                GEOGCD=GEOGCD,  # Nine digit code for the Instance (i.e. E01000001).
                GEOGNM=GEOGNM,   # Name of the Instance
                GEOGNMW=GEOGNMW,  # Welsh name of the Instance
                SI_ID=SI_ID,  # Number of legislation which defines the Instance, if applicable (i.e.  Statutory Instruments)
                SI_TITLE=SI_TITLE,  # Name of legislation which defines the Instance, if applicable (i.e. Statutory Instruments)
                OPER_DATE=OPER_DATE,  # Date when the Instance came into use (usually the enforcement date of legislation which defines the instance)
                TERM_DATE=TERM_DATE,  # Date when the Instance was archived (usually the day before the enforcement date of legislation which defines the new instance)
                PARENTCD=PARENTCD,  # Nine digit code of the parent instance in the hierarchy (if there is one).
                ENTITYCD=ENTITYCD,  # Three digit code prefix for the Entity (i.e. E01). This field is the code allocated from the Register of Geographic Codes.
                OWNER=OWNER,  # Geography owner of the entity
                STATUS=STATUS,  # States whether the Instance is live or terminated
                AREAEHECT=AREAEHECT,  # 'Extent of the Realm' measurement, in hectares, to 2 decimal places. 'Extent of the Realm' is typically co-incident with Mean Low Water
                AREACHECT=AREACHECT,  # Area to Mean High Water, in hectares, to 2 decimal places. Measurements are limited to the Mean High Water mark and include all tracts of inland water
                AREAIHECT=AREAIHECT,  # Area of inland water, in hectares, to 2 decimal places. This is the surface area of inland water with a surface area measurement of more than 1km2
                AREALHECT=AREALHECT,  # Area to Mean High Water excluding area of inland water (land area), in hectares, to 2 decimal places.
            )
    filter_by = {k:v for k,v in filter_by.items() if not v is None}    
        
    result = \
        csvw_functions_extra.get_rows(
            table_name = table_name,
            data_folder = data_folder,
            database_name = database_name,
            filter_by = filter_by,
            fields = fields,
            limit = limit,
            pandas = pandas,
            metadata_filename = metadata_filename,
            verbose = verbose
            )
    
    return result


def get_equivalent(
        ):
    """
    """
    # TO DO
    
    








# # --- old functions below ---

# def get_previous_codes(
#         code,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     table_name='Code_History_Database_May_2023_UK_Changes'
    
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"""
#             SELECT 
#                 GEOGCD_P
#             FROM
#                 "{table_name}"
#             WHERE
#                 GEOGCD = "{code}"
#             """
#         #print(query)
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#     return result


# def get_next_codes(
#         code,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     table_name='Code_History_Database_May_2023_UK_Changes'
    
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"""
#             SELECT 
#                 GEOGCD
#             FROM
#                 "{table_name}"
#             WHERE
#                 GEOGCD_P = "{code}"
#             """
#         #print(query)
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#     return result


# def get_latest_codes(
#         code,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     result=set()
    
#     def _get_next_codes(
#             result,
#             codes,
#             fp_database
#             ):
        
#         for code in codes:
            
#             x=get_next_codes(code,fp_database)  # a list of codes
            
#             result.update(x)
            
#             result = _get_next_codes(result,x,fp_database)
            
#         return result
    
#     result =  _get_next_codes(result,[code],fp_database)
    
#     return list(result)


# def get_parent_codes(
#         code,
#         data_folder=_default_data_folder,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     entity_code=\
#         get_code_entity(
#             code,
#             fp_database
#             )
        
#     if entity_code in ['E00','W00','E01','W01','E02','W02']:
    
#         table_name='OA_to_LSOA_to_MSOA_to_LAD_December_2021_v3'
        
#         metadata_table_group_dict=\
#             _read_metadata_table_group_dict(
#                 data_folder
#                 )
            
#         metadata_table_dict=[x for x in metadata_table_group_dict['tables'] 
#                              if x['https://purl.org/berg/csvw_functions/vocab/sql_table_name']['@value']==table_name][0]
            
#         for column_dict in metadata_table_dict['tableSchema']['columns']:
            
#             #print(column_dict)
            
#             column_entities=[x['@value'] for x in column_dict.get('http://www.purl.org/berg/ogp_vocab/entities',[])]
            
#             if entity_code in column_entities:
                
#                 column_name=column_dict['name']
#                 parent_name=column_dict['http://www.purl.org/berg/ogp_vocab/parent']['@value']
                
#                 break
            
#             else:
                
#                 raise Exception(f'entity_code {entity_code}')
        
#     else:
        
#         raise Exception(f'entity_code {entity_code}')
        
        
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"""
#             SELECT 
#                 {parent_name}
#             FROM
#                 "{table_name}"
#             WHERE
#                 {column_name} = "{code}"
            
#             """
#         #print(query)
#         result=[x[0] for x in c.execute(query).fetchall()]
        
#     return result
   

# def get_code_entity(
#         code,
#         fp_database=os.path.join(_default_data_folder,_default_database_name)
#         ):
#     """
#     """
    
#     table_name='Code_History_Database_May_2023_UK_Equivalents'
    
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"""
#             SELECT 
#                 ENTITYCD
#             FROM
#                 "{table_name}"
#             WHERE
#                 GEOGCD = "{code}"
#             LIMIT 1
#             """
#         #print(query)
#         result=[x[0] for x in c.execute(query).fetchall()][0]
        
#     return result
    










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



#%% NSPL_AUG_2020 functions

def get_NSPL_AUG_2020_UK_rows(
        pcd=None,
        
        ctry=None,
        data_folder = '_data',
        database_name = 'ogp_data.sqlite',
        verbose=False
        ):
    """
    """
    
    table_name='NSPL_AUG_2020_UK'
    
    where_clause=\
            csvw_functions_extra.get_where_string(
                dict(
                    pcd=pcd,  # 
                    
                    ctry=ctry,  # 
                    
                    )
                )
        
    query=f"SELECT * FROM {table_name} {where_clause};"

    result=\
        csvw_functions_extra.run_sql(
            sql_query=query, 
            data_folder=data_folder, 
            database_name=database_name,
            verbose=verbose
            )
    
    return result
    



#%% data folder - old


# def update_data_files(
#         data_folder=_default_data_folder,
#         latest_data_file_info_download_url=r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/latest_data_file_info.json',
#         fp_database=_default_database_fp,
#         reload_database_tables=False
#         ):
#     """
#     """
    
#     urllib.request.urlcleanup()
    
#     # download latest data file info
#     _update_latest_data_file_info(
#         data_folder,
#         latest_data_file_info_download_url
#         )
    
#     # open latest data file info
#     latest_data_file_info=\
#         _get_latest_data_file_info_json(
#                 data_folder
#                 )
    
#     # update data files
#     for x in latest_data_file_info:
        
#         #print(x)
        
#         data_filename=x['data_filename']
        
#         # download data_file        
#         fp=os.path.join(data_folder,data_filename)
#         base,ext=os.path.splitext(fp)
#         download_url=x['data_download_url']
        
#         if not os.path.exists(fp):
            
#             urllib.request.urlretrieve(
#                 url=download_url, 
#                 filename=fp
#                 )
            
#         # unzip data file if needed
#         if ext=='.zip':
            
#             with zipfile.ZipFile(fp) as z:
                
#                 for y in x['extract']:
                
#                     fp2=os.path.join(data_folder,y['data_filename'])
                    
#                     if not os.path.exists(fp2):
                
#                         with open(fp2, 'wb') as f:
                            
#                             f.write(z.read(y['data_filepath']))
                    
            
#         # download metadata file
#         fp=os.path.join(data_folder,f'{data_filename}-metadata.xml')
#         download_url=x['metadata_download_url']
        
#         if not os.path.exists(
#                 fp
#                 ):
            
#             urllib.request.urlretrieve(
#                 url=download_url, 
#                 filename=fp
#                 )
            
#         # import data to database
        
#         if ext=='.zip':
#             table_names=[os.path.splitext(y['data_filename'])[0] for y in x['extract']]
#         else:
#             table_names=[os.path.splitext(data_filename)[0]]
        
#         for table_name in table_names:
        
#             if reload_database_tables or \
#                 not _check_if_table_exists_in_database(
#                         fp_database, 
#                         table_name
#                         ):
            
#                 csvw_metadata=\
#                     _read_csvw_metadata_json(
#                             table_name
#                             )
                
#                 _create_database_table(
#                     fp_database, 
#                     table_name,
#                     csvw_metadata
#                     )
        
        
#         #break
        
        

        

# def _update_latest_data_file_info(
#         data_folder=_default_data_folder,
#         download_url=r'https://raw.githubusercontent.com/building-energy/ogp_functions/main/latest_data_file_info.json'
#         ):
#     """
#     # downloads the latest data file information from GitHub

#     # - the file on GitHub can be updated as new data files are released
#     #   on the Open Geography Portal website.
    
#     # saves the file in the 'data_folder'
    
#     # note sometimes a caching issue means a previous version might be saved instead.
    
    
#     """

#     # --- temporary for development ----
#     import shutil
#     shutil.copyfile(
#         os.path.join(os.pardir,'latest_data_file_info.json'),
#         os.path.join('_data','latest_data_file_info.json')
#         )
#     return
#     # ---




#     urllib.request.urlcleanup()
    
#     fp=os.path.join(data_folder,'latest_data_file_info.json')

#     urllib.request.urlretrieve(
#         url=download_url, 
#         filename=fp
#         )
    

# def _get_latest_data_file_info_json(
#         data_folder=_default_data_folder,
#         ):
#     """
#     # download the latest data file information from GitHub

#     # - the file on GitHub can be updated as new data files are released
#     #   on the Open Geography Portal website.
    
#     """
#     fp=os.path.join(data_folder,'latest_data_file_info.json')
    
#     with open(fp) as f:
#         latest_data_file_info=json.load(f)
        
#     return latest_data_file_info
        


# def _get_metadata_xml(
#         download_url
#         ):
#     """
    
#     returns XML -> a lxml.etree root node (element)
    
#     """
    
#     urllib.request.urlcleanup()
    
#     with urllib.request.urlopen(download_url) as url:
#         #print(url.read())
#         root = etree.fromstring(url.read())
        
#     return root
    

# def _parse_metadata_xml(
#         root
#         ):
#     """
#     """

#     d=dict(
#         title=root.xpath('dataIdInfo/idCitation/resTitle')[0].text,
#         creation_date=root.xpath('dataIdInfo/idCitation/date/createDate')[0].text,
#         publication_date=root.xpath('dataIdInfo/idCitation/date/pubDate')[0].text,
#         id_code=root.xpath('dataIdInfo/idCitation/citId/identCode')[0].text,
#         abstract=BeautifulSoup(root.xpath('dataIdInfo/idAbs')[0].text, "lxml").text,
#         purpose=root.xpath('dataIdInfo/idPurp')[0].text
#         )

#     d['fieldnames']=[x.strip() for x in d['abstract'].split('Field Names -')[1].split('Field Types -')[0].split(',')]
#     d['fieldtypes']=[x.strip() for x in d['abstract'].split('Field Types -')[1].split('Field Lengths -')[0].split(',')]
#     d['description']=d['abstract'].split('(File Size -')[0].strip()


#     return d
    
    
# def download_latest_data_files(
#         data_folder=_default_data_folder
#         ):
#     """
#     """
    
#     # get latest data file into from GitHub
#     latest_data_file_info=get_latest_data_file_info()
    
#     # create the data folder if it doesn't exist
#     if not os.path.exists(data_folder):
        
#         os.makedirs(data_folder)
        
#     # save latest data file info
#     with open(os.path.join(data_folder,'latest_data_file_info.json'),'w') as f:
        
#         json.dump(latest_data_file_info,f,indent=4)
        
#     # # download files
#     for file_info in latest_data_file_info:
        
#         download_url = file_info['download_url']  # str
#         zip_file = file_info.get('zip_file',False)  # boolean
        
#         if zip_file:
            
#             data_files = file_info['data_files']  # a list
            
#             # download zip file
#             urllib.request.urlretrieve(
#                 url=download_url, 
#                 filename='_temp.zip'
#                 )
            
#             # extract single files from zip file
#             with zipfile.ZipFile('_temp.zip') as z:
                
#                 for data_file in data_files:
                
#                     with open(os.path.join(data_folder,data_file), 'wb') as f:
                        
#                         f.write(z.read(data_file))
            
#             # remove temporary zip file
#             os.remove('_temp.zip')
            
#         else:
            
#             # download single files
            
#             data_file = file_info['data_file']
            
#             urllib.request.urlretrieve(
#                 url=download_url, 
#                 filename=data_file
#                 )
            
#     # create changes table in database
#     _create_changes_table(
#         fp_database=_get_fp_database()
#         )
    
#     # create changehistory table in database
#     _create_changehistory_table(
#         fp_database=_get_fp_database()
#         )

    




# def load_data(
#         data_folder=_default_data_folder
#         ):
#     """
#     """
#     d={}
    
#     # Changes.csv
    
#     fp=os.path.join(data_folder,'Changes.csv')
    
#     with open(fp,encoding='utf-8-sig') as f:
        
#         csvreader=csv.DictReader(f)
        
#         for row in csvreader:
            
#             geogcd=row['GEOGCD']
#             geogcd_p=row['GEOGCD_P']
            
#             x=d.setdefault(geogcd,{})
#             y=x.setdefault('changes',[])
#             y.append(row)
            
#             x=d.setdefault(geogcd_p,{})
#             y=x.setdefault('__next__',[])
#             y.append(geogcd)
    
#     # ChangeHistory.csv
    
#     fp=os.path.join(data_folder,'ChangeHistory.csv')
    
#     with open(fp,encoding='utf-8-sig') as f:
        
#         csvreader=csv.DictReader(f)
        
#         for row in csvreader:
            
#             geogcd=row['GEOGCD']
#             parentcd=row['PARENTCD']
            
#             x=d.setdefault(geogcd,{})
#             y=x.setdefault('changehistory',[])
#             y.append(row)
            
#             x=d.setdefault(parentcd,{})
#             y=x.setdefault('__children__',[])
#             y.append(geogcd)
    
    
#     return d
    


# def get_previous_codes(code,data):
#     ""
#     return [x['GEOGCD_P'] for x in data[code]['changes']]


# def get_next_codes(code,data):
#     ""
#     return data[code].get('__next__',[])


# def get_latest_codes(code,data):
#     """
#     """
#     result=set()
    
#     def _get_next_codes(
#             result,
#             codes,
#             data):
        
#         for code in codes:
            
#             x=get_next_codes(code,data)  # a list of codes
            
#             result.update(x)
            
#             result = _get_next_codes(result,x,data)
            
#         return result
    
#     result =  _get_next_codes(result,[code],data)
    
#     return list(result)


# def get_parent_codes(
#         code,
#         data
#         ):
#     """
#     """
#     return [x['PARENTCD'] for x in data[code]['changehistory']
#             if x['PARENTCD']!='']


# def get_child_codes(code,data):
#     ""
#     return data[code].get('__children__',[])

# def get_ancestor_codes(
#         code,
#         data
#         ):
#     """
#     """
#     result=set()
    
#     def _get_parent_codes(
#             result,
#             codes,
#             data
#             ):
        
#         for code in codes:
            
#             x=get_parent_codes(code,data)  # a list of codes
            
#             result.update(x)
            
#             result = _get_parent_codes(result,x,data)
            
#         return result
    
#     result =  _get_parent_codes(result,[code],data)
    
#     return list(result)


# def get_descendent_codes(
#         code,
#         data
#         ):
#     """
#     """
#     result=set()
    
#     def _get_child_codes(
#             result,
#             codes,
#             status):
        
#         for code in codes:
            
#             x=get_child_codes(code,data)  # a list of codes
                            
#             result.update(x)
            
#             result = _get_child_codes(result,x,data)
            
#         return result
    
#     result =  _get_child_codes(result,[code],data)
    
#     return list(result)




# #%% read metadata files

# # Changes-schema-metadata.json
# fp=os.path.join(
#     pkg_resources.files(ogp_functions),
#     'Changes-schema-metadata.json'
#     )
# with open(fp) as f:
#     changes_schema_metadata=json.load(f)

# # ChangeHistory-schema-metadata.json
# fp=os.path.join(
#     pkg_resources.files(ogp_functions),
#     'ChangeHistory-schema-metadata.json'
#     )
# with open(fp) as f:
#     changehistory_schema_metadata=json.load(f)






#%% database functions - old

# def _get_fp_database():
#     ""
#     return os.path.join(_default_data_folder,'ogp.sqlite')


# def _check_if_table_exists_in_database(
#         fp_database,
#         table_name
#         ):
#     ""
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f"SELECT count(*) FROM sqlite_master WHERE type='table' AND name='{table_name}';"
#         return True if c.execute(query).fetchall()[0][0] else False
    
    
# def _create_database_table(
#         fp_database,
#         table_name,
#         csvw_metadata,
#         verbose=True
#         ):
#     """Creates a table in the sqlite database.
    
#     Replaces any existing table.
    
#     """
    
#     # drop table in database
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f'DROP TABLE IF EXISTS "{table_name}";'
#         print(query)
#         c.execute(query)
#         conn.commit()
    
#     # create query
#     datatype_map={
#     'integer':'INTEGER',
#     'decimal':'REAL'
#     }
#     query=f'CREATE TABLE "{table_name}" ('
#     for column_dict in csvw_metadata['columns']:
#         name=column_dict['name']
#         datatype=datatype_map.get(column_dict['datatype']['base'],'TEXT')
#         query+=f"{name} {datatype}"
#         query+=", "
#     query=query[:-2]
#     query+=');'
    
#     if verbose:
#         print('---QUERY TO CREATE TABLE---')
#         print(query)
    
#     # create empty table in database
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         c.execute(query)
#         conn.commit()
        
#     # create indexes
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         for column_dict in csvw_metadata['columns']:
#             column_name=column_dict['name']
#             notes=column_dict.get('notes')
#             if notes=='SETINDEX':
#                 index_name=f'{table_name}_{column_name}'
#                 query=f'CREATE INDEX "{index_name}" ON "{table_name}"("{column_name}")'
#                 print(query)
#                 c.execute(query)
#                 conn.commit()
    
#     # import data into table
#     fp_database2=fp_database.replace('\\','\\\\')
#     fp_csv=os.path.join(_default_data_folder,f'{table_name}.csv')
#     fp_csv2=fp_csv.replace('\\','\\\\')
#     command=f'sqlite3 {fp_database2} -cmd ".mode csv" ".import --skip 1 {fp_csv2} {table_name}"'
#     if verbose:
#         print('---COMMAND LINE TO IMPORT DATA---')
#         print(command)
#     subprocess.run(command)
#     if verbose:
#         print('Number of rows after import: ', _get_row_count_in_database_table(fp_database,table_name))
    
    
    


# def _create_changes_table(
#         fp_database,
#         verbose=True
#         ):
#     """Creates a changes table in the sqlite database.
    
#     Replaces any existing 'changes' table.
    
#     """
    
#     # drop table in database
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query='DROP TABLE IF EXISTS changes;'
#         c.execute(query)
#         conn.commit()
    
#     # create query
#     datatype_map={
#     'integer':'INTEGER',
#     'decimal':'REAL'
#     }
#     query='CREATE TABLE changes ('
#     for column_dict in changes_schema_metadata['columns']:
#         name=column_dict['name']
#         datatype=datatype_map.get(column_dict['datatype']['base'],'TEXT')
#         query+=f"{name} {datatype}"
#         query+=", "
#     query=query[:-2]
#     query+=');'
    
#     if verbose:
#         print('---QUERY TO CREATE TABLE---')
#         print(query)
    
#     # create empty table in database
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         c.execute(query)
#         conn.commit()
        
#     # create indexes
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query="CREATE INDEX index_changes_GEOGCD ON changes(GEOGCD)"
#         c.execute(query)
#         query="CREATE INDEX index_changes_GEOGCD_P ON changes(GEOGCD_P)"
#         c.execute(query)
#         conn.commit()
        
#     # import data into table
#     fp_database2=fp_database.replace('\\','\\\\')
#     fp_csv=os.path.join(_default_data_folder,'Changes.csv')
#     fp_csv2=fp_csv.replace('\\','\\\\')
#     command=f'sqlite3 {fp_database2} -cmd ".mode csv" ".import --skip 1 {fp_csv2} changes"'
#     if verbose:
#         print('---COMMAND LINE TO IMPORT DATA---')
#         print(command)
#     subprocess.run(command)
#     if verbose:
#         print('Number of rows after import: ', _get_row_count_in_database_table(fp_database,'changes'))
    
    
# def _create_changehistory_table(
#         fp_database,
#         verbose=True
#         ):
#     """Creates a changehistory table in the sqlite database.
    
#     Replaces any existing 'changehistory' table.
    
#     """
    
#     # drop table in database
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query='DROP TABLE IF EXISTS changehistory;'
#         c.execute(query)
#         conn.commit()
    
#     # create query
#     datatype_map={
#     'integer':'INTEGER',
#     'decimal':'REAL'
#     }
#     query='CREATE TABLE changehistory ('
#     for column_dict in changehistory_schema_metadata['columns']:
#         name=column_dict['name']
#         datatype=datatype_map.get(column_dict['datatype']['base'],'TEXT')
#         query+=f"{name} {datatype}"
#         query+=", "
#     query=query[:-2]
#     query+=');'
    
#     if verbose:
#         print('---QUERY TO CREATE TABLE---')
#         print(query)
    
#     # create empty table in database
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         c.execute(query)
#         conn.commit()
        
#     # create indexes
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query="CREATE INDEX index_changehistory_GEOGCD ON changehistory(GEOGCD)"
#         c.execute(query)
#         query="CREATE INDEX index_changehistory_PARENTCD ON changehistory(PARENTCD)"
#         c.execute(query)
#         query="CREATE INDEX index_changehistory_STATUS ON changehistory(STATUS)"
#         c.execute(query)
#         conn.commit()
        
#     # import data into table
#     fp_database2=fp_database.replace('\\','\\\\')
#     fp_csv=os.path.join(_default_data_folder,'ChangeHistory.csv')
#     fp_csv2=fp_csv.replace('\\','\\\\')
#     command=f'sqlite3 {fp_database2} -cmd ".mode csv" ".import --skip 1 {fp_csv2} changehistory"'
#     if verbose:
#         print('---COMMAND LINE TO IMPORT DATA---')
#         print(command)
#     subprocess.run(command)
#     if verbose:
#         print('Number of rows after import: ', _get_row_count_in_database_table(fp_database,'changehistory'))
    
    
    
        
# def _get_row_count_in_database_table(
#         fp_database,
#         table_name,
#         column_name='*'
#         ):
#     """Gets number of rows in table
    
#     """
#     with sqlite3.connect(fp_database) as conn:
#         c = conn.cursor()
#         query=f'SELECT COUNT({column_name}) FROM "{table_name}"'
#         return c.execute(query).fetchone()[0]
    





#%% class - old

# class OGPdata():
#     """
#     """
    
#     def __init__(
#             self,
#             data_folder='_data'
#         ):
#         """
#         """
#         self.data_folder=data_folder
        
#         self.df_changes=self._load_changes_dataframe()
#         #print(self._df_changes)
        
#         self.df_changehistory=self._load_changehistory_dataframe()
        
        
        
        

#     def _load_changes_dataframe(self):
#         ""
#         fp=os.path.join(self.data_folder,'Changes.csv')
#         return pd.read_csv(fp)
        
    
#     def _load_changehistory_dataframe(self):
#         ""
#         fp=os.path.join(self.data_folder,'ChangeHistory.csv')
#         return pd.read_csv(fp)


#     def get_previous_codes(self,code):
#         """Returns the previous codes of a code change.
#         """
        
#         return self.df_changes[self.df_changes.GEOGCD==code].GEOGCD_P.dropna().to_list()
    
#     def get_next_codes(self,code):
#         """
#         """
        
#         return self.df_changes[self.df_changes.GEOGCD_P==code].GEOGCD.dropna().to_list()
        
        
#     def get_latest_codes(self,code):
#         """
#         """
#         result=set()
        
#         def _get_next_codes(
#                 result,
#                 codes):
            
#             for code in codes:
                
#                 x=self.get_next_codes(code)  # a list of codes
                
#                 result.update(x)
                
#                 result = _get_next_codes(result,x)
                
#             return result
        
#         result =  _get_next_codes(result,[code])
        
#         return list(result)
    
    
#     def get_parent_codes(
#             self,
#             code,
#             status='live'  # 'live' or 'terminated' or none 
#             ):
#         """
#         """
        
#         if status is None:
            
#             mask = self.df_changehistory.GEOGCD==code
            
#         else:
            
#             mask = (self.df_changehistory.GEOGCD==code) & (self.df_changehistory.STATUS==status)
            
#         result = self.df_changehistory[mask].PARENTCD.dropna().to_list()
            
#         return result
    
    
#     def get_ancestor_codes(
#             self,
#             code,
#             status='live'  # 'live' or 'terminated' or none 
#             ):
#         """
#         """
#         result=set()
        
#         def _get_parent_codes(
#                 result,
#                 codes,
#                 status):
            
#             for code in codes:
                
#                 x=self.get_parent_codes(code,status)  # a list of codes
                
#                 result.update(x)
                
#                 result = _get_parent_codes(result,x,status)
                
#             return result
        
#         result =  _get_parent_codes(result,[code],status)
        
#         return list(result)
       
        
#     def get_child_codes(
#             self,
#             code,
#             status='live'  # 'live' or 'terminated' or none 
#             ):
#         """
#         """
      
#         if status is None:
            
#             mask = self.df_changehistory.PARENTCD==code
            
#         else:
            
#             mask = (self.df_changehistory.PARENTCD==code) & (self.df_changehistory.STATUS==status)
            
#         result = self.df_changehistory[mask].GEOGCD.dropna().to_list()
            
#         return result
       

#     def get_descendent_codes(
#             self,
#             code,
#             status='live'  # 'live' or 'terminated' or none 
#             ):
#         """
#         """
#         result=set()
        
#         def _get_child_codes(
#                 result,
#                 codes,
#                 status):
            
#             for code in codes:
                
#                 if code[1:3]=='00':
#                     continue
                
#                 x=self.get_child_codes(code,status)  # a list of codes
                                
#                 result.update(x)
                
#                 result = _get_child_codes(result,x,status)
                
#             return result
        
#         result =  _get_child_codes(result,[code],status)
        
#         return list(result)





