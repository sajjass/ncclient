#!/usr/bin/python
from ncclient import manager

def main():

	with manager.connect(host='10.130.170.252',\
					 port=830,\
                                         #unknown_host_cb=default_unknown_host_cb,\
					 username='test1',\
					 password='test1234',\
					 hostkey_verify=False,\
					 allow_agent=True,\
                                         key_filename=None,\
					 look_for_keys=False,\
                                         ssh_config=None
					 ) as netconf_manager:
	
				
		ptp_domain = '''
					<?xml version="1.0" encoding="UTF-8"?>
					<rpc xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="3">
					<get-config>
						<source>
							<running/>
						</source>
						<filter type="subtree">
						<ptp-datasets xmlns="urn:ietf:params:xml:ns:yang:ietf-ptp-dataset">
							<domain-number>100</domain-number>
						</ptp-datasets>
						</filter>
					</get-config>
					</rpc>
					'''
		ptp_domain_output = netconf_manager.get(('subtree', ptp_domain))				
		
		print ptp_domain_output

if __name__ == '__main__':
	main()
