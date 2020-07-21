"# meraki-scripts" 

> You should include a file named credential.py in the same directory with content as below:
```
APIKEY = "<YOUR IP KEY>"
```

1. **meraki_get.py:** _Core file included in other scripts, no need to run._

2. **get_device_status.py:** _Looks for a device with a serial number asked for your input; while saving all devices in your organization
as a json file in the same directory. (You can search by including characters)_

3. **get_clients.py:** _Retrieves all clients info in your organization and saves as a json file in the same directory._
__BEWARE!!: it retrieves one by one for each networks, so it may take some considerable time; e.g it took about 50 minutes
for about 3000 networks in an organization.__

4. **get_client_info.py:** _Finds a client against IP/MAC address and prints client specific info such as device, network,
 port, ssid... It needs **get_clients.py** script to be run in order to function._ 
 
> Mac address searches with symbols dash or colon, upper case, lower case are all valid. 
>Last for character seach without symbol is valid as well.
