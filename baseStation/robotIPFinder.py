from threading import Thread
import time
import os
import re


class RobotFinder(Thread):
    ROBOT_MAC = 'a0:a8:cd:62:c3:75'
    IP_NOT_FOUND = '0.0.0.0'
    SLEEP_TIME_IN_MINS = 5
    ip_address = IP_NOT_FOUND

    def __init__(self, callback):
        Thread.__init__(self)
        self.callback = callback
        self.is_stopped = False

    def run(self):
        while self.ip_address == self.IP_NOT_FOUND and self.is_stopped is False:
            time.sleep(self.SLEEP_TIME_IN_MINS)
            self.ip_address = self._attempt_find()
        self.callback(self.ip_address)

    def _attempt_find(self):
        arp_pipe = self._get_arp_pipe()
        lines_of_arp_exit = arp_pipe[1].read().split("\n")
        ip_address = self._parse_answer(lines_of_arp_exit)
        return ip_address

    def _get_arp_pipe(self):
        return os.popen2('/usr/sbin/arp -a', '');

    def _parse_answer(self, lines_of_arp_exit):
        ip_address = self.IP_NOT_FOUND
        reg_ip = re.compile('(?:\()(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3})(?:\))')
        reg_mac = re.compile('((?:[0-9A-f]{1,2}[:]){5}(?:[0-9A-f]{1,2}))')
        for lineOfArpExit in lines_of_arp_exit:
            found_mac = reg_mac.findall(lineOfArpExit);
            found_ip = reg_ip.findall(lineOfArpExit);
            if(len(found_mac) > 0) and (len(found_ip) > 0):
                if found_mac[0].lower() == self.ROBOT_MAC.lower():
                    ip_address = found_ip[0]
                    break
        return ip_address

    def stop(self):
        self.is_stopped = True