import serial
import time
#, timeout = 0.5
ser = serial.Serial('com2', 9600) # Establish the connection on a specific port
print ser.readline()
#data = int(raw_input())
#ser.write(str(chr(data)))
#data = int(raw_input())
#ser.write(str(chr(data)))
while(True):

    #
    data = int(raw_input())
    ser.write(str(chr(data))) # Convert the decimal number to ASCII then send it to the Arduino
    #
    data = int(raw_input()) # Read the newest output from the Arduino
    ser.write(str(chr(data))) # Convert the decimal number to ASCII then send it to the Arduino


    #print ser.readline() # Read the newest output from the Arduino

    while(ser.inWaiting()):
        print ser.readline()
ser.close()