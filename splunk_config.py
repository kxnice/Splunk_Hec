import os
import urllib3
import requests
import splunklib.client as client
import xml.etree.ElementTree as ET


class Splunk:
    HOST = "localhost"
    PORT = 8089
    BEARER_TOKEN = os.environ.get('BEARER_TOKEN')

    service = client.connect(
        host=HOST,
        port=PORT,
        splunkToken=BEARER_TOKEN)

    @staticmethod
    def enable_token_authentication() -> None:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        try:
            res = requests.post("https://localhost:8089/services/admin/token-auth/tokens_auth",
                                headers={'Authorization': f'Bearer {os.environ.get("BEARER_TOKEN")}'}, verify=False,
                                data={'disabled': 'false'})
            res.raise_for_status()
        except Exception as e:
            print(e)

    @classmethod
    def create_hec_endpoint(cls) -> None:
        cls.service.post("/services/data/inputs/http", name="hec_python", source="kulmiye_hec_source",
                         index="hec", disabled=0)

    @classmethod
    def get_hec_token(cls) -> str:
        hec_token = cls.service.get('/services/data/inputs/http/hec_python')
        hec_decoded_xml = hec_token.body.read()
        hec_decoded_xml = ET.fromstring(hec_decoded_xml.decode('utf-8'))
        parse_hec_token = hec_decoded_xml.find('.//s:key[@name="token"]',
                                               namespaces={'s': 'http://dev.splunk.com/ns/rest'})
        return parse_hec_token.text
