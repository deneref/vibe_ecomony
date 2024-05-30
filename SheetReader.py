import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame


class SheetReader():
    def __init__(self):

        self.cred_path = 'secrets/credentials.json'
        self.spreadsheet_id = '18UNzxVBTrOM3JYKR5YMun_6MJ0sUQ62vrJG9Rv6qqe0'

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.cred_path,
            ['https://www.googleapis.com/auth/spreadsheets'])
        httpAuth = credentials.authorize(httplib2.Http())

        self.service = apiclient.discovery.build('sheets', 'v4', http=httpAuth)

    def readSheet(self, sheet_name: str) -> DataFrame:
        rows = self.service.spreadsheets().values().get(
            spreadsheetId=self.spreadsheet_id,
            range=sheet_name,
            majorDimension='ROWS'
        ).execute()

        data = rows.get('values')

        df = DataFrame(data[1:], columns=[
            'supply_id', 'category', 'item_amt'])
        return df
