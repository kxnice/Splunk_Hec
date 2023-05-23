from splunk_config import Splunk
from google_poc import GCP_GBQ
import json
import requests


def set_environment():
    Splunk.enable_token_authentication()
    Splunk.create_hec_endpoint()

    def poc():
        bigquery_object = GCP_GBQ()
        bigquery_results = bigquery_object.construct_query()
        payload = json.dumps(bigquery_results)
        try:
            res = requests.post("https://localhost:8088/services/collector", verify=False, headers={"Authorization": f"Splunk {Splunk.get_hec_token()}"},
                                data=payload)
            res.raise_for_status()
        except Exception as e:
            print(e)
    poc()


if __name__ == '__main__':
    try:
        set_environment()
        print("Success")
    except Exception as e:
        print(e)
