#!/usr/bin/python
import subprocess
import os
import re
import sys
from src.core.setcore import *

# definepath
definepath=os.getcwd()
sys.path.append(definepath)


meta_path = meta_path()

# launch msf listener
PrintInfo("The payload can be found in the SET home directory.")
choice = raw_input(setprompt("0", "Start the listener now? [yes|no]"))
if choice == "yes" or choice == "y":

    # if we didn't select the SET interactive shell as our payload
    if not os.path.isfile("src/program_junk/set.payload"):
        PrintInfo("Please wait while the Metasploit listener is loaded...")
        subprocess.Popen("ruby %s/msfconsole -L -n -r src/program_junk/meta_config" % (meta_path), shell=True).wait()

    # if we did select the set payload as our option
    if os.path.isfile("src/program_junk/set.payload"):
        fileopen = file("src/program_junk/port.options", "r")
        set_payload = file("src/program_junk/set.payload", "r")
        port = fileopen.read().rstrip()
        set_payload = set_payload.read().rstrip()
        if set_payload == "SETSHELL":
            PrintInfo("Starting the SET Interactive Shell Listener on %s." % (port))
            subprocess.Popen("python src/payloads/set_payloads/listener.py %s" % (port), shell=True).wait()
        if set_payload == "RATTE":
            PrintInfo("Starting the RATTE Shell on %s." % (port))
            subprocess.Popen("src/payloads/ratte/ratteserver %s" % (port), shell=True).wait()
