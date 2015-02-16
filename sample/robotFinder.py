import random
import sys
from threading import Thread
import time
import os, re

class RobotFinder(Thread):
    ROBOT_MAC = "a0:a8:cd:62:c3:75"
    IP_NOT_FOUND = "0.0.0.0"

    def __init__(self, callback):
        Thread.__init__(self)
        self.callback = callback

    def run(self):
        ipAddress = self.IP_NOT_FOUND
        while(ipAddress == self.IP_NOT_FOUND):
            time.sleep(5)
            arpPipe=os.popen2("/usr/sbin/arp -a","");
            linesOfArpExit = arpPipe[1].read().split("\n")
            regIp = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
            regMac = re.compile("((?:[0-9A-f]{1,2}[:]){5}(?:[0-9A-f]{1,2}))")
            for lineOfArpExit in linesOfArpExit:
                foundMac = regMac.findall(lineOfArpExit);
                foundIp = regIp.findall(lineOfArpExit);
                if(len(foundMac) > 0) and (len(foundIp) > 0):
                    if foundMac[0].lower() == self.ROBOT_MAC.lower():
                        ipAddress = foundIp[0]
        self.callback(ipAddress)