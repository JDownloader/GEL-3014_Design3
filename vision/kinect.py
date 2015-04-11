import cv2
from distanceCalibration import DistanceCalibration
import numpy as np



class NoKinectDetectedException(Exception):
    def __init__(self):
        pass


class Kinect():
    def __init__(self, table):
        self.capt_obj = cv2.VideoCapture(cv2.cv.CV_CAP_OPENNI)
        self.table = table
        self.distanceCalibration = DistanceCalibration(self.table)
        flags, img = self.capt_obj.read()
        if flags is False:
            raise NoKinectDetectedException()

    def _apply_matrix_transformation(self, point_in_world):
        position = self.distanceCalibration.apply_matrix_transformation(point_in_world)
        return (int(position[0]*1000), int(position[1]*1000+40))

    def grab_new_image(self, bilateral_filter_activated=False, median_filter_activated=False):
        self.capt_obj.grab()
        flags, img = self.capt_obj.retrieve(None, cv2.cv.CV_CAP_OPENNI_BGR_IMAGE)
        if not flags:
            print >> self.capt_obj.stderr, "Error with RGB image"
            return None
        else:
            if bilateral_filter_activated:
                img_bi = img[200:340, :]
                img_bi = cv2.bilateralFilter(img_bi, 20, 25, 25)
                img = np.concatenate([img[0:199, :], img_bi, img[341:480, :]])
            if median_filter_activated:
                img = cv2.medianBlur(img, 5)
        return img

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

    def find_object_position(self, img_mask, x_shift=0):
        position_in_world = self._find_position_in_world(img_mask, x_shift)
        position = self._apply_matrix_transformation(position_in_world)
        return position

    def _find_position_in_world(self, img_mask, x_shift=0):
        point_centre = self._get_centre_object(img_mask)
        point1_ref = self._get_world_in_cloud(point_centre, x_shift)
        return np.mat(point1_ref)

    def _get_world_in_cloud(self, point_centre, x_shift=0):
        pixel_cloud = self.get_img_cloud_map()
        point_world = pixel_cloud[point_centre[1] + x_shift, point_centre[0]]
        point_ref = [[-point_world[0]], [point_world[2]], [1]]
        return point_ref