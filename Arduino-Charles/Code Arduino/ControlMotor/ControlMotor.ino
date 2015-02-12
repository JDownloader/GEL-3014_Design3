// Gestion du temps!
unsigned long previousMillis1 = 0;
unsigned long previousMillis2 = 0;
unsigned long previousMillis3 = 0;
unsigned long previousMillis4 = 0;
unsigned long currentMillis = 0;
// Descriptiond des pins!

  // outputs
  int Out_PWM_moteur_1  = 10;
  int Out_PWM_moteur_2  = 11;
  int Out_PWM_moteur_3  = 12;
  int Out_PWM_moteur_4  = 13;
  
  int CW1    = 46;  //Moteur #1 pin ClockWise  
  int CCW1   = 47;  //Moteur #1 pin CounterClockWise  
  int CW2    = 48;  //Moteur #2 pin ClockWise  
  int CCW2   = 49;  //Moteur #2 pin CounterClockWise  
  int CW3    = 50;  //Moteur #3 pin ClockWise  
  int CCW3   = 51;  //Moteur #3 pin CounterClockWise  
  int CW4    = 52;  //Moteur #4 pin ClockWise  
  int CCW4   = 53;  //Moteur #4 pin CounterClockWise  
  
  // Vitesse de fonctionnement
  byte Speed1 = 0; // Vitesse Moteur #1
  byte Speed2 = 0; // Vitesse Moteur #2
  byte Speed3 = 0; // Vitesse Moteur #3
  byte Speed4 = 0; // Vitesse Moteur #4
  
  //Inputs
  int CapteurHall_1   = 42;  // Capteur Hall Moteur #1
  int CapteurHall_2    = 43;  // Capteur Hall Moteur #2
  int CapteurHall_3    = 44;  // Capteur Hall Moteur #3
  int CapteurHall_4    = 45;  // Capteur Hall Moteur #4
  
  // Compteurs de distance
  unsigned int counted1 = 0;
  unsigned int counted2 = 0;
  unsigned int counted3 = 0;
  unsigned int counted4 = 0;

  // Constante la communication serial
  byte Commande      = 0;
  byte NumeroMoteur  = 0;
  byte Direction     = 0;
  byte Vitesse         = 0;
  

  

