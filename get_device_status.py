#!/usr/bin/env python3
"""

"""

from meraki_get import *


def get_devices_sts() -> list:
    org_id_list = get_organization_ids()
    dev_statuses = []
    for org_id in org_id_list:
        dev_statuses.extend(get_data("organizations/{}/deviceStatuses".format(org_id)))
    return dev_statuses


def get_devices():
    # check if devices status file exists and current
    if path.isfile("devices_status.json"):
        file_lifetime = int((time.time() - path.getmtime("devices_status.json"))/3600)

        if file_lifetime > DEV_LIVE:  # get current devices status, if the file is older
            devices = get_devices_sts()
            with open("devices_status.json", "w") as json_file:
                json.dump(devices, json_file, indent=4)
        else:
            with open("devices_status.json") as json_file:
                devices = json.load(json_file)

    else:
        devices = get_devices_sts()
        with open("devices_status.json", "w") as json_file:
            json.dump(devices, json_file, indent=4)
    ##
    return devices


def search_device(serial) -> list:
    devices = get_devices()
    found_devices = []
    for device in devices:
        if serial in device['serial']:
            device['net_name'] = get_data("networks/{}".format(device['networkId']))['name']
            found_devices.append(device)

    return found_devices


def print_device_info(serial):
    found_devices = search_device(serial)
    if not found_devices:
        print("Device not found")
        return
    else:
        print("{:^20} {:^20} {:^20} {:^20} {:^20} {:^20} {:^25}".format("Name", "Serial", "Mac Address",
                                                                        "Public IP", "Network Name", "Status",
                                                                        "Last Seen"))
        print("-" * 20, "-" * 20, "-" * 20, "-" * 20, "-" * 20, "-" * 20, "-" * 25)
        for device in found_devices:
            dev_name, dev_ser, dev_mac, dev_pub, \
            dev_net, dev_status, last_seen = str(device['name']), str(device['serial']), str(device['mac']), \
                                             str(device['publicIp']), str(device['net_name']), str(device['status']), \
                                             str(device['lastReportedAt'])
            print("{:20} {:^20} {:^20} {:^20} {:<20} {:^20} {:>25}".format(dev_name, dev_ser, dev_mac,
                                                                           dev_pub, dev_net, dev_status, last_seen))


def main():
    serial = input("Enter Device Serial Number: ")
    serial = serial.upper()
    print_device_info(serial)


if __name__ == "__main__":
    main()
