__author__ = 'Gabriel'

from enum import Enum
import serial
from serial.tools.list_ports import comports
import maestro


class Robot:
    """
    Object robot a utiliser pour la communication station de base - robot
    """

    def __init__(self):
        self.led_color = LedColor()
        self.led_controller = LedController()
        self.camera_controller = CameraController()
        self.gripper_controller = GripperController()
        self.movement_controller = MovementController()


class LedColor(Enum):
    """
    Couleurs pour les LED
    """
    red = 'R'
    green = 'G'
    blue = 'B'
    yellow = 'Y'
    white = 'W'
    black = 'K'
    off = 'F'


class LedController:
    """
    Classe qui s'occupe de faire la communication avec le controller de led
    """

    def __init__(self):

        # determiner quel port com est utilise
        for port in comports():
            if port[2].find('PID=2341') > -1:
                comPort = port[0]

        # initier la com. serial
        self.ser_com = serial.Serial(comPort, 9600)

    def led(self, color=LedColor.off, pos=9):
        """
        Attribuer une couleur (incluant off) a une DEL
        :param color: Couleur de la DEL
        :param pos: position de la DEL. 0-8 = drapeau, 9 = "control led"
        :return:
        """
        self.ser_com.write(str(pos) + color.value)
        print(str(pos) + color.value)

    def ser_com_close(self):
        """
        Fermeture de la com. CLEANUP
        """
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


class GripperController:
    def __init__(self):
        """
        Channel 2: Position verticale
        Channel 3: Pince
        """
        for port in comports():
            if port[1].find('Command') > -1:
                com_port = port[0]
                self.gripper_contr = maestro.Controller(com_port)
        self.channel_vertical = 2
        self.channel_pince = 3
        self.min_vertical = 704.00
        self.max_vertical = 2096.00
        self.pos_vertical_transport_cube = 1785.00
        self.pos_vertical_table = 1264.75
        self.min_pliers = 454.25
        self.max_pliers = 2374.50
        self.pos_pliers_open_big = 2031.00
        self.pos_pliers_open_small = 1156.75
        self.pos_pliers_closed = 850.00
        self.gripper_contr.setRange(self.channel_vertical, self.min_vertical, self.max_vertical)
        self.gripper_contr.setTarget(self.channel_vertical, self.pos_vertical_table)
        self.gripper_contr.setRange(self.channel_pince, self.min_pliers, self.max_pliers)
        self.gripper_contr.setTarget(self.channel_pince, self.pos_pliers_open_big)

    def gripper_raised(self, raised):
        """
        Leve et baisse le prehenseur
        :param raised: Bool. True = prehenseur leve, false = prehenseur a la hauteur de la table
        """
        if raised:
            self.gripper_contr.setTarget(self.channel_vertical, self.pos_vertical_transport_cube)
        else:
            self.gripper_contr.setTarget(self.channel_vertical, self.pos_vertical_table)

    def pliers_opened(self, opened, opening_size):
        """
        Ouvre et ferme les pinces
        :param opened: Bool. True = pinces ouvertes a la grosseur de size. False = pinces fermees pour prendre 1 block
        :param opening_size: small ou big. small = ouvert un peu pour deposer le cube. big = ouvert bcp pour prendre
        le cube
        """
        if not opened:
            self.gripper_contr.setTarget(self.channel_pince, self.pos_pliers_closed)
        elif opened and opening_size == 'small':
            self.gripper_contr.setTarget(self.channel_pince, self.pos_pliers_open_big)
        elif opened and opening_size == 'big':
            self.gripper_contr.setTarget(self.channel_pince, self.pos_pliers_open_small)


class MovementController:
    def __init__(self):
        # determiner quel port com est utilise
        for port in comports():
            if port[2].find('PID=2A03') > -1:
                comPort = port[0]
        # initier la com. serial
        self.ser_com = serial.Serial(comPort, 9600)
        self.mm_to_step_factor = 1

    def move(self, direction, distance, speed):
        """
        Deplacer le robot dans la direction voulue de la distance voulue a la vitesse voulue
        :param direction: Direction du deplacement par rapport a la direction de la camera embarque.
         Valeurs possibles: 'forward', 'reverse', 'left', 'right'
        :param distance: Distance en mm du deplacement
        :param speed: Vitesse du deplacement en % (0 = pas de mouvement, 100 = vitesse max)
        """
        if direction == 'forward':
            self.ser_com.write(str(1))
        elif direction == 'right':
            self.ser_com.write(str(2))
        elif direction == 'reverse':
            self.ser_com.write(str(3))
        elif direction == 'left':
            self.ser_com.write(str(4))
        else:
        # RAISE ERROR
            pass

        self.ser_com.write(str(speed))
        self.ser_com.write(str(distance * self.mm_to_step_factor))

    def ser_com_close(self):
        """
        Fermeture de la com. CLEANUP
        """
        self.ser_com.close()
