# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:08:36 2023

@author: cvskf
"""

import unittest

from ogp_functions import ogp_functions
import csvw_functions_extra

import datetime
import json
import os

metadata_filename = 'ogp_tables-metadata.json'

class TestDataFolder(unittest.TestCase):
    ""
    
    def test_get_available_csv_file_names(self):
        ""
        result = \
            ogp_functions.get_available_csv_file_names(
                )
        self.assertEqual(
            result,
            [
                'Local_Authority_District_to_Region_December_2022.csv', 
                'OA_to_LSOA_to_MSOA_to_LAD_December_2021_v3.csv', 
                'NSPL21_MAY_2023_UK.csv', 
                'NSPL_AUG_2020_UK.csv', 
                'Code_History_Database_May_2023_UK_ChangeHistory.csv', 
                'Code_History_Database_May_2023_UK_Changes.csv', 
                'Code_History_Database_May_2023_UK_Equivalents.csv'
                ]
            )
        
        
    def _test_download_and_import_data(self):
        ""
        ogp_functions.download_and_import_data(
            verbose=True,
            )
        
        
    def _test__download_table_group_LOCAL_METADATA(self):
        ""
        fp_table_group_metadata = \
            os.path.join(os.pardir,metadata_filename)
        
        csvw_functions_extra.download_table_group(
            metadata_document_location = fp_table_group_metadata,
            data_folder = '_data',
            overwrite_existing_files = False,
            verbose = True
            )
        
    def test_get_ogp_field_names_in_database(self):
        ""
        result = \
            ogp_functions.get_ogp_field_names_in_database(
                )
        #print(result)
        self.assertEqual(
            result,
            {
                'Local_Authority_District_to_Region_December_2022': [
                    'LAD22CD', 'LAD22NM', 'RGN22CD', 'RGN22NM', 'ObjectId'
                    ], 
                'OA_to_LSOA_to_MSOA_to_LAD_December_2021_v3': [
                    'OA21CD', 'LSOA21CD', 'LSOA21NM', 'LSOA21NMW', 'MSOA21CD', 'MSOA21NM', 'MSOA21NMW', 'LAD22CD', 'LAD22NM', 'LAD22NMW', 'ObjectId'
                    ], 
                'NSPL21_MAY_2023_UK': [
                    'pcd', 'pcd2', 'pcds', 'dointr', 'doterm', 'usertype', 'oseast1m', 'osnrth1m', 'osgrdind', 'oa21', 'cty', 'ced', 'laua', 'ward', 'nhser', 'ctry', 'rgn', 'pcon', 'ttwa', 'itl', 'park', 'lsoa21', 'msoa21', 'wz11', 'sicbl', 'bua22', 'ru11ind', 'oac11', 'lat', 'long', 'lep1', 'lep2', 'pfa', 'imd', 'icb'
                    ], 
                'NSPL_AUG_2020_UK': [
                    'pcd', 'pcd2', 'pcds', 'dointr', 'doterm', 'usertype', 'oseast1m', 'osnrth1m', 'osgrdind', 'oa11', 'cty', 'ced', 'laua', 'ward', 'hlthau', 'nhser', 'ctry', 'rgn', 'pcon', 'eer', 'teclec', 'ttwa', 'pct', 'nuts', 'park', 'lsoa11', 'msoa11', 'wz11', 'ccg', 'bua11', 'buasd11', 'ru11ind', 'oac11', 'lat', 'long', 'lep1', 'lep2', 'pfa', 'imd', 'calncv', 'stp'
                    ], 
                'Code_History_Database_May_2023_UK_ChangeHistory': [
                    'GEOGCD', 'GEOGNM', 'GEOGNMW', 'SI_ID', 'SI_TITLE', 'OPER_DATE', 'TERM_DATE', 'PARENTCD', 'ENTITYCD', 'OWNER', 'STATUS', 'AREAEHECT', 'AREACHECT', 'AREAIHECT', 'AREALHECT'
                    ], 
                'Code_History_Database_May_2023_UK_Changes': [
                    'GEOGCD', 'GEOGNM', 'GEOGNMW', 'GEOGCD_P', 'GEOGNM_P', 'GEOGNMW_P', 'SI_ID', 'SI_TITLE', 'OPER_DATE', 'ENTITYCD', 'YEAR'
                    ], 
                'Code_History_Database_May_2023_UK_Equivalents': [
                    'GEOGCD', 'GEOGNM', 'GEOGNMW', 'GEOGCDO', 'GEOGNMO', 'GEOGCDD', 'GEOGNMD', 'GEOGCDH', 'GEOGNMH', 'GEOGCDS', 'GEOGNMS', 'GEOGCDI', 'GEOGNMI', 'GEOGCDWG', 'GEOGNMWG', 'GEOGNMWWG', 'OPER_DATE', 'TERM_DATE', 'ENTITYCD', 'YEAR', 'STATUS'
                    ]
                }
            )
        
    
    def test_get_ogp_table_names_in_database(self):
        ""
        result = \
            ogp_functions.get_ogp_table_names_in_database(
                )
        #print(result)
        self.assertEqual(
            result,
            [
                'Local_Authority_District_to_Region_December_2022', 
                'OA_to_LSOA_to_MSOA_to_LAD_December_2021_v3', 
                'NSPL21_MAY_2023_UK', 
                'NSPL_AUG_2020_UK', 
                'Code_History_Database_May_2023_UK_ChangeHistory', 
                'Code_History_Database_May_2023_UK_Changes', 
                'Code_History_Database_May_2023_UK_Equivalents'
                ]
            )
    
    
    
    def _test_set_data_folder(self):
        ""
        
        fp=os.path.join(os.pardir,'ogp_tables-metadata.json')
        
        ogp_functions.set_data_folder(
            metadata_document_location=fp,
            #overwrite_existing_files=True,
            #remove_existing_tables=True,
            verbose=True
            )
        
        
        
class TestBoundariesData(unittest.TestCase):
    ""
    
    def test_get_available_boundaries_names(self):
        ""
        result = \
            ogp_functions.get_available_boundaries_names(
                )
        #print(result)


    def test_download_boundaries_data(self):
        ""
        result = \
            ogp_functions.download_boundaries_data(
                )
        #print(result)
        
        
    def test_get_downloaded_boundaries_names(self):
        ""
        result = \
            ogp_functions.get_downloaded_boundaries_names(
                )
        print(result)
        
    def _test_plot_boundaries(self):
        ""
        ogp_functions.plot_boundaries(
            name = 'Local_Authority_Districts_May_2023_UK_BUC_V2'
            )


class TestCodeHistoryDatabaseFunctions(unittest.TestCase):
    ""
    
    
    def test1(self):
        ""
        
        result=ogp_functions.get_CHD_change_history_rows(
            GEOGCD = 'E07000044',
            table_name = 'Code_History_Database_May_2023_UK_ChangeHistory',
            verbose = False
            )
        print(result)
    
    def test_get_CHD_change_rows(self):
        ""
        
        result=ogp_functions.get_CHD_change_rows(
            GEOGCD = 'E00000001',
            table_name = 'Code_History_Database_May_2023_UK_Changes',
            verbose = False
            )
        #print(result)
        self.assertEqual(
            result,
            [
                {
                    'GEOGCD': 'E00000001', 
                    'GEOGNM': '', 
                    'GEOGNMW': '', 
                    'GEOGCD_P': '00AAFA0001', 
                    'GEOGNM_P': '', 
                    'GEOGNMW_P': '', 
                    'SI_ID': '1111/1001', 
                    'SI_TITLE': 'GSS re-coding strategy', 
                    'OPER_DATE': '01/01/2009', 
                    'ENTITYCD': 'E00', 
                    'YEAR': 2009
                    }
                ]
            )
        
        
    def _test_get_change_hitory(self):
        ""
        
        result=ogp_functions.get_CHD_change_history(
            GEOGCD='E00000001',
            table_name='Code_History_Database_May_2023_UK_ChangeHistory'
            )
        
        self.assertEqual(
            result,
            [
                {
                    'GEOGCD': 'E00000001', 
                     'GEOGNM': '', 
                     'GEOGNMW': '', 
                     'SI_ID': '1111/1001', 
                     'SI_TITLE': 'GSS re-coding strategy', 
                     'OPER_DATE': '01/01/2009', 
                     'TERM_DATE': '', 
                     'PARENTCD': 'E01000001', 
                     'ENTITYCD': 'E00', 
                     'OWNER': 'ONS', 
                     'STATUS': 'live', 
                     'AREAEHECT': 0.67, 
                     'AREACHECT': 0.67, 
                     'AREAIHECT': 0.0, 
                     'AREALHECT': 0.67
                     }
                ]
            )


class TestNSPL_AUG2020Functions(unittest.TestCase):
    ""
    
    def _test_get_NSPL_AUG_2020_UK_rows(self):
        
        result=ogp_functions.get_NSPL_AUG_2020_UK_rows(
            pcd='AB1 0AA'
            )
        
        self.assertEqual(
            result,
            [
                {'pcd': 'AB1 0AA', 
                 'pcd2': 'AB1  0AA', 
                 'pcds': 'AB1 0AA', 
                 'dointr': '198001', 
                 'doterm': '199606', 
                 'usertype': '0', 
                 'oseast1m': '385386', 
                 'osnrth1m': '0801193', 
                 'osgrdind': '1', 
                 'oa11': 'S00090303', 
                 'cty': 'S99999999', 
                 'ced': 'S99999999', 
                 'laua': 'S12000033', 
                 'ward': 'S13002843', 
                 'hlthau': 'S08000020', 
                 'nhser': 'S99999999', 
                 'ctry': 'S92000003', 
                 'rgn': 'S99999999', 
                 'pcon': 'S14000002', 
                 'eer': 'S15000001', 
                 'teclec': 'S09000001', 
                 'ttwa': 'S22000047', 
                 'pct': 'S03000012', 
                 'nuts': 'S31000935', 
                 'park': 'S99999999', 
                 'lsoa11': 'S01006514', 
                 'msoa11': 'S02001237', 
                 'wz11': 'S34002990', 
                 'ccg': 'S03000012', 
                 'bua11': 'S99999999', 
                 'buasd11': 'S99999999', 
                 'ru11ind': '3', 
                 'oac11': '1C3', 
                 'lat': 57.101474, 
                 'long': -2.242851, 
                 'lep1': 'S99999999', 
                 'lep2': 'S99999999', 
                 'pfa': 'S23000009', 
                 'imd': '6808', 
                 'calncv': 'S99999999', 
                 'stp': 'S99999999'}]
            )



class TestMainFunctions(unittest.TestCase):
    ""
    
    # def test_get_region_from_local_authority_district(self):
    #     ""
        
    #     result=ogp_functions.get_region_from_local_authority_district(
    #         'E06000001'
    #         )
    #     #print(result)
        
    #     self.assertEqual(
    #         result,
    #         ['E12000001']
    #         )
        
        
    # def test_get_local_authority_district_from_region(self):
    #     ""
        
    #     result=ogp_functions.get_local_authority_district_from_region(
    #         'E12000001'
    #         )
    #     #print(result)
        
    #     self.assertEqual(
    #         set(result),
    #         set(['E06000001', 'E06000002', 'E06000003', 'E06000004', 
    #              'E06000005', 'E06000047', 'E06000057', 'E08000021', 
    #              'E08000022', 'E08000023', 'E08000024', 'E08000037'])
    #         )

    # def test_get_previous_codes(self):
    #     ""
    #     code='E06000063'
    #     result=ogp_functions.get_previous_codes(
    #         code
    #         )
    #     #print(result)
        
    #     self.assertEqual(
    #         set(result),
    #         set(['E07000028','E07000026','E07000029'])
    #         )
        
        
    # def test_get_next_codes(self):
    #     ""
    #     code='E07000026'
    #     result=ogp_functions.get_next_codes(
    #         code
    #         )
    #     #print(result)
        
    #     self.assertEqual(
    #         set(result),
    #         set(['E06000063'])
    #         )
        
        
    # def test_get_latest_codes(self):
    #     ""
    #     code='E07000026'
    #     result=ogp_functions.get_latest_codes(
    #         code
    #         )
    #     #print(result)
        
    #     self.assertEqual(
    #         set(result),
    #         set(['E06000063'])
    #         )
        
        
    # def test_get_code_entity(self):
    #     ""
    #     code='E07000026'
    #     result=ogp_functions.get_code_entity(
    #         code
    #         )
    #     #print(result)
        
    #     self.assertEqual(
    #         result,
    #         'E07'
    #         )
        
        
    # def test_get_parent_codes(self):
    #     ""
    #     code='E00130460'
    #     result=ogp_functions.get_parent_codes(
    #         code
    #         )
    #     self.assertEqual(
    #         set(result),
    #         set(['E01025710'])
    #         )
                  
        



    
    # def test_update_data_files(self):
    #     ""
        
    #     ogp_functions.update_data_files(
            
    #         reload_database_tables=False
    #         )
        
    # def test___read_csvw_metadata_json(self):
    #     ""
        
    #     result=ogp_functions._read_csvw_metadata_json(
    #         'Local_Authority_District_to_Region_(December_2022)_Lookup_in_England'
    #         )
    #     #print(result)
    
    # def _test__update_latest_data_file_info(self):
    #     ""
        
    #     ogp_functions._update_latest_data_file_info()
    
    
    # def test__get_latest_data_file_info_json(self):
    #     ""
        
    #     result=ogp_functions._get_latest_data_file_info_json()
    #     #print(result[0])
    
    
    # def test__get_metadata_xml(self):
    #     ""
        
    #     download_url='https://www.arcgis.com/sharing/rest/content/items/78b348cd8fb04037ada3c862aa054428/info/metadata/metadata.xml'
    #     result=ogp_functions._get_metadata_xml(
    #         download_url
    #         )
    #     #print(result)
    
    
    # def tst__parse_metadata_xml(self):
    #     ""
        
    #     download_url='https://www.arcgis.com/sharing/rest/content/items/78b348cd8fb04037ada3c862aa054428/info/metadata/metadata.xml'
    #     metadata_xml=\
    #         ogp_functions._get_metadata_xml(
    #             download_url
    #             )
    #     result=\
    #         ogp_functions._parse_metadata_xml(
    #             metadata_xml
    #             )
    #     #print(result)
    
    
    
    # def _test_download_latest_data_files(self):
    #     ""
        
    #     #ogp_functions.download_latest_data_files()
        
        
        
    
    # def _test_load_data(self):
    #     ""
        
    #     result=ogp_functions.load_data()
        
    #     print(len(result))
    #     #print(result)
    #     #print([result[x] for x in list(result.keys())[:]])
        
        
    # def _test_load_data2(self):
    #      ""
         
    #      with open('data.json') as f:
    #          result=json.load(f)
    
    
    
    
    
        
    
        
        
          
        
    # def _test_get_child_codes(self):
    #     ""
    #     code='E01025710'
    #     result=ogp_functions.get_child_codes(
    #         code,
    #         data
    #         )
    #     self.assertEqual(
    #         set(result),
    #         set(['E00130450', 'E00130457', 'E00130458', 'E00130460'])
    #         )
        
        
    # def _test_get_ancestor_codes(self):
    #     ""
    #     code='E00130460'
    #     result=ogp_functions.get_ancestor_codes(
    #         code,
    #         data
    #         )
    #     self.assertEqual(
    #         set(result),
    #         set(['E10000018', 'E07000130', 'E02005354', 'E12000004', 'E92000001', 'E01025710'])
    #         )
        
        
    # def _test_get_descendent_codes(self):
    #     ""
    #     code='E02005354'
    #     result=ogp_functions.get_descendent_codes(
    #         code,
    #         data
    #         )
    #     self.assertEqual(
    #         set(result),
    #         set(
    #             ['E00130463', 'E00178480', 'E33016309', 'E00130442', 'E33014322', 
    #              'E01034004', 'E00130464', 'E00130466', 'E33016308', 'E01025708', 
    #              'E00130472', 'E00130452', 'E00130460', 'E00130451', 'E33016307', 
    #              'E01025714', 'E00130454', 'E00130462', 'E00173301', 'E00130467', 
    #              'E01034005', 'E00130465', 'E33014320', 'E33014321', 'E00130453', 
    #              'E00130479', 'E00173302', 'E00173303', 'E00178593', 'E00178581', 
    #              'E00130437', 'E00130455', 'E00178631', 'E01025711', 'E01025713', 
    #              'E00130444', 'E01025710', 'E00130458', 'E00130477', 'E00130478', 
    #              'E00130459', 'E33016310', 'E01025712', 'E00178546', 'E00130456', 
    #              'E00130476', 'E00130457', 'E00130450', 'E00130438', 'E00130461', 
    #              'E00130445']
    #             )
    #         )
        
        
    # def _test_Class(self):
        
    #     code='E06000063'
    #     result=o.get_previous_codes(
    #         code
    #         )
    #     print(result)
        
    #     code='E07000026'
    #     result=o.get_next_codes(
    #         code
    #         )
    #     print(result)
        
    #     code='E07000026'
    #     result=o.get_latest_codes(
    #         code
    #         )
    #     print(result)
        
    #     code='E00130460'
    #     result=o.get_parent_codes(
    #         code
    #         )
    #     print(result)
        
    #     code='E00130460'
    #     result=o.get_ancestor_codes(
    #         code
    #         )
    #     print(result)
        
    #     code='E01025710'
    #     result=o.get_child_codes(
    #         code
    #         )
    #     print(result)
        
    #     code='E02005354'
    #     result=o.get_descendent_codes(
    #         code
    #         )
    #     print(result)
        
    
    
if __name__=='__main__':
    
    unittest.main()