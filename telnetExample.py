#!/usr/bin/python
import telnetlib

tn = telnetlib.Telnet("10.130.170.252")
#tn.read_until(" Entering server port, ..... type ^z for port menu.")
#tn.write("")
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