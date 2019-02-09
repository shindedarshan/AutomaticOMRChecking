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
    imgPix = np.array(img)
    rows = img.height
    columns = img.width
    diag = np.sqrt(rows**2 + columns**2)
    thetaArr = range(0,91)
    rhoArr = range(0,int(diag))
    hough_mat = np.zeros((len(rhoArr), len(thetaArr)))
    for i in range(rows):
        for j in range(columns):
            if imgPix[i,j] == 0:
                for theta in thetaArr:
                    rho = (j * np.cos(np.deg2rad(theta))) + (i * np.sin(np.deg2rad(theta)))
                    hough_mat[int(rho), theta] += 1 
    return hough_mat

def drawLines(lines, file):
    print('inside draw lines')
    #img = cv2.imread('a-3.jpg')
    img = cv2.imread(file)
    x = []
    y = []
    for rho, theta in lines:
        cos_val = np.cos(np.deg2rad(theta))
        sin_val = np.sin(np.deg2rad(theta))
        x0 = cos_val * rho
        y0 = sin_val * rho
        if theta <= 2:
            y_set = set(y)
            curr_set = set(range(int(x0)-22,int(x0)+22))
            if len(y_set.intersection(curr_set)) > 0:
                continue
            y.append(x0)
        if theta >= 88:
            x_set = set(x)
            curr_set = set(range(int(y0)-12,int(y0)+12))
            if len(x_set.intersection(curr_set)) > 0:
                continue
            x.append(y0)
        
        x1 = int(x0 + 4000 * (-sin_val)) 
        y1 = int(y0 + 4000 * (cos_val)) 
        x2 = int(x0 - 4000 * (-sin_val)) 
        y2 = int(y0 - 4000 * (cos_val)) 
        cv2.line(img, (x1, y1), (x2, y2), (0, 0, 0), 2)
        #print(x1,y1,x2,y2)
    cv2.imwrite(file, img)
    return x, y

def getLines(mat):
    print('inside get lines')
    tuple_list = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            tuple_list.append((mat[i,j],i,j))
    sorted_tuples = sorted(tuple_list, key=lambda tup: tup[0],reverse = True)
    count_horizon = 25
    count_verticle = 55
    lines = []
    count = 0
    for tpl in sorted_tuples:
        count += 1
        #print(count)
        if count_horizon > 0 or count_verticle > 0:
            if tpl[2] <= 2 and count_verticle > 0:
              count_verticle -= 1
              lines.append((tpl[1],tpl[2]))
            elif tpl[2] >= 88 and count_horizon > 0:
              count_horizon -= 1
              lines.append((tpl[1],tpl[2]))
    return lines

def binary(img):
    imgPix = np.array(img)
    imgPix[imgPix > 50] = 255
    imgPix[imgPix <= 50] = 0
    return Image.fromarray(imgPix)

def detectMarkedAnswers(img, x, y):
    x = np.sort(x).astype('uint16')
    y = np.sort(y).astype('uint16')
    imgPix = np.array(img)
    areaSum = []
    for i in range(len(x)-1):
        for j in range(len(y)-1):
            matSum = np.sum(imgPix[x[i]:x[i+1],y[j]:y[j+1]])
            areaSum.append((x[i], x[i+1], y[j], y[j+1], matSum)) 
    return areaSum

def colorBox(img, areaSum):
    imgArr = np.array(img)
    for box in sorted(areaSum, key=lambda val: val[4],reverse = False):
        if box[4] < 65000:
            imgArr[np.ix_(range(box[0],box[1]), range(box[2],box[3]))] = 120
    Image.fromarray(imgArr).save('coloredBox.jpg')
    
    
img = Image.open('a-30.jpg').convert('L')
img = binary(img)
imgPixal = np.array(img)
imgPix = imgPixal[650:]

pixArr1 = imgPix[15:495]
img1 = Image.fromarray(pixArr1)
img1.save('int1.jpg')
mat1 = hough(img1)
lines1 = getLines(mat1)
x1, y1 = drawLines(lines1, 'int1.jpg')
img1 = Image.open('int1.jpg').convert('L')
arr1 = np.array(img1)

pixArr2 = imgPix[495:972]
img2 = Image.fromarray(pixArr2)
img2.save('int2.jpg')
mat2 = hough(img2)
lines2 = getLines(mat2)
x2, y2 = drawLines(lines2, 'int2.jpg')
img2 = Image.open('int2.jpg').convert('L')
arr2 = np.array(img2)
areaSum = detectMarkedAnswers(img2, x2, y2)
colorBox(img2, areaSum)

pixArr3 = imgPix[972:1400]
img3 = Image.fromarray(pixArr3)
img3.save('int3.jpg')
mat3 = hough(img3)
lines3 = getLines(mat3)
x3, y3 = drawLines(lines3, 'int3.jpg')
img3 = Image.open('int3.jpg').convert('L')
arr3 = np.array(img3)

img = Image.open('linesDetected.jpg').convert('L')
arr = np.array(img)
arr = np.concatenate((imgPixal[:650],arr1, arr2, arr3), axis = 0)
Image.fromarray(arr).save('linesDetected.jpg')

#print('x:', x)
#print('y:', y)