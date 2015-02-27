void loop() 
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
//  PID_roue1.Compute();
//  PID_roue2.Compute();
//  PID_roue3.Compute();
//  PID_roue4.Compute();
//  analogWrite(Pin_PWM4,vitesse_PWM4);
//  analogWrite(Pin_PWM3,vitesse_PWM3);
//  analogWrite(Pin_PWM2,vitesse_PWM2);
//  analogWrite(Pin_PWM1,vitesse_PWM1);
  if (Serial.available()== 2) 
  {
    Serie();    
  }
  
  if ((currentMillis - previousMillis) >= periode_echantillonnage)
    {
      vitesse_mesure_roue1 = (distance_roue1-distance_precedente_moteur1)/periode_echantillonnage;
      vitesse_mesure_roue2 = (distance_roue2-distance_precedente_moteur2)/periode_echantillonnage;
      vitesse_mesure_roue3 = (distance_roue3-distance_precedente_moteur3)/periode_echantillonnage;
      vitesse_mesure_roue4 = (distance_roue4-distance_precedente_moteur4)/periode_echantillonnage;
      
      Serial.print(currentMillis);
      Serial.print(',');
      Serial.print(Vitesse);    // Byte de vitesse commandé
      Serial.print(',');
      Serial.print(vitesse_mesure_roue1);   // Nombre de pas depuis la dernière simulation
      Serial.print(',');
      Serial.print(vitesse_mesure_roue2);  
      Serial.print(',');
      Serial.print(vitesse_mesure_roue3);  
      Serial.print(',');
      Serial.print(vitesse_mesure_roue4);  
      Serial.println(' ');
      distance_precedente_moteur1 = distance_roue1;
      distance_precedente_moteur2 = distance_roue2;
      distance_precedente_moteur3 = distance_roue3;
      distance_precedente_moteur4 = distance_roue4;
      previousMillis = currentMillis;
    }
  if(Unstarted)
  {
    digitalWrite(CW1, LOW);
    digitalWrite(CW2, LOW);
    digitalWrite(CW3, LOW);
    digitalWrite(CW4, LOW);
  
    digitalWrite(CCW1, LOW);
    digitalWrite(CCW2, LOW);
    digitalWrite(CCW3, LOW);
    digitalWrite(CCW4, LOW);
    distance_roue1 = 0;
    distance_roue2 = 0;
    distance_roue3 = 0;
    distance_roue4 = 0;
  }
  if (ident = true)
  {
    Identification(); 
  }
}


