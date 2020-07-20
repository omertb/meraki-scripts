from get_clients import *
from getch import getch
import pprint
import pdb


def get_clients_by_mac(mac, all_clients) -> list:
    clients = list(filter(lambda client: client['mac'] == mac, all_clients))
    return clients


def get_clients_by_ip(ip, all_clients) -> list:
    clients = list(filter(lambda client: client['ip'] == ip, all_clients))
    return clients


def main():
    all_clients = get_clients()

    if all_clients is None:
        print("Run get_clients.py and wait for clients.json file to be created;\n"
              "it may take a considerable time depending on your organization (1-2 sec. for each network).")
        return

    else:
        print("Choose by which you would like to look for a client:\n"
              "1. IP\n"
              "2. MAC\n"
              "Press any key to exit\n")

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

    pprint.pprint(clients)


if __name__ == '__main__':
    main()

