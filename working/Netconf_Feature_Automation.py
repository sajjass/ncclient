# !/usr/bin/python

import os, socket
import time
from ncclient import manager
from ncclient.transport import errors
from xlrd import open_workbook
import Write_Netconf_Oper_Results_to_Excel
import hostinfo
import tlnt

global conn, sessionId, current_working_dir
global operations, dataStores
global filterData, configData, book, clicommandData, outputfilterData
global row_count_to_append_result, active_sheet_name, adding_sheet

row_count_to_append_result = 0
active_sheet_name = ""
current_working_dir = os.getcwd()

book = open_workbook(current_working_dir + "\RPC_XML_Data.xlsx")

operations = ["merge", "remove", "replace", "delete", "create"]
dataStores = ["running", "startup", "candidate"]

def connect(host, port, user, password):
    try:
        # connect to the Netconf server
        conn = manager.connect(host=host, port=port, username=user, password=password, hostkey_verify=False)

        sessionId = conn.session_id

        print 'connected:', conn.connected, ' .... to host', host, 'on port:', port

        # Get session parameters
        print 'session-id:', sessionId
        print 'client capabilities:'
        print '####################'
        for i in conn.client_capabilities:
            print ' ', i
        print 'server capabilities:'
        print '####################'
        for i in conn.server_capabilities:
            print ' ', i
        # return this conn object to process edit and get operations to __main__ method
        return conn

    except errors.SSHError:
        print 'Unable to connect to host:', host, 'on port:', port

# Method will be called while locking the data store
def datastore_lock(datastore):
    print '\nlocking the datastore :' + datastore
    try:
        conn.lock(datastore)
    except:
        print "DataStore already locked. Please restart the Netconf server and then Execute the script again"

# Method will be called while unlocking the data store
def datastore_unlock(datastore):
    print '\nunlocking the datastore :' + datastore
    conn.unlock(datastore)

def Netconf_Get_Config_Operation(datastore, filterData, containername):
    print 'Retrieving config using filter from %s datastore for %s container, please wait ...' % (datastore, containername)
    print '\n Request filterData :' + '\n' + filterData
    get_config_response = conn.get_config(source=datastore, filter=('subtree', filterData)).data_xml
    return get_config_response


def Netconf_Edit_Config_Operation():
    for sheet_index in range(book.nsheets):
        sheet_index_number = book.sheet_by_index(sheet_index)
        # Initializing the number to 0. This value will be used to append the output date to Excel rows.
        row_count_to_append_result = 0

        for row in range(1, sheet_index_number.nrows):
            node_name = sheet_index_number.row(row)[0].value
            filterData = sheet_index_number.row(row)[1].value
            configData = sheet_index_number.row(row)[2].value
            clioutputData = sheet_index_number.row(row)[3].value
            clicommandData = sheet_index_number.row(row)[4].value

            for datastore in dataStores:
                try:
                    # Lock the datastore until we finish using that datastore
                    datastore_lock(datastore)

                    # we have to make sure both startup and candidate datastores are having proper fields before working on them
                    # So copying from running (which are always have proper fields) to startup and candidate and working on them
                    if datastore == "startup":
                        conn.copy_config("running", "startup")
                    if datastore == "candidate":
                        conn.copy_config("running", "candidate")

                    for operation in operations:
                        try:
                            # Starting from row count 1. because row value 0 is left for headers.
                            row_count_to_append_result = row_count_to_append_result + 1

                            # Perform Edit operation based on datastore and operation. Here we are submitting the operation value dynamically.
                            dataConfig = configData % operation
                            print '###################################################################'
                            print "\n edit_config" + " operation: " + operation + " on datastore: " + datastore + " on container: " + sheet_index_number.name
                            print '\n Request configData :' + '\n' + dataConfig
                            edit_config_response = conn.edit_config(target=datastore, config=dataConfig)
                            print '\n Response from server for configData :' + '\n' + str(edit_config_response)
                            time.sleep(2)

                            # Performing Get-config operation to check the edit-config data was successfully configured or not
                            print "\n get_config" + " after operation: " + operation + " on datastore: " + datastore + " on container: " + sheet_index_number.name
                            get_config_response_output = Netconf_Get_Config_Operation(datastore, filterData, sheet_index_number.name)
                            print '\n Response from server for filterData :' + '\n' + get_config_response_output
                            print '###################################################################'
                            time.sleep(2)

                            # telnet cli output check is required when datastore is running
                            if datastore != "running":
                                # send the data to form into excel file. The below line will be executed for the datastores startup and candidate
                                writeExcel.WriteResults(operation, datastore, node_name,
                                                                               sheet_index, sheet_index_number.name,
                                                                               row_count_to_append_result, dataConfig,
                                                                               edit_config_response, filterData,
                                                                               get_config_response_output,
                                                                               clicommandData="None",
                                                                               telnet_cli_output="None")
                            else:
                                # Run the telnet command if current datastore is Running
                                telnet_cli_output = telnet.runCmd(cmd=clicommandData)

                                # send the data to form into excel file. The below line will be executed for the datastore running
                                writeExcel.WriteResults(operation, datastore, node_name,
                                                                               sheet_index, sheet_index_number.name,
                                                                               row_count_to_append_result, dataConfig,
                                                                               edit_config_response, filterData,
                                                                               get_config_response_output,
                                                                               clicommandData, telnet_cli_output)

                        except errors.NCClientError as e:
                            print '\n Response from server :' + '\n' + str(e.message)
                            # send the data to form into excel file. The below line will be executed for the operation loop error.
                            writeExcel.WriteResults(operation, datastore, node_name, sheet_index,
                                                                           sheet_index_number.name,
                                                                           row_count_to_append_result, dataConfig,
                                                                           str(e.message), filterData="None", \
                                                                           get_config_response_output="None",
                                                                           clicommandData="None",
                                                                           telnet_cli_output="None")

                            # Eventhough exception caught we wanted to rotate the for loop to continue with our remaining requests
                            pass
                    # unlock the datastore after doing all the operations
                    datastore_unlock(datastore)

                except errors.NCClientError as e:
                    print e.message
                    pass


if __name__ == '__main__':
    conn = connect(hostinfo.host, hostinfo.port, hostinfo.username, hostinfo.password)
    telnet = tlnt.telnet(host=hostinfo.host)
    telnet.login()
    writeExcel = Write_Netconf_Oper_Results_to_Excel.Results()

    print "\nPerform Netconf Edit-conifg and Get-config operations......!!!"
    if conn.connected:
        Netconf_Edit_Config_Operation()
    else:
        print "Connection to Netconf server not established."

    # Make sure session is closed after finishing work
    print "Closing the connection to Server...!!!"
    try:
        conn.close_session()
    except conn.operations.OperationError as e:
        print "Unable to Close the session"
    telnet.close()