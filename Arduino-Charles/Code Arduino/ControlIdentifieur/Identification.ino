void Identification()
{
    if(previousMillisIdent-currentMillis < 100 && identSTEP == 0)
    {
      IdentificationMode(1, true, 150);
    }
    if(previousMillisIdent-currentMillis < 1000 && identSTEP == 1)
    {
      IdentificationMode(1, false, 0);
    }
    if(previousMillisIdent-currentMillis < 1500 && identSTEP == 2)
    {
      IdentificationMode(1, true, 100);
    }
    if(previousMillisIdent-currentMillis < 2000 && identSTEP == 3)
    {
      IdentificationMode(1, false, 0);
    }
    if(previousMillisIdent-currentMillis < 1300 && identSTEP == 4)
    {
      IdentificationMode(1, true, 200);
    }
    if(previousMillisIdent-currentMillis < 3000 && identSTEP == 5)
    {
      //FermetureGenerale();
      ident = false;
    }
}

void IdentificationMode(byte mode, bool etat, int vitesse)
{
  switch ( mode ) 
  {
    case 1: 
      analogWrite(Pin_PWM3,Vitesse);
      analogWrite(Pin_PWM2,Vitesse);
      
      digitalWrite(CW3, HIGH);
      digitalWrite(CCW2, HIGH);
      
      previousMillisIdent = currentMillis;
      identSTEP++;
    break;
    
    default:
      // Code
    break;
   }
}
