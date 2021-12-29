# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 13:16:49 2021

@author: seran
"""


def pHones(sheet_number):
    import gspread
    import numpy as np
    import pandas as pd
    from oauth2client.service_account import ServiceAccountCredentials

    print('************ QUE HAY DE NUEVO *******************')
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
    sheet_instance = sheet.get_worksheet(sheet_number)

    # get all the records of the data
    records_data = sheet_instance.get_all_records()

    records_df = pd.DataFrame.from_dict(records_data)

    info = np.array(records_df)

    phones = []
    for row in info:
        phones.append([row[2],row[3]])

    return phones
