'''@author = 'sajjas'
@date = '5/July/2017' '''

#!/usr/bin/python

from ncclient import manager
from ncclient.transport import errors
import sys

def connect(host, port, user, password):
    global conn
    global sessionId

    try:
        # connect to the Netconf server
        conn = manager.connect(host=host, port=port, username=user, password=password, hostkey_verify=False)

        sessionId = conn.session_id

        print 'connected:', conn.connected, ' .... to host', host, 'on port:', port

        # Get session parameters
        print 'session-id:', sessionId
        print 'client capabilities:'
        for i in conn.client_capabilities:
            print ' ', i
        print 'server capabilities:'
        for i in conn.server_capabilities:
            print ' ', i
        conn.close_session()
    except errors.SSHError:
        print 'Unable to connect to host:', host, 'on port:', port

if __name__ == '__main__':
    connect("10.130.170.252", 830, "admin", "")

