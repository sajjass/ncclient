# !/usr/bin/python

from ncclient import manager
from ncclient.transport import errors
import sys, time, telnetlib

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

# Method will be called while locking the data store
def datastore_lock(datastore):
    print "locking the datastore :" + datastore
    conn.lock(datastore)

# Method will be called while unlocking the data store
def datastore_unlock(datastore):
    print "unlocking the datastore :" + datastore
    conn.unlock(datastore)

def get_config_intf_description(datastore):
    print 'Retrieving interface description config using filter, please wait ...'
    get_config_response = conn.get_config(source=datastore, filter=('subtree', filterData)).data_xml
    return get_config_response


def edit_config_intf_description():
    operations = ["merge", "remove", "replace", "delete", "create"]
    dataStores = ["running", "startup", "candidate"]

    try:
        for datastore in dataStores:
            # Lock the datastore until we finish using that datastore
            datastore_lock(datastore)

            # we have to make sure both startup and candidate datastores are having proper fields before working on them
            # So copying from running (which always have proper fields) to startup and candidate and working on them
            if datastore == "startup":
                conn.copy_config("running", "startup")
            if datastore == "candidate":
                conn.copy_config("running", "candidate")

            for operation in operations:
                description_text = "ncclient_" + operation

                # Perform Edit operation based on datastore and operation
                edit_config_response = conn.edit_config(target=datastore, config=configData % (operation, description_text))
                print "\n edit_config" + " operation: " + operation + " datastore: " + datastore
                print edit_config_response
                time.sleep(2)

                # Performing Get-config operation to check the edit-config data was successfully configured or not
                get_config_response_output = get_config_intf_description(datastore)
                print "\n get_config" + " after operation: " + operation + " datastore: " + datastore
                print  get_config_response_output
                time.sleep(2)

                telnet_dut()

            # unlock the datastore after doing all the operations
            datastore_unlock(datastore)

    except errors.NCClientError as e:
        print(e.message)

def telnet_dut():

    tn = telnetlib.Telnet("10.130.170.252")
    # tn.read_until(" Entering server port, ..... type ^z for port menu.")
    # tn.write("")
    tn.read_until("User:")
    tn.write("admin\n")
    tn.read_until("Password:")
    tn.write("\n")
    tn.write("enable\n")
    tn.read_until("#")
    tn.write("terminal length 0\n")
    tn.read_until("#")
    tn.write("show running-config interface 0/1\n")
    intfConfig = tn.read_until("#")
    print intfConfig

if __name__ == '__main__':
    conn = connect("10.130.170.252", 830, "admin", "")
    print "Going to execute EDIT-conifg and GET-config operations......!!!"
    if conn.connected:
        edit_config_intf_description()

    # Make sure session is closed after finishing work
    conn.close_session()
