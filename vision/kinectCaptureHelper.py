import numpy as np
import cv2
import sys
from os import path

here = path.abspath(path.dirname(__file__))


class KinectCaptureHelper():
    def save_kinect_capture(self, kinect, file_name, img_rgb=None):
        try:
            map = kinect.get_img_cloud_map()
            np.save(here + '/capture/' + file_name + '.npy', map)
            if img_rgb is None:
                img_rgb = kinect.grab_new_image()
            cv2.imwrite(here + '/capture/' + file_name + '.png', img_rgb)
        except Exception:
            print sys.exc_info()