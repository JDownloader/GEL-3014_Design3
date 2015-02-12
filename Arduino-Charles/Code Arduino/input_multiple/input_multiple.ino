// Constante pour l'ouverture l'accès serial
byte brightness=0;
byte led=0;
byte commande=0;

//sert aux rampes
int i;
bool RampeUp = 0;
byte RampeUpStatut = 0;
byte RampeUpFin = 0;
byte RampeUpLed = 0;

unsigned long previousMillisUp = 0; 

bool RampeDown = 0;
byte RampeDownStatut = 0;
byte RampeDownFin = 0;
byte RampeDownLed = 0;
unsigned long previousMillisDown = 0; 

//Pour le

const long interval = 10;


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
unsigned long currentMillis = millis();

  // check if data has been sent from the computer:
  if (Serial.available()==3) {
    // read the most recent byte (which will be from 0 to 255):
    commande = Serial.read();
    led = Serial.read();
    brightness = Serial.read();
    

    //Serial.print("I received:");
    Serial.print("Commande");
    Serial.print(commande);
    Serial.print("    Led:");
    Serial.print(led);
    Serial.print("    Brightness:");
    Serial.print(brightness);
    Serial.println();
    

    if(commande==1){
      analogWrite(led, brightness);
    }
    if(commande==10){
      analogWrite(10, brightness);
      analogWrite(11, brightness);
      analogWrite(12, brightness);
      analogWrite(13, brightness);
    }
    if(commande==20)
    {
      RampeUp=1;
      RampeUpFin = brightness;
      RampeUpStatut = 0;
      RampeUpLed = led;
    }
    if(commande==30)
    {
      RampeDown=1;
      RampeDownFin = 0;
      RampeDownStatut = brightness;
      RampeDownLed = led;
    }
    if(commande==40)
    {
      delay(5000);
    }
  } // fin de la boucle qui attend 2 entrées sur le port série
  
  if(RampeUp == 1)
    {
        if(currentMillis - previousMillisUp >= interval) 
        {
          // save the last time you blinked the LED 
          previousMillisUp = currentMillis;   
          analogWrite(10, RampeUpStatut);
          RampeUpStatut++;
          //Serial.print(RampeUpStatut);
          //Serial.print(previousMillisUp);
          if(RampeUpStatut >= RampeUpFin)
          {
             RampeUp = 0; 
          }
        }
    }
    if(RampeDown == 1)
    {
        if(currentMillis - previousMillisDown >= interval) 
        {
          // save the last time you blinked the LED 
          previousMillisDown = currentMillis;   
          analogWrite(11, RampeDownStatut);
          RampeDownStatut--;
          if(RampeDownStatut <= RampeDownFin)
          {
             RampeDown = 0; 
          }
        }
    }
}

