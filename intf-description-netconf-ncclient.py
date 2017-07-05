'''@author = 'sajjas'
@date = '5/July/2017' '''

# !/usr/bin/python

from ncclient import manager
from ncclient.transport import errors
import sys, time

global conn, sessionId
global operations, dataStores
global filterData, configData

def connect(host, port, user, password):
    global conn, sessionId
    global operations, dataStores
    global filterData, configData

    filterData = '''
						<if:interfaces xmlns:if="urn:ietf:params:xml:ns:yang:ietf-interfaces">
							<if:interface>
								<if:name>0/1</if:name>
								<if:description/>
							</if:interface>
						</if:interfaces>
				 '''
    configData = '''
					<nc:config xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
						<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
							<interface>
								<name>0/1</name>
								<description nc:operation="%s">%s</description>
							</interface>
						</interfaces>
					</nc:config>
				 '''

    try:
        # connect to the Netconf server
        conn = manager.connect(host=host, port=port, username=user, password=password, hostkey_verify=False)

        print 'locking configuration'

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
        # return this conn object to process edit and get operations to __main__ method
        return conn
    except errors.SSHError:
        print 'Unable to connect to host:', host, 'on port:', port


def get_config_intf_description(datastore):
    print 'Retrieving interface description config using filter, please wait ...'
    get_config_response = conn.get_config(source=datastore, filter=('subtree', filterData)).data_xml
    return get_config_response


def edit_config_intf_description():
    operations = ["merge", "remove", "replace", "delete", "create"]
    dataStores = ["running", "startup", "candidate"]

    for datastore in dataStores:
        if datastore == "startup":
            conn.copy_config("running", "startup")
        if datastore == "candidate":
            conn.copy_config("running", "candidate")
        for operation in operations:
            description_text = "ncclient_" + operation

            # Perform edit operation based on datastore and operation
            edit_config_response = conn.edit_config(target=datastore, config=configData % (operation, description_text))
            print "\n edit_config" + " operation: " + operation + " datastore: " + datastore
            print edit_config_response
            time.sleep(2)
            get_config_response_output = get_config_intf_description(datastore)
            print "\n get_config" + " after operation: " + operation + " datastore: " + datastore
            print  get_config_response_output
            time.sleep(2)

if __name__ == '__main__':
    conn = connect("10.130.170.252", 830, "admin", "")
    print "Going to execute EDIT and GET operations......"
    if conn.connected:
        edit_config_intf_description()
    conn.close_session()