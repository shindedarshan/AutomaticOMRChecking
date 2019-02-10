# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 15:54:29 2019

@author: Darshan
"""

from PIL import Image
import numpy as np

def encrypt(imageFile, ansFile, outFile):
    img = Image.open(imageFile)
    ans = open(ansFile)
    imgPix = np.array(img)
    ansArr = []
    barCode = []
    
    for line in ans:
        ansArr.append(line.rstrip('\n').split(' ')[1])
    
    for question in ansArr:
        bitArr = ''
        for answers in question:
            bitArr += format(ord(answers),'08b')
        bitArr = bitArr.ljust(40,'0')
        bitArr = bitArr.replace('0', 'x').replace('1', '0').replace('x', '1')
        bitArr = ''.join([bit*5 for bit in bitArr])
        for i in range(20):
            barCode.append(bitArr)
        for i in range(5):
            barCode.append(''.ljust(200,'1'))
    
    barCode = ''.join(barCode)
    barCodeArr = np.array(list(barCode)).reshape(2125,200)
    barCodeArr = barCodeArr.astype('uint8')
    barCodeArr[barCodeArr == 1] = 255
    imgPix[:2125, :200] = barCodeArr[:2125,:200]
    newImg = Image.fromarray(imgPix)
    newImg.save(outFile)
    
def decrypt(imageFile, outFile):
    img = Image.open(imageFile).convert("L")
    out = open(outFile, 'w')
    imgPix = np.array(img)
    subImg = imgPix[np.ix_(range(2125), range(200))]
    i = 0
    while i < 2125:
        temp = subImg[np.ix_(range(i,i+20), range(200))]
        maxStream = getMaxOccStream(temp)
        row = get8BitStream(maxStream)
        print(str(np.packbits(row)) + '\n')
        out.write(''.join(chr(i) for i in np.trim_zeros(np.packbits(row))))
        out.write('\n')
        i += 25
    out.close()
    
def getMaxOccStream(arr):
    out = []
    for i in range(arr.shape[1]):
        count = np.bincount(arr[:,i])
        out.append(np.argmax(count))
    return out

def get8BitStream(vec):
    out = []
    vec = np.array(vec)
    vec = vec / 255
    vec[vec == 0] = 5
    vec[vec == 1] = 0
    vec[vec == 5] = 1
    for i in range(40):
        subVec = vec[5*i:(5*i) + 5]
        subVec = np.array(subVec, dtype = np.int64)
        count = np.bincount(subVec)
        out.append(np.argmax(count))
    return out

#encrypted_file = encrypt('a-3.jpg','a-3_groundtruth.txt', 'encrypted_image.png')
decrypt('20190204163506657_0001-1.png', 'decoded_ans.txt')
