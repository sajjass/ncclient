#!/usr/bin/python
from ncclient import manager
import sys

def get_config(host):
    with manager.connect(host = host, port = 830, username = "admin", password = "", hostkey_verify=False) as m:
        get_config_interface = '''
                                       <if:interfaces xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                                            <if:interface>
                                                 <if:name>0/1</if:name>
                                            </if:interface>
                                       </if:interfaces>
                                '''
        c = m.get_config(source='running', filter=('subtree',get_config_interface)).data_xml
        with open("%s.xml" %host, 'w') as f:
            f.write(c)
            print c

if __name__ == "__main__":
    get_config(sys.argv[1])
