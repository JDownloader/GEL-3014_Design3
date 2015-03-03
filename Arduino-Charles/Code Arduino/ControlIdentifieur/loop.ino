void loop() 
{
  // put your main code here, to run repeatedly:
  



  if (Serial.available()== 2) 
  {
    Serie();    
  }
  unsigned long currentMillis = millis();
  int deltaTime = currentMillis - previousMillis;
  if ((deltaTime) >= periode_echantillonnage)
    {
      noInterrupts();
      vitesse_mesure_roue1 = (float)(distance_roue1-distance_precedente_moteur1)/(float)deltaTime;
      Serial.print("11,");
      Serial.print(vitesse_mesure_roue1);
      vitesse_mesure_roue2 = (float)(distance_roue2-distance_precedente_moteur2)/(float)deltaTime;
      Serial.print("22,");
      Serial.print(vitesse_mesure_roue2);
      vitesse_mesure_roue3 = (float)(distance_roue3-distance_precedente_moteur3)/(float)deltaTime;
      Serial.print("33,");
      Serial.print(vitesse_mesure_roue3);
      vitesse_mesure_roue4 = (float)(distance_roue4-distance_precedente_moteur4)/(float)deltaTime;
      Serial.print("44,");
      Serial.print(vitesse_mesure_roue4);


      
       
      
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
      interrupts();
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


