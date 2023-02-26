"""
IMS website example:

import urllib

url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=08259129-e1ec-45f2-be1e-f60c2878ddf3&limit=5&q=title:jones'

fileobj = urllib.request.urlopen(url)
print(fileobj.read())

^^^this returns a binary string which can unpacked with the following

json.loads(fileobj.read().decode("UTF-8"))


* after running the open form of the url:
    url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=08259129-e1ec-45f2-be1e-f60c2878ddf3

    still haven't figured out why this query returns only the first 100 records of the data
* need to figure out how to fetch "resource_id"
"""
import json
import urllib


class ImsClient:
    base_url: str = "https://data.gov.il/api/3/action/datastore_search?"

    def __init__(self, resource_id: str):
        self.resource_id = resource_id

    def get_response(self, additional_args: dict = {}):
        url = f"{self.base_url}resource_id={self.resource_id}"
        for k, v in additional_args.items():
            url = f"{url}&{k}={v}"
        fileobj = urllib.request.urlopen(url)

        return json.loads(fileobj.read().decode("UTF-8"))



