void Serie()
{
    // read the most recent byte (which will be from 0 to 255):
    Commande      = Serial.read();
    NumeroMoteur  = Serial.read();
    Direction     = Serial.read();
    Vitesse       = Serial.read();
    
    Serial.print("Commande");
    Serial.print(Commande);
    Serial.print("    Moteur:");     //Sera inutile
    Serial.print(NumeroMoteur);      //Sera inutile
    Serial.print("    Direction:");  //Sera inutile
    Serial.println(Direction);       //Sera inutile
    Serial.print("    Vitesse:");
    Serial.println(Vitesse);
    
  
  switch ( Commande ) 
  {
    case 1:
      // DROIT DEVANT !
      digitalWrite(CW1, true);
      digitalWrite(CCW1, false);
      analogWrite(Pin_PWM1,Vitesse);
      
      digitalWrite(CW1, false);
      digitalWrite(CCW3, true);
      analogWrite(Pin_PWM3,Vitesse);

      break;
    case 2:
      // TRIBORD TOUTE (droite) !
      digitalWrite(CW2, true);
      digitalWrite(CCW2, false);
      analogWrite(Pin_PWM2,Vitesse);
      
      digitalWrite(CW4, false);
      digitalWrite(CCW4, true);
      analogWrite(Pin_PWM4,Vitesse);
      break;
    default:
      // Code
      break;
}

}
