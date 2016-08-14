# encoding=utf-8
import math
import numpy as np
import cv2
import time

__author__ = 'terry'


# 生成特征
def generate_slide_feature(split_size=2,
                           feature_width=10,
                           feature_height=10,
                           hv=1,
                           lv=-1,
                           midv=0,
                           rad_range=math.pi / 2,
                           ex=100):
    feature_objs = []
    # 画中心点两条直线
    mid_y = int(feature_width / 2)
    s_mid_y = mid_y - 1
    mid_x = int(feature_height / 2)
    s_mid_x = mid_x - 1
    if s_mid_y >= 0:
        # 图都不大搞毛
        for i in range(0, split_size + 1):
            blank_image = np.zeros((feature_width, feature_height, 1), np.float64)
            blank_image[:, :] = midv
            delta = rad_range / split_size * i
            if delta == 0:
                # 横线特殊情况
                plus_start_point = (0, mid_y)
                plus_end_point = (feature_width, mid_y)
                minus_start_point = (0, s_mid_y)
                minus_end_point = (feature_width, s_mid_y)
                cv2.line(blank_image, plus_start_point, plus_end_point, hv)
                cv2.line(blank_image, minus_start_point, minus_end_point, lv)
            elif math.fabs(delta - math.pi / 2) < 1.0 / ex:
                # 竖线特殊情况
                plus_start_point = (mid_x, 0)
                plus_end_point = (mid_x, feature_height)
                minus_start_point = (s_mid_x, 0)
                minus_end_point = (s_mid_x, feature_height)
                cv2.line(blank_image, plus_start_point, plus_end_point, hv)
                cv2.line(blank_image, minus_start_point, minus_end_point, lv)
            else:
                tan_delta = math.tan(delta)
                plus_start_point = (0, int(mid_y - mid_x * tan_delta))
                plus_end_point = (feature_width, int(tan_delta * (feature_width - mid_x) + mid_y))
                cv2.line(blank_image, plus_start_point, plus_end_point, hv)
                # 赋值凹点
                minus_image = np.zeros((feature_width, feature_height, 1), np.float64)
                for n in range(0, feature_height):
                    for m in range(0, feature_width - 1):
                        value = blank_image[m, n]
                        if value == hv:
                            minus_image[m + 1, n] = lv
                blank_image = blank_image + minus_image
            feature_obj = {"feature": blank_image, "angle": delta}
            feature_objs.append(feature_obj)
    return feature_objs
