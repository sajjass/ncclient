#! /usr/bin/python
#
# Connect to the NETCONF server passed on the command line and
# display their capabilities. This script and the following scripts
# all assume that the user calling the script is known by the server
# and that suitable SSH keys are in place. For brevity and clarity
# of the examples, we omit proper exception handling.
#
# $ ./nc01.py broccoli admin

from ncclient import manager
import sys, os, warnings
warnings.simplefilter("ignore", DeprecationWarning)

def capabilities(host, username, password):

	with manager.connect(host=host,\
				 port=830,\
				 username=username,\
				 password=password,\
				 hostkey_verify=False,\
				 allow_agent=True,\
                                 key_filename=None,\
				 look_for_keys=False,\
                                 ssh_config=None
				 ) as m:
            print m.session_id	
            print m.connected	
            print m.get_config(source="running", filter=None)	
            for c in m.server_capabilities:
                print c

if __name__ == '__main__':
    capabilities(sys.argv[1], sys.argv[2], sys.argv[3])

