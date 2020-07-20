#!/usr/bin/env python3
"""

"""
import requests
import json
from credential import *
from constants import *
from os import path
import time

# suppress certificate verification warnings
# requests.packages.urllib3.disable_warnings()

cred_header = {
    'X-Cisco-Meraki-API-Key': APIKEY
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


def get_org_nets() -> list:
    org_id_list = get_organization_ids()
    nets_list = []

    # check if networks file exists and current
    if path.isfile("org_networks.json"):
        file_lifetime = int((time.time() - path.getmtime("org_networks.json"))/3600)

        if file_lifetime > NET_LIFE:  # get current networks, if the file is older
            for org in org_id_list:
                nets_list.extend(get_data("organizations/{}/networks".format(org)))
            with open("org_networks.json", "w") as json_file:
                json.dump(nets_list, json_file, indent=4)
        else:
            with open("org_networks.json") as json_file:
                nets_list = json.load(json_file)

    else:
        for org in org_id_list:
            nets_list.extend(get_data("organizations/{}/networks".format(org)))
        with open("org_networks.json", "w") as json_file:
            json.dump(nets_list, json_file, indent=4)

    return nets_list


def main():
    get_org_nets()


if __name__ == "__main__":
    main()
