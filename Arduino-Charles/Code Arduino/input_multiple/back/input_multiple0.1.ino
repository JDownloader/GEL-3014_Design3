byte brightness=0;
byte led=0;
int i=0;


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
  if (Serial.available()==2) {
    // read the most recent byte (which will be from 0 to 255):
    led = Serial.read();
    brightness = Serial.read();
    

    //Serial.print("I received:");
    Serial.print("Led:");
    Serial.print(led);
    Serial.print("    Brightness:");
    Serial.print(brightness);
    Serial.println();
    

    if(led==1){
      analogWrite(10, brightness);
      Serial.println("Led sur pin 10 ajusté");
    }
    if(led==2){
      analogWrite(11, brightness);
      Serial.println("Led sur pin 11 ajusté");
    }
    if(led==3){
      analogWrite(12, brightness);
    }
    if(led==4){
      analogWrite(13, brightness);
    }
    if(led==10){
      analogWrite(10, brightness);
      analogWrite(11, brightness);
      analogWrite(12, brightness);
      analogWrite(13, brightness);
    }
    if(led==20){
      i =  0;
      while (i < brightness){
        
        analogWrite(10, i);
        analogWrite(11, i);
        analogWrite(12, i);
        analogWrite(13, i);
        i++;
        delay(50);
       }
    }
    if(led==30){
      i = brightness;
      while (i > 0 ){
        
        analogWrite(10, i);
        analogWrite(11, i);
        analogWrite(12, i);
        analogWrite(13, i);
        i--;
        delay(50);
       }
    }
    
  }
}

