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
      FermetureGenerale();
      digitalWrite(CW1, true);
      analogWrite(Pin_PWM1,Vitesse);
      
      digitalWrite(CCW3, true);
      analogWrite(Pin_PWM3,Vitesse);

      break;
    case 2:
      // TRIBORD TOUTE (droite) !
      FermetureGenerale();
      digitalWrite(CW2, true);
      analogWrite(Pin_PWM2,Vitesse);
      
      digitalWrite(CCW4, true);
      analogWrite(Pin_PWM4,Vitesse);
      
      break;
    case 3:
      // On se replis !!
      FermetureGenerale();
      digitalWrite(CCW1, true);
      analogWrite(Pin_PWM1,Vitesse);
      
      digitalWrite(CW3, true);
      analogWrite(Pin_PWM3,Vitesse);

      break;
    case 4:
      // Mouissallions à babord !!
      FermetureGenerale();
      digitalWrite(CW2, true);
      analogWrite(Pin_PWM2,Vitesse);
      
      digitalWrite(CCW4, true);
      analogWrite(Pin_PWM4,Vitesse);

      break;
    case 101:
      // DANGERRRRRRR !!
      FermetureGenerale();
      digitalWrite(CW1, true);
      analogWrite(Pin_PWM1,Vitesse);
      digitalWrite(CW2, true);
      analogWrite(Pin_PWM2,Vitesse);
      digitalWrite(CW3, true);
      analogWrite(Pin_PWM3,Vitesse);
      digitalWrite(CW4, true);
      analogWrite(Pin_PWM4,Vitesse);

      break;
    case 102:
      // Identification !!
      FermetureGenerale();
      ident = true;
      previousMillisIdent = currentMillis;
      break;
      
    default:
      // Code
      break;
}

}
