

class RobotCommand():
    def perform_command(self, robot):
        pass


class LedColor(RobotCommand):
    """
    Attribuer une couleur (incluant off) a une DEL
    """
    def __init__(self, led_color, led_pos):
        """
        :param color: Couleur de la DEL. Liste des couleurs:
        red = 'R'
        green = 'G'
        blue = 'B'
        yellow = 'Y'
        white = 'W'
        black = 'K'
        off = 'F'
        :param led_pos: position de la DEL. 0-8 = drapeau, 9 = "control led"
        """
        self.led_color = led_color
        self.led_pos = led_pos

    def perform_command(self, robot):
        robot.led_controller.led(self.led_color, self.led_pos)


class LedEndSerialCommunication(RobotCommand):
    """
    Cleanup de la communication serial. Fermeture de celle-ci
    """
    def __init__(self):
        pass

    def perform_command(self, robot):
        robot.led_controller.ser_com_close()


class CameraResetPos(RobotCommand):
    """
    Reset la position de la camera embarquee a sa position initiale
    """
    def __init__(self):
        pass

    def perform_command(self, robot):
        robot.camera_controller.reset_pos()


class GripperPosition(RobotCommand):
    """
    Position verticale du prehenseur
    """
    def __init__(self, raised):
        """
        :param raised: Bool. True = prehenseur leve, False = prehenseur a la hauteur de la table
        """
        self.raised = raised

    def perform_command(self, robot):
        robot.gripper_controller.gripper_raised(self.raised)

class GripperPliers(RobotCommand):
    """
    Ouvre ou ferme les pinces du prehenseur
    """
    def __init__(self, opened, size='small'):
        """
        :param opened: Bool. True = pinces ouvertes, False = pinces fermees
        :param size: 'small' = ouerture petite (deposer le cube) 'big' = grosse ouverture (prendre cube). Affecte
        seulement opened = True
        """
        self.opened = opened
        self.size = size

    def perform_command(self, robot):
        robot.gripper_controller.pliers_opened(self.opened, self.size)


class Move(RobotCommand):
    """
    Deplacer le robot
    """
    def __init__(self, direction, distance, speed):
        """
        Deplacer le robot dans la direction voulue de la distance voulue a la vitesse voulue
        :param direction: Direction du deplacement par rapport a la direction de la camera embarque.
         Valeurs possibles: 'forward', 'reverse', 'left', 'right'
        :param distance: Distance en mm du deplacement
        :param speed: Vitesse du deplacement en % (0 = pas de mouvement, 100 = vitesse max)
        :return:
        """
        self.direction = direction
        self.distance = distance
        self.speed = speed

    def perform_command(self, robot):
        robot.movement_controller.move(self.direction, self.distance, self.speed)


class MoveEndSerialCommunication(RobotCommand):
    """
    Terminer la communication serial. CLEANUP
    """
    def __init__(self):
        pass

    def perform_command(self, robot):
        robot.movement_controller.ser_com_close()