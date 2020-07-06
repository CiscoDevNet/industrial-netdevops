# -*- coding: utf-8 -*-
#
# NETCONF on Cisco IR1101
# Flo Pachinger / flopach, Cisco Systems, Dec 2019
# Apache License 2.0
#
from ncclient import manager
import xmltodict
import xml.dom.minidom

#Input here the connection parameters for the IOS XE device
#Do not forget to enable RESTCONF: device(config)#netconf-yang
m = manager.connect(host="<ip address of the device>",
                    port=830,
                    username="",
                    password="",
                    hostkey_verify=False)

# get capabilities / all supported YANG models of the device
def get_capabilities():
    for c in m.server_capabilities:
        print(c)

# get the running config in XML of the device
def get_running_config():
    netconf_reply = m.get_config(source='running')
    netconf_data = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
    print(netconf_data)

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

# Enable or disable the interface of FastEthernet 4 on the IR1101
# depends on the user input
def change_interface4(v):
    config = '''
        <config>
              <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>FastEthernet0/0/4</name>
                    <enabled>false</enabled>
                </interface>
              </interfaces>
          </config>
        '''
    config_dict = xmltodict.parse(config)

    if v == int(1):
        config_dict["config"]["interfaces"]["interface"]["enabled"] = "true"
        config = xmltodict.unparse(config_dict)

    netconf_reply = m.edit_config(target='running', config=config)
    print("Did it work? {}".format(netconf_reply.ok))

# Get SCADA information from the IR1101
def set_scada_config():
    config = '''
    <config>
        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
            <scada-gw>
                <protocol xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-scada-gw">
                    <t101>
                        <config-t101>
							<channel>
								<name>testchannel101</name>
								<config-t101-channel>
									<bind-to-interface>Async0/2/0</bind-to-interface>
								</config-t101-channel>
							</channel>
							<session>
								<name>testsession101</name>
							</session>
							<sector>
								<name>testsector101</name>
							</sector>
						</config-t101>
					</t101>
					<t104>
						<config-t104>
							<channel>
								<name>testchannel104</name>
							</channel>
							<session>
								<name>testsession104</name>
							</session>
							<sector>
								<name>testsector104</name>
							</sector>
						</config-t104>
					</t104>
				</protocol>
            </scada-gw>
        </native>
      </config>
    '''
    netconf_reply = m.edit_config(target='running', config=config)
    print("Did it work? {}".format(netconf_reply.ok))

if __name__ == "__main__":
    while True:
        print("""Welcome to RESTCONF on IR1101! Here are your options
              0: Quit
              1: Get all the YANG models from the device
              2: Get running config
              3: Get status of all interfaces of the device
              4e: Enable FastEthernet 4 on IR1101
              4d: Disable FastEthernet 4 on IR1101
              5: Set predefined SCADA config to IR1101\n
              """)
        var = input("Enter: ")
        if var == "0":
            exit()
        elif var == "1":
            get_capabilities()
        elif var == "2":
            get_running_config()
        elif var == "3":
            get_allinterfaces()
        elif var == "4e":
            change_interface4(1)
        elif var == "4d":
            change_interface4(0)
        elif var == "5":
            set_scada_config()
        else:
            print("Wrong input")
        print("Done.\n")
