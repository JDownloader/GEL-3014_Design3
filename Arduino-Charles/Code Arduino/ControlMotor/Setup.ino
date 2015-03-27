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
  pinMode(Pin_PWM1, OUTPUT), digitalWrite(Pin_PWM1, 0);
  pinMode(Pin_PWM2, OUTPUT), digitalWrite(Pin_PWM2, 0);
  pinMode(Pin_PWM3, OUTPUT), digitalWrite(Pin_PWM3, 0);
  pinMode(Pin_PWM4, OUTPUT), digitalWrite(Pin_PWM4, 0);
  
  attachInterrupt(CapteurHall_1, Interrupt_Motor1, RISING);
  attachInterrupt(CapteurHall_2, Interrupt_Motor2, RISING);
  attachInterrupt(CapteurHall_3, Interrupt_Motor3, FALLING);
  attachInterrupt(CapteurHall_4, Interrupt_Motor4, FALLING);
  
  
  
  Serial.begin(9600); // Ouverture du port série
  while (!Serial);    // Attente de la confirmation!
  
    


  PID_roue1.SetSampleTime(periode_echantillonnage);
  PID_roue2.SetSampleTime(periode_echantillonnage);  
  PID_roue3.SetSampleTime(periode_echantillonnage);
  PID_roue4.SetSampleTime(periode_echantillonnage);

  PID_roue1.SetMode(AUTOMATIC);
  PID_roue2.SetMode(AUTOMATIC);
  PID_roue3.SetMode(AUTOMATIC);
  PID_roue4.SetMode(AUTOMATIC);
  
  double PIDMIN = 0; // ne sert plus!
  double PIDMAX = 255; 
  PID_roue1.SetOutputLimits(PIDMIN, PIDMAX);
  PID_roue2.SetOutputLimits(PIDMIN, PIDMAX);
  PID_roue3.SetOutputLimits(PIDMIN, PIDMAX); // était à -5
  PID_roue4.SetOutputLimits(PIDMIN, PIDMAX);
  
}



