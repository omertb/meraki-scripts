"# meraki-scripts" 

> You should include a file named credential.py in the same directory with content as below:
```
APIKEY = "<YOUR IP KEY>"
```

1. **meraki_get:** _Core file included in other scripts, no need to run._
2. **get_device_status:** _Looks for a device with a serial number asked for your input; while saving all devices in your oganization
as a json file in the same directory._

3. **get_clients:** _Retrieves all clients info in your organization and saves as a json file in the same directory._
__BEWARE!!: it retrieves one by one for each networks, so it may take some considerable time; e.g it took about 50 minutes
for about 3000 networks in an organization.__
