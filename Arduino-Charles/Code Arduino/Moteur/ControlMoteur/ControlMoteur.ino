int previousMillis = 0;

// Descriptiond des pins!

  // outputs
  unsigned int Speed1 = 0; // Vitesse Moteur #1
  unsigned int Speed2 = 0; // Vitesse Moteur #2
  unsigned int Speed3 = 0; // Vitesse Moteur #3
  unsigned int Speed4 = 0; // Vitesse Moteur #4
  
  int CW1    = 46;  //Moteur #1 pin ClockWise  
  int CCW1   = 47;  //Moteur #1 pin CounterClockWise  
  int CW2    = 48;  //Moteur #2 pin ClockWise  
  int CCW2   = 49;  //Moteur #2 pin CounterClockWise  
  int CW3    = 50;  //Moteur #3 pin ClockWise  
  int CCW3   = 51;  //Moteur #3 pin CounterClockWise  
  int CW4    = 52;  //Moteur #4 pin ClockWise  
  int CCW4   = 53;  //Moteur #4 pin CounterClockWise  
  
  //Inputs
  int Position1    = 42;  // Capteur Hall Moteur #1
  int Position2    = 43;  // Capteur Hall Moteur #2
  int Position3    = 44;  // Capteur Hall Moteur #3
  int Position4    = 45;  // Capteur Hall Moteur #4
  
void setup() 
{
  Serial.begin(9600);
  
  // Déclaration des pins
  pinMode(CW1, OUTPUT), digitalWrite(CW1, LOW);
  pinMode(CW2, OUTPUT), digitalWrite(CW2, LOW);
  pinMode(CW3, OUTPUT), digitalWrite(CW3, LOW);
  pinMode(CW4, OUTPUT), digitalWrite(CW4, LOW);
  pinMode(CCW1, OUTPUT), digitalWrite(CCW1, LOW);
  pinMode(CCW2, OUTPUT), digitalWrite(CCW2, LOW);
  pinMode(CCW3, OUTPUT), digitalWrite(CCW3, LOW);
  pinMode(CCW4, OUTPUT), digitalWrite(CCW4, LOW);
  
  pinMode(13, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(10, OUTPUT);
  
  attachInterrupt(Position1, Motor1, RISING);
  attachInterrupt(Position2, Motor2, RISING);
  attachInterrupt(Position3, Motor3, RISING);
  attachInterrupt(Position4, Motor4, RISING);
  
  
}

void loop() 
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();

}

void Motor1()
{
  counted++;
}
void Motor2()
{
  counted2++;
}
void Motor3()
{
  counted++;
}
void Motor4()
{
  counted2++;
}
