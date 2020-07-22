from get_clients import *
from getch import getch
import pprint


# Deauthentication Reason Code Table
reason_codes = {
    '0' : 'Reserved.',
    '1' : 'Unspecified reason.',
    '2' : 'Previous authentication no longer valid.',
    '3' : 'Deauthenticated because sending station (STA) is leaving or has left Independent Basic Service Set (IBSS) or ESS.',
    '4' : 'Disassociated due to inactivity.',
    '5' : 'Disassociated because WAP device is unable to handle all currently associated STAs.',
    '6' : 'Class 2 frame received from nonauthenticated STA.',
    '7' : 'Class 3 frame received from nonassociated STA.',
    '8' : 'Disassociated because sending STA is leaving or has left Basic Service Set (BSS).',
    '9' : 'STA requesting (re)association is not authenticated with responding STA.',
    '10' : 'Disassociated because the information in the Power Capability element is unacceptable.',
    '11' : 'Disassociated because the information in the Supported Channels element is unacceptable.',
    '12' : 'Disassociated due to BSS Transition Management.',
    '13' : 'Invalid element, that is, an element defined in this standard for which the content does not meet the specifications in Clause 8.',
    '14' : 'Message integrity code (MIC) failure.',
    '15' : '4-Way Handshake timeout.',
    '16' : 'Group Key Handshake timeout.',
    '17' : 'Element in 4-Way Handshake different from (Re)Association Request/Probe Response/Beacon frame.',
    '18' : 'Invalid group cipher.',
    '19' : 'Invalid pairwise cipher.',
    '20' : 'Invalid AKMP.',
    '21' : 'Unsupported RSNE version.',
    '22' : 'Invalid RSNE capabilities.',
    '23' : 'IEEE 802.1X authentication failed.',
    '24' : 'Cipher suite rejected because of the security policy.'
}

def get_clients_by_mac(mac, all_clients) -> list:
    clients = list(filter(lambda client: client['mac'].replace(":", "").endswith(mac), all_clients))
    return clients


def get_clients_by_ip(ip, all_clients) -> list:
    clients = list(filter(lambda client: client['ip'] == ip, all_clients))
    return clients


def get_client_events(client) -> list:
    cli_id = client['id']
    net_id = client['net_id']
    events = get_data("networks/{}/clients/{}/events".format(net_id, cli_id))
    return events


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


def chunk_string(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def print_client_events(events):
    print("\n### Related Event Logs ###")
    print("{:<25} {:^20} {:^12} {:^30} {:^20} {:^40}".format("Log Time", "Client MAC Address", "Chnl/RSSI/VL",
                                                             "DNS/DHCP", "DHCP MAC Address", "Event Log"))
    print("-" * 25, "-" * 20, "-" * 12, "-" * 30, "-" * 20, "-" * 40)
    for event in events:
        log_time = time.ctime(event['occurredAt'])
        cli_mac = event['details']['clientMac']
        rssi, channel, vlan, dns_ip, dhcp_ip, dhcp_mac, reason = 'na', 'na', 'na', 'na', 'na', 'na', 'na'

        if event['type'] == '802.11 association':
            rssi = event['details']['rssi']
            channel = event['details']['channel']

        elif event['type'] == 'WPA authentication':
            pass

        elif event['type'] == 'WPA deauthentication':
            pass

        elif event['type'] == '802.11 disassociation':
            reason = reason_codes[event['details']['reason']]
            dns_ip = event['details']['dnsServer'] if 'dnsServer' in event['details'] else 'na'
            dhcp_ip = event['details']['dhcpServer']
            dhcp_mac = event['details']['dhcpServerMac']
            channel = event['details']['channel']

        elif event['type'] == 'DHCP lease':
            dns_ip = event['details']['dns']
            dhcp_ip = event['details']['serverIp']
            dhcp_mac = event['details']['serverMac']
            vlan = event['details']['vlan']

        else:
            print("Unknown Event Type, review needed:")
            print(event)
            return

        cha_rss_vla = channel + "/" + rssi + "/" + vlan
        dns_dhcp = dns_ip + "/" + dhcp_ip

        event_log = event['type'] + ": " + reason
        event_log_list = list(chunk_string(event_log, 40))

        print("{:<25} {:^20} {:^12} {:^30} {:^20}".format(log_time, cli_mac, cha_rss_vla, dns_dhcp, dhcp_mac), end = '')
        print("{:<40}".format(event_log_list[0]))
        for line in event_log_list[1:]:
            print("{:111}{:<40}".format("", line))


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

    # get client events
    client_events = []
    for client in clients:
        client_events.extend(get_client_events(client))

    if not client_events:
        print("Client related logs not found.")
        return
    else:
        print_client_events(client_events)


if __name__ == '__main__':
    main()

