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
    mid_y = int(feature_height / 2)
    s_mid_y = mid_y - 1
    mid_x = int(feature_width / 2)
    s_mid_x = mid_x - 1
    if s_mid_y >= 0:
        # 图都不大搞毛
        for i in range(0, split_size + 1):
            blank_image = np.zeros((feature_height, feature_width, 1), np.float64)
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
                plus_end_point = (feature_height, int(tan_delta * (feature_height - mid_x) + mid_y))
                cv2.line(blank_image, plus_start_point, plus_end_point, hv)
                # 赋值凹点
                for m in range(0, feature_width):
                    h_time = 0
                    h_start = -1
                    for n in range(0, feature_height):
                        value = blank_image[n, m]
                        if h_start == -1 and value == hv:
                            h_start = n
                            h_time += 1
                        elif value == hv and h_start != -1:
                            h_time += 1
                        elif h_time != 0 and value == midv:
                            break
                    #
                    if h_start != -1:
                        for n in range(h_start + h_time, h_start + 2 * h_time + 1):
                            if n < feature_height and h_time > 0:
                                blank_image[n, m] = -1
                                h_time -= 1
                            else:
                                break
            feature_obj = {"feature": blank_image, "angle": delta}
            feature_objs.append(feature_obj)
    return feature_objs
