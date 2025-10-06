---
source: "website"
content_type: "blogs_resources"
url: "https://www.byteworks.com/resources/blog/using-meraki-api-to-edit-and-add-data/"
title: "Using Meraki API to Edit and Add Data"
domain: "www.byteworks.com"
path: "/resources/blog/using-meraki-api-to-edit-and-add-data/"
scraped_time: "2025-10-05T02:01:13.545560"
url_depth: 3
word_count: 1468
client_name: "byteworks"
---

# Using Meraki API to edit and add data

In a previous blog post, we discussed how to read data from the Meraki API. This time we will build on that and now add and edit Meraki data through the API. The first question that may come to mind is why one would want to use the API vs just using the Meraki dashboard. One reason is it can give you predictable results you can use multiple times. I had a customer recently where we wanted to add the same two SSIDs to 30 different Meraki networks. You could do that by hand, but it is tedious, and there is no guarantee you do the exact same thing every time. So in that case we built the SSID on one network and tested it, then pulled the XML for that config and wrote a script to push that same config to all the networks. So it can save time and improve accuracy.

For this blog post, we’re going to go over another script done recently that is mostly in the time-saving category. In this one, we had a customer who was adding over 100 APs. The installer created a spreadsheet with serial numbers, room numbers, building numbers, and lots of other data. The goal was to add all those APs to Meraki, move them to the wireless network, and rename them based on building and room number. Again, this can be done through the dashboard, but we’d prefer not to have to enter in a bunch of serial numbers and AP names if we can avoid it. This script does use a python library called pandas to read the excel spreadsheet and does a little data manipulation to get some of it in the right format. We will not be covering those pieces in-depth, but we are leaving them here for completeness. if you would like to learn more about pandas and data formats, there are lots of good python resources on those.

So let’s get started. The first section of the code here is almost identical to the last blog post in getting the organization ID and the network ID and also loading in the python libraries we’re going to use Since this script was running on a production network we did not hard code the API key into the script and simply prompted the user to enter it which is a good way to do it on a script that will be run manually. We won’t use these till later on in the script, but we do like to go on and grab them early.

```python
import pandas as pd
import meraki
from pprint import pprint

API_KEY=input ("enter API Key: ")

dashboard = meraki.DashboardAPI(API_KEY)

orgs = dashboard.organizations.getOrganizations()

for org in orgs:
    if 'West Georgia Technical College' in org['name']:
        orgID = org['id']

print (orgID)

networks = dashboard.organizations.getOrganizationNetworks(orgID)

for network in networks:
    if "WGTC - wireless" in network['name']:
        netID = network['id']

print (netID)
```

You can see the prior blog for details on what we are doing here but in the end, The orgID will have the organization ID and netID will have the network ID which we will use later.

```python
workbook = pd.read_excel(‘~/Downloads/AP.xlsx’,sheet_name=0)
```

This line is just to open the excel spreadsheet, and the data will be used later. “sheet-name=0” simply pulls up the first tab. The spreadsheet is one where the first row is column headings, and the other rows have the data. Pandas will recognize this and then later on let us pull data by column header which is why you’ll see in the rest of the code why things can be pulled by name.

The next thing we are going to do is start a loop that loops through all of the rows in the spreadsheet that have data. In this case, iteration is the variable I really care about since that will be used to cycle through the rows of the spreadsheet. Then we take the serial number of the current row and put it in serial, and AP_Name becomes the AP name (the logic is room 100 of building 123 would be called AP100123.

```python
for iteration, AP in enumerate(workbook['Serial Number ']):
    serial = [str(workbook['Serial Number '].iloc[iteration])]
    if serial.lower() != "nan":
        AP_Name = "AP" + str(int(workbook['BLDG#'].iloc[iteration])) + str(workbook['Room#'].iloc[iteration])
        print (AP_Name)
```

So at this point, we have our organization ID, Network ID, serial number of this specific AP, and what name we want the AP to have. That is all the information we need, and now we can start actually making the changes on Meraki. It is important to point out that the serial number has square brackets around it. This is important and required. The reason is that the first two functions we will call (claim device and add the device to the network) can be called with multiple serial numbers in a single API call. So if multiple can be sent that must be enclosed in square brackets. Then if you were sending more than the one you’d have the serials comma separated in the list like ([AAAA-AAAA-AAAA, BBBB-BBBB-BBBB, CCCC-CCCC-CCCC]. Since we are using a loop, we are just sending the one serial number per API call, but it still needs to be in square brackets since it is still a list even if it only has one entry.

The first step is to claim the AP. If you want to see the details, go to https://developer.cisco.com/meraki/api-latest/#!introduction/meraki-dashboard-api and API->Organizations->Configure->Inventory->Claim into organization inventory. On the right, you can select template -> Meraki python library and see sample code for what we are using. If you are on that page and check on “schema definition” on the left, you will see where it lists “serials” as an array and even indicates the square brackets. That is how you can know it needs to be enclosed in the square brackets like above.

Now let’s look at the code.

```python
try:
            response = dashboard.organizations.claimIntoOrganizationInventory(
                orgID, 
                serials=serial
            )
        except:
            print ("error has occurred")

        print(response)
```

That is really all there is to it on the API code. We simply pass the organization ID and the serial and it gets claimed. This same API call can also be passed order numbers or license information as well. Getting all the data that you need is the toughest part. Actually calling the APIs is a very simple process. The try is there so if somebody had already claimed one of the serials or we needed to run the script a second time an error from Meraki like “serial has already been claimed” won’t crash the program. It will simply output there was an error and continue.

Next, we will add the AP to the network it needs to go into, and we already grabbed that number earlier in the script. Documentation on this function is at API->Networks->Configure->Devices->Claim Network Devices.

```python
try:
            response = dashboard.networks.claimNetworkDevices(
                netID, serials=serial
            )
        except:
            print ("error has occurred")

        print(response)
```

Again, like above very straightforward. Just pass the serial number (or numbers) and the network ID, and it gets added to the network.

The final piece of this script was to rename the AP. Now, this function can only be done on one serial number at a time, so the first time is going to be to remove the square brackets from the serial number before passing it to the API call. Documentation is at API->Devices->Configuration->Update Devices. If you look at the documentation while in this case, we are just changing the name, this same function can change a lot of other things on the device like tags, latitude, longitude, or floorplan ID. So let’s look at the code.

```python
serial = workbook['Serial Number '].iloc[iteration]
        print (serial)

        try:
            response = dashboard.devices.updateDevice(
                serial, 
                name=AP_Name
            )
        except:
            print ("error has occurred")

        print (response)
```

The Meraki API library just makes this all very easy to do. Just pass serial and tell it you want to change the name. Simple as that.

The net result of this script is that once we ran it, all 120 APs got claimed, added to the wireless network, and renamed per the naming convention in just a few minutes. That is definitely a time saver.

Going to close with just the last section of code here we had in the script which just did a pull for the AP data after the above was run just so we have a copy of the final end state config for each device. Since we are just retrieving data all that is needed is just the serial number. Hopefully, this has been helpful in showing how easy the Meraki API with Meraki python library is to use and how it can be used to save a bunch of time on tedious tasks to give yourself time to work on more complicated tasks.