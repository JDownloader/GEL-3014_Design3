void loop() 
{
  // put your main code here, to run repeatedly:
  



  if (Serial.available()== 2) 
  {
    Serie();    
  }

  int deltaTime = millis() - previousMillis;
  if ((deltaTime) >= periode_echantillonnage)
    {
      

      vitesse_mesure_roue1 = float(distance_roue1-distance_precedente_moteur1)/float(millis() - previousMillis);
      vitesse_mesure_roue2 = float(distance_roue2-distance_precedente_moteur2)/float(millis() - previousMillis);
      vitesse_mesure_roue3 = float(distance_roue3-distance_precedente_moteur3)/float(millis() - previousMillis);
      vitesse_mesure_roue4 = float(distance_roue4-distance_precedente_moteur4)/float(millis() - previousMillis);
      
      Serial.print("11,");
      Serial.print(currentMillis);
      Serial.print(",");
      Serial.print(Vitesse);
      Serial.print(",");
      Serial.println(vitesse_mesure_roue1);

      Serial.print("22,");
      Serial.print(currentMillis);
      Serial.print(",");
      Serial.print(Vitesse);
      Serial.print(",");
      Serial.println(vitesse_mesure_roue2);

      Serial.print("33,");
      Serial.print(currentMillis);
      Serial.print(",");
      Serial.print(Vitesse);
      Serial.print(",");
      Serial.println(vitesse_mesure_roue3);

      Serial.print("44,");
      Serial.print(currentMillis);
      Serial.print(",");
      Serial.print(Vitesse);
      Serial.print(",");
      Serial.println(vitesse_mesure_roue4);


      previousMillis = currentMillis;
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
  if (ident = true)
  {
    Identification(); 
  }
}


