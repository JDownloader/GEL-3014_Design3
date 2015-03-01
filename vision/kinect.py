import cv2
from distanceCalibration import DistanceCalibration

class NoKinectDetectedException(Exception):
    def __init__(self):
        pass

class Kinect():

    def __init__(self):
        self.capt_obj = cv2.VideoCapture(cv2.cv.CV_CAP_OPENNI)
        self.distanceCalibration = DistanceCalibration()
        flags, img = self.capt_obj.read()
        if flags is False:
            raise NoKinectDetectedException()

    def _apply_matrix_transformation(self, point_in_world):
        return self.distanceCalibration.apply_matrix_transformation(point_in_world)

    def grab_new_image(self):
        self.capt_obj.grab()

    def get_img_cloud_map(self):
        flags_p, img_cloud_map = self.capt_obj.retrieve(None, cv2.cv.CV_CAP_OPENNI_POINT_CLOUD_MAP)
        return img_cloud_map

    def _get_centre_object(self, img_mask):
        moments = cv2.moments(img_mask)
        area = moments['m00']
        x, y = 0, 0
        if area < 2000000 and area != 0:
            x = int(moments['m10']/area)
            y = int(moments['m01']/area)
        centre = (x, y)
        return centre

