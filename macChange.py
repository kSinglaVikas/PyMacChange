#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()

    parser.add_option("-i", "--interface", dest="interface", help="detail of the interface")
    parser.add_option("-m", "--mac", dest="newMac", help="New Mac address to be assigned")
    (options, arguments) = parser.parse_args()

    if not options.interface:
        parser.error("Please specify the interface. use --help for more info")
    elif not options.newMac:
        parser.error("Please specify new Mac. Use --help for more info")
    return options

def changeMac(interface, newMac):
    print("[+] Change the Mac for " + interface + " to " + newMac)

    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", newMac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface]).decode("utf-8")
    mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac:
        return mac.group(0)
    else:
        print("Unable to get the mac")

def verifyChange(interface, newMac):
    latestMac = get_current_mac(interface)
    if latestMac == newMac:
        print("MAC address changed to: " + newMac)
    else:
        print("Unable to change the Mac address")

options = get_arguments()

currentMac = get_current_mac(options.interface)

if currentMac != options.newMac:
    changeMac(options.interface, options.newMac)
    verifyChange(options.interface, options.newMac)
else:
    print("New mac is same as current")
