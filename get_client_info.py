from get_clients import *
from getch import getch


def get_clients_by_mac(mac, all_clients) -> list:
    clients = list(filter(lambda client: client['mac'] == mac, all_clients))
    return clients


def get_clients_by_ip(ip, all_clients) -> list:
    clients = list(filter(lambda client: client['ip'] == ip, all_clients))
    return clients


def print_clients_info(clients):
    print("{:^17} {:^18} {:^16} {:^20} {:^20} {:^20} {:^14} {:^16} {:^25}".format("IP Address", "MAC Address", "OS",
                                                                                  "Vendor", "Device Name",
                                                                                  "Network Name", "Network Type",
                                                                                  "Vlan/Port/SSID", "Last Seen"))
    print("-" * 17, "-" * 18, "-" * 16, "-" * 20, "-" * 20, "-" * 20, "-" * 14, "-" * 14, "-" * 25)

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

        ip, mac, os, vendor, dev_name, net_name, last_seen = str(client['ip']), str(client['mac']), str(client['os']), \
                                                             str(client['manufacturer']), str(dev_name), str(net_name), \
                                                             str(client['lastSeen'])
        vendor = vendor[:19]  # strip to fit into 20 characters

        print("{:^17} {:^18} {:^16} {:^20} {:^20} {:^20} {:^14} {:^16} {:^25}".format(ip, mac, os, vendor, dev_name,
                                                                                      net_name, net_type,
                                                                                      vlan_port_ssid, last_seen))


def main():
    all_clients = get_clients()

    if all_clients is None:
        print("Run get_clients.py and wait for clients.json file to be created;\n"
              "it may take a considerable time depending on your organization (1-2 sec. for each network).")
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

            if clients is None:
                print("client not found!")
                return
            else:
                break

        elif option == 2:
            mac_addr = input("Enter a Mac address: ")
            clients = get_clients_by_mac(mac_addr, all_clients)

            if clients is None:
                print("client not found!")
                return
            else:
                break

        else:
            return

    print_clients_info(clients)


if __name__ == '__main__':
    main()

