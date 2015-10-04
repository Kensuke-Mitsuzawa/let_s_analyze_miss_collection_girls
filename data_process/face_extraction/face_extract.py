#! -*- coding: utf-8 -*-
__author__ = 'kensuke-mi'

"""This script extracts human face from image file.
"""

import cv2
import os
import Image
import ImageOps


COLOR = (255, 255, 255) #白
CASCADE_PATH = "/Users/kensuke-mi/.pyenv/versions/anaconda-2.1.0/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml"
assert os.path.exists(CASCADE_PATH)
RESIZED_TUPLE = (100, 100)


def detectFace(image):
    image_gray = cv2.cvtColor(image, cv2.cv.CV_BGR2GRAY)
    image_gray = cv2.equalizeHist(image_gray)

    cascade = cv2.CascadeClassifier(CASCADE_PATH)
    facerect = cascade.detectMultiScale(image_gray, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))

    return facerect


def extract_face(facerect_list, image, path_to_save):
    """顔の部分を切り出す。ただし、顔は１つの写真に一人しかいない前提なので注意

    :param facerect_list:
    :param image:
    :param path_to_save:
    :return:
    """
    assert os.path.exists(os.path.dirname(path_to_save))

    for rect in facerect_list:
        x = rect[0]
        y = rect[1]
        w = rect[2]
        h = rect[3]

        # img[y: y + h, x: x + w]
        cv2.imwrite(path_to_save, image[y:y+h, x:x+w])

        return image[y:y+h, x:x+w]


def draw_line_face(facerect_list, image, path_to_save):
    """顔部分を白い線で囲む

    :param facerect_list:
    :param image:
    :param path_to_save:
    :return:
    """
    assert os.path.exists(os.path.dirname(path_to_save))
    #検出した顔を囲む矩形の作成
    for rect in facerect_list:
        cv2.rectangle(image, tuple(rect[0:2]),tuple(rect[0:2]+rect[2:4]), COLOR, thickness=2)
    #認識結果の保存
    cv2.imwrite(path_to_save, image)



def resize_pic_opencv(im, save_path, size_tuple, gray_scale=True):
    """画像サイズ調整とグレースケール化。ただし、OpenCV使用

    :param im:
    :param save_path:
    :param size_tuple:
    :param gray_scale:
    :return:
    """
    assert isinstance(size_tuple, tuple)
    assert os.path.exists(os.path.dirname(save_path))
    assert isinstance(gray_scale, bool)

    resized_im = cv2.resize(im,size_tuple)
    if gray_scale==True:
        processed_img = cv2.cvtColor(resized_im, cv2.cv.CV_BGR2GRAY)
    else:
        processed_img = resized_im

    cv2.imwrite(save_path, processed_img)

    return save_path



def resize_pic_pil(input_path, save_path, size_tuple, gray_scale=True):
    """画像サイズを変更するコード
    ただし、PILライブラリを使用

    :param input_path:
    :param save_path:
    :param size_tuple:
    :param gray_scale:
    :return:
    """
    assert isinstance(size_tuple, tuple)
    assert os.path.exists(input_path)
    assert os.path.exists(os.path.dirname(save_path))
    assert isinstance(gray_scale, bool)

    resized_pic = Image.open(input_path).resize(size_tuple)
    if gray_scale==True:
        processed_img = ImageOps.grayscale(resized_pic)
    else:
        processed_img = resized_pic

    processed_img.save(save_path)



def example_usage():

    imagefile_name = '../../extracted/miss_collection/pics/Adachi Mako.jpg'
    path_to_resized = ''
    save_path_test = './demo.jpg'
    main_procedure(imagefile_name, save_path_test, path_to_resized)


def main_procedure(imagefile_name, path_to_save, path_to_resized):
    # IMPORTANAT this mrthod requires FULL PATH not relative path
    assert os.path.exists(imagefile_name)
    assert os.path.exists(os.path.dirname(path_to_save))
    assert os.path.exists(path_to_resized)

    print u'start processing {}'.format(imagefile_name)
    try:
        image = cv2.imread(imagefile_name)
        facerect_list = detectFace(image)
    except cv2.error:
        print u'[WARNING] problem happens while processing {}'.format(imagefile_name)
        return False
    else:
        if len(facerect_list) > 0:
            image_obj = extract_face(facerect_list, image, path_to_save)
            file_name = os.path.basename(path_to_save)
            path_to_save_resized = os.path.join(path_to_resized, file_name)
            resize_pic_opencv(im=image_obj, save_path=path_to_save_resized, size_tuple=RESIZED_TUPLE, gray_scale=True)
        else:
            return False

