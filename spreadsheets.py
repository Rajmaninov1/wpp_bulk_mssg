# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 13:16:49 2021

@author: seran
"""


def connect_to_api(sheet_number):
    """
    
    """
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials

    # define the scope
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name(
        'Keys.json', scope)

    # authorize the clientsheet
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('MarkeBot')

    # get the first sheet of the Spreadsheet
    return sheet.get_worksheet(sheet_number)
    

def get_information(sheet_number):
    """
    
    """
    import numpy as np
    import pandas as pd

    # gets the sheet instance
    sheet_instance = connect_to_api(sheet_number)

    # get all the records of the data
    records_data = sheet_instance.get_all_records()

    records_df = pd.DataFrame.from_dict(records_data)

    info = np.array(records_df)

    phones = []
    for row in info:
        phones.append([row[2],row[3],row[4],row[5]])

    return phones


def sheet_update(sheet_number,message_sended_list,sheet_range):
    """
    
    """
    # gets the sheet instance
    sheet_instance = connect_to_api(sheet_number)

    sheet_instance.update(sheet_range,message_sended_list)

    return True


def get_sheets_names(document_number):
    """
    
    """
    from oauth2client.service_account import ServiceAccountCredentials
    import gspread

    scope = ["https://spreadsheets.google.com/feeds",
             'https://www.googleapis.com/auth/spreadsheets',
             "https://www.googleapis.com/auth/drive.file",
             "https://www.googleapis.com/auth/drive"]   
    
    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('Keys.json',scope)
    
    # authorize the clientsheet 
    client = gspread.authorize(creds)
    
    # get the instance of the Spreadsheet
    sheet = client.open(document_number)
    
    hojas = sheet.worksheets()
    dic_id = {} # Dictionary with id's
    dic_in = {} # Dictionary with indexs
    names = []
    for i in range(len(hojas)):
        dic_id.update({hojas[i].title:hojas[i].id})
        dic_in.update({hojas[i].title:i})
        names.append(hojas[i].title)
        
    print('Seleccione la hoja con la cual desea trabajar \n')
    for key,value in dic_in.items():
        print(f'Hoja de nombre {key:.>{20}} se selecciona con {value}')
        
    sel = input('Por favor ingrese su opción: ')
    opt = int(sel)
    print(f'Ha elegido la opción {sel} que corresponde a la hoja de nombre "{names[opt]}"')
 
    return opt