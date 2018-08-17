# Requirements
$ sudo apt-get install bluetooth bluez bluez-tools rfkill rfcomm

# Start the bluetooth service and enable automatic startup, assuming you're using systemd as the init daemon
$ sudo systemctl start bluetooth.service
$ sudo systemctl enable bluetooth.service

# Before start scanning make sure that your bluetooth device is turned on and not blocked, you can check that with the rfkill command
$ sudo rfkill list

# If the bluetooth device is blocked (soft or hard blocked), unblock it with the rfkill command again
$ sudo rfkill unblock bluetooth

# Bring up the bluetooth device with hciconfig command and start scanning, make sure the target device's bluetooth is on and It's discoverable.
$ sudo hciconfig hci0 up
$ hcitool scan
Scanning ...
	20:F8:67:14:00:C1	WS-633BT
# Here 20:F8:67:14:00:C1 is the bluetooth MAC address and WS-633BT is the name of the bluetooth device. Note that 

# Now we have the bluetooth MAC address of the target device, use the bluetoothctl command to know which services (like DUN, Handsfree audio) are available on that target device.
$ bluetoothctl
[NEW] Controller D0:57:7B:DA:C0:9A chromebook [default]
[bluetooth]# scan on
Discovery started
[CHG] Device 20:F8:67:14:00:C1 RSSI: -38

[bluetooth]# info 20:F8:67:14:00:C1
Device 20:F8:67:14:00:C1
	Name: WS-633BT
	Alias: WS-633BT
	Class: 0x240408
	Icon: audio-card
	Paired: no
	Trusted: no
	Blocked: no
	Connected: no
	LegacyPairing: no
	RSSI: -38

# Ping the bluetooth device
$ sudo l2ping 20:F8:67:14:00:C1

# hcitool connect and pair devices
# Connecting to the bluetooth device with rfcomm, this command requires root privilege, so use sudo.
$ sudo rfcomm connect <bluetooth host device> <Target bluetooth device MAC> <channel>
$ sudo rfcomm connect hci0 20:F8:67:14:00:C1 2

# The device/phone will prompt to accept this connection request. Now the bluetooth client device should be available as /dev/rfcomm0

# Send file through OBEX/OPP to a remote bluetooth device, the first command is a generic example
$ sudo bt-obex -p <Bluetooth remote device mac address> /path/to/file
$ sudo bt-obex -p 20:F8:67:14:00:C1 ~/img/some_pic.png

# Now receive some file from the remote device, an OBEX server example, first start bt-obex in server mode listening for bluetooth connection.
$ bt-obex -s /path/to/output/folder

# Replace /path/to/output/folder with a folder of your choice, like /tmp . Now send some file from the bluetooth client device, i.e. a phone. The sent file should be in the bt-obex output folder.
