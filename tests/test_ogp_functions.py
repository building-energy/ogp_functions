# -*- coding: utf-8 -*-
"""
Created on Wed Aug  9 13:08:36 2023

@author: cvskf
"""

import unittest

from ogp_functions import ogp_functions



class TestOGPFunctions(unittest.TestCase):
    ""
    
    def test_download_latest_data_files(self):
        ""
        
        ogp_functions.download_latest_data_files()
    
    
    
    
if __name__=='__main__':
    
    unittest.main()