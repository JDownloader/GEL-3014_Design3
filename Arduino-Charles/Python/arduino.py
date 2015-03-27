# -*- encoding:utf-8 -*-
import serial

ser = serial.Serial('com9', 9600) # Establish the connection on a specific port


while(True):
    data = int(raw_input())
    ser.write(str(chr(data))) # Commande

    data = int(raw_input()) #
    ser.write(str(chr(data))) # Vitesse

    data = int(raw_input()) #
    ser.write(str(chr(data))) # Distance (sera multiplié par 10)
    while(ser.inWaiting()):
        print ser.readline()