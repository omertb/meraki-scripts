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
    if response.status_code == 200:
        response_list = json.loads(response.text)
        return response_list
    else:
        return None


def get_organization_ids() -> list:
    org_data_list = get_data("organizations")
    org_id_list = []
    for organization in org_data_list:
        org_id_list.append(organization['id'])
    return org_id_list


def get_templates():
    org_id_list = get_organization_ids()
    templates_dict = {}
    for org_id in org_id_list:
        templates = get_data('organizations/{}/configTemplates'.format(org_id))
        templates_dict.update({ i['name'] : i['id'] for i in templates})
    return templates_dict
        


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
    print("Number of Organizations: {}".format(len(get_organization_ids())))
    print("Number of Networks: {}".format(len(get_org_nets())))


if __name__ == "__main__":
    main()
