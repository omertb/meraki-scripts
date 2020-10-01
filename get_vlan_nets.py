#!/usr/bin/env python3
"""

"""

from meraki_get import *


def get_network_vlans(net_id) -> list:
    uri_suffix = "networks/{}/vlans".format(net_id)
    vlan_list = get_data(uri_suffix)
    return vlan_list


def get_network_name(net_id) -> dict:
    uri_suffix = "networks/{}".format(net_id)
    network_dict = get_data(uri_suffix)
    return network_dict['name']


def main():
    net_list = get_org_nets()

    with open("net_name_list.txt") as f:
        name_str = f.read()
    name_list = name_str.splitlines()

    for name in name_list:
        index = next((i for i, network in enumerate(net_list) if network['name'] == name), None)
        net_id = net_list[index]['id']
        network_name = net_list[index]['name']
        vlan_10 = next(vlan['subnet'] for vlan in get_network_vlans(net_id) if vlan['id'] == 10)
        print("{:<30} - {:<20} - {:<60}".format(net_id, vlan_10, network_name))


if __name__ == '__main__':
    main()
