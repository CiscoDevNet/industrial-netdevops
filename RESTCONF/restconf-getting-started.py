# -*- coding: utf-8 -*-
#
# RESTCONF getting started
# Flo Pachinger / flopach, Cisco Systems, Dec 2019
# Apache License 2.0
#
import requests
import json

#Input here the connection parameters for the IOS XE device
#Do not forget to enable RESTCONF: device(config)#restconf
host = '10.10.20.48'
port = 443
username = 'developer'
password = 'C1sco12345'


# get the running config in XML of the device
def get_running_config_json():
    url = "https://{h}:{p}/restconf/data/Cisco-IOS-XE-native:native".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+json"}
    response = requests.get(url, auth=(username, password),headers=headers, verify=False)
    print(response.text)

# get the running config in XML of the device
def get_running_config_xml():
    url = "https://{h}:{p}/restconf/data/Cisco-IOS-XE-native:native".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+xml"}
    response = requests.get(url, auth=(username, password),headers=headers, verify=False)
    print(response.text)

# get the hostname of the device
def get_hostname():
    url = "https://{h}:{p}/restconf/data/Cisco-IOS-XE-native:native/hostname".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+json"}
    response = requests.get(url, auth=(username, password),headers=headers, verify=False)
    print(response.text)

# get all the YANG models
def get_yangmodels():
    url = "https://{h}:{p}/restconf/data/netconf-state/capabilities".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+json"}
    response = requests.get(url, auth=(username, password),headers=headers, verify=False)
    print(json.dumps(response.json(),indent=4))

# get all interfaces
def get_allinterfaces():
    url = "https://{h}:{p}/restconf/data/ietf-interfaces:interfaces".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+json"}
    response = requests.get(url, auth=(username, password),headers=headers, verify=False)
    print(json.dumps(response.json(),indent=4))

# get all interfaces and the enabled/disabled status
def get_allinterfaces_status():
    url = "https://{h}:{p}/restconf/data/ietf-interfaces:interfaces".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+json"}
    response = requests.get(url, auth=(username, password),headers=headers, verify=False)
    jsondata = json.loads(response.content)

    #Request all information an cycle through each interface
    for item in jsondata["ietf-interfaces:interfaces"]["interface"]:
        if "name" in item:
            int_name = item["name"]
        if "enabled" in item:
            int_status = item["enabled"]
        print("{} - enabled: {}".format(int_name,int_status))

# change interface GigabitEthernet3
# 0 --> disable | 1 --> enable
def change_interface(user_selection):
    if int(user_selection) == 1:
        int_status = "true"
    else:
        int_status = "false"

    url = "https://{h}:{p}/restconf/data/ietf-interfaces:interfaces/interface=GigabitEthernet3".format(h=host, p=port)
    headers = { "Content-Type" : "application/yang-data+json", "Accept" : "application/yang-data+json"}
    config = """ 
    {
      "ietf-interfaces:interface": {
          "name": "GigabitEthernet3",
          "type": "iana-if-type:ethernetCsmacd",
          "enabled": """+int_status+"""
      }
    }
    """

    response = requests.put(url, auth=(username, password),headers=headers, data=config, verify=False)
    print(response.status_code)

# copy running-configuration startup-configuration
def save_running_config():
    url = "https://{h}:{p}/restconf/operations/cisco-ia:save-config".format(h=host, p=port)
    headers = { "Accept" : "application/yang-data+json"}
    response = requests.post(url, auth=(username, password),headers=headers, verify=False)
    print(response.status_code)

if __name__ == "__main__":
    while True:
        print("""Welcome to RESTCONF on IOS XE devices! Here are your options
              0: Quit
              1: Get running config (JSON)
              2: Get running config (XML)
              3: Get the hostname
              4: Get all YANG models
              5: Get all Interfaces
              6: Get the status of all interfaces
              7: Enable GigabitEthernet3
              8: Disable GigabitEthernet3
              9: Save the running-configuration
              """)
        var = input("Enter: ")
        if var == "0":
            exit()
        elif var == "1":
            get_running_config_json()
        elif var == "2":
            get_running_config_xml()
        elif var == "3":
            get_hostname()
        elif var == "4":
            get_yangmodels()
        elif var == "5":
            get_allinterfaces()
        elif var == "6":
            get_allinterfaces_status()
        elif var == "7":
            change_interface(1)
        elif var == "8":
            change_interface(0)
        elif var == "9":
            save_running_config()
        else:
            print("Wrong input")
        print("Done.\n")
