import unittest
from ncclient import manager
from ncclient.transport import errors
import sys, time, telnetlib
import config
import hostinfo
import tlnt
import time
import re

conn=None
sessionId=None
operations=None
dataStores=None
filterData=None
configData=None
telnet=None

operations = ["merge", "remove", "replace", "delete", "create"]
dataStores = ["running", "startup", "candidate"]
#conn = manager.connect(host=hostinfo.host"10.130.170.252", port=830, username="admin", password="", hostkey_verify=False)
conn = manager.connect(host=hostinfo.host, port=hostinfo.port, username=hostinfo.username, password=hostinfo.password, hostkey_verify=hostinfo.hostkey_verify)
filterData = config.filterData
configData = config.configData
description_text=None

class TestUseCase(unittest.TestCase):
        ConsoleData = None
        dataMatch = None
        def setUp(self):
                try:
                        sessionId = conn.session_id;
                        print 'connected:', conn.connected
                        print 'session_id:', sessionId
                        print 'client capabilities:'
                        for i in conn.client_capabilities:
                                pass
                                #print ' ', i
                        print 'server capabilities:'
                        for i in conn.server_capabilities:
                                pass
                                #print ' ', i
                except :
                        print 'exception in getting data'
        def test_01(self):
                if conn.connected:
                        conn.lock(dataStores[0])
                        description_text = 'ncclient_' + operations[0]
                        rv = conn.edit_config(target = dataStores[0], config = configData %(operations[0], description_text))
                        conn.unlock(dataStores[0])
                        print rv
                else :
                        self.assertFalse(1,"Connection not established")
                        return -1
                telnet.checkMode()
                ConsoleData = telnet.runCmd(cmd="show running-config interface 0/1")
                dataMatch =re.search(description_text, ConsoleData)
                self.assertNotEqual(None, dataMatch,"running config dont match")
        def test_02(self):
                if conn.connected:
                        conn.lock(dataStores[0])
                        rv = conn.get_config(source = dataStores[0], filter = ('subtree', filterData)).data_xml
                        conn.unlock(dataStores[0])
                        print rv
                else :
                        self.assertFalse(1,"Connection not established")
                        return -1
                description_text = 'ncclient_' + operations[0]
                telnet.checkMode()
                ConsoleData = telnet.runCmd(cmd="show running-config interface 0/1")
                dataMatch =re.search(description_text, ConsoleData)
                self.assertNotEqual(None, dataMatch, "running config dont match")
        def tearDown(self):
                pass
                #conn.close_session()


if __name__ == '__main__':
        telnet=tlnt.telnet(host=hostinfo.telnethost, port=hostinfo.telnetport)
        unittest.main()
        conn.close_session()
        telnet.close()
