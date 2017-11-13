#coding=utf-8
import os
import numpy
from skimage import io,data

def CompressionRate(sourceFile, compressedFile):
    source_size = os.path.getsize(sourceFile)
    compressed_size = os.path.getsize(compressedFile)
    compression_rate = (source_size + 0.0) / (compressed_size + 0.0)
    print "Source_size: " + str(source_size)
    print "Compressed_size: " + str(compressed_size)
    return compression_rate

def SNR(sourceFile, decompressedFile):
    source_img = io.imread(sourceFile)
    decompressed_img = io.imread(decompressedFile)
    wid = source_img.shape[0]
    hei = source_img.shape[1]
    if len(source_img.shape) == 2:
        sum1 = 0.0
        sum2 = 0.0
        for i in range(0, wid):
            for j in range(0, hei):
                # 算原图里所有元素的平方的平均值
                val1 = source_img[i, j]
                val2 = decompressed_img[i, j]
                sum1 += numpy.square(val1)
                # 算均方误差
                sum2 += numpy.square(val1 - val2)
        SNR = sum1 / sum2
    else:
        sum1 = 0.0
        sum2 = 0.0
        for i in range(0, wid):
            for j in range(0, hei):
                # 算原图里所有元素的平方的平均值
                val1r = source_img[i, j][0] / 255.0
                val1g = source_img[i, j][1] / 255.0
                val1b = source_img[i, j][2] / 255.0
                val2r = decompressed_img[i, j][0] / 255.0
                val2g = decompressed_img[i, j][1] / 255.0
                val2b = decompressed_img[i, j][2] / 255.0
                # print "r: " + str(val1r) + " " + str(val2r)
                # print "g: " + str(val1g) + " " + str(val2g)
                # print "b: " + str(val1b) + " " + str(val2b)
                sum1 += numpy.square(val1r) + numpy.square(val1g) + numpy.square(val1b)
                # 算均方误差
                sum2 += numpy.square(val1r - val2r) + numpy.square(val1g - val2g)\
                        + numpy.square(val1b - val2b)
        SNR = sum1 / sum2
    return SNR