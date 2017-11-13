from huffman import HuffmanCoding
from evaluator import *



#imagePath = "Color/Image01.bmp"
#imagePath = "Color/Image02.bmp"
#imagePath = "Gray/Image03.bmp"
imagePath = "Gray/Image04.bmp"
h = HuffmanCoding(imagePath)

output_path = h.compress()
print("Compressed file path: " + output_path)
decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)

print "Compression Rate: " + str(round(CompressionRate(imagePath, output_path), 4))
print "SNR: " + str(round(SNR(imagePath, decom_path), 4))
