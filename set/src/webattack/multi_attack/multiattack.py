#!/usr/bin/env python
import re
import sys
import os
import subprocess
import time
import signal

# Grab the central imports
definepath = os.getcwd()
sys.path.append(definepath)
from src.core.setcore import *

operating_system = check_os()

#######################################################
# Heres the brains behind the multiattack vector.
# This preps each check and payload for each attack
# vector.
#######################################################


def return_menu():
    PrintStatus("Option added. You may select additional vectors")
    time.sleep(2)
    print("""\nSelect which additional attacks you want to use:\n""")

# option designators needed to ensure its defined ahead of time
java_applet="off"
meta_attack="off"
harvester="off"
tabnabbing="off"
mlitm="off"
webjacking="off"

# turning flag on
def flag_on(vector):
	PrintInfo("Turning the %s Attack Vector to " % (vector) + bcolors.GREEN + "ON" + bcolors.ENDC)

# turning flag off
def flag_off(vector):
        PrintInfo("Turning the %s Attack Vector to " % (vector) + bcolors.RED + "OFF" + bcolors.ENDC)

# filewriting
def write_file(filename,results):
	filewrite=file("src/program_junk/%s" % (filename), "w")
	filewrite.write(results)
	filewrite.close()

# specify attackvector
filewrite=file("src/program_junk/attack_vector","w")
filewrite.write("multiattack")
filewrite.close()

# on and off switch detection variable
trigger=""

# set toggle flags here
toggleflag_java=(bcolors.RED+" (OFF)" + bcolors.ENDC)
toggleflag_meta=(bcolors.RED+" (OFF)" + bcolors.ENDC)
toggleflag_harv=(bcolors.RED+" (OFF)" + bcolors.ENDC)
toggleflag_tabnab=(bcolors.RED+" (OFF)" + bcolors.ENDC)
toggleflag_mlitm=(bcolors.RED+" (OFF)" + bcolors.ENDC)
toggleflag_webjacking=(bcolors.RED+" (OFF)" + bcolors.ENDC)

# grab current path
definepath=os.getcwd()

# default flag for webdav to be off
webdav_enable="OFF"

# clean up cloner directory
subprocess.Popen("rm -rf src/program_junk/web_clone;mkdir src/program_junk/web_clone/", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

# set a quick loop to see what the user wants 
a=1

print ("""
[*************************************************************]

        	Multi-Attack Web Attack Vector

[*************************************************************]

 The multi attack vector utilizes each combination of attacks
 and allow the user to choose the method for the attack. Once
 you select one of the attacks, it will be added to your 
 attack profile to be used to stage the attack vector. When
 your finished be sure to select the 'I'm finished' option.""")
print("""\nSelect which attacks you want to use:
""")

while a==1:
	trigger=""
	print "   1. Java Applet Attack Method" + toggleflag_java
	print "   2. Metasploit Browser Exploit Method" + toggleflag_meta
	print "   3. Credential Harvester Attack Method" + toggleflag_harv
	print "   4. Tabnabbing Attack Method" + toggleflag_tabnab
	print "   5. Man Left in the Middle Attack Method" + toggleflag_mlitm
	print "   6. Web Jacking Attack Method" + toggleflag_webjacking
	print "   7. Use them all - A.K.A. 'Tactical Nuke'" 
	print "   8. I'm finished and want to proceed with the attack"
	print "\n  99. Return to Main Menu\n"


	profile=raw_input(setprompt(["2","16"], "Enter selections one at a time (8 to finish)"))

	if profile == "": profile = "7"
	# if the option is something other than 1-7 flag invalid option
	# this will make sure its an integer, if not assign an 9 which will trigger invalid option
	try:	# this will trigger an error if it isnt an integer
		profile=int(profile)
		# convert it back
		profile=str(profile)
	# if it triggers an exception reassign profile to option 8
	except: profile = "10"

	# if you want to return to main menu
	if profile == "99":
		break

	# trigger invalid option
	if int(profile) >= 10:
		raw_input("\nInvalid option, press " + bcolors.RED+"{return}" + bcolors.ENDC + " to go back to the menu.")

	if profile == "7":
                if operating_system == "windows":
                    PrintWarning("Sorry this option is not available in Windows")
                    pause = raw_input("{Press return} to go back to attack selection")
                if operating_system != "windows":
                    print bcolors.RED + (r"""
                                  ..-^~~~^-..
                                .~           ~.
                               (;:           :;)
                                (:           :)
                                  ':._   _.:'
                                      | |
                                    (=====)
                                      | |
                                      | |
                                      | |
                                   ((/   \))""") + bcolors.ENDC

                    print "\nSelecting everything SET has in its aresenal, you like sending a nuke don't you?"
                    print "\n[*] Note that tabnabbing is not enabled in the tactical nuke, select manually if you want.\n"
                    java_applet="on"
                    meta_attack="on"
                    harvester="on"
                    break		

	if profile == "8":
		break

	# java applet on/off
	if profile == "1":
		if java_applet == "off":
			flag_on("Java Applet")
			return_menu()
			java_applet="on"
			trigger=1
			#toggle_flags here
			toggleflag_java=(bcolors.GREEN+" (ON)" + bcolors.ENDC)

		if java_applet == "on":
			if trigger != 1:
				flag_off("Java Applet")
				return_menu()
				java_applet="off"
				# toggle flags here
				toggleflag_java=(bcolors.RED+" (OFF)" + bcolors.ENDC)

	# metasploit client_side on/off
	if profile == "2":
                if operating_system == "windows":
                    PrintWarning("Sorry this option is not available in Windows")
                    pause = raw_input("{Press return} to go back to attack selection")
                if operating_system != "windows":
                    if meta_attack=="off":
                            flag_on("Metasploit Client Side")
                            return_menu()
                            meta_attack="on"
                            trigger=1
                            # toggle flags here
                            toggleflag_meta=(bcolors.GREEN+" (ON)" + bcolors.ENDC)

                    if meta_attack=="on":
			if trigger != 1:
				flag_off("Metasploit Client Side")
				return_menu()
                	        meta_attack="off"
				# toggle flags here
				toggleflag_meta=(bcolors.RED+" (OFF)" + bcolors.ENDC)


	# harvester on/off
	if profile == "3":
		if harvester == "off":
			flag_on("Harvester")
			return_menu()
			harvester="on"
			trigger=1
			# toggle flags here
			toggleflag_harv=(bcolors.GREEN+" (ON)" + bcolors.ENDC)
			if mlitm == "on":
				mlitm="off"
				toggleflag_mlitm=(bcolors.RED+" (OFF)" + bcolors.ENDC)

		if harvester == "on":
			if trigger != 1:
				flag_off("Harvester")
				return_menu()
                	        harvester="off"
				# toggle flags here				
				toggleflag_harv=(bcolors.RED+" (OFF)" + bcolors.ENDC)

	# if tabnabbing is enabled, no need for harvester to be enabled as well
	if profile == "4": 
		if tabnabbing == "off":
			flag_on("Tabnabbing")
			return_menu()
			tabnabbing="on"
			trigger=1
			harvester="on"
			# toggle flags here
			toggleflag_tabnab=(bcolors.GREEN+" (ON)" + bcolors.ENDC)
			if mlitm == "on":
				mlitm="off"
				toggleflag_mlitm=(bcolors.RED+" (OFF)" + bcolors.ENDC)
			print webjacking
			if webjacking == "on":
				webjacking = "off"
				toggleflag_webjacking=(bcolors.RED+" (OFF)" + bcolors.ENDC)

		if tabnabbing == "on":
			if trigger != 1:
				flag_off("Tabnabbing")
				return_menu()
                	        tabnabbing="off"
				harvester="off"
				# toggle flags here
				toggleflag_tabnab=(bcolors.RED+" (OFF)" + bcolors.ENDC)	

	# turn man left in the middle to on
	if profile== "5":

                if mlitm == "off":
			flag_on("Man Left in the Middle")
                        mlitm="on"
			return_menu()
			trigger=1
			if harvester == "on" or tabnabbing == "on":
				print "[*] You cannot use MLITM and Harvester/Tabnabbing in the same attack!"
				print "[*] Disabling Harvesting and/or Tabnabbing"
				harvester="off"
				tabnabbing="off"
				# toggle flags here
				toggleflag_mlitm=(bcolors.GREEN+" (ON)"+ bcolors.ENDC)
				toggleflag_tabnab=(bcolors.RED+" (OFF)" + bcolors.ENDC)
				toggleflag_harv=(bcolors.RED+" (OFF)" + bcolors.ENDC)

                if mlitm == "on":
			if trigger != 1:
				flag_off("Man Left in the Middle")
				return_menu()
				mlitm="off"
				# toggle flags here
				toggleflag_mlitm=(bcolors.RED+" (OFF)" + bcolors.ENDC)

        # turn webjacking on
        if profile== "6":

                if webjacking == "off":
                        flag_on("Web Jacking")
                        webjacking="on"
                        return_menu()
                        trigger=1
                        if tabnabbing == "on" or mlitm == "on":
                                print "[*] You cannot use MLITM and Tabnabbing in the same attack!"
                                print "[*] Disabling MLITM and/or Tabnabbing"
                                mlitm="off"
                                tabnabbing="off"
				harvester="on"
                        	# toggle flags here
                                toggleflag_mlitm=(bcolors.GREEN+" (ON)" + bcolors.ENDC)
                                toggleflag_tabnab=(bcolors.RED+" (OFF)" + bcolors.ENDC)
				toggleflag_harv=(bcolors.GREEN+" (ON)" + bcolors.ENDC)	
			if harvester == "off":
				harvester="on"
				toggleflag_harv=(bcolors.GREEN+" (ON)" + bcolors.ENDC)
			toggleflag_webjacking=(bcolors.GREEN+" (ON)" + bcolors.ENDC)

                if webjacking == "on":
                        if trigger != 1:
                                flag_off("Web Jacking")
                                return_menu()
                                webjacking="off"
                                # toggle flags here
                                toggleflag_webjacking=(bcolors.RED+" (OFF)" + bcolors.ENDC)


# next series of flags needed
payloadgen=0

# write handler files for detection
if java_applet == "on":
	write_file("multi_java","multiattack=java_on")
if meta_attack == "on":
	write_file("multi_meta","multiattack=meta_on")
if tabnabbing == "on":
	write_file("multi_tabnabbing","multiattack=tabnabbing_on")
if harvester == "on":
	write_file("multi_harvester","multiattack=harvester_on")
if mlitm == "on":
	write_file("multi_mlitm","multiattack=mlitm_on")
if webjacking == "on":
	write_file("multi_webjacking","multiattack=webjacking_on")

# hit cloner flag
# if any of the flags are turned on, then trigger to see if ARP Cache needs to be enabled
if java_applet =="on" or meta_attack == "on" or harvester == "on" or tabnabbing == "on" or mlitm == "on":

        # web cloner start here
        sys.path.append("src/webattack/web_clone")
        try: reload(cloner)
        except: import cloner

        # arp cache attack, will exit quickly
        # if not in config file
        if operating_system != "windows":
            sys.path.append("src/core/arp_cache")
            try: reload(arp_cache)
            except: import arp_cache

# start the stuff for java applet
if java_applet == "on":
	sys.path.append("src/core/payloadgen/")
	try: reload(create_payloads)
	except: import create_payloads
	payloadgen=1
	# Allow Self-Signed Certificates
	fileopen=file("config/set_config", "r").readlines()
	for line in fileopen:
		line=line.rstrip()
		match=re.search("SELF_SIGNED_APPLET=ON", line)
		if match:
			sys.path.append("src/html/unsigned/")
			import self_sign

# start the stuff for metasploit client side
if meta_attack == "on":
	sys.path.append("src/webattack/browser_exploits/")
	import gen_payload

	# this checks to see if the MSF payload uses webdav, if so we have to force port 80
	if os.path.isfile("src/program_junk/webdav_enabled"):
		webdav_enabled="on"

# set this incase msf attack, java applet, and harvester is needed
pexpect_flag="off"

# start the stuff for harvester
if harvester == "on" or tabnabbing == "on" or webjacking == "on":
        if tabnabbing == "on" or webjacking == "on":
		# if tabnabbing is on, set th tabnabbing to on
                sys.path.append("src/webattack/tabnabbing")
                try: reload(tabnabbing)
                except: import tabnabbing
	# if the harvester is on set the multi_harvester flag
	sys.path.append("src/webattack/harvester")
        #try: reload(harvester)
        #except: import harvester
	if java_applet == "on" or meta_attack == "on":
		pexpect_flag="on"
		a=subprocess.Popen("python src/webattack/harvester/harvester.py", shell=True)
# start stuff for mlitm
if mlitm == "on":
        sys.path.append("src/webattack/mlitm")
	if java_applet == "on" or meta_attack == "on":
		a=subprocess.Popen("python src/mlitm/mlitm.py")
	else:
        	try: reload(mlitm)
        	except: import mlitm

# start the web server
if java_applet == "on" or meta_attack == "on":
	sys.path.append("src/html/")
	try: reload(spawn)
	except: import spawn

	# if using man left in the middle
	if mlitm == "on":
		try:
                        # a.terminate only works on Python > 2.6
                        a.terminate()
                except AttributeError:
                        # if it fails pull pid for subprocess thread then terminate it
                        os.kill( a.pid , signal.SIGTERM)

	# if using cred harvester or tabnabbing
	if harvester == "on" or tabnabbing == "on":
                sys.path.append("src/webattack/harvester/")
                import report_generator
		try:
			# a.terminate only works on Python > 2.6
			a.terminate()
		except AttributeError:
			# if it fails pull pid for subprocess thread then terminate it
			os.kill( a.pid , signal.SIGTERM)
		raw_input("\nReport exported. Press "+ bcolors.RED+"{return}" + bcolors.ENDC+" to return to the menu.")
