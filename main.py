# encoding=utf-8
import math
import time
import cv2

from imgFeatures.SlideFeatureGenerator import generate_slide_feature

__author__ = 'terry'
if __name__ == "__main__":
    #
    # dst_width = 500
    # dst_height = 500
    # 生成各种特征
    features_obj_array = generate_slide_feature(10, 10, 10, rad_range=math.pi / 2)
    src_img = cv2.imread("/home/terry/FERET/FERET-001/01.tif", cv2.CV_LOAD_IMAGE_GRAYSCALE)
    # 直方图均值化
    src_img = cv2.equalizeHist(src_img)
    # 与特征做卷积
    for feature_obj in features_obj_array:
        dst = cv2.filter2D(src_img, -1, feature_obj['feature'])
        angle = feature_obj['angle'] * 180 / math.pi
        print angle
        # cv2.imwrite("/home/terry/features/" + str(angle) + ".jpg", dst)
        cv2.imshow("showme", dst)
        cv2.imshow("feature", feature_obj['feature'])
        cv2.waitKey(1)
        time.sleep(0.5)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


