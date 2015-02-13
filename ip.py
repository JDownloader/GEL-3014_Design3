import os, re
ROBOT_MAC = "a0:a8:cd:62:c3:75"
IP_NOT_FOUND = "0.0.0.0"

ipAddress = IP_NOT_FOUND
arpPipe=os.popen2("/usr/sbin/arp -a","");
linesOfArpExit = arpPipe[1].read().split("\n")
regIp = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
regMac = re.compile("((?:[0-9A-f]{1,2}[:]){5}(?:[0-9A-f]{1,2}))")
for lineOfArpExit in linesOfArpExit:
    foundMac = regMac.findall(lineOfArpExit);
    foundIp = regIp.findall(lineOfArpExit);
    if(len(foundMac) > 0) and (len(foundIp) > 0):
        if foundMac[0].lower() == ROBOT_MAC.lower():
            ipAddress = foundIp[0]