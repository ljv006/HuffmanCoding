import heapq
import os
from functools import total_ordering
from skimage import io,data
import numpy
import matplotlib.pyplot as plt
from skimage.color import *
"""
Code for Huffman Coding, compression and decompression.
Explanation at http://bhrigu.me/blog/2017/01/17/huffman-coding-python-implementation/
"""


@total_ordering
class HeapNode:
    def __init__(self, char, freq):
		self.char = char
		self.freq = freq
		self.left = None
		self.right = None

    # defining comparators less_than and equals
    def __lt__(self, other):
		return self.freq < other.freq

    def __eq__(self, other):
		if (other == None):
		    return False
		if (not isinstance(other, HeapNode)):
		    return False
		return self.freq == other.freq


class HuffmanCoding:
    def __init__(self, path):
		self.path = path
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}

    # functions for compression:

    def make_frequency_dict(self, img):
		frequency = {}
		wid = img.shape[0]
		hei = img.shape[1]
		for x in range(0, wid - 1):
			for y in range(0, hei - 1):
				character = img[x, y]
				if not character in frequency:
					frequency[character] = 0
				frequency[character] += 1
		return frequency

    def make_heap(self, frequency):
		for key in frequency:
		    node = HeapNode(key, frequency[key])
		    heapq.heappush(self.heap, node)

    def merge_nodes(self):
		while (len(self.heap) > 1):
		    node1 = heapq.heappop(self.heap)
		    node2 = heapq.heappop(self.heap)

		    merged = HeapNode(None, node1.freq + node2.freq)
		    merged.left = node1
		    merged.right = node2

		    heapq.heappush(self.heap, merged)

    def make_codes_helper(self, root, current_code):
		if (root == None):
		    return

		if (root.char != None):
		    self.codes[root.char] = current_code
		    self.reverse_mapping[current_code] = root.char
		    return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)

    def get_encoded_text(self, img):
		encoded_text = ""
		ne = ""
		wid = img.shape[0]
		hei = img.shape[1]
		turn = 0
		for x in range(0, wid - 1):
			for y in range(0, hei - 1):
				turn += 1
				character = img[x, y]
				encoded_text = encoded_text + self.codes[character]
				ne += self.codes[character]
		return encoded_text

    def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
		    encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text

    def get_byte_array(self, padded_encoded_text):
		if (len(padded_encoded_text) % 8 != 0):
		    print("Encoded text not padded properly")
		    exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
		    byte = padded_encoded_text[i:i + 8]
		    b.append(int(byte, 2))
		return b

    def compress(self):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".bin"
		sourceName = filename + "_source" + ".jpg"
		with open(output_path, 'wb') as output:
			img = io.imread(self.path)
			img_gray = rgb2gray(img)
			io.imsave(sourceName, img_gray)
			frequency = self.make_frequency_dict(img)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(img)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			output.write(bytes(b))

		print("Compressed")
		return output_path

    """ functions for decompression: """

    def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:]
		encoded_text = padded_encoded_text[:-1 * extra_padding]

		return encoded_text

    def decode_text(self, encoded_text):
		current_code = ""
		source_image = io.imread(self.path)
		wid = source_image.shape[0]
		hei = source_image.shape[1]
		x = 0
		y = 0
		decoded_img = numpy.zeros((wid,hei))
		for bit in encoded_text:
		    current_code += bit
		    if (current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_img[x, y] = character
				y += 1
				if y == hei - 1:
					x += 1
					y = 0
				current_code = ""
		return decoded_img

    def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".jpg"

		with open(input_path, 'rb') as file:
			bit_string = ""

			byte = file.read(1)
			while (len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)
			encoded_text = self.remove_padding(bit_string)
			decompressed_img = self.decode_text(encoded_text)
			io.imshow(decompressed_img)
			plt.show()
			decompressed_img /= 255
			io.imsave(output_path, decompressed_img)

		print("Decompressed")
		return output_path

