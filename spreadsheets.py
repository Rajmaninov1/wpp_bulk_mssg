# -*- coding: utf-8 -*-
"""
Created on Sat Dec 18 13:16:49 2021

@author: seran
"""


def connect_to_api(sheet_number):
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
    

def pHones(sheet_number):
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
        phones.append([row[2],row[3],row[4]])

    return phones


def message_sended(sheet_number,message_sended_list,sheet_range):
    import numpy as np
    import pandas as pd

    # gets the sheet instance
    sheet_instance = connect_to_api(sheet_number)

    sheet_instance.update(sheet_range,message_sended_list)

    return True