import numpy as np
import cv2


class KinectCaptureHelper():
    def save_kinect_capture(self, kinect, file_name, img_rgb=None):
        try:
            map = kinect.get_img_cloud_map()
            np.save('capture/' + file_name + '.npy', map)
            if img_rgb is None:
                img_rgb = kinect.grab_new_image()
            cv2.imwrite('capture/' + file_name + '.png', img_rgb)
        except Exception:
            pass