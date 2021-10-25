from io import BytesIO
from PIL import Image
import requests
from bs4 import BeautifulSoup
from urllib import request
from urllib.request import urlopen
import re
import os
import sys
import json
import datetime
import numpy as np
import skimage.draw
import imgaug
import cv2
import matplotlib.pyplot as plt
from timeit import default_timer as timer
import colorsys
import imageio
import custom
# python custom.py splash --weights=logs\mask_rcnn_experiment_0096.h5 --image=KakaoTalk_20210927_204431533_19.jpg

color_hsv = {'white': [0, 0, 100], 'yellow': [60, 100, 100], 'orange': [25, 80, 100], 'pink': [300, 100, 100],
                 'red': [0, 100, 100],
                 'brown': [14, 65, 69], 'mild_green': [130, 45, 55], 'green': [135, 65, 65],
                 'bluish_green': [180, 100, 50], 'blue': [261, 100, 100],
                 'blue2': [244, 70, 90], 'blue3': [196, 80, 90], 'navy': [227, 60, 78], 'light_purple': [324, 73, 73],
                 'purple': [263, 77, 76], 'gray': [33, 8, 55], 'black': [0, 0, 0]}

# model = "C:/Users/user/PycharmProjects/maskrcnn-custom/logs/mask_rcnn_experiment_0096.h5"
# img_link = "C:/Users/user/PycharmProjects/maskrcnn-custom/KakaoTalk_20210927_204431533_19.jpg"

def get_img_inform(model, img_link):#custom파일에서 이미지 정보 출력
    result = custom.detect_and_color_splash(model, img_link)
    shape_list = {1: 'capsule', 2: 'circle', 3: 'diamond', 4: 'ellipse', 5: 'hexagon', 6: 'octagon', 7: 'pentagon',
                  8: 'square', 9: 'triangle'}
    # {'rois': array([], shape=(0, 4), dtype=int32), 'class_ids': array([], dtype=int32),
     # 'scores': array([], dtype=float32), 'masks': array([], shape=(2016, 1134, 0), dtype=float64)}
    # print(result['rois'])
    # print(type(result['rois']))
    if result['rois'].shape == (0,4):
        color_result = ''
        shape_result = ''
        print(color_result, shape_result)
        return color_result, shape_result

    box = result['rois'][0]
    shape_result = shape_list[result['class_ids'][0]]

    # [blue green red]
    mid_box = [(box[2] + box[0]) / 2, (box[3] + box[1]) / 2]
    # print(mid_box)
    # 1. 이미지 저장후 링크형식 보내기
    img = skimage.io.imread(img_link)
    # 2. 이미지 저장없이 변수로 보내기
    # tmp = Image.open(img_link)
    # tmp = np.array(tmp)
    # img = imageio.core.util.Array(tmp)
    ############
    mid_rgb = list(img[int((box[2] + box[0]) / 2), int((box[3] + box[1]) / 2)])
    # print(mid_rgb)
    mid_hsv = list(rgb_to_hsv(mid_rgb[2], mid_rgb[1], mid_rgb[0]))
    # print(mid_hsv)
    # 하양, 노랑, 주황, 분홍, 빨강, 갈색, 연두, 초록, 청록,파랑,남색,자주, 보라, 회색, 검정

    min = 10000
    color_result = ''
    for key, value in color_hsv.items():
        # print(key,value)
        tmp = 0
        for x in range(0, 3):
            if abs(mid_hsv[x] - value[x]) > 70:
                tmp = 110
                break
            tmp += abs(mid_hsv[x] - value[x])
        if min > tmp:
            min = tmp
            color_result = key

    # print(color_result)
    # print(color[color_result])
    return color_result, shape_result

def rgb_to_hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = (df/mx)*100
    v = mx*100
    return h, s, v

# {'rois': array([[1097, 1043, 1573, 1483]]), 'class_ids': array([2]), 'scores': array([0.98981524], dtype=float32), 'masks': array([[[False],

# print(box)#[1097 1043 1573 1483]
# print(shape_result)#circle
# box = [1097,1043,1573,1483] #x1 y1 x2 y2
# #y1 x1 y2 x2
# shape_result = 'circle'

def crawling_link(link, crawling_result):#크롤링해서 링크따오는 함수
    response = requests.get(link)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        # title = soup.select_one("a href")
        # print(title)
        # print(soup)


        if soup.find('div', attrs={'class': 'list_wrap'}) == None:
            crawling_result = None

        else:
            for href in soup.find('div', attrs={'class': 'list_wrap'}).find_all("strong", {"class": "title"}):
                # print(href.find("a")["href"])
                # print("https://terms.naver.com" + href.find("a")["href"])
                crawling_result.append("https://terms.naver.com" + href.find("a")["href"])
            # print(crawling_result)

    else:
        print(response.status_code)

    return crawling_result

def crawling_get_link_img_name(shape_result,color_result, text_result):#의약품사전링크에서 검색결과 따오기
    crawling_shape_list = {"circle": "1", "triangle": "4", "square": "5", "diamond": "6", "pentagon": "8", "hexagon": "9",
             "octagon": "10"}
    crawling_color_list = {"white": "16384", "yellow": "8", "orange": "512", "pink": "32", "red": "64", "brown": "1",
                            "mild_green": "128", "green": "2048", "bluish_green": "1024", "blue": "8196", "navy": "4",
                            "light_purple": "256", "purple": "16", "gray": "32768", "black": "2"}
    # 하양, 노랑, 주황, 분홍, 빨강, 갈색, 연두, 초록, 청록,파랑,남색,자주, 보라, 회색, 검정

    if shape_result != 'capsule' and shape_result != 'ellipse':
        object = crawling_shape_list[shape_result]
    color = crawling_color_list[color_result]

    if text_result == None:
        text_result = ''

    total = []
    crawling_name = []
    crawling_img = []
    crawling_result = []
    if shape_result == "ellipse":
        object = [2,7]
        for i in object:
            i = str(i)
            link = "https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&shape="+i+"&color="+color+"&dosageForm=&divisionLine=&identifier="+text_result
            crawling_link(link, crawling_result)
    else:
        if shape_result == "capsule":
            link = "https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&shape=7&color="+color+"&dosageForm=2&divisionLine=&identifier="+text_result
        else:
            link = "https://terms.naver.com/medicineSearch.naver?mode=exteriorSearch&shape="+object+"&color="+color+"&dosageForm=&divisionLine=&identifier="+text_result
        crawling_link(link, crawling_result)

    if crawling_result == None:
        crawling_img=None
        crawling_name=None

    else:
        for i in crawling_result:#링크에서 이미지와 이름 읽어오는거
            response = requests.get(i)
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            img = soup.find('img')
            img_src = img.get("data-src")
            # print(img_src)
            if img_src != None:
                # res = request.urlopen(img_src).read()
                # img = Image.open(BytesIO(res))
                # crawling_img.append(img)
                crawling_img.append(img_src)

            name = soup.title.string
            if not name.startswith('[접근 오류]'):
                crawling_name.append(name)

        for a,b,c in zip(crawling_name, crawling_img, crawling_result):
            tmp = {'medicine_name' : a, 'medicine_image' : b, 'link' : c}
            total.append(tmp)
    # print(total)
    return total


# color_result, shape_result = get_img_inform(model, img_link)
# print(color_result,shape_result)
# crawling_img, crawling_name, crawling_link = crawling_get_link_img_name(shape_result, color_result)
# print(crawling_link)
# print(crawling_img)
# print(crawling_name)

# for i in crawling_img:
#     i.show()
