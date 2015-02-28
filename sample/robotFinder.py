from CodeWarrior.Metrowerks_Shell_Suite import _Prop_Stop_at_temp_breakpoint
import random
import sys
from threading import Thread
import time
import os, re


class RobotFinder(Thread):
    ROBOT_MAC = "a0:a8:cd:62:c3:75"
    IP_NOT_FOUND = "0.0.0.0"
    ip_address = IP_NOT_FOUND

    def __init__(self, callback):
        Thread.__init__(self)
        self.callback = callback

    def run(self):
        while self.ip_address == self.IP_NOT_FOUND:
            time.sleep(5)
            self.ip_adress = self._attempt_find()
        self.callback(self.ip_address)

    def _attempt_find(self):
        ip_address = self.IP_NOT_FOUND
        arp_pipe=os.popen2("/usr/sbin/arp -a","");
        lines_of_arp_exit = arp_pipe[1].read().split("\n")
        reg_ip = re.compile("\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}")
        reg_mac = re.compile("((?:[0-9A-f]{1,2}[:]){5}(?:[0-9A-f]{1,2}))")
        for lineOfArpExit in lines_of_arp_exit:
            found_mac = reg_mac.findall(lineOfArpExit);
            found_ip = reg_ip.findall(lineOfArpExit);
            if(len(found_mac) > 0) and (len(found_ip) > 0):
                if found_mac[0].lower() == self.ROBOT_MAC.lower():
                    ip_address = found_ip[0]
        return ip_address