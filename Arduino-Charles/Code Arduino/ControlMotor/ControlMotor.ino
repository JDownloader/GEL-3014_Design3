#include <PID_v1.h>
// Descriptiond des pins!

  // outputs
    // Commande vitesse
      int Pin_PWM1  = 3;
      int Pin_PWM2  = 4;
      int Pin_PWM3  = 5;
      int Pin_PWM4  = 6;
    
    // Sens de rotation
      int CW1    = 53;  //Moteur #1 pin ClockWise  
      int CCW1   = 52;  //Moteur #1 pin CounterClockWise  
      int CW2    = 51;  //Moteur #2 pin ClockWise  
      int CCW2   = 50;  //Moteur #2 pin CounterClockWise  
      int CW3    = 49;  //Moteur #3 pin ClockWise  
      int CCW3   = 48;  //Moteur #3 pin CounterClockWise  
      int CW4    = 47;  //Moteur #4 pin ClockWise  
      int CCW4   = 46;  //Moteur #4 pin CounterClockWise  
    
  // Inputs
    int CapteurHall_1    = 42;  // Capteur Hall Moteur #1
    int CapteurHall_2    = 43;  // Capteur Hall Moteur #2
    int CapteurHall_3    = 44;  // Capteur Hall Moteur #3
    int CapteurHall_4    = 45;  // Capteur Hall Moteur #4
  
// Vitesse de fonctionnement - Variable commandée?!?
  double vitesse_PWM1 = 0; // Vitesse Moteur #1
  double vitesse_PWM2 = 0; // Vitesse Moteur #2
  double vitesse_PWM3 = 0; // Vitesse Moteur #3
  double vitesse_PWM4 = 0; // Vitesse Moteur #4
    
// Compteurs de distance
  unsigned int distance_roue1 = 0;
  unsigned int distance_roue2 = 0;
  unsigned int distance_roue3 = 0;
  unsigned int distance_roue4 = 0;
  
  unsigned int distance_precedente_moteur1 = 0;
  unsigned int distance_precedente_moteur2 = 0;
  unsigned int distance_precedente_moteur3 = 0;
  unsigned int distance_precedente_moteur4 = 0;
  
  double vitesse_mesure_roue1 = 0;
  double vitesse_mesure_roue2 = 0;
  double vitesse_mesure_roue3 = 0;
  double vitesse_mesure_roue4 = 0;
  
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

// Gestion du temps!
  unsigned long previousMillis  = 0;
  unsigned long previousMillis1 = 0;
  unsigned long previousMillis2 = 0;
  unsigned long previousMillis3 = 0;
  unsigned long previousMillis4 = 0;
  unsigned long previousMillisIdent = 0;
  unsigned long currentMillis = 0;


