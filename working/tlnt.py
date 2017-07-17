import telnetlib

class telnet():
        def __init__(self,host=None,port=23):
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
                    self.tn.write("enable\n")
                    self.tn.read_until("#")

        def runCmd(self,cmd=None):
            try:
                if self.tn.expect(["User:"], 2)[1]:
                    self.login()
                self.tn.write("\n")
                if self.tn.expect(['#'],2)[1]:
                     self.tn.read_very_eager()
                     self.tn.write(str(cmd)+"\n")
                     if self.tn.read_until(['The system has unsaved changes.\
                                        Would you like to save them now? (y/n)'], 2)[1]:
                         self.tn.write("y\n")

                     if self.tn.read_until(['Configuration Saved!\
                                        Are you sure you would like to reset the system? (y/n)'], 2)[1]:
                         self.tn.write("y\n")

                     clicommmandOutput = self.tn.read_until("#")
                     print '#############################'
                     print "CLI command : %s" % cmd
                     print "\nCLI output :", clicommmandOutput
                     print '#############################'
                return clicommmandOutput
            except:
                if self.tn.expect(["User:"], 2)[1]:
                    self.login()
                    return

        def close(self):
                self.tn.close()

