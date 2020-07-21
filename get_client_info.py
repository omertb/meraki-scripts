from get_clients import *
from getch import getch


def get_clients_by_mac(mac, all_clients) -> list:
    clients = list(filter(lambda client: client['mac'].replace(":", "").endswith(mac), all_clients))
    return clients


def get_clients_by_ip(ip, all_clients) -> list:
    clients = list(filter(lambda client: client['ip'] == ip, all_clients))
    return clients


def print_clients_info(clients):
    print("{:^17} {:^18} {:^14} {:^20} {:^20} {:^20} {:^14} {:^16} {:^22} {:^8}".format("IP Address", "MAC Address",
                                                                                        "OS", "Vendor", "Device Name",
                                                                                        "Network Name", "Network Type",
                                                                                        "Vlan/Port/SSID", "Last Seen",
                                                                                        "Status"))
    print("-" * 17, "-" * 18, "-" * 14, "-" * 20, "-" * 20, "-" * 20, "-" * 14, "-" * 16, "-" * 22, "-" * 8)

    for client in clients:
        # dev_name = next((device['name'] for device in devices if device['name'] == client['recentDeviceSerial']), None)
        dev_name = str(client['recentDeviceName'])
        # net_idx = next((i for i, network in enumerate(networks)
        #                          if network["id"] == client['net_id']), None)

        net_type = str(client['net_type'])  # str(networks[net_idx]['type'])
        net_name = str(client['net_name'])  # str(networks[net_idx]['name'])
        vlan = str(client['vlan'])
        ssid = str(client['ssid'])
        port = str(client['switchport'])
        vlan_port_ssid = vlan + "/" + port + "/" + ssid

        ip, mac, status, vendor, dev_name, \
        net_name, last_seen, os = str(client['ip']), str(client['mac']), str(client['status']), \
                                  str(client['manufacturer']), str(dev_name), str(net_name), \
                                  str(client['lastSeen']), str(client['os'])

        vendor = vendor[:20]  # strip to fit into 20 characters

        print("{:^17} {:^18} {:^14} {:^20} {:^20} "
              "{:^20} {:^14} {:^16} {:^22} {:^8}".format(ip, mac, os, vendor, dev_name, net_name, net_type,
                                                         vlan_port_ssid, last_seen, status))


def main():
    all_clients = get_clients()

    if all_clients is None:
        print("Run get_clients.py and wait for clients.json file to be created;\n"
              "it may take a considerable time depending on the size of your organization (1 sec. for each network).")
        return

    else:
        print("\nChoose by which you would like to look for a client:\n"
              "1. IP\n"
              "2. MAC\n"
              "\nPress any key to exit\n")

    while True:
        option = getch()

        try:
            option = int(option)
        except ValueError:
            quit()

        if option == 1:
            ip_addr = input("Enter an ip address: ")
            clients = get_clients_by_ip(ip_addr, all_clients)

            if not clients:
                print("\nClient not found!")
                return
            else:
                break

        elif option == 2:
            mac_addr = input("Enter a Mac address: ")
            mac_addr = mac_addr.lower().replace(":", "").replace("-", "")
            clients = get_clients_by_mac(mac_addr, all_clients)

            if not clients:
                print("\nClient not found!")
                return
            else:
                break

        else:
            return

    print_clients_info(clients)


if __name__ == '__main__':
    main()

