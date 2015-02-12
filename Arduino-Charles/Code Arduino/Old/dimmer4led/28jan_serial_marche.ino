/*
  Dimmer

 Demonstrates the sending data from the computer to the Arduino board,
 in this case to control the brightness of an LED.  The data is sent
 in individual bytes, each of which ranges from 0 to 255.  Arduino
 reads these bytes and uses them to set the brightness of the LED.

 The circuit:
 LED attached from digital pin 9 to ground.
 Serial connection to Processing, Max/MSP, or another serial application

 created 2006
 by David A. Mellis
 modified 30 Aug 2011
 by Tom Igoe and Scott Fitzgerald

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/Dimmer

 */

byte brightness;
byte led;

void setup()
{

  // initialize the serial communication:
  Serial.begin(9600);
  // initialize the ledPin as an output:
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  while (!Serial);
}

void loop() {


  // check if data has been sent from the computer:
  if (Serial.available()) {
    // read the most recent byte (which will be from 0 to 255):
    //led = Serial.read();
    brightness = Serial.read();
    

    Serial.print("I received:");
    Serial.print(brightness);
    Serial.println();
    
    analogWrite(13, brightness);
    analogWrite(12, brightness);
    analogWrite(11, brightness);
    if(brightness==1){
      analogWrite(10, brightness);
    }
      
    
    // set the brightness of the LED:
    //analogWrite(ledPin, brightness);
    //Serial.print("I received: ");
    //Serial.print(brightness);
    //Serial.printin();
    //delay(200);
  }
}

