import readchar
from meraki_get import *
import pprint


def get_clients():
    # check if device status file exists and current
    if path.isfile("clients.json"):
        file_lifetime = int((time.time() - path.getmtime("clients.json"))/3600)

        if file_lifetime > CLI_LIFE:  # get current clients, if the file is older
            nets = get_org_nets()
            clients = []
            # t1 = time.time()

            for net in nets:
                net_clients = get_data("networks/{}/clients".format(net['id']))
                for client in net_clients:
                    # network ids are added to each client
                    # where it doesn't contain in api response
                    client['net_id'] = net['id']

                clients.extend(net_clients)
                # pprint.pprint(net_clients)
            # t2 = time.time()
            # print("All clients retrieve time: {}".format(t2 - t1))

            with open("clients.json", "w") as json_file:
                json.dump(clients, json_file, indent=4)
            # t3 = time.time()
            # print("File Write Time: {}".format(t3-t2))
        else:
            with open("clients.json") as json_file:
                clients = json.load(json_file)

    else:
        nets = get_org_nets()
        clients = []
        for net in nets:
            net_clients = get_data("networks/{}/clients".format(net['id']))
            for client in net_clients:  # network ids are added to each client where it doesn't contain in api response
                client['net_id'] = net['id']
            clients.extend(net_clients)

        with open("clients.json", "w") as json_file:
            json.dump(clients, json_file, indent=4)

    return clients


def main():
    get_clients()


if __name__ == "__main__":
    main()
