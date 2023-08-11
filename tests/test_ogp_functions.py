# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:08:36 2023

@author: cvskf
"""

import unittest

from ogp_functions import ogp_functions

import datetime
import json


# get latest_data_file_info JSON
#latest_data_file_info=ogp_functions.get_latest_data_file_info_json()

#data=ogp_functions.load_data()

#with open('data.json','w') as f:
#    json.dump(data,f,indent=4)


#o=ogp_functions.OGPdata()


class TestMainFunctions(unittest.TestCase):
    ""
    
    def test_get_region_from_local_authority_district(self):
        ""
        
        result=ogp_functions.get_region_from_local_authority_district(
            'E06000001'
            )
        #print(result)
        
        self.assertEqual(
            result,
            ['E12000001']
            )
        
        
    def test_get_local_authority_district_from_region(self):
        ""
        
        result=ogp_functions.get_local_authority_district_from_region(
            'E12000001'
            )
        #print(result)
        
        self.assertEqual(
            set(result),
            set(['E06000001', 'E06000002', 'E06000003', 'E06000004', 
                 'E06000005', 'E06000047', 'E06000057', 'E08000021', 
                 'E08000022', 'E08000023', 'E08000024', 'E08000037'])
            )

    def test_get_previous_codes(self):
        ""
        code='E06000063'
        result=ogp_functions.get_previous_codes(
            code
            )
        #print(result)
        
        self.assertEqual(
            set(result),
            set(['E07000028','E07000026','E07000029'])
            )
        
        
    def test_get_next_codes(self):
        ""
        code='E07000026'
        result=ogp_functions.get_next_codes(
            code
            )
        #print(result)
        
        self.assertEqual(
            set(result),
            set(['E06000063'])
            )
        
        
    def test_get_latest_codes(self):
        ""
        code='E07000026'
        result=ogp_functions.get_latest_codes(
            code
            )
        #print(result)
        
        self.assertEqual(
            set(result),
            set(['E06000063'])
            )
        
        
    def test_get_code_entity(self):
        ""
        code='E07000026'
        result=ogp_functions.get_code_entity(
            code
            )
        #print(result)
        
        self.assertEqual(
            result,
            'E07'
            )
        
        
    def test_get_parent_codes(self):
        ""
        code='E00130460'
        result=ogp_functions.get_parent_codes(
            code
            )
        self.assertEqual(
            set(result),
            set(['E01025710'])
            )
                  
        


class TestDataFolder(unittest.TestCase):
    ""
    
    def test_update_data_files(self):
        ""
        
        ogp_functions.update_data_files(
            
            reload_database_tables=False
            )
        
    def test___read_csvw_metadata_json(self):
        ""
        
        result=ogp_functions._read_csvw_metadata_json(
            'Local_Authority_District_to_Region_(December_2022)_Lookup_in_England'
            )
        #print(result)
    
    def _test__update_latest_data_file_info(self):
        ""
        
        ogp_functions._update_latest_data_file_info()
    
    
    def test__get_latest_data_file_info_json(self):
        ""
        
        result=ogp_functions._get_latest_data_file_info_json()
        #print(result[0])
    
    
    def test__get_metadata_xml(self):
        ""
        
        download_url='https://www.arcgis.com/sharing/rest/content/items/78b348cd8fb04037ada3c862aa054428/info/metadata/metadata.xml'
        result=ogp_functions._get_metadata_xml(
            download_url
            )
        #print(result)
    
    
    def tst__parse_metadata_xml(self):
        ""
        
        download_url='https://www.arcgis.com/sharing/rest/content/items/78b348cd8fb04037ada3c862aa054428/info/metadata/metadata.xml'
        metadata_xml=\
            ogp_functions._get_metadata_xml(
                download_url
                )
        result=\
            ogp_functions._parse_metadata_xml(
                metadata_xml
                )
        #print(result)
    
    
    
    def _test_download_latest_data_files(self):
        ""
        
        #ogp_functions.download_latest_data_files()
        
        
        
    
    def _test_load_data(self):
        ""
        
        result=ogp_functions.load_data()
        
        print(len(result))
        #print(result)
        #print([result[x] for x in list(result.keys())[:]])
        
        
    def _test_load_data2(self):
         ""
         
         with open('data.json') as f:
             result=json.load(f)
    
    
    
    
    
        
    
        
        
          
        
    def _test_get_child_codes(self):
        ""
        code='E01025710'
        result=ogp_functions.get_child_codes(
            code,
            data
            )
        self.assertEqual(
            set(result),
            set(['E00130450', 'E00130457', 'E00130458', 'E00130460'])
            )
        
        
    def _test_get_ancestor_codes(self):
        ""
        code='E00130460'
        result=ogp_functions.get_ancestor_codes(
            code,
            data
            )
        self.assertEqual(
            set(result),
            set(['E10000018', 'E07000130', 'E02005354', 'E12000004', 'E92000001', 'E01025710'])
            )
        
        
    def _test_get_descendent_codes(self):
        ""
        code='E02005354'
        result=ogp_functions.get_descendent_codes(
            code,
            data
            )
        self.assertEqual(
            set(result),
            set(
                ['E00130463', 'E00178480', 'E33016309', 'E00130442', 'E33014322', 
                 'E01034004', 'E00130464', 'E00130466', 'E33016308', 'E01025708', 
                 'E00130472', 'E00130452', 'E00130460', 'E00130451', 'E33016307', 
                 'E01025714', 'E00130454', 'E00130462', 'E00173301', 'E00130467', 
                 'E01034005', 'E00130465', 'E33014320', 'E33014321', 'E00130453', 
                 'E00130479', 'E00173302', 'E00173303', 'E00178593', 'E00178581', 
                 'E00130437', 'E00130455', 'E00178631', 'E01025711', 'E01025713', 
                 'E00130444', 'E01025710', 'E00130458', 'E00130477', 'E00130478', 
                 'E00130459', 'E33016310', 'E01025712', 'E00178546', 'E00130456', 
                 'E00130476', 'E00130457', 'E00130450', 'E00130438', 'E00130461', 
                 'E00130445']
                )
            )
        
        
    def _test_Class(self):
        
        code='E06000063'
        result=o.get_previous_codes(
            code
            )
        print(result)
        
        code='E07000026'
        result=o.get_next_codes(
            code
            )
        print(result)
        
        code='E07000026'
        result=o.get_latest_codes(
            code
            )
        print(result)
        
        code='E00130460'
        result=o.get_parent_codes(
            code
            )
        print(result)
        
        code='E00130460'
        result=o.get_ancestor_codes(
            code
            )
        print(result)
        
        code='E01025710'
        result=o.get_child_codes(
            code
            )
        print(result)
        
        code='E02005354'
        result=o.get_descendent_codes(
            code
            )
        print(result)
        
    
    
if __name__=='__main__':
    
    unittest.main()