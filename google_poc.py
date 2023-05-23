from os import environ
from datetime import date
from google.cloud import bigquery
from google.oauth2 import service_account


class GCP_GBQ:
    def __init__(self):
        self.keys = environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        self.scopes = ['https://www.googleapis.com/auth/bigquery']
        self.credentials = service_account.Credentials.from_service_account_file(self.keys, scopes=self.scopes)
        self.client = bigquery.Client(credentials=self.credentials)

    def construct_query(self) -> list:
        results = []
        query = self.client.query(
            "SELECT unique_key, case_number, date, block, primary_type, description, location_description, year FROM "
            "`bigquery-public-data.chicago_crime.crime` LIMIT 1000")
        for items in query.result():
            rows = dict()
            rows['sourcetype'] = '_json'
            rows['event'] = dict()
            for key, value in items.items():
                rows['event'].update({key: value})
                if isinstance(value, date):
                    date_object = date.strftime(value, "%Y/%m/%d /%H/%M/%S UTC")
                    rows['event'].update({key: date_object})
            results.append(rows)
        return results
