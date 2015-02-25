void loop() 
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  
  if (Serial.available()== 2) 
  {
    Serie();    
  }
  
//  if (currentMillis - previousMillis >= periode_echantillonnage)
//    {
//      vitesse_mesure_roue1 = (distance_roue1-distance_precedente_moteur1)/periode_echantillonnage;
//      vitesse_mesure_roue2 = (distance_roue2-distance_precedente_moteur1)/periode_echantillonnage;
//      vitesse_mesure_roue3 = (distance_roue3-distance_precedente_moteur1)/periode_echantillonnage;
//      vitesse_mesure_roue4 = (distance_roue4-distance_precedente_moteur1)/periode_echantillonnage;
//      
//      Serial.println(currentMillis);
//      Serial.print(Vitesse);    // Byte de vitesse commandé
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue1);   // Nombre de pas depuis la dernière simulation
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue2);  
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue3);  
//      Serial.print(',');
//      Serial.print(vitesse_mesure_roue4);  
//      Serial.print(',');
//      distance_precedente_moteur1 = distance_roue1;
//      distance_precedente_moteur2 = distance_roue2;
//      distance_precedente_moteur3 = distance_roue3;
//      distance_precedente_moteur4 = distance_roue4;
//      previousMillis = currentMillis;
//    }

  if (ident = true)
  {
    Identification(); 
  }
}


