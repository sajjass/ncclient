#!/usr/bin/python
from ncclient import manager
import sys

def edit_config(host):
    with manager.connect(host = host, port = 830, username = "admin", password = "", hostkey_verify=False) as m:
        edit_config_interface = '''
                                <nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
                                    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                        <interface>
                                            <name>0/1</name>
                                            <description nc:operation="create">restconf</description>
                                        </interface>
                                     </interfaces>
                                 </nc:config>
                                  '''
        c = m.edit_config(target='running', config=edit_config_interface)
        print c

if __name__ == "__main__":
    edit_config(sys.argv[1])
