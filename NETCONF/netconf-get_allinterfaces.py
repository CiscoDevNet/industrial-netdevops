# -*- coding: utf-8 -*-
#
# Get all interfaces NETCONF
# Flo Pachinger / flopach, Cisco Systems, Dec 2019
# Apache License 2.0
#
from ncclient import manager
import xmltodict
import xml.dom.minidom

#Input here the connection parameters for the IOS XE device
#Do not forget to enable RESTCONF: device(config)#netconf-yang
m = manager.connect(host="<ip of the device>",
                    port=830,
                    username="",
                    password="",
                    hostkey_verify=False)

# Get the status of all interfaces of the device
def get_allinterfaces():
    filter = '''
    <filter>
          <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
          </interfaces>
      </filter>
    '''
    netconf_reply = m.get_config(source='running', filter=filter)
    netconf_data = xmltodict.parse(netconf_reply.xml)
    for x in netconf_data["rpc-reply"]["data"]["interfaces"]["interface"]:
        print("Interface: {} - enabled:{}".format(x["name"], x["enabled"]))

get_allinterfaces()