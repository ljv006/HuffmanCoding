from huffman import HuffmanCoding
import sys

path = "sample.txt"

h = HuffmanCoding(path)

output_path = h.compress()
print("Compressed file path: " + output_path)
print str(len(h.reverse_mapping))
decom_path = h.decompress(output_path)
print("Decompressed file path: " + decom_path)