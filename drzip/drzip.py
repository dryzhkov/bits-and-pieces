#!/usr/bin/env python3
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument('--compress', action='store_true', help='to compress data')
parser.add_argument('--decompress', action='store_true',
                    help='to decompress data')
args = parser.parse_args()


def compress(original):
    print(original)


def decompress(compressed):
    print(compressed)


if __name__ == "__main__":
    c = vars(args)["compress"]
    d = vars(args)["decompress"]

    if c == True:
        compress(sys.stdin.read())
    else:
        decompress(sys.stdin.read())
