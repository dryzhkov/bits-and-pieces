#!/usr/bin/env python3
import argparse
import sys
from operator import attrgetter

parser = argparse.ArgumentParser()
parser.add_argument('--compress', action='store_true', help='to compress data')
parser.add_argument('--decompress', action='store_true',
                    help='to decompress data')
args = parser.parse_args()

class Node:

    def __init__(self, count, byte=-1):
        self.left = None
        self.right = None
        self.byte = byte
        self.count = count

    def __repr__(self):
        return 'node(' + repr(self.byte) + ', ' + repr(self.count) + ')'

    def print(self):
        print(self.__repr__())

        if self.left != None: 
            self.left.print()
        
        if self.right != None:
            self.right.print()

def compress(original):
    huff_tree = build_tree(original)
    # huff_tree.print()
    bits_table = {}
    build_table(huff_tree, bits_table)
    print(bits_table)

def decompress(compressed):
    print(compressed)

def build_tree(data):
    count_map = {}

    for byte in data:
        if byte in count_map:
            count_map[byte] += 1
        else:
            count_map[byte] = 1
    
    counter_list = [Node(v, k) for k, v in count_map.items()]
    
    while len(counter_list) > 1:
        min_left = min(counter_list, key=attrgetter('count'))
        counter_list.remove(min_left)
        min_right = min(counter_list, key=attrgetter('count'))
        counter_list.remove(min_right)

        parent = Node(min_left.count + min_right.count)
        parent.left = min_left
        parent.right = min_right

        counter_list.append(parent)
    
    return counter_list.pop()

def build_table(node, table, path = []):
    if node.left == None and node.right == None: # left
        table[node] = path
    else:
        build_table(node.left, table, path + [0])
        build_table(node.right, table, path + [1])

if __name__ == "__main__":
    c = vars(args)["compress"]
    d = vars(args)["decompress"]

    if c == True:
        compress(bytes(sys.stdin.read(), "utf-8"))
    else:
        decompress(bytes(sys.stdin.read(), "utf-8"))
