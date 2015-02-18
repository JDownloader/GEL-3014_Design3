void Identification()
{
      if(previousMillisIdent-currentMillis < 100 && identSTEP == 0)
      {
        digitalWrite(CCW1, true);
        analogWrite(Pin_PWM1,100);
      
        digitalWrite(CW3, true);
        analogWrite(Pin_PWM3,100);
        previousMillisIdent = currentMillis;
        identSTEP = 1;
      }
      if(previousMillisIdent-currentMillis < 1000 && identSTEP == 1)
      {
        digitalWrite(CCW1, true);
        analogWrite(Pin_PWM1,0);
      
        digitalWrite(CW3, true);
        analogWrite(Pin_PWM3,0);
        previousMillisIdent = currentMillis;
        identSTEP = 2;
      }
      if(previousMillisIdent-currentMillis < 1500 && identSTEP == 2)
      {
        digitalWrite(CCW1, true);
        analogWrite(Pin_PWM1,150);
      
        digitalWrite(CW3, true);
        analogWrite(Pin_PWM3,150);
        previousMillisIdent = currentMillis;
        identSTEP = 3;
      }
      if(previousMillisIdent-currentMillis < 2000 && identSTEP == 3)
      {
        digitalWrite(CCW1, true);
        analogWrite(Pin_PWM1,0);
      
        digitalWrite(CW3, true);
        analogWrite(Pin_PWM3,0);
        previousMillisIdent = currentMillis;
        identSTEP = 4;
      }
      if(previousMillisIdent-currentMillis < 1300 && identSTEP == 4)
      {
        digitalWrite(CCW1, true);
        analogWrite(Pin_PWM1,100);
      
        digitalWrite(CW3, true);
        analogWrite(Pin_PWM3,100);
        
        previousMillisIdent = currentMillis;
        identSTEP = 5;
      }
      if(previousMillisIdent-currentMillis < 3000 && identSTEP == 5)
      {
        FermetureGenerale();
        previousMillisIdent = currentMillis;
        identSTEP = 0;
        ident = false;
      }
}
