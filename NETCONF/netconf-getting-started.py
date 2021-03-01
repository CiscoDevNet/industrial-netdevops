# -*- coding: utf-8 -*-
#
# NETCONF getting started
# Flo Pachinger / flopach, Cisco Systems, Dec 2019
# Apache License 2.0
#
from ncclient import manager
import xmltodict
import xml.dom.minidom
import lxml.etree as ET

#Input here the connection parameters for the IOS XE device
#Do not forget to enable NETCONF: device(config)#netconf-yang
m = manager.connect(host="10.10.20.48",
                    port=830,
                    username="developer",
                    password="C1sco12345",
                    hostkey_verify=False)

print("Connected.")

# get the running config in XML of the device
def get_running_config():
    netconf_reply = m.get_config(source='running')
    netconf_data = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
    print(netconf_data)

# get hostname and IOS version of the device - loading the whole config
# this should take longer
def get_hostname():
    netconf_reply = m.get_config(source='running')
    netconf_data = xmltodict.parse(netconf_reply.xml)
    print("IOS Version: {}".format(netconf_data["rpc-reply"]["data"]["native"]["version"]))
    print("Hostname: {}".format(netconf_data["rpc-reply"]["data"]["native"]["hostname"]))

# get hostname and IOS version of the device - using a filter
# this should be faster
def get_hostname_filter():
    filter = '''
    <filter xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
          <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
              <hostname></hostname>
              <version></version>
          </native>
      </filter>
    '''
    netconf_reply = m.get_config(source='running', filter=filter)
    netconf_data = xmltodict.parse(netconf_reply.xml)
    print("IOS Version: {}".format(netconf_data["rpc-reply"]["data"]["native"]["version"]))
    print("Hostname: {}".format(netconf_data["rpc-reply"]["data"]["native"]["hostname"]))

# get capabilities / all supported YANG models of the device
def get_capabilities():
    for c in m.server_capabilities:
        print(c)

# change interface GigabitEthernet3
# 0 --> disable | 1 --> enable
def change_interface(user_selection):
  config = '''
      <config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
              <interface>
                  <name>GigabitEthernet3</name>
                  <enabled>false</enabled>
              </interface>
            </interfaces>
    </config>
      '''
  config_dict = xmltodict.parse(config)

  if int(user_selection) == 1:
      config_dict["config"]["interfaces"]["interface"]["enabled"] = "true"
      config = xmltodict.unparse(config_dict)

  netconf_reply = m.edit_config(target='running', config=config)
  print("Did it work? {}".format(netconf_reply.ok))

# copy run start
def save_running_config():
    rpc_body = '''<cisco-ia:save-config xmlns:cisco-ia="http://cisco.com/yang/cisco-ia"/>'''
    netconf_reply = m.dispatch(ET.fromstring(rpc_body)).xml 
    print("Did it work? {}".format(netconf_reply))

if __name__ == "__main__":
    while True:
        print("""Welcome to NETCONF on IOS XE devices! Here are your options
              0: Quit
              1: Get running config
              2: Get hostname and IOS version (whole config)
              3: Get hostname and IOS version (filter used)
              4: Get all the YANG models from the device
              5: Enable GigabitEthernet3
              6: Disable GigabitEthernet3
              7: Save the running-configuration
              """)
        var = input("Enter: ")
        if var == "0":
            exit()
        elif var == "1":
            get_running_config()
        elif var == "2":
            get_hostname()
        elif var == "3":
            get_hostname_filter()
        elif var == "4":
            get_capabilities()
        elif var == "5":
            change_interface(1)
        elif var == "6":
            change_interface(0)
        elif var == "7":
            save_running_config()
        else:
            print("Wrong input")
        print("Done.\n")
