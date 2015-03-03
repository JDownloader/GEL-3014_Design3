# -*- encoding:utf-8 -*-
import serial
import Tkinter

ser = serial.Serial('com2', 9600) # Establish the connection on a specific port
top = Tkinter.Tk()

def foward():
   ser.write(str(chr(1)))
   ser.write(str(chr(vitesse.get())))
def backward():
   ser.write(str(chr(2)))
   ser.write(str(chr(vitesse.get())))
def right():
   ser.write(str(chr(3)))
   ser.write(str(chr(vitesse.get())))
def left():
   ser.write(str(chr(4)))
   ser.write(str(chr(vitesse.get())))
def Clockwise():
   ser.write(str(chr(101)))
   ser.write(str(chr(vitesse.get())))
def CounterClockWise():
   ser.write(str(chr(102)))
   print(vitesse.get())
def Shutdown():
    ser.write(str(chr(99)))
    ser.write(str(chr(vitesse.get())))
    top.deiconify()
vitesse = Tkinter.IntVar()

A = Tkinter.Button(top, text ="Avant", command = foward)
B = Tkinter.Button(top, text ="Arrière", command = backward)
C = Tkinter.Button(top, text ="Droite", command = right)
D = Tkinter.Button(top, text ="Gauche", command = left)
E = Tkinter.Button(top, text ="Clockwise", command =Clockwise)
F = Tkinter.Button(top, text ="CounterClockWise", command =CounterClockWise)
G = Tkinter.Button(top, text ="Fermeture!!", command =Shutdown)

speed = Tkinter.Scale( top,  from_=0, to=255, variable=vitesse, orient="horizontal")

A.pack(anchor="w")
B.pack(anchor="w")
C.pack(anchor="w")
D.pack(anchor="w")
E.pack(anchor="e")
F.pack(anchor="e")
G.pack()
speed.pack()




#print ser.readline()
while(True):
    #top.mainloop()
    data = int(raw_input())
    ser.write(str(chr(data))) # Convert the decimal number to ASCII then send it to the Arduino

    data = int(raw_input()) # Read the newest output from the Arduino
    ser.write(str(chr(data))) # Convert the decimal number to ASCII then send it to the Arduino
    while(ser.inWaiting()):
        print ser.readline()