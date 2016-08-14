# encoding=utf-8
import cv2
import cv
import math
import time

from imgFeatures.SlideFeatureGenerator import generate_slide_feature

__author__ = 'terry'
if __name__ == "__main__":
    #
    # dst_width = 500
    # dst_height = 500
    # 生成各种特征
    features_obj_array = generate_slide_feature(500, 50, 50, rad_range=math.pi / 2)
    # 读取图像
    src_img = cv2.imread("/home/terry/Desktop/cat.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
    # src_img = cv2.resize(src_img, (dst_width, dst_height))
    # 与特征做卷积
    cv2.imshow("showme", src_img)
    cv2.waitKey(0)
    for feature_obj in features_obj_array:
        dst = cv2.filter2D(src_img, -1, feature_obj['feature'])
        angle = feature_obj['angle'] * 180 / math.pi
        cv2.imwrite("/home/terry/features/" + str(angle) + ".jpg", dst)
        cv2.imshow("showme", dst)
        cv2.imshow("feature", feature_obj['feature'])
        cv2.waitKey(1)
        time.sleep(0.01)
    cv2.waitKey(0)

