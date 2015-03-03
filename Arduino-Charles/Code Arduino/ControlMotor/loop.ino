void loop() 
{
  // put your main code here, to run repeatedly:
  



  if (Serial.available()== 2) 
  {
    Serie();    
  }
  if(distance_roue2>10000)
  {
    FermetureGenerale();
  }
  unsigned long currentMillis = millis();
  int deltaTime = currentMillis - previousMillis;
  if ((deltaTime) >= periode_echantillonnage)
    {
      //noInterrupts();
      vitesse_mesure_roue1 = (float)(distance_roue1-distance_precedente_moteur1)/(float)deltaTime;
      //Serial.print("11,");
      PID_roue1.Compute();
      double vitesse_mesure_roue2 = (float)(distance_roue2-distance_precedente_moteur2)/(float)deltaTime;
      Serial.print("  Différence2:");
      Serial.print(distance_roue2-distance_precedente_moteur2);
      Serial.print("  Vitesse2:");
      Serial.println(vitesse_mesure_roue2,DEC);
      Serial.print("22,");
      PID_roue2.Compute();
      vitesse_mesure_roue3 = (float)(distance_roue3-distance_precedente_moteur3)/(float)deltaTime;
      Serial.print("  Différence3:");
      Serial.print(distance_roue3-distance_precedente_moteur3);
      Serial.print("  Vitesse3:");
      Serial.println(vitesse_mesure_roue3);
      Serial.print("33,");
      PID_roue3.Compute();
      vitesse_mesure_roue4 = (float)(distance_roue4-distance_precedente_moteur4)/(float)deltaTime;
      //Serial.print("44,");
      PID_roue4.Compute();
      analogWrite(Pin_PWM1,vitesse_PWM1); 
      analogWrite(Pin_PWM2,vitesse_PWM2);
      analogWrite(Pin_PWM3,vitesse_PWM3);
      analogWrite(Pin_PWM4,vitesse_PWM4);
      
      
       
      
//      Serial.print(currentMillis);
//      Serial.print(',');
//      Serial.print(Vitesse);    // Byte de vitesse commandé
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue1,DEC);   // Nombre de pas depuis la dernière simulation
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue2,DEC);  
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue3,DEC);  
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue4,DEC);  
//      Serial.println(' ');
      distance_precedente_moteur1 = distance_roue1;
      distance_precedente_moteur2 = distance_roue2;
      distance_precedente_moteur3 = distance_roue3;
      distance_precedente_moteur4 = distance_roue4;
      previousMillis = currentMillis;
      //interrupts();
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


