void setup() 
{
  // Déclaration des pins
  pinMode(CW1, OUTPUT), digitalWrite(CW1, LOW);
  pinMode(CW2, OUTPUT), digitalWrite(CW2, LOW);
  pinMode(CW3, OUTPUT), digitalWrite(CW3, LOW);
  pinMode(CW4, OUTPUT), digitalWrite(CW4, LOW);
  pinMode(CCW1, OUTPUT), digitalWrite(CCW1, LOW);
  pinMode(CCW2, OUTPUT), digitalWrite(CCW2, LOW);
  pinMode(CCW3, OUTPUT), digitalWrite(CCW3, LOW);
  pinMode(CCW4, OUTPUT), digitalWrite(CCW4, LOW);
  
  // PWM
  pinMode(SortieVitesse1, OUTPUT), digitalWrite(SortieVitesse1, 0);
  pinMode(SortieVitesse2, OUTPUT), digitalWrite(SortieVitesse2, 0);
  pinMode(SortieVitesse3, OUTPUT), digitalWrite(SortieVitesse3, 0);
  pinMode(SortieVitesse4, OUTPUT), digitalWrite(SortieVitesse4, 0);
  
  attachInterrupt(CapteurHall_1, Interrupt_Motor1, RISING);
  attachInterrupt(CapteurHall_2, Interrupt_Motor2, RISING);
  attachInterrupt(CapteurHall_3, Interrupt_Motor3, RISING);
  attachInterrupt(CapteurHall_4, Interrupt_Motor4, RISING);
  
  
  Serial.begin(9600); // Ouverture du port série
  while (!Serial);    // Attente de la confirmation!
}



