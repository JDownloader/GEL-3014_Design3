import serial
import time

ser = serial.Serial('com2', 9600) # Establish the connection on a specific port
print ser.readline()
while(True):

    #ser.flushInput()
    #

    data = int(raw_input())
    ser.write(str(chr(data))) # Convert the decimal number to ASCII then send it to the Arduino
    print ser.readline() # Read the newest output from the Arduino

ser.close()