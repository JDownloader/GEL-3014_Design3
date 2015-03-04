# -*- encoding:utf-8 -*-
import serial
import Tkinter

ser = serial.Serial('com2', 9600) # Establish the connection on a specific port


#print ser.readline()
while(True):
    #top.mainloop()
    data = int(raw_input())
    ser.write(str(chr(data))) # Commande

    data = int(raw_input()) #
    ser.write(str(chr(data))) # Vitesse

    data = int(raw_input()) #
    ser.write(str(chr(data))) # Distance (sera multiplié par 10)
    while(ser.inWaiting()):
        print ser.readline()