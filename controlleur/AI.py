__author__ = 'Gabriel'

etat = 0
#etat 0: startup
#etat 1: obtenir question
#etat 2: prendre cube
#etat 3: déposer cube
while True:
    if etat == 0:
        #startup stuff, etablir connection etc?
        etat = 1
    if etat == 1:
        #localiser le robot
        #se rendre à la zone atlas
        #while pos != pos_atlas:
           # pass
        #obtenir la question
        etat = 2
    if etat == 2:
        #allumer del
        #while pos - pos_cube > 300 (mm)
            #macropathfinding
        #micropathfinding
        #if pos - pos_cube > 20mm and pos - pos_cube < 40mm
        #prendre cube
        etat = 3
    if etat == 3:
        #macropathfinding
        #micropathfinding
        #deposer cube
        #if drapeau complet
            #etat = 1
        #else
            #etat = 2
        pass


