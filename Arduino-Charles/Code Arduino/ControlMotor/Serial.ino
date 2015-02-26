void Serie()
{

    // read the most recent byte (which will be from 0 to 255):
    Commande      = Serial.read();
    Vitesse       = Serial.read();
    
    Serial.print("Commande");
    Serial.print(Commande);
    Serial.print("    Vitesse: ");
    Serial.println(Vitesse);
    
  Unstarted = 0;
  switch ( Commande ) 
  {
    
    case 1:
      // DROIT DEVANT !
      FermetureGenerale();

      digitalWrite(CCW3, HIGH);
      analogWrite(Pin_PWM3,Vitesse);
      
      digitalWrite(CW2, HIGH);
      analogWrite(Pin_PWM2,Vitesse);
      break;
    case 2:
      // TRIBORD TOUTE (droite) !
      FermetureGenerale();

      
      digitalWrite(CCW1, HIGH);
      analogWrite(Pin_PWM1,Vitesse);
      
      digitalWrite(CW4, HIGH);
      analogWrite(Pin_PWM4,Vitesse);
      break;
    case 3:
      // On se replis !!
      FermetureGenerale();

      digitalWrite(CW3, HIGH);
      analogWrite(Pin_PWM3,Vitesse);
      
      digitalWrite(CCW2, HIGH);
      analogWrite(Pin_PWM2,Vitesse);
      break;
    case 4:
      // Mouissallions à babord !!
      FermetureGenerale();
      
      digitalWrite(CW1, HIGH);
      analogWrite(Pin_PWM1,Vitesse);
      
      digitalWrite(CCW4, HIGH);
      analogWrite(Pin_PWM4,Vitesse);
      break;
    case 101:
      // DANGERRRRRRR !!
      FermetureGenerale();
      digitalWrite(CW1, HIGH);
      analogWrite(Pin_PWM1,Vitesse);
      digitalWrite(CW2, HIGH);
      analogWrite(Pin_PWM2,Vitesse);
      digitalWrite(CW3, HIGH);
      analogWrite(Pin_PWM3,Vitesse);
      digitalWrite(CW4, HIGH);
      analogWrite(Pin_PWM4,Vitesse);

      break;
    case 102:
      // DANGERRRRRRR !!
      FermetureGenerale();
      digitalWrite(CCW1, HIGH);
      analogWrite(Pin_PWM1,Vitesse);
      digitalWrite(CCW2, HIGH);
      analogWrite(Pin_PWM2,Vitesse);
      digitalWrite(CCW3, HIGH);
      analogWrite(Pin_PWM3,Vitesse);
      digitalWrite(CCW4, HIGH);
      analogWrite(Pin_PWM4,Vitesse);

      break;
    case 103:
      // Identification !!
      FermetureGenerale();
      ident = true;
      identSTEP = 0;
      previousMillisIdent = currentMillis;
      break;
      
    case 104:
      // Identification !!
      FermetureGenerale();
      ident = false;
      identSTEP = 0;
      previousMillisIdent = currentMillis;
      break;
   case 105:
      digitalWrite(31, HIGH);
      break;
   case 106:
      digitalWrite(31, LOW);
      break;
    default:
      // Code
      break;
  }
}

void FermetureGenerale()
{
    digitalWrite(CW1, LOW);
    digitalWrite(CW2, LOW);
    digitalWrite(CW3, LOW);
    digitalWrite(CW4, LOW);
  
    digitalWrite(CCW1, LOW);
    digitalWrite(CCW2, LOW);
    digitalWrite(CCW3, LOW);
    digitalWrite(CCW4, LOW);
}

