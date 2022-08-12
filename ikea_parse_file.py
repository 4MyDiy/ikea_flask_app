"""
Usage: 
This script will parse an XML file. We do expect the following elements to be found, at least partially, 
otherwise it will result in an empty value
The script will collect all availabe XML elements(but can be changed to collect only the ones specified in the assignment)
The script will also insert all values found into a database(2 tables respectively)

Things out of scope: 
-xml format validation
-string validation
-hardcoded server values-should be read from somewhere file/db/table names
-we could parse the attirbutes/elemenst in a loop(an enhancement)

How to run:
The script needs an XML file location provided(it is hardcoded and not required for testing puprosed within the script, 
but if run from a cmd line we can change to a required parameter)
2 tables need to be set up.I use Microsoft SQL Server. 
CREATE statements are attached.
The server connections also need to be changed, based on a DB of choice/also some imports need to be added via pip cmd.
"""

import xml.etree.ElementTree as ET
from os.path import exists
import argparse
import pyodbc
import datetime

def parse_file(path):

    try:
              
        if exists(path):
            
            tree = ET.parse(path)
            root = tree.getroot()
            
            #find all HSI elements
            if root.find('HSI').find('SBSN') is not None:
                hsi_sbsn = root.find('HSI').find('SBSN').text.replace(" ","")
            else:
                hsi_sbsn=""   
            if root.find('HSI').find('SPN') is not None:
                hsi_spn = root.find('HSI').find('SPN').text.replace(" ","")
            else:
                hsi_spn=""        
            if root.find('HSI').find('UUID') is not None:
                hsi_uuid = root.find('HSI').find('UUID').text.replace(" ","")
            else:
                hsi_uuid=""
            if root.find('HSI').find('SP') is not None:
                hsi_sp = root.find('HSI').find('SP').text.replace(" ","")
            else:
                hsi_sp=""    
            if root.find('HSI').find('cUUID') is not None:
                hsi_cuuid = root.find('HSI').find('cUUID').text.replace(" ","")
            else:
                hsi_cuuid=""    
            if root.find('HSI').find('VIRTUAL').find("STATE") is not None:
                hsi_virtial_state = root.find('HSI').find('VIRTUAL').find("STATE").text.replace(" ","")
            else:
                hsi_virtial_state=""
            
            #find all MP elements
            if root.find('MP').find('ST') is not None:
                mp_st = root.find('MP').find('ST').text.replace(" ","")
            else:
                mp_st=""
            if root.find('MP').find('PN') is not None:
                mp_pn = root.find('MP').find('PN').text.replace(" ","")
            else:
                mp_pn=""
            if root.find('MP').find('FWRI') is not None:
                mp_fwri = root.find('MP').find('FWRI').text.replace(" ","")
            else:
                mp_fwri=""
            if root.find('MP').find('BBLK') is not None:
                mp_bblk = root.find('MP').find('BBLK').text.replace(" ","")
            else:
                mp_bblk=""
            if root.find('MP').find('HWRI') is not None:
                mp_hwri = root.find('MP').find('HWRI').text.replace(" ","")
            else:
                mp_hwri=""
            if root.find('MP').find('SN') is not None:
                mp_sn = root.find('MP').find('SN').text.replace(" ","")
            else:
                mp_sn=""
            if root.find('MP').find('UUID') is not None:
                mp_uuid = root.find('MP').find('UUID').text.replace(" ","")
            else:
                mp_uuid=""
            if root.find('MP').find('IPM') is not None:
                mp_ipm = root.find('MP').find('IPM').text.replace(" ","")
            else:
                mp_ipm=""
            if root.find('MP').find('SSO') is not None:
                mp_sso = root.find('MP').find('SSO').text.replace(" ","")
            else:
                mp_sso=""
            if root.find('MP').find('PWRM') is not None:
                mp_pwrm = root.find('MP').find('PWRM').text.replace(" ","")
            else:
                mp_pwrm=""
        
            #build dictonaries with HSI and MP elements
            hsi_dict = {"SBSN":hsi_sbsn,"SPN":hsi_spn,"UUID":hsi_uuid,"SP":hsi_sp,"cUUID":hsi_cuuid,"VIRTUAL_STATE":hsi_virtial_state,"PARSED_DATE":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            #build dictonaries with MP elements
            mp_dict = {"ST":mp_st,"PN":mp_pn,"FWRI":mp_fwri,"BBLK":mp_bblk,"HWRI":mp_hwri,"SN":mp_sn,"UUID":mp_uuid,"IPM":mp_ipm,"SSO":mp_sso,"PWRM":mp_pwrm,"PARSED_DATE":datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            #insert HSI elements
            insert_parsed_data(hsi_dict,"IKEA_HSI")
             #insert MP elements
            insert_parsed_data(mp_dict,"IKEA_MP")
        else:
            print ("File does not exist")

    except Exception as e:
        print(e)
        exit(1)			

def insert_parsed_data(data_dict,table_name):
	
    try:
        #set up SQL server connection
        conn = pyodbc.connect('Driver={SQL Server};'
                        'Server=LAPTOP-TMP50LAM;'
                        'Database=AdhocDB;'
                        'Trusted_Connection=yes;')
    
        cursor = conn.cursor()
        #parse columns
        dict_columns=",".join(list(data_dict.keys()))
        #parse values
        dict_values= "','".join(list(data_dict.values()))
        
        #build the insert statement
        insert_stmnt="INSERT INTO "+table_name+ "("+dict_columns+") VALUES ('"+dict_values+"')"
        print(insert_stmnt) 
        #execute the insert
        cursor.execute(insert_stmnt)
        conn.commit()
        cursor.close()	
	
    except Exception as e:
        print(e)
        exit(1)			
	

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--FilePath',required=False, help='File path to process the data')
    #Parse args
    args = parser.parse_args()
    file_path = "C:\\Dev\\Python\\Data\\ikea_challenge.xml" #args.FilePath
    parse_file(file_path)