#include <PID_v1.h>
// Descriptiond des pins!

  // outputs
    // Commande vitesse
      #define Pin_PWM1   3
      #define Pin_PWM2   4
      #define Pin_PWM3   5
      #define Pin_PWM4   6
    
    // Sens de rotation
      #define CW1     53  //Moteur #1 pin ClockWise  
      #define CCW1    52  //Moteur #1 pin CounterClockWise  
      #define CW2     51  //Moteur #2 pin ClockWise  
      #define CCW2    50  //Moteur #2 pin CounterClockWise  
      #define CW3     49  //Moteur #3 pin ClockWise  
      #define CCW3    48  //Moteur #3 pin CounterClockWise  
      #define CW4     47  //Moteur #4 pin ClockWise  
      #define CCW4    46  //Moteur #4 pin CounterClockWise  
    
  // Inputs
    #define CapteurHall_1     42  // Capteur Hall Moteur #1
    #define CapteurHall_2     43  // Capteur Hall Moteur #2
    #define CapteurHall_3     44  // Capteur Hall Moteur #3
    #define CapteurHall_4     45  // Capteur Hall Moteur #4
    
    #define periode_echantillonnage 5 // Période d'échantillonnage en milli secondes
    
// Variable commandée
  double vitesse_PWM1 = 0; // Vitesse Moteur #1
  double vitesse_PWM2 = 0; // Vitesse Moteur #2
  double vitesse_PWM3 = 0; // Vitesse Moteur #3
  double vitesse_PWM4 = 0; // Vitesse Moteur #4
  
// Variable mesurée
  double vitesse_mesure_roue1 = 0;  // Vitesse mesurée
  double vitesse_mesure_roue2 = 0;
  double vitesse_mesure_roue3 = 0;
  double vitesse_mesure_roue4 = 0;
   
// Compteurs de distance
  volatile int distance_roue1 = 0;
  volatile int distance_roue2 = 0;
  volatile int distance_roue3 = 0;
  volatile int distance_roue4 = 0;
  
  int distance_precedente_moteur1 = 0;
  int distance_precedente_moteur2 = 0;
  int distance_precedente_moteur3 = 0;
  int distance_precedente_moteur4 = 0;
  
  double vitesse_PID1 = 0;
  double vitesse_PID2 = 0;
  double vitesse_PID3 = 0;
  double vitesse_PID4 = 0;

  

  
// Constante la communication serial
  byte Commande      = 0;
  byte Vitesse       = 0;
  byte Distance      = 0;

  
// Variable d'état
  bool Unstarted = 1;

// Gestion du temps!
  volatile unsigned long previousMillis  = 0;
  volatile unsigned long currentMillis = 0;



  
  #define kp  6 //11.3 //24.16; //
  #define ki  50 //0.8817;//
  #define kd  0
  
  PID PID_roue1(&vitesse_mesure_roue1, &vitesse_PWM1, &vitesse_PID1,kp,ki,kd, DIRECT);
  PID PID_roue2(&vitesse_mesure_roue2, &vitesse_PWM2, &vitesse_PID2,kp,ki,kd, DIRECT);
  PID PID_roue3(&vitesse_mesure_roue3, &vitesse_PWM3, &vitesse_PID3,kp,ki,kd, DIRECT);
  PID PID_roue4(&vitesse_mesure_roue4, &vitesse_PWM4, &vitesse_PID4,kp,ki,kd, DIRECT);
 

  


