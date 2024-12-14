# -*- coding: utf-8 -*-
"""Huffman.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lIsU-PFZf56O94ORRCVkJ0oEBw6DUE6f
"""

import heapq
from collections import Counter
import time

start_time = time.time()

class HuffmanCoding:
    class Node:
        def __init__(self, char, freq):
            self.char = char
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def __init__(self, text):
        self.text = text
        self.frequency = Counter(text)
        self.heap = []
        self.codes = {}
        self.reverse_codes = {}

    def build_heap(self):
        for char, freq in self.frequency.items():
            node = self.Node(char, freq)
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = self.Node(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(self.heap, merged)

    def build_codes_helper(self, node, current_code):
        if node is None:
            return
        if node.char is not None:
            self.codes[node.char] = current_code
            self.reverse_codes[current_code] = node.char
        self.build_codes_helper(node.left, current_code + "0")
        self.build_codes_helper(node.right, current_code + "1")

    def build_codes(self):
        root = heapq.heappop(self.heap)
        self.build_codes_helper(root, "")

    def get_encoded_text(self):
        encoded_text = ""
        for char in self.text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)
        byte_array = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            byte_array.append(int(byte, 2))
        return byte_array

    def compress(self, output_path):
        self.build_heap()
        self.merge_nodes()
        self.build_codes()
        encoded_text = self.get_encoded_text()
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)

        with open(output_path, 'wb') as output:
            # Store the frequency dictionary length
            output.write(len(self.frequency).to_bytes(2, 'big'))
            # Store the frequency dictionary
            for char, freq in self.frequency.items():
                output.write(char.encode('utf-8'))
                output.write(freq.to_bytes(4, 'big'))
            # Store the encoded text
            output.write(byte_array)

        return output_path

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)
        padded_encoded_text = padded_encoded_text[8:]
        encoded_text = padded_encoded_text[:-1*extra_padding]
        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_codes:
                character = self.reverse_codes[current_code]
                decoded_text += character
                current_code = ""
        return decoded_text

    def decompress(self, input_path, output_path):
        with open(input_path, 'rb') as file:
            # Read the frequency dictionary length
            freq_dict_length = int.from_bytes(file.read(2), 'big')
            # Read the frequency dictionary
            frequency = {}
            for _ in range(freq_dict_length):
                char = file.read(1).decode('utf-8')
                freq = int.from_bytes(file.read(4), 'big')
                frequency[char] = freq

            # Build the Huffman tree from the frequency dictionary
            self.frequency = frequency
            self.build_heap()
            self.merge_nodes()
            self.build_codes()

            # Read the encoded text
            bit_string = ""
            byte = file.read(1)
            while byte:
                byte = ord(byte)
                bits = bin(byte)[2:].rjust(8, '0')
                bit_string += bits
                byte = file.read(1)

        encoded_text = self.remove_padding(bit_string)
        decompressed_text = self.decode_text(encoded_text)

        with open(output_path, 'w') as output:
            output.write(decompressed_text)

        return output_path

# Example usage:
input_file_path = 'image_base64_00.txt'
output_compressed_path = 'compressed_00.txt'
output_decompressed_path = 'decompressed.txt'

# Read the content of the provided text file
with open(input_file_path, 'r') as file:
    text = file.read()

# Create a HuffmanCoding instance
huffman = HuffmanCoding(text)

# Compress the text file
huffman.compress(output_compressed_path)

# Decompress the text file
# huffman.decompress(output_compressed_path, output_decompressed_path)

end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time:.2f} seconds")

