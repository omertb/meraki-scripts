#!/usr/bin/env python3
"""

"""
import requests
import json
import pprint
from credential import *

# suppress certificate verification warnings
# requests.packages.urllib3.disable_warnings()

cred_header = {
    'X-Cisco-Meraki-API-Key': apikey
}


def get_data(item) -> list:
    url = "https://api.meraki.com/api/v0/{}".format(item)
    response = requests.request("GET", url, headers=cred_header)
    response_list = json.loads(response.text)
    return response_list


def get_organization_ids() -> list:
    org_data_list = get_data("organizations")
    org_id_list = []
    for organization in org_data_list:
        org_id_list.append(organization['id'])
    return org_id_list


def get_device_statuses() -> list:
    org_id_list = get_organization_ids()
    dev_statuses = []
    for org_id in org_id_list:
        #print("{}/deviceStatuses".format(org_id))
        dev_statuses.extend(get_data("organizations/{}/deviceStatuses".format(org_id)))
    return dev_statuses


def main():
    pprint.pprint(get_device_statuses())


if __name__ == "__main__":
    main()
