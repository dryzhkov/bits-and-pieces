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

    def __init__(self, byte, count):
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


def decompress(compressed):
    print(compressed)

def build_tree(data):
    count_map = {}

    for byte in data:
        if byte in count_map:
            count_map[byte] += 1
        else:
            count_map[byte] = 1
    
    counter_list = [Node(k, v) for k, v in count_map.items()]
    print(counter_list)
    
    while len(counter_list) > 1:
        min_left = min(counter_list, key=attrgetter('count'))
        counter_list.remove(min_left)
        min_right = min(counter_list, key=attrgetter('count'))
        counter_list.remove(min_right)

        parent = Node(-1, min_left.count + min_right.count)
        parent.left = min_left
        parent.right = min_right

        counter_list.append(parent)

        print(counter_list)
    
    root = counter_list.pop()

    root.PrintTree()

    return root

if __name__ == "__main__":
    c = vars(args)["compress"]
    d = vars(args)["decompress"]

    if c == True:
        compress(bytes(sys.stdin.read(), "utf-8"))
    else:
        decompress(bytes(sys.stdin.read(), "utf-8"))
