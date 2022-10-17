import requests
import pprint
import json
import os
from time_functions import get_time_difference


#########################################################
###  -------- SECTION START - API REQUEST FOR DATA --------
url = "https://api.511.org/transit/StopMonitoring?api_key=b6c22a4f-6f67-4313-b2db-65b391da6d0b&stopCode=15539&agency=SF&Format=json"
payload={}
headers = {
  'Cookie': 'AWSELB=253BFF17149287196F6405573CBD843136012AF257BB1A91CC7DDE2456CF5B26B58E5C3D84C7EA58D0E8FF6B18600BD37E3B0D7E1F0E335CC2F550D9B27B9BD6DA4E75B97F',
  'content-type': 'application/json'
}
response = requests.get(url, headers=headers, data=payload)

### This API is creating an error and needs to be decode. Explanation on website below. 
### https://speedysense.com/python-fix-json-loads-unexpected-utf-8-bom-error/
decoded_data = response.text.encode().decode('utf-8-sig')
data = json.loads(decoded_data)

###  -------- SECTION END - API REQUEST FOR DATA --------
#########################################################


#########################################################
###  -------- SECTION START - FILE READING & WRITING --------
### reference link for reading & writing: https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
### reference link for  function: https://note.nkmk.me/en/python-os-path-getsize/

### utility function for reading file length
def get_number_of_files(path='.'):
  total = 0
  with os.scandir(path) as it:
    for entry in it:
        total += 1
  return total

### Serializing json
json_object = json.dumps(data, indent=4)
 
### Get the length of the folder for adding a number to the file name
folder_length = get_number_of_files("json_examples")

### Writing the file
with open(F"json_examples/example_{folder_length}.json", "w") as outfile:
    outfile.write(json_object)

### Reading the file
# Opening JSON file
with open('json_examples/no_bus_example.json', 'r') as openfile:
 
    # Reading from json file
    example_json = json.load(openfile)


###  -------- SECTION END - FILE READING & WRITING -------- 
#########################################################

#########################################################
###  -------- SECTION START - TRANSFORMING DATA --------
##### Add error handling - spefically when looking for nested object that might not be ther - this API wonky 

### Uncomment below to test an error json 
# nested_data = example_json["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]

nested_data = data["ServiceDelivery"]["StopMonitoringDelivery"]["MonitoredStopVisit"]

### check that there is a bus schedule returned
if not nested_data: 
    print("No Bus Schedule Found")
else:
    bus_number = nested_data[0]["MonitoredVehicleJourney"]["LineRef"]
    direction = nested_data[0]["MonitoredVehicleJourney"]["DirectionRef"]
    bus_stop = nested_data[0]["MonitoredVehicleJourney"]["MonitoredCall"]["StopPointName"]

    arrivals = []

    for i in nested_data:
        arrivals.append(i["MonitoredVehicleJourney"]["MonitoredCall"]["ExpectedArrivalTime"])


    # pprint.pprint(data, depth=4)

    print(f"Bus Number: {bus_number}")
    print(f"Direction: {direction}")
    print(f"Bus Stop: {bus_stop}")

    arrival_times = []
    for i in arrivals:
        arrival_times.append(get_time_difference(i))

    pprint.pprint(arrival_times)



###  -------- SECTION END - TRANSFORMING DATA --------
#########################################################