void Serie()
{

    // read the most recent byte (which will be from 0 to 255):
    Commande      = Serial.read();
    Vitesse       = Serial.read();
    //Distance      = Serial.read();
    
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
      
      distance_roue2 = 0;
      distance_roue3 = 0;
      
      vitesse_PID2 = Vitesse;
      vitesse_PID3 = Vitesse; 
      
      
      digitalWrite(CCW3, HIGH);
      digitalWrite(CW2, HIGH);
      PID_roue2.SetMode(1);
      PID_roue3.SetMode(1);



      break;
    case 2:
      // TRIBORD TOUTE (droite) !
      FermetureGenerale();

      distance_roue1 = 0;
      distance_roue4 = 0;
      
      vitesse_PID1 = Vitesse;
      vitesse_PID4 = Vitesse;

      
      digitalWrite(CCW1, HIGH);
      digitalWrite(CW4, HIGH);
      
//      analogWrite(Pin_PWM1,Vitesse);
//      analogWrite(Pin_PWM4,Vitesse);
      break;
    case 3:
      // On se replis !!
      FermetureGenerale();
      
      distance_roue2 = 0;
      distance_roue3 = 0;

      vitesse_PID3 = Vitesse; 
      vitesse_PID2 = Vitesse;

      digitalWrite(CW3, HIGH);
      digitalWrite(CCW2, HIGH);
      PID_roue2.SetMode(1);
      PID_roue3.SetMode(1);

      break;
    case 4:
      // Mouissallions à babord !!
      FermetureGenerale();
      distance_roue1 = 0;
      distance_roue4 = 0;
      vitesse_PID1 = Vitesse;
      vitesse_PID4 = Vitesse;

      
      digitalWrite(CW1, HIGH);
      digitalWrite(CCW4, HIGH);

      break;
    case 101:
      // DANGERRRRRRR !!
      FermetureGenerale();
      distance_roue1 = 0;
      distance_roue2 = 0;
      distance_roue3 = 0;
      distance_roue4 = 0;
      vitesse_PID1 = Vitesse;
      vitesse_PID2 = Vitesse;
      vitesse_PID3 = Vitesse; 
      vitesse_PID4 = Vitesse;
      digitalWrite(CW1, HIGH);
      digitalWrite(CW2, HIGH);
      digitalWrite(CW3, HIGH);
      digitalWrite(CW4, HIGH);


      break;
    case 102:
      // DANGERRRRRRR !!
      FermetureGenerale();
      distance_roue1 = 0;
      distance_roue2 = 0;
      distance_roue3 = 0;
      distance_roue4 = 0;
      vitesse_PID1 = Vitesse;
      vitesse_PID2 = Vitesse;
      vitesse_PID3 = Vitesse; 
      vitesse_PID4 = Vitesse;
      digitalWrite(CCW1, HIGH);
      digitalWrite(CCW2, HIGH);
      digitalWrite(CCW3, HIGH);
      digitalWrite(CCW4, HIGH);



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
   case 99:
      FermetureGenerale();
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
    
    PID_roue1.SetMode(0);
    PID_roue2.SetMode(0);
    PID_roue3.SetMode(0);
    PID_roue4.SetMode(0);
    
    vitesse_PID1 = 0;
    vitesse_PID2 = 0;
    vitesse_PID3 = 0; 
    vitesse_PID4 = 0;
    
    PID_roue1.Reset();
    PID_roue2.Reset();
    PID_roue3.Reset();
    PID_roue4.Reset();
    
    distance_precedente_moteur1 = 0;
    distance_precedente_moteur2 = 0;
    distance_precedente_moteur3 = 0;
    distance_precedente_moteur4 = 0;
    
    distance_roue1 = 0;
    distance_roue2 = 0;
    distance_roue3 = 0;
    distance_roue4 = 0;
    
    
 
}

