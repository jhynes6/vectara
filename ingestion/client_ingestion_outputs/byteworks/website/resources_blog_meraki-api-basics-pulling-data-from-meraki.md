---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/meraki-api-basics-pulling-data-from-meraki/"
title: "Meraki API Basics – Pulling Data from Meraki"
domain: "www.byteworks.com"
path: "/resources/blog/meraki-api-basics-pulling-data-from-meraki/"
scraped_time: "2025-10-05T02:01:54.654865"
url_depth: 3
word_count: 1799
client_name: "byteworks"
---

# Meraki API Basics – Pulling Data from Meraki

Anybody who has used Meraki knows that at times it can be tough to pull data from and if you want data and information from multiple devices it can take a lot of clicks. However, Meraki has a really good API that can give a better way of pulling data and updating data on Meraki that can be a lot quicker than the GUI, especially when spanned over multiple devices and networks.

So for this article, we are going to go through how to pull all the switch port configurations and running states from a Meraki switch. We will be using python for this and while this isn’t a python blog we are not going to use anything very complex so it should be understood what we are doing even if you are new to python. To help with this we are going to use the Meraki library available for python which makes the code shorter and more readable. We are also going to focus a lot on how to use the Meraki API documentation so that when we finish you should be able to look up other things with fairly simple modifications to the code we are going to work on. For this, we are going to use the Meraki devnet sandbox so you can run any of the code here yourself and it should work. Be aware that Meraki doesn’t rate-limit the sandbox so sometimes if a script fails it may just need to be re-run due to failure from rate-limiting.

Our final goal for this is to retrieve port configs and the port running states for all ports on switch ms01-dl1 which is in-network DevNetLab in the organization DeLab.

So the first step here is to get a list of organizations. With the devnet sandboxes found on developer.cisco.com there is a Meraki API key available there we can use for those. In a production environment, you’d need to go into your Meraki account and org and create your own personal API key. Here we are using 6bec40cf957de430a6f1f2baa056b99a4fac9ea0.

Next, we need to see what query needs to run so we go to the Meraki API documentation at https://developer.cisco.com/meraki/api-v1/. From here navigate to Endpoint -> API -> Organizations and click on “Get Organizations”. Now right off this screen if you expand headers and see “X-Cisco-Meraki-API-Key” you can put in the API key above and hit run and it will run the query and display the results. All pages in the documentation support this and it is very useful. However, we want to run this in python so again on the right-hand pane hit “templates” then “Meraki Python library” You will get the below

```python
import meraki

# Defining your API key as a variable in source code is not recommended
API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY)

response = dashboard.organizations.getOrganizations()

print(response)
```

I am going to add a few lines to make the output easier to read by adding “pprint” which stands for “pretty print” so the final code is

```python
import meraki
from pprint import pprint

# Defining your API key as a variable in source code is not recommended
API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY)

response = dashboard.organizations.getOrganizations()

pprint(response)
```

This code is taking the API key and then runs a query to the dashboard to pull all organizations. Note that if you have never used the Meraki library you may need to run “pip install meraki” to install it. When we run it we get a lot of organizations including this one that we want.

```json
{'api': {'enabled': True},
  'cloud': {'region': {'name': 'North America'}},
  'id': '681155',
  'licensing': {'model': 'per-device'},
  'name': 'DeLab',
  'url': 'https://n392.meraki.com/o/49Gm_c/manage/organization/overview'}
```

So there are the details on the DeLab organization we are looking for and the field here we mostly care about is the id number which we can then use to pull the list of networks. Do we have to manually do this search and then manually add in the id number? Nope. So what we are going to do is write a simple loop to check all of the organizations returned by the getOrganizations() functions, find the one called DeLab, and save its id number. The code for this looks like the below.

```python
import meraki
from pprint import pprint

# Defining your API key as a variable in source code is not recommended
API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY)

orgs = dashboard.organizations.getOrganizations()

for org in orgs:
    if 'DeLab' in org['name']:
        orgID = org['id']

print (orgID)
```

And after this is run we get the output we wanted with “681155” as the output which matches the id above.

So next step is to retrieve the list of networks and find the network we are looking for. If you go back to the documentation and go to Endpoints -> API -> Organizations -> Networks you will see the query “get all networks” and on the right again we can go to templates and Meraki python library and see the query that we need. So to the code above we are simply going to add the exact same construct as for organizations to search networks for the network we want so we add in the code below.

```python
networks = dashboard.organizations.getOrganizationNetworks(orgID)

for network in networks:
    if "DevNetLab" in network['name']:
        netID = network['id']

print (netID)
```

Now when we run this we get “L_783626335162466515” which is the network ID for DevNetLab.

So the final iteration of this, we need to search through all of the devices in that network and look for the switch we want to get data from. The documentation for this is under Endpoints -> API -> Networks -> Devices and you should see “Get Network Devices” and the template Meraki library function of “dashboard.networks.getNetworkDevices( network_id )”. So we are simply going to do the same thing a third time looking for the switch in question with the following addition.

```python
devices = dashboard.networks.getNetworkDevices(netID)

for device in devices:
    if "ms01-dl3" in device['name']:
        serial = device['serial']

print (serial)
```

And when run we get the serial number Q2HP-W3HC-2C8D.

Now to the fun part of pulling all the configurations from the switch. So in the documentation, we want to go to Endpoints -> API -> Products -> Switch -> Configure and you should see “get device switch ports”. If you look at the API call on that screen you’ll see the parameter that needs to be passed is the serial number which is why we grabbed the serial above. Template -> Meraki Python Library shows us the query is “dashboard.switch.getDeviceSwitchPorts(serial)” so let’s add that to the code we already have wit

```python
portconfig = dashboard.switch.getDeviceSwitchPorts(serial)

pprint (portconfig)
```

That is it. Just two lines and we get a ton of information about how all the ports on this switch are configured. As an example, this is port 1 at the time I ran this

```json
{'accessPolicyType': 'Open',
  'allowedVlans': 'all',
  'enabled': True,
  'isolationEnabled': False,
  'linkNegotiation': 'Auto negotiate',
  'linkNegotiationCapabilities': ['Auto negotiate',
                                  '1 Gigabit full duplex (forced)',
                                  '100 Megabit (auto)',
                                  '100 Megabit half duplex (forced)',
                                  '100 Megabit full duplex (forced)',
                                  '10 Megabit (auto)',
                                  '10 Megabit half duplex (forced)',
                                  '10 Megabit full duplex (forced)'],
  'name': None,
  'poeEnabled': True,
  'portId': '1',
  'portScheduleId': None,
  'rstpEnabled': True,
  'stpGuard': 'disabled',
  'tags': [],
  'type': 'trunk',
  'udld': 'Alert only',
  'vlan': 1,
  'voiceVlan': None},
```

Now we also want to grab what the current state of this port is so again going back to the documentation Endpoints -> API -> Products -> Switch -> Monitor -> ports and you should see “Get Device Switch port statuses” and on the right, under template and Meraki library we find the function as dashboard.switch.getDeviceSwitchPortsStatuses(serial) so let’s go try that. Again only two real lines are needed here

```python
portstatus = dashboard.switch.getDeviceSwitchPortsStatuses(serial)

pprint (portstatus)
```

And from that, we then get details on the current status of all the ports. Below is port 1 when I ran this

```json
{'cdp': {'address': '192.168.128.7',
          'capabilities': 'Router, Switch',
          'deviceId': '0c8ddbb277f8',
          'platform': 'Meraki MR52 Cloud Managed AP',
          'portId': 'Port 0',
          'version': '1'},
  'clientCount': 1,
  'duplex': 'full',
  'enabled': True,
  'errors': [],
  'isUplink': False,
  'lldp': {'chassisId': '0c:8d:db:b2:77:f8',
           'portDescription': 'eth0',
           'portId': '0',
           'systemCapabilities': 'Two-port MAC Relay',
           'systemDescription': 'Meraki MR52 Cloud Managed AP',
           'systemName': 'Meraki MR52 - ap01-dl1'},
  'portId': '1',
  'powerUsageInWh': 169.8,
  'secureConnect': {'active': False,
                    'authenticationStatus': 'Disabled',
                    'configOverrides': {},
                    'enabled': False},
  'speed': '1 Gbps',
  'status': 'Connected',
  'trafficInKbps': {'recv': 2.1, 'sent': 1.5, 'total': 3.6},
  'usageInKb': {'recv': 22807, 'sent': 15766, 'total': 38573},
  'warnings': []},
 {'clientCount': 1,
  'duplex': 'full',
  'enabled': True,
  'errors': [],
  'isUplink': True,
  'lldp': {'chassisId': '0c:8d:db:b0:c2:dc',
           'portDescription': 'lan port 0',
           'portId': '0',
           'systemCapabilities': '',
           'systemDescription': 'Meraki MX65 Cloud Managed Router',
           'systemName': 'Meraki MX65 - mx01-dl1'},
  'portId': '2',
  'powerUsageInWh': 0.0,
  'secureConnect': {'active': False,
                    'authenticationStatus': 'Disabled',
                    'configOverrides': {},
                    'enabled': False},
  'speed': '1 Gbps',
  'status': 'Connected',
  'trafficInKbps': {'recv': 2.1, 'sent': 4.0, 'total': 6.1},
  'usageInKb': {'recv': 22732, 'sent': 42904, 'total': 65636},
  'warnings': []},
```

Hopefully, you are starting to see that after we get through the initial exercise of getting org numbers and network numbers and so forth that pulling data is really pretty easy and can be as easy as finding in the docs the data you want and adding the query line.

Before we leave I’m going to make one modification that also shows how automation can help save time in gathering data. So this time instead of pulling data from just one switch we are going to modify it to pull data from ALL switches within a specific network. So to do this we are going to modify the look for devices that instead of looking for name matching out switch it looks for model contains “ms” (for Meraki switch) and runs the above two commands on everything that is “MS”. With that change, the final complete code looks like

```python
import meraki
from pprint import pprint

# Defining your API key as a variable in source code is not recommended
API_KEY = '6bec40cf957de430a6f1f2baa056b99a4fac9ea0'
# Instead, use an environment variable as shown under the Usage section
# @ https://github.com/meraki/dashboard-api-python/

dashboard = meraki.DashboardAPI(API_KEY)

orgs = dashboard.organizations.getOrganizations()

for org in orgs:
    if 'DeLab' in org['name']:
        orgID = org['id']

print (orgID)

networks = dashboard.organizations.getOrganizationNetworks(orgID)

for network in networks:
    if "DevNetLab" in network['name']:
        netID = network['id']

print (netID)

devices = dashboard.networks.getNetworkDevices(netID)

for device in devices:
    if "MS" in device['model']:
        serial = device['serial']
        portconfig = dashboard.switch.getDeviceSwitchPorts(serial)
        pprint (portconfig)
        portstatus = dashboard.switch.getDeviceSwitchPortsStatuses(serial)
        pprint (portstatus)
```

Hopefully, this gives you a good starting point for being able to use the Meraki API to pull data. In a future blog, we will go over how to use the API to make changes.