void loop() 
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  
  if (Serial.available()== 4) 
  {
    Serie();    
  }
  
  if (currentMillis - previousMillis >= 100)
    {
      Serial.print(counted1);  
      Serial.print(',');
      Serial.print(counted2);  
      Serial.print(',');
      Serial.print(counted3);  
      Serial.print(',');
      Serial.print(counted4);  
      Serial.print(',');
      Serial.println(currentMillis);
      counted1 = 0;
      counted2 = 0;
      counted3 = 0;
      counted4 = 0;
      previousMillis = currentMillis;
    }

}


