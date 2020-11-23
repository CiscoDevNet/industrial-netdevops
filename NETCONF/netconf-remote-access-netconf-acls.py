# -*- coding: utf-8 -*-
#
# Remote Access with NETCONF + ACLs
# Flo Pachinger / flopach, Cisco Systems, May 2020
# Apache License 2.0
#
from ncclient import manager
import xmltodict
import xml.dom.minidom

m = manager.connect(host="172.19.88.15",port=830,username="cisco",password="Cisco123!",hostkey_verify=False)

# get the running config in XML of the device
def get_running_config():
    netconf_reply = m.get_config(source='running')
    netconf_data = xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml()
    print(netconf_data)

# Create the ACL
def create_remoteaccess():
    config = '''
      <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <ip>
                    <access-list>
                        <extended xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-acl">
                            <name>remote-access</name>
                            <access-list-seq-rule>
                                <sequence>10</sequence>
                                <ace-rule>
                                    <action>permit</action>
                                    <protocol>tcp</protocol>
                                    <any/>
                                    <dst-any/>
                                    <dst-eq>22</dst-eq>
                                </ace-rule>
                            </access-list-seq-rule>
                            <access-list-seq-rule>
                                <sequence>20</sequence>
                                <ace-rule>
                                    <action>permit</action>
                                    <protocol>tcp</protocol>
                                    <any/>
                                    <dst-any/>
                                    <dst-eq>830</dst-eq>
                                </ace-rule>
                            </access-list-seq-rule>
                            <access-list-seq-rule>
                                <sequence>30</sequence>
                                <ace-rule>
                                    <action>permit</action>
                                    <protocol>tcp</protocol>
                                    <any/>
                                    <dst-host>172.19.88.14</dst-host>
                                    <dst-eq>www</dst-eq>
                                </ace-rule>
                            </access-list-seq-rule>
                            <access-list-seq-rule>
                                <sequence>40</sequence>
                                <ace-rule>
                                    <action>deny</action>
                                    <protocol>ip</protocol>
                                    <any/>
                                    <dst-any/>
                                </ace-rule>
                            </access-list-seq-rule>
                        </extended>
                    </access-list>
                </ip>
            </native>
        </config>
      '''
    config_dict = xmltodict.parse(config)

    netconf_reply = m.edit_config(target='running', config=config)
    print("Did it work? {}".format(netconf_reply.ok))

# Add or delete the ACL group to the Northbound-Interface
def change_remoteaccess():
    config = '''
      <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                <interface>
                    <GigabitEthernet>
                        <name>1/3</name>
                        <ip>
                            <access-group>
                                <in>
                                    <acl>
                                        <acl-name>remote-access</acl-name>
                                        <in/>
                                    </acl>
                                </in>
                            </access-group>
                        </ip>
                    </GigabitEthernet>
                </interface>
            </native>
        </config>
      '''
    config_dict = xmltodict.parse(config)

    if int(var) == 4:
      config_dict["config"]["native"]["interface"]["GigabitEthernet"]["ip"]["access-group"]["@operation"] = "delete"
      config = xmltodict.unparse(config_dict)

    netconf_reply = m.edit_config(target='running', config=config)
    print("Did it work? {}".format(netconf_reply.ok))

if __name__ == "__main__":
    while True:
        print("""Welcome to RESTCONF on IOS XE devices! Here are your options
              0: Quit
              1: Get running config
              2: Create Remote Access ACL
              3: Enable Remote Access on Interface 1/3
              4: Disable Remote Access on Interface 1/3
              """)
        var = input("Enter: ")
        if var == "0":
            exit()
        elif var == "1":
            get_running_config()
        elif var == "2":
            create_remoteaccess()
        elif var == "3":
            change_remoteaccess()
        elif var == "4":
            change_remoteaccess()
        else:
            print("Wrong input")
        print("Done.\n")
