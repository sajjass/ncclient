import getpass
import sys
import telnetlib
import re
import pdb
import time


class telnet():
        ConsoleData=None;
        def __init__(self,host=None,port=None):
                self.host = host;
                self.port = port;
                self.tn = telnetlib.Telnet(self.host, self.port)
        def login(self):
               self.tn.write("\n")
               if self.tn.expect(["User:"],2)[1]:
                    print "dut is in login mode"
                    self.tn.write("admin"+ "\n")
                    self.tn.expect(["Password:"])
                    self.tn.write("\n")

               if self.tn.expect([">"],2)[1]:
                    print "dut is in priv mode"
                    self.tn.write("enable"+ "\n")

               if self.tn.expect(['#']):
                    print "dut is in exec mode"
                    self.tn.write("show platform vpd"+ "\n")
        def checkMode(self):
            self.tn.write("\n")
            if self.tn.expect(["User:"],2)[1]:
                 print "dut is in login mode"
                 self.login()
            elif self.tn.expect([">"],2)[1]:
                 print "dut is in priv mode"
                 self.tn.write("enable"+ "\n")
            self.tn.write("\n")
            if self.tn.expect(['#'], 2)[1]:
                 print "dut is in exec mode only"
                 self.tn.read_very_eager()
        def runCmd(self,cmd=None):
            self.tn.write("\n")
            if self.tn.expect(['#'],2)[1]:
                 self.tn.read_very_eager()
                 self.tn.write(cmd+"\n")
                 ConsoleData = self.tn.read_until("#")
            return ConsoleData
        def close(self):
                self.tn.close()

