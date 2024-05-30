import httplib2
import apiclient.discovery

import gspread
from oauth2client.service_account import ServiceAccountCredentials


class ApiService():
    def __init__(self):
        self.cred_path = 'secrets/credentials.json'
        self.spreadsheet_id = '18UNzxVBTrOM3JYKR5YMun_6MJ0sUQ62vrJG9Rv6qqe0'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.cred_path,
            ['https://www.googleapis.com/auth/spreadsheets'])

        self.gc = gspread.authorize(credentials)
        self.sh = self.gc.open_by_key(self.spreadsheet_id)

    def getGcService(self):
        return self.gc

    def getWorksheet(self):
        return self.sh
