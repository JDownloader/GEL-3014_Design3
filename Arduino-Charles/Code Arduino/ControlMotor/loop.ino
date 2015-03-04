void loop() 
{
  if (Serial.available()== 3) 
  {
    Serie();    
  }
  if(distance_roue2>10000)
  {
    FermetureGenerale();
  }
  if(distance_roue1>(Distance*10))
  {
    FermetureGenerale();
  }
  

  
  
  if ((millis() - previousMillis) >= periode_echantillonnage)
    {
      vitesse_mesure_roue1 = float(distance_roue1-distance_precedente_moteur1)/float(millis() - previousMillis)*50.0;
      vitesse_mesure_roue2 = float(distance_roue2-distance_precedente_moteur2)/float(millis() - previousMillis)*50.0;
      vitesse_mesure_roue3 = float(distance_roue3-distance_precedente_moteur3)/float(millis() - previousMillis)*50.0;
      vitesse_mesure_roue4 = float(distance_roue4-distance_precedente_moteur4)/float(millis() - previousMillis)*50.0;
//      
//      Serial.print("Vitesse roue2:");
//      Serial.println(vitesse_mesure_roue2);
//      Serial.print("Vitesse roue3:");
//      Serial.println(vitesse_mesure_roue3);

      //Serial.print("11");
      PID_roue1.Compute();
      //Serial.print("22");
      PID_roue2.Compute();
      //Serial.print("33");
      PID_roue3.Compute();
      //Serial.print("44");
      PID_roue4.Compute();
      analogWrite(Pin_PWM1,vitesse_PWM1); 
      analogWrite(Pin_PWM2,vitesse_PWM2);
      analogWrite(Pin_PWM3,vitesse_PWM3);
      analogWrite(Pin_PWM4,vitesse_PWM4);
      
      previousMillis = millis();
      distance_precedente_moteur1 = distance_roue1;
      distance_precedente_moteur2 = distance_roue2;
      distance_precedente_moteur3 = distance_roue3;
      distance_precedente_moteur4 = distance_roue4;
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
}


