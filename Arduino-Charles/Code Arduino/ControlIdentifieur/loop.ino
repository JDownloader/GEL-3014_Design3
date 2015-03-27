void loop() 
{

  if (Serial.available()== 2) 
  {
    Serie();    
  }
  
  if ((millis() - previousMillis) >= periode_echantillonnage)
    {
      //currentMillis = millis()
      vitesse_mesure_roue1 = (float(distance_roue1-distance_precedente_moteur1))/(float(millis() - previousMillis));
      vitesse_mesure_roue2 = (float(distance_roue2-distance_precedente_moteur2))/(float(millis() - previousMillis));
      vitesse_mesure_roue3 = (float(distance_roue3-distance_precedente_moteur3))/(float(millis() - previousMillis));
      vitesse_mesure_roue4 = (float(distance_roue4-distance_precedente_moteur4))/(float(millis() - previousMillis));
      
      previousMillis = millis();
      distance_precedente_moteur1 = distance_roue1;
      distance_precedente_moteur2 = distance_roue2;
      distance_precedente_moteur3 = distance_roue3;
      distance_precedente_moteur4 = distance_roue4;

//      Serial.print("11,");
//      Serial.print(millis());
//      Serial.print(",");
//      Serial.print(Vitesse);
//      Serial.print(",");
//      Serial.print(distance_roue1);
//      Serial.print(",");
//      Serial.print(distance_precedente_moteur1);
//      Serial.print(",");
//      Serial.println(vitesse_mesure_roue1, DEC);
//      //Serial.println(distance_roue1);

      Serial.print("22,");
      Serial.print(millis());
      Serial.print(",");
      Serial.print(previousMillis2);
      Serial.print(",");  
      Serial.print(Vitesse);
      Serial.print(",");
      Serial.print(distance_roue2);
      Serial.print(",");
      Serial.print(distance_precedente_moteur2);
      Serial.print(",");
      Serial.println(vitesse_mesure_roue2, DEC);
      //Serial.println(distance_roue2);

      Serial.print("33,");
      Serial.print(millis());
      Serial.print(",");
      Serial.print(Vitesse);
      Serial.print(",");
      Serial.print(distance_roue3);
      Serial.print(",");
      Serial.print(distance_precedente_moteur3);
      Serial.print(",");
      Serial.println(vitesse_mesure_roue3, DEC);
      // Serial.println(distance_roue3);

//      Serial.print("44,");
//      Serial.print(millis());
//      Serial.print(",");
//      Serial.print(Vitesse);
//      Serial.print(",");
//      Serial.print(distance_roue4);
//      Serial.print(",");
//      Serial.print(distance_precedente_moteur4);
//      Serial.print(",");
//      Serial.println(vitesse_mesure_roue4, DEC);
//      //Serial.println(distance_roue4);


      

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


