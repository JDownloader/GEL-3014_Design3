void loop() 
{
  // put your main code here, to run repeatedly:
  unsigned long currentMillis = millis();
  
  if (Serial.available()== 4) 
  {
    Serie();    
   }
}

