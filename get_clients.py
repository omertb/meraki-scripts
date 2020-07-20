from meraki_get import *


def update_clients():
    # check if device status file exists and current
    if path.isfile("clients.json"):
        file_lifetime = int((time.time() - path.getmtime("clients.json"))/3600)

        if file_lifetime > CLI_LIFE:  # get current clients, if the file is older
            nets = get_org_nets()
            clients = []

            for net in nets:
                net_clients = get_data("networks/{}/clients".format(net['id']))
                for client in net_clients:
                    # network ids are added to each client
                    # where it doesn't contain in api response
                    client['net_id'] = net['id']

                clients.extend(net_clients)

            with open("clients.json", "w") as json_file:
                json.dump(clients, json_file, indent=4)
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


def get_clients():
    if path.isfile("clients.json"):
        with open("clients.json") as json_file:
            clients = json.load(json_file)
        return clients
    else:
        return None


def main():
    update_clients()


if __name__ == "__main__":
    main()
