void FuncSerie()
{
    // read the most recent byte (which will be from 0 to 255):
    Commande      = Serial.read();
    NumeroMoteur  = Serial.read();
    Direction     = Serial.read();
    Vitesse       = Serial.read();
    
    Serial.print("Commande");
    Serial.print(Commande);
    Serial.print("    Moteur:");
    Serial.print(NumeroMoteur);
    Serial.print("    Direction:");
    Serial.println(Direction);
    Serial.print("    Vitesse:");
    Serial.println(Vitesse);
    
    if(Commande==1){
      analogWrite(NumeroMoteur, Vitesse);
    }
    if(Commande==10)
    {
      digitalWrite(CW1, High);
      digitalWrite(CCW3, High);
      analogWrite(Out_PWM_moteur_1,255);
      analogWrite(Out_PWM_moteur_3,255);
    }


}
