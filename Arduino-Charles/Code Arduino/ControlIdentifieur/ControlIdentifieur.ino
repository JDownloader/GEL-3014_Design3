// Descriptiond des pins!

  // outputs
    // Commande vitesse
      #define Pin_PWM1   3
      #define Pin_PWM2   4
      #define Pin_PWM3   5
      #define Pin_PWM4   6
      
//    Nouvelle position
      #define CW1     23  //Moteur #1 pin ClockWise  
      #define CCW1    25  //Moteur #1 pin CounterClockWise  
      #define CW2     22  //Moteur #2 pin ClockWise  
      #define CCW2    24  //Moteur #2 pin CounterClockWise  
      #define CW3     27  //Moteur #3 pin ClockWise  
      #define CCW3    29  //Moteur #3 pin CounterClockWise  
      #define CW4     26  //Moteur #4 pin ClockWise  
      #define CCW4    28  //Moteur #4 pin CounterClockWise  
    
  // Inputs
    #define CapteurHall_1     31  // Capteur Hall Moteur #1
    #define CapteurHall_2     33  // Capteur Hall Moteur #2
    #define CapteurHall_3     30  // Capteur Hall Moteur #3
    #define CapteurHall_4     32  // Capteur Hall Moteur #4

// Vitesse de fonctionnement - Variable commandée?!?
  double vitesse_PWM1 = 0; // Vitesse Moteur #1
  double vitesse_PWM2 = 0; // Vitesse Moteur #2
  double vitesse_PWM3 = 0; // Vitesse Moteur #3
  double vitesse_PWM4 = 0; // Vitesse Moteur #4
  
  double vitesse_mesure_roue1 = 0;  //Vitesse mesurée
  double vitesse_mesure_roue2 = 0;  //Vitesse mesurée
  double vitesse_mesure_roue3 = 0;  //Vitesse mesurée
  double vitesse_mesure_roue4 = 0;  //Vitesse mesurée
      
// Compteurs de distance
  int distance_roue1 = 0;
  int distance_roue2 = 0;
  int distance_roue3 = 0;
  int distance_roue4 = 0;
  
  int distance_precedente_moteur1 = 0;
  int distance_precedente_moteur2 = 0;
  int distance_precedente_moteur3 = 0;
  int distance_precedente_moteur4 = 0;
  

  int periode_echantillonnage = 50; // Période d'échantillonnage en milli secondes
  double vitesse_PID; // identique à vitesse mais type double VS byte
  
// Constante la communication serial
  byte Commande      = 0;
  byte NumeroMoteur  = 0;
  byte Direction     = 0;
  byte Vitesse       = 0;
  

  
// Variable d'état
  bool ident = false;
  int  identSTEP = 0;
  bool Unstarted = 1;

// Gestion du temps!
  unsigned long previousMillis  = 0;
  unsigned long previousMillis1 = 0;
  unsigned long previousMillis2 = 0;
  unsigned long previousMillis3 = 0;
  unsigned long previousMillis4 = 0;
  unsigned long previousMillisIdent = 0;
  unsigned long currentMillis = 0;
  

  


