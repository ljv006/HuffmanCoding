from huffman import HuffmanCoding
from skimage import io,data
import matplotlib.pyplot as plt
import sys

path = "sample.txt"
# imagePath = "Gray/Image01.jpg"
imagePath = "Color/Image01.jpg"
h = HuffmanCoding(imagePath)

output_path = h.compress()
print("Compressed file path: " + output_path)
print "mapping " + str(len(h.reverse_mapping))
decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)
