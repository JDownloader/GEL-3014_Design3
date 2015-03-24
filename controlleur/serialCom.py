__author__ = 'Gabriel'

from enum import Enum
import serial
from serial.tools.list_ports import comports
import maestro

#Couleurs pour les LED
class LedColor(Enum):
    red = 'R'
    green = 'G'
    blue = 'B'
    yellow = 'Y'
    white = 'W'
    black = 'K'
    off = 'F'


#Classe qui s'occupe de faire la communication avec le controlleur de led
class LedController:

    def __init__(self):

        #determiner quel port com est utilise
        for port in comports():
            if port[2].find('PID=2341') > -1:
                comPort = port[0]

        #initier la com. serial
        self.ser_com = serial.Serial(comPort, 9600)

    #color = Couleur de la led (on utilise les couleurs de LedColor)
    #pos = Position de la led qu'on veut allumer, de 0 a 9
    #Led du drapeau : 0 a 8
    #Led de fin de cycle = 9
    def led(self, color = LedColor.off, pos = 9):
        self.ser_com.write(str(pos) + color.value)
        print(str(pos) + color.value)

    #Fermeture de la com. CLEANUP, DOIT ETRE FAIT
    def serComClose(self):
        self.ser_com.close()


class CameraController:
    def __init__(self):
        """
        Channel 0: Position verticale
        Channel 1: Position horizontale
        """
        for port in comports():
            if port[1].find('Command') > -1:
                com_port = port[0]
                self.cam_contr = maestro.Controller(com_port)

        self.pos_vertical = 0
        self.pos_horizontal = 0
        self.channel_vertical = 0
        self.channel_horizontal = 1
        self.cam_contr.setTarget(self.channel_horizontal, self.pos_horizontal)
        self.cam_contr.setTarget(self.channel_vertical, self.pos_vertical)

    def reset_pos(self):
        self.cam_contr.setTarget(self.channel_horizontal, self.pos_horizontal)
        self.cam_contr.setTarget(self.channel_vertical, self.pos_vertical)

class PrehenseurController:
    def __init__(self):
        """
        Channel 2: Position verticale
        Channel 3: Pince
        """
        for port in comports():
            if port[1].find('Command') > -1:
                com_port = port[0]
                self.prehenseur_contr = maestro.Controller(com_port)
        self.channel_vertical = 2
        self.channel_pince = 3
        self.min_vertical = 0
        self.max_vertical = 0
        self.pos_vertical_transport_cube = 0
        self.pos_vertical_table = 0
        self.min_pince = 0
        self.max_pince = 0
        self.pos_pince_ouverte_prendre_cube = 0
        self.pos_pince_ouverte_deposer_cube = 0
        self.pos_pince_ferme_prendre_cube = 0
        self.prehenseur_contr.setRange(self.channel_vertical, self.min_vertical, self.max_vertical)
        self.prehenseur_contr.setTarget(self.channel_vertical, self.pos_vertical_table)
        self.prehenseur_contr.setRange(self.channel_pince, self.min_pince, self.max_pince)
        self.prehenseur_contr.setTarget(self.channel_pince, self.pos_pince_ouverte_prendre_cube)

    def lever_prehenseur_transport(self):
        self.prehenseur_contr.setTarget(self.channel_vertical, self.pos_vertical_transport_cube)

    def baisser_prehenseur_cube(self):
        self.prehenseur_contr.setTarget(self.channel_vertical, self.pos_vertical_table)

    def fermer_pince_cube(self):
        self.prehenseur_contr.setTarget(self.channel_pince, self.pos_pince_ferme_prendre_cube)

    def ouvrir_pince_deposer_cube(self):
        self.prehenseur_contr.setTarget(self.channel_pince, self.pos_pince_ouverte_deposer_cube)

    def ouvrir_pince_prendre_cube(self):
        self.prehenseur_contr.setTarget(self.channel_pince, self.pos_pince_ouverte_prendre_cube)


class RouesController:
    def __init__(self):
        #determiner quel port com est utilise
        for port in comports():
            if port[2].find('PID=2A03') > -1:
                comPort = port[0]
        #initier la com. serial
        self.ser_com = serial.Serial(comPort, 9600)

    def avancer_avant(self, distance, vitesse):
        """
        avancer vers l'avant
        :param distance: distance en mm.
        :param vitesse: vitesse du deplacement en %
        """
        distance_cm = distance*10

        self.ser_com.write(str(1))
        self.ser_com.write(str(vitesse))
        self.ser_com.write(str(distance_cm))

    def avancer_droite(self, distance, vitesse):
        """
        avancer vers la droite
        :param distance: distance en mm.
        :param vitesse: vitesse du deplacement en %
        """
        distance_cm = distance*10
        self.ser_com.write(str(2))
        self.ser_com.write(str(vitesse))
        self.ser_com.write(str(distance_cm))

    def reculer(self, distance, vitesse):
        """
        reculer
        :param distance: distance en mm.
        :param vitesse: vitesse du deplacement en %
        """
        distance_cm = distance*10
        self.ser_com.write(str(3))
        self.ser_com.write(str(vitesse))
        self.ser_com.write(str(distance_cm))

    def avancer_gauche(self, distance, vitesse):
        """
        avancer vers l'avant
        :param distance: distance en mm.
        :param vitesse: vitesse du deplacement en %
        """
        distance_cm = distance*10
        self.ser_com.write(str(4))
        self.ser_com.write(str(vitesse))
        self.ser_com.write(str(distance_cm))