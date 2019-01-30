import numpy as np
from PIL import Image
from PIL import ImageFilter

def encodeAnsToImg(imageFile, ansFile):
    img = Image.open(imageFile)
    imgPix = np.array(img)
    ans = open(ansFile)
    ansArr = []
    for line in ans:
        ansArr.append(line.rstrip('\n').split(' ')[1])
    ansBitArr = []
    for question in ansArr:
        bitArr = ''
        for answers in question:
            bitArr += format(ord(answers),'08b')
        ansBitArr.append(bitArr.ljust(40,'0'))
    
    for j in range(len(ansBitArr)):
        for i in range(len(ansBitArr[j])):
            intBit = int(ansBitArr[j][i]) % 2
            intImgPix = int(imgPix[j][i]) % 2
            if intBit == 0:
                imgPix[j][i] -= intImgPix
            else:
                imgPix[j][i] += (intImgPix-1)
    
    newImg = Image.fromarray(imgPix)
    newImg.save('encrypted_image.jpg')
    return newImg

def decodeAnswerFromImg(imageFile, outFile):
    out = open(outFile, 'w')
    imgPix = np.array(imageFile)
    ansPix = imgPix[np.ix_(range(85), range(40))]
    ansPix = ansPix % 2
    for ans in ansPix:
       out.write(''.join(chr(i) for i in np.trim_zeros(np.packbits(ans))))
       out.write('\n')
    out.close()

newImg = encodeAnsToImg('a-3.jpg','a-3_groundtruth.txt')
decodeAnswerFromImg(newImg, 'decoded_ans.txt')

