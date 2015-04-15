from camera import Camera
from visionRobot import VisionRobot

if __name__ == "__main__":
    vision = VisionRobot('blue')
    print vision.find_cube_center()