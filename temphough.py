# -*- coding: utf-8 -*-
"""
Created on Tue Feb  5 23:40:59 2019

@author: Darshan
"""
import numpy as np
from PIL import Image
import cv2

def hough(img):
    print('Inside hough')
    #img = Image.open('temp1.jpg').convert('L')
    imgPix = np.array(img)
    rows = img.height
    columns = img.width
    diag = np.sqrt(rows**2 + columns**2)
    #nrho = 2*q + 1
    #thetaArr = np.linspace(-10,11, 21)
    thetaArr = range(0,91)
    rhoArr = range(0,int(diag))
    #rhoArr = np.linspace(-q, q, (2*q + 1))
    hough_mat = np.zeros((len(rhoArr), len(thetaArr)))
    for i in range(rows):
        for j in range(columns):
            if imgPix[i,j] == 0:
                for theta in thetaArr:
                    rho = (j * np.cos(np.deg2rad(theta))) + (i * np.sin(np.deg2rad(theta)))
                    hough_mat[int(rho), theta] += 1 
    return hough_mat

def drawLines(lines):
    print('Inside drawLines')
    #lines = zip(np.where(mat > 400)[0], np.where(mat > 400)[1])
    img = cv2.imread("blank_form.jpg")
    for rho, theta in lines:
        cos_val = np.cos(np.deg2rad(theta))
        sin_val = np.sin(np.deg2rad(theta))
        x0 = cos_val * rho
        y0 = sin_val * rho
        x1 = int(x0 + 4000 * (-sin_val)) 
        y1 = int(y0 + 4000 * (cos_val)) 
        x2 = int(x0 - 4000 * (-sin_val)) 
        y2 = int(y0 - 4000 * (cos_val)) 
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        print(x1,y1,x2,y2)
    cv2.imwrite('linesDetected.jpg', img)

def getLines(mat):
    print('Inside getLines')
    tuple_list = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            tuple_list.append((mat[i,j],i,j))
    print('Tuple list generated')
    sorted_tuples = sorted(tuple_list, key=lambda tup: tup[0],reverse = True)
    print('Tuple sorting done')
    count_horizon = 77
    count_verticle = 55
    lines = []
    count = 0
    for tpl in sorted_tuples:
        count += 1
        print(count)
        if count_horizon > 0 or count_verticle > 0:
            if tpl[2] <= 2 and count_verticle > 0:
              count_verticle -= 1
              lines.append((tpl[1],tpl[2]))
              print('verticle line added... ' + str(count_verticle) + ' remaining')
            elif tpl[2] >= 88 and count_horizon > 0:
              count_horizon -= 1
              lines.append((tpl[1],tpl[2]))
              print('horizontal line added... ' + str(count_horizon) + ' remaining')
    return lines

img = Image.open('blank_form.jpg').convert('L')
mat = hough(img)
lines = getLines(mat)
drawLines(lines)

