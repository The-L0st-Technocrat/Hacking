  spooftooph

Copyright (C) 2009-2011 Shadow Cave LLC

Written 2009-2011 by JP Dunning (.ronin)
ronin [ at ] shadowcave [dt] org
<www.hackfromacave.com>

 
  License

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 as
published by the Free Software Foundation;

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT OF THIRD PARTY RIGHTS.
IN NO EVENT SHALL THE COPYRIGHT HOLDER(S) AND AUTHOR(S) BE LIABLE FOR ANY 
CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES 
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION
OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN 
CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

ALL LIABILITY, INCLUDING LIABILITY FOR INFRINGEMENT OF ANY PATENTS, 
COPYRIGHTS, TRADEMARKS OR OTHER RIGHTS, RELATING TO USE OF THIS SOFTWARE IS 
DISCLAIMED.

  ABOUT

Spooftooph is designed to automate spoofing or cloning Bluetooth device 
Name, Class, and Address.  See 'Usage' for more information of its capabilities.

  REQUIREMENTS

- libbluetooth-dev 
- libncurses5-dev

  RECOMMENDED PACKAGES

- bluetooth 
- bluez 
- bluez-tools 
- rfkill 
- rfcomm 
- btscanner

  INSTALL

1. Run "make" to compile binaries.
2. Run "make install" to install into system.
3. Run "make clean" to delete binaries from spooftooph directory.

  RESOURCES

- BlueZ
- BlueZ-devel
- ncurses
- ncurses-devel 

  USAGE

To modify the Bluetooth adapter, spooftooth must be run with root privileges.  
Spooftooph offers five modes of usage:

 1) Specify NAME, CLASS and ADDR.

> spooftooph -i hci0 -n new_name -a 00:11:22:33:44:55 -c 0x1c010c

 2) Randomly generate NAME, CLASS and ADDR.

> spooftooph -i hci0 -r

 3) Scan for devices in range and select device to clone.  Optionally dump the device 
 information in a specified log file.

> spooftooph -i hci0 -s -d file.log

 4) Load in device info from log file and specify device info to clone.

> spooftooph -i hci0 -l file.log

 5) Clone a random devices info in range every X seconds.

> spooftooph -i hci0 -t 10



  HELP

NAME
        spooftooph

SYNOPSIS
        spooftooph -i dev [-m] [-sd] [-nac] [-r] [-l] [-t]

DESCRIPTION
        -a <address>    : Specify new ADDR
        -b <num_lines>  : Number of Bluetooth profiles to display per page
        -c <class>      : Specify new CLASS
        -d <log>        : Dump scan into log file
        -h              : Help
        -i <dev>        : Specify interface
        -l <log>        : Load a list of Bluetooth profiles to clone from saved log
        -n <name>       : Specify new NAME
        -m              : Specify multiple interfaces durring selection.
        -r              : Assign random NAME, CLASS, and ADDR
        -s              : Scan for devices in local area
        -t <time>       : Time interval to clone device in range

# First step is to enable the Bluetooth service locally on the PC.
$ service bluetooth start

# Next, we need to enable the Bluetooth interface and see its configuration (the same way as physical Ethernet interfaces and wireless 
# interfaces, the Bluetooth one also has MAC address called as the BD address).
$ sudo hciconfig hci0 up
$ sudo hciconfig hci0

# When we know that the interface is UP and running, we need to scan a Bluetooth network for the devices visible in the close environment 
# (this is the equivalent of airodump-ng from the 802.11 wireless world). This is done using tool called btscanner.
$ sudo btscanner
# Type i (inquiry scan) and select the bluetooth device you want to hack (enter)
Address: The MAC address of our local Bluetooth device    ie: A0:02:DC:11:4F:85
Found by: The MAC address of the target Bluetooth device  ie: 10:AE:60:58:F1:37
Name: The name of the target Bluetooth device             ie: Tyler

# The main idea here is that Tyler's device is authenticated and paired with another Bluetooth device. For the attacker to impersonate 
# itself as a "Tyler" and pair directly with other node, we need to spoof our MAC address and set our Bluetooth name to "Tyler".

# To impersonate Bluetooth information, there is a tool called spooftooth, that we need to use here (equivalent of macchanger, that we 
# have to use to bypass MAC authentication in WEP scenario with MAC filtering). What we have done below, is that we have changed the 
# MAC address of our Bluetooth dongle (hci0 device) to the one, we have found using btscanner. We have also changed the name of the 
# Bluetooth device to 'LAB'. This is the one I am using locally in my Bluetooth pairing setup between two smartphones.
$ spooftooph -i hci0 -n LAB -a 10:AE:60:58:F1:37
