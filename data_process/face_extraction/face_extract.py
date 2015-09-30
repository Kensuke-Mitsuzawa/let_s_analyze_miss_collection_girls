#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

"""This script extracts human face from image file.
"""

import cv2
import os

COLOR = (255, 255, 255) #白
CASCADE_PATH = "/Users/kensuke-mi/.pyenv/versions/anaconda-2.1.0/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
assert os.path.exists(CASCADE_PATH)

def detectFace(image):
    image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    image_gray = cv2.equalizeHist(image_gray)

    cascade = cv2.CascadeClassifier(CASCADE_PATH)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))

    return facerect


def extract_face(facerect_list, image, path_to_save):
    assert os.path.exists(os.path.dirname(path_to_save))

    for rect in facerect_list:
        #cv2.imwrite('demo.jpg', image[rect])
        print rect
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]

        # img[y: y + h, x: x + w]
        cv2.imwrite(path_to_save, image[y:y+h, x:x+w])


def draw_line_face(facerect_list, image, path_to_save):
    assert os.path.exists(os.path.dirname(path_to_save))
    #検出した顔を囲む矩形の作成
    for rect in facerect_list:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), COLOR, thickness=2)
    #認識結果の保存
    cv2.imwrite(path_to_save, image)


def main_procedure(imagefile_name, path_to_save):
    assert os.path.exists(imagefile_name)
    assert os.path.exists(os.path.dirname(path_to_save))

    image = cv2.imread(imagefile_name)
    facerect_list = detectFace(image)
    if len(facerect_list) > 0:
        extract_face(facerect_list, image, path_to_save)


def example_usage():

    imagefile_name = '../../extracted/miss_collection/pics/Adachi Mako.jpg'
    save_path_test = './demo.jpg'
    main_procedure(imagefile_name, save_path_test)


def girls_face_process():
    PATH_INPUT_DIR = '../../extracted/miss_collection/pics'
    PATH_SAVE_DIR = '../../extracted/miss_collection/face'

    path_pics_list = [os.path.join(PATH_INPUT_DIR, path_pic) for path_pic in os.listdir(PATH_INPUT_DIR)]
    path_save_list = [os.path.join(PATH_SAVE_DIR, path_pic) for path_pic in os.listdir(PATH_INPUT_DIR)]

    for index, path_input in enumerate(path_pics_list):
        main_procedure(imagefile_name=path_input, path_to_save=path_save_list[index])



if __name__ == '__main__':
    #example_usage()
    girls_face_process()

